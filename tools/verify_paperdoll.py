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

# Also check sync between docs/design and game/data/tables
TABLES_JSON_PATH = os.path.join(REPO, "game/data/tables/paperdoll_slots.json")
with open(TABLES_JSON_PATH, "r", encoding="utf-8") as f2:
    data_tables = json.load(f2)
s1 = json.dumps(data, sort_keys=True, indent=2)
s2 = json.dumps(data_tables, sort_keys=True, indent=2)
if s1 != s2:
    errors.append("[SPEC SYNC] docs/design/paperdoll_slots.json and game/data/tables/paperdoll_slots.json differ (sort_keys diff is not empty)!")

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

# Helper functions for pattern expansion
def expand_wildcards(path):
    results = [path]
    while True:
        new_results = []
        expanded_any = False
        for p in results:
            m_range = re.search(r'\{(\d+)\.\.(\d+)\}', p)
            if m_range:
                expanded_any = True
                start, end = int(m_range.group(1)), int(m_range.group(2))
                for i in range(start, end + 1):
                    new_results.append(p[:m_range.start()] + str(i) + p[m_range.end():])
                continue
            m_set = re.search(r'\{([^{}]+,[^{}]+)\}', p)
            if m_set:
                expanded_any = True
                for opt in m_set.group(1).split(','):
                    new_results.append(p[:m_set.start()] + opt.strip() + p[m_set.end():])
                continue
            new_results.append(p)
        results = new_results
        if not expanded_any:
            break
    return results

def check_slot_dir_has_png(repo, rel_path):
    base_dir = rel_path.split("{")[0].rstrip("/")
    abs_dir = os.path.join(repo, base_dir)
    if not os.path.isdir(abs_dir):
        return False, []
    pngs = []
    for root, dirs, files in os.walk(abs_dir):
        for f in sorted(files):
            if f.endswith('.png') and not f.endswith('.png.import'):
                pngs.append(os.path.join(root, f))
    return len(pngs) > 0, pngs

# 3. Check bidirectional exists for all existing/pending assets
print("=== ASSET BIDIRECTIONAL EXISTS CHECK ===")
existing_count = 0
pending_count = 0
existing_missing = []
pending_already_exists = []

for r in races:
    rid = r["race_id"]
    status = r["asset_naming_conventions"]["status"]
    print(f"\n--- Race: {rid} ---")
    for item in status.get("existing", []):
        path = item.split(" ")[0]
        if "{slot_id}" in path or "{item_id}" in path or "{slot}" in path or "{id}" in path:
            has_png, pngs = check_slot_dir_has_png(REPO, path)
            if not has_png:
                existing_missing.append(f"{rid} -> {path}")
                errors.append(f"[EXISTING MISSING] {rid} -> {path}")
                print(f"  ❌ EXISTING MISSING: {path} (0 png found)")
            else:
                existing_count += 1
                print(f"  ✓ EXISTING OK (DIR HAS {len(pngs)} PNGs): {path}")
        else:
            variants = expand_wildcards(path)
            missing = [v for v in variants if not os.path.exists(os.path.join(REPO, v))]
            if missing:
                for m in missing:
                    existing_missing.append(f"{rid} -> {m}")
                    errors.append(f"[EXISTING MISSING] {rid} -> {m}")
                print(f"  ❌ EXISTING MISSING: {path} (missing: {missing})")
            else:
                existing_count += 1
                print(f"  ✓ EXISTING OK: {path} ({len(variants)} files checked)")

    for item in status.get("pending", []):
        path = item.split(" ")[0]
        if "{slot_id}" in path or "{item_id}" in path or "{slot}" in path or "{id}" in path:
            has_png, pngs = check_slot_dir_has_png(REPO, path)
            if has_png:
                pending_already_exists.append(f"{rid} -> {path} (found {len(pngs)} pngs)")
                errors.append(f"[PENDING ALREADY EXISTS] {rid} -> {path}")
                print(f"  ❌ PENDING ALREADY EXISTS: {path} (found {len(pngs)} pngs)")
            else:
                pending_count += 1
                print(f"  ✓ PENDING OK (ABSENT): {path}")
        else:
            variants = expand_wildcards(path)
            found = [v for v in variants if os.path.exists(os.path.join(REPO, v))]
            if found:
                for fd in found:
                    pending_already_exists.append(f"{rid} -> {fd}")
                    errors.append(f"[PENDING ALREADY EXISTS] {rid} -> {fd}")
                print(f"  ❌ PENDING ALREADY EXISTS: {path} (already exists: {found})")
            else:
                pending_count += 1
                print(f"  ✓ PENDING OK (ABSENT): {path} ({len(variants)} files checked)")

print("\n=== SUMMARY: BIDIRECTIONAL ASSET STATUS ===")
print(f"existing but MISSING: {len(existing_missing)}")
for m in existing_missing:
    print(f"  - {m}")
print(f"pending but ALREADY EXISTS: {len(pending_already_exists)}")
for p in pending_already_exists:
    print(f"  - {p}")

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
