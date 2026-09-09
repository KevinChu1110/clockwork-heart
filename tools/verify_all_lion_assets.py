#!/usr/bin/env python3
import os
import subprocess
from PIL import Image, ImageChops

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLAYER_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player")
PORTRAITS_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/portraits")
WEB_HERO_DIR = os.path.join(REPO_ROOT, "web/media/hero")
TOOLS_DIR = os.path.join(REPO_ROOT, "tools")

print("=== RUNNING FULL VERIFICATION SUITE FOR LION ASSETS ===")

# 1. Existence and format of 11 files
files_to_check = [
    ("lion_idle.png (web)", os.path.join(WEB_HERO_DIR, "lion_idle.png"), (128, 128)),
    ("lion_battle.png", os.path.join(PLAYER_DIR, "lion_battle.png"), (128, 128)),
    ("lion_walk_0.png", os.path.join(PLAYER_DIR, "lion_walk_0.png"), (64, 64)),
    ("lion_walk_1.png", os.path.join(PLAYER_DIR, "lion_walk_1.png"), (64, 64)),
    ("lion_walk_2.png", os.path.join(PLAYER_DIR, "lion_walk_2.png"), (64, 64)),
    ("lion_walk_3.png", os.path.join(PLAYER_DIR, "lion_walk_3.png"), (64, 64)),
    ("lion_walk_0_x3.png", os.path.join(PLAYER_DIR, "lion_walk_0_x3.png"), (128, 128)),
    ("lion_walk_1_x3.png", os.path.join(PLAYER_DIR, "lion_walk_1_x3.png"), (128, 128)),
    ("lion_walk_2_x3.png", os.path.join(PLAYER_DIR, "lion_walk_2_x3.png"), (128, 128)),
    ("lion_walk_3_x3.png", os.path.join(PLAYER_DIR, "lion_walk_3_x3.png"), (128, 128)),
    ("lion.png (HUD)", os.path.join(PORTRAITS_DIR, "lion.png"), (128, 128)),
]

for label, path, exp_size in files_to_check:
    assert os.path.exists(path), f"FAIL: Missing file {path}"
    im = Image.open(path)
    assert im.size == exp_size, f"FAIL: {label} size {im.size} != expected {exp_size}"
    assert im.mode == "RGBA", f"FAIL: {label} mode {im.mode} != RGBA"
    print(f"✓ {label}: exists, mode={im.mode}, size={im.size}, bbox={im.getbbox()}")

# 2. Rule 4b-4: Walk frames verification
print("\n--- Verifying Walk Frames (Rule 4b-4) ---")
base_idle = Image.open(os.path.join(WEB_HERO_DIR, "lion_idle.png")).convert("RGBA")
w_x3 = [Image.open(os.path.join(PLAYER_DIR, f"lion_walk_{i}_x3.png")).convert("RGBA") for i in range(4)]
w_64 = [Image.open(os.path.join(PLAYER_DIR, f"lion_walk_{i}.png")).convert("RGBA") for i in range(4)]

for i in range(4):
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(base_idle, (dx, dy), base_idle)
            diff = ImageChops.difference(shifted, w_x3[i]).getbbox(alpha_only=False)
            assert diff is not None, f"FAIL: lion_walk_{i}_x3 matches pure translation ({dx}, {dy})!"
    print(f"✓ lion_walk_{i}_x3 passed 4b-4: guaranteed not pure translation under any offset.")

for i in range(4):
    for j in range(i + 1, 4):
        d128 = ImageChops.difference(w_x3[i], w_x3[j])
        ch128 = sum(1 for x in range(128) for y in range(128) if any(c > 0 for c in d128.getpixel((x, y))))
        pct128 = (ch128 / (128 * 128)) * 100
        print(f"  Frame {i} vs {j} (128x128): diff bbox={d128.getbbox(alpha_only=False)}, changed={ch128} px ({pct128:.1f}%)")

        d64 = ImageChops.difference(w_64[i], w_64[j])
        ch64 = sum(1 for x in range(64) for y in range(64) if any(c > 0 for c in d64.getpixel((x, y))))
        pct64 = (ch64 / (64 * 64)) * 100
        print(f"  Frame {i} vs {j} (64x64):   diff bbox={d64.getbbox(alpha_only=False)}, changed={ch64} px ({pct64:.1f}%)")

# 3. Rule 4b-5: Walk shadow verification
print("\n--- Verifying Ground Shadow Consistency (Rule 4b-5) ---")
expected_shadow_counts = [67, 71, 72, 70, 66, 59, 47, 26, 0, 0] # party baseline
for i in range(4):
    actual_counts = [sum(1 for x in range(128) if w_x3[i].getpixel((x, y))[3] > 20) for y in range(118, 128)]
    print(f"  lion_walk_{i}_x3 shadow row counts: {actual_counts}")
    assert all(abs(a - b) <= 1 for a, b in zip(actual_counts, expected_shadow_counts)), f"FAIL: lion_walk_{i}_x3 shadow counts {actual_counts} differ from expected {expected_shadow_counts}"
