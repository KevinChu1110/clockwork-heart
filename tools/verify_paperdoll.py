import json
import os
import glob
import re
import sys

REPO = "/opt/side/bravesoul-game"
JSON_PATH = os.path.join(REPO, "docs/design/paperdoll_slots.json")
SPEC_PATH = os.path.join(REPO, "docs/design/PAPERDOLL_SLOTS_SPEC.md")

errors = []

# 1. Zero-fur & banned words check in docs/design/
banned_regex = re.compile(r'毛簇|毛球|絨|短劍|匕首|葫蘆|blood|長矛|鍛爐雙面戰斧')
for fname in ["paperdoll_slots.json", "PAPERDOLL_SLOTS_SPEC.md"]:
    fpath = os.path.join(REPO, "docs/design", fname)
    with open(fpath, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            m = banned_regex.search(line)
            if m:
                errors.append(f"[BANNED PATTERN '{m.group()}'] {fname}:{idx}: {line.strip()}")

# 2. Check JSON validity and archetype/weapon
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

expected_archetypes = {
    "rabbit": "劍士 (Knight)",
    "lion": "騎士 (Knight)",
    "fox": "法師 (Mage)",
    "boar": "戰士 (Viking)",
    "macaque": "武術家 (Monk)"
}

races = data["races_specification"]["races"]
assert len(races) == 5

for r in races:
    rid = r["race_id"]
    arch = r.get("class_archetype")
    exp = expected_archetypes.get(rid)
    if arch != exp:
        errors.append(f"[ARCHETYPE MISMATCH] {rid}: got '{arch}', expected '{exp}'")

# Check weapons in sample_variants
weapon_slot = [s for s in data["slots_architecture"]["slots"] if s["slot_id"] == "weapon"][0]
weapon_variants = {w["id"]: w["name"] for w in weapon_slot["sample_variants"]}
expected_weapons = {
    "wpn_dawn_blade": "晨曦發條單手長劍",
    "wpn_spring_claws": "機關發條靈爪護手",
    "wpn_knight_lance": "皇家黃銅突刺長槍",
    "wpn_astral_staff": "星盤晶核秘術法杖",
    "wpn_anvil_greathammer": "鍛爐鐵砧重型戰鎚"
}
for wid, exp_name in expected_weapons.items():
    actual_name = weapon_variants.get(wid)
    if actual_name != exp_name:
        errors.append(f"[WEAPON MISMATCH] {wid}: got '{actual_name}', expected '{exp_name}'")

# 3. Check bidirectional exists for all existing/pending assets
print("=== ASSET BIDIRECTIONAL EXISTS CHECK ===")
existing_count = 0
pending_count = 0

for r in races:
    rid = r["race_id"]
    status = r["asset_naming_conventions"]["status"]
    print(f"\n--- Race: {rid} ---")
    for item in status.get("existing", []):
        path = item.split(" ")[0]
        full_path = os.path.join(REPO, path)
        # Handle wildcards
        pattern = full_path.replace("{0..3}", "*").replace("{0..3}_x3", "*")
        matched = glob.glob(pattern) if ("*" in pattern or "{" in pattern) else [full_path]
        exists = any(os.path.exists(p) for p in matched)
        if not exists:
            errors.append(f"[EXISTING MISSING] {rid} -> {path}")
            print(f"  ❌ EXISTING MISSING: {path}")
        else:
            existing_count += 1
            print(f"  ✓ EXISTING OK: {path}")

    for item in status.get("pending", []):
        path = item.split(" ")[0]
        if "{" in path and "slot_id" in path:
            print(f"  ✓ PENDING DIR (SPEC ONLY): {path}")
            pending_count += 1
            continue
        full_path = os.path.join(REPO, path)
        pattern = full_path.replace("{0..3}", "*").replace("{0..3}_x3", "*")
        matched = glob.glob(pattern) if ("*" in pattern or "{" in pattern) else [full_path]
        exists = any(os.path.exists(p) for p in matched)
        if exists:
            errors.append(f"[PENDING ALREADY EXISTS] {rid} -> {path}")
            print(f"  ❌ PENDING ALREADY EXISTS: {path}")
        else:
            pending_count += 1
            print(f"  ✓ PENDING OK (ABSENT): {path}")

print(f"\nTotal Existing Verified: {existing_count}")
print(f"Total Pending Verified: {pending_count}")

# 4. Summary table: Role x Weapon
print("\n=== CROSS-CHECK: ROLE x WEAPON ===")
role_weapon_table = [
    ("兔 (rabbit)", "劍士 (Knight)", "單手長劍 / 晨曦發條單手長劍", "sword (劍)"),
    ("獅 (lion)", "騎士 (Knight)", "騎士長槍 / 皇家黃銅突刺長槍", "spear (長槍)"),
    ("狐 (fox)", "法師 (Mage)", "法杖 / 星盤晶核秘術法杖", "magic (法杖)"),
    ("豬 (boar)", "戰士 (Viking)", "巨鎚 / 鍛爐鐵砧重型戰鎚", "hammer (鎚)"),
    ("猴 (macaque)", "武術家 (Monk)", "靈爪護手 / 機關發條靈爪護手", "claw (爪)")
]
for role, arch, wname, wcls in role_weapon_table:
    print(f"  {role:<15} | 職業: {arch:<14} | 武器: {wname:<25} | 體系: {wcls}")

if errors:
    print(f"\n❌ FAILED with {len(errors)} errors:")
    for err in errors:
        print(f"  {err}")
    sys.exit(1)
else:
    print("\n✅ ALL CHECKS PASSED PERFECTLY (0 errors)!")
    sys.exit(0)