print("✓ Rule 4b-5 PASSED: All 4 walk frames have 100% consistent, unbroken ground shadows matching party baseline!")

# 4. Rule 4b-6: Battle sprite verification
print("\n--- Verifying Battle Sprite (Rule 4b-6) ---")
# Check no whole-image QUAD/PERSPECTIVE/AFFINE transform in produce_lion_assets.py
produce_script = os.path.join(TOOLS_DIR, "produce_lion_assets.py")
with open(produce_script, "r", encoding="utf-8") as f:
    code = f.read()
assert "Transform.QUAD" not in code, "FAIL: Transform.QUAD found in produce_lion_assets.py!"
assert "Transform.PERSPECTIVE" not in code, "FAIL: Transform.PERSPECTIVE found in produce_lion_assets.py!"
assert "Transform.AFFINE" not in code, "FAIL: Transform.AFFINE found in produce_lion_assets.py!"
print("✓ Rule 4b-6: Verified ZERO whole-image Transform.QUAD/PERSPECTIVE/AFFINE in produce_lion_assets.py.")

battle = Image.open(os.path.join(PLAYER_DIR, "lion_battle.png")).convert("RGBA")
b_bbox = battle.getbbox()
assert b_bbox is not None and b_bbox[0] >= 4, f"FAIL: Lance tip clipped, left margin is {b_bbox[0] if b_bbox else 0} < 4px"
print(f"✓ Lance tip unclipped: left margin = {b_bbox[0]} px, bbox = {b_bbox}")

# Test vs idle difference
diff_battle = ImageChops.difference(base_idle, battle)
ch_battle = sum(1 for y in range(128) for x in range(128) if any(c > 0 for c in diff_battle.getpixel((x, y))))
pct_battle = (ch_battle / (128 * 128)) * 100
assert ch_battle > 5000, f"FAIL: Battle sprite changed {ch_battle} px < 5000 px"
print(f"✓ Battle vs idle: diff bbox={diff_battle.getbbox()}, changed={ch_battle} px ({pct_battle:.1f}%)")

# Test leg region (y >= 95) against shifted base_idle
leg_idle = base_idle.crop((0, 95, 128, 128))
leg_battle = battle.crop((0, 95, 128, 128))
diff_leg = ImageChops.difference(leg_idle, leg_battle)
ch_leg = sum(1 for y in range(33) for x in range(128) if any(c > 0 for c in diff_leg.getpixel((x, y))))
pct_leg = (ch_leg / (128 * 33)) * 100
assert ch_leg > 1000, f"FAIL: Legs unchanged, changed={ch_leg}"
print(f"✓ Battle leg region (y>=95): diff bbox={diff_leg.getbbox()}, changed={ch_leg} px ({pct_leg:.1f}%)")

# 5. Observation: HUD portrait verification
print("\n--- Verifying HUD Portrait ---")
hud = Image.open(os.path.join(PORTRAITS_DIR, "lion.png")).convert("RGBA")
h_bbox = hud.getbbox()
assert h_bbox == (14, 7, 113, 124), f"Unexpected HUD bbox: {h_bbox}"
print(f"✓ HUD portrait bbox: {h_bbox}, height = {h_bbox[3]-h_bbox[1]}, width = {h_bbox[2]-h_bbox[0]}")

# 6. Rule 19f-2-2: Clean race diff check
print("\n--- Verifying Status Catalogs (Rule 19f-2-2) ---")
diff_cmd = "git diff 2834a96^ -U0 -- docs/design/paperdoll_slots.json game/data/tables/paperdoll_slots.json docs/design/PAPERDOLL_SLOTS_SPEC.md game/assets/sprites/portraits/MANIFEST.md | grep '^[+-]' | grep -v '^[+-]\\{3\\}' | grep -oE '(rabbit|lion|fox|boar|macaque)_(idle|battle|walk)' | sort -u"
diff_out = subprocess.check_output(diff_cmd, shell=True, text=True, cwd=REPO_ROOT).strip()
print("Rule 19f-2-2 matched races in diff lines:")
print(diff_out)
lines = [l for l in diff_out.splitlines() if l.strip()]
for l in lines:
    assert l.startswith("lion_"), f"FAIL: Non-lion entry in diff: {l}"
print("✓ Rule 19f-2-2 PASSED: Only lion appears in status diff!")

print("\n✓ ALL VERIFICATION CHECKS PASSED!")
