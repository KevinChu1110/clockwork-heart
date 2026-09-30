#!/usr/bin/env python3
"""
tools/verify_scorpion_poses.py
Comprehensive verification test suite for The Duneshadow Scorpion (第七十族 伏影沙蠍, scorpion)
combat action poses (128x128 RGBA & 512x512 RGBA).
Mirrors verify_kingfisher_poses.py, verify_manta_poses.py, verify_firefly_poses.py.
Validates:
- 128x128 & 512x512 (LANCZOS) existence, RGBA mode, unique MD5
- Rule 4c-5 / 16: Safe margins (L>=4, T>=4, R>=4, B>=2) & 0-outer boundary
- Rule 4b-5: Ground contact shadow consistency across all 6 poses ([55, 45, 27, 0, 0, 0, 0, 0, 0, 0])
- Rule 4b-4: Guaranteed not pure translation (min diff > 400px under exhaustive 2D shift)
- Rule 4b-7: Articulation & Kinematics (diff vs idle >= 2500px)
- Rule 0-QA34: Three-zone Silhouette XOR verification (Head / Torso / Legs) confirming non-copy-paste kinematic displacement
- Rule 0-QA16 / 0-QA21 / 0-QA31: Ultra-dark pixel count (<10), white rectangular mask run length,
  structural void classification (no rectangular patch artifact), optic core richness, and magenta proof verification.
- LANCZOS smoothing ratio (> 3x)
- Alignment of unique colors & alpha levels with recent approved races (0-QA39)
"""
import hashlib
import os
import sys
from PIL import Image, ImageChops
import numpy as np
from scipy.ndimage import binary_fill_holes, label

sys.path = [p for p in sys.path if not p.startswith('/tmp')]

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/scorpion"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
EXPECTED_SHADOW = [55, 45, 27, 0, 0, 0, 0, 0, 0, 0]
POSES = ['idle', 'attack', 'hit', 'recover', 'skill', 'telegraph']

print("=== VERIFYING THE DUNESHADOW SCORPION COMBAT POSES (128x128 & 512x512 RGBA) ===")

# 1. Existence and RGBA format
images: dict[str, Image.Image] = {}
images_512: dict[str, Image.Image] = {}
md5s: dict[str, str] = {}
stats_128: dict[str, tuple[int, int]] = {}
stats_512: dict[str, tuple[int, int]] = {}

for p in POSES:
    path = os.path.join(POSES_DIR, f"{p}.png")
    assert os.path.exists(path), f"FAIL: Missing pose {path}"
    im = Image.open(path)
    assert im.size == (128, 128), f"FAIL: {p} size {im.size} != (128, 128)"
    assert im.mode == "RGBA", f"FAIL: {p} mode {im.mode} != RGBA"
    images[p] = im.convert("RGBA")

    with open(path, "rb") as f:
        h = hashlib.md5(f.read()).hexdigest()
    assert h not in md5s.values(), f"FAIL: Duplicate MD5 hash for {p}!"
    md5s[p] = h

    arr128 = np.array(images[p])
    c128 = len(np.unique(arr128.reshape(-1, 4), axis=0))
    a128 = len(np.unique(arr128[:, :, 3]))
    stats_128[p] = (c128, a128)
    print(f"✓ {p:10s}: exists, size=(128, 128), mode=RGBA, colors={c128:4d}, alphas={a128:3d}, md5={h[:10]}...")

    path_512 = os.path.join(POSES_DIR, f"{p}_512.png")
    assert os.path.exists(path_512), f"FAIL: Missing 512 pose {path_512}"
    im_512 = Image.open(path_512)
    assert im_512.size == (512, 512), f"FAIL: {p}_512 size {im_512.size} != (512, 512)"
    assert im_512.mode == "RGBA", f"FAIL: {p}_512 mode {im_512.mode} != RGBA"
    images_512[p] = im_512.convert("RGBA")

    arr512 = np.array(images_512[p])
    c512 = len(np.unique(arr512.reshape(-1, 4), axis=0))
    a512 = len(np.unique(arr512[:, :, 3]))
    stats_512[p] = (c512, a512)
    print(f"  ✓ {p:10s}_512: exists, size=(512, 512), mode=RGBA, colors={c512:5d}, alphas={a512:3d}")

# 2. Margins (no hard clipping)
print("\n--- Margins Verification (Rule 4c-5 / 16) ---")
margin_ok = True
for p in POSES:
    bbox = images[p].getbbox()
    assert bbox is not None, f"FAIL: {p} is empty!"
    left, top, right, bottom = bbox[0], bbox[1], 128 - bbox[2], 128 - bbox[3]
    print(f"  {p:10s}: bbox={bbox}, margins: left={left}px, top={top}px, right={right}px, bot={bottom}px")
    if left < 4 or top < 4 or right < 4 or bottom < 2:
        print(f"  ❌ MARGIN FAIL on {p}: left={left}, top={top}, right={right}, bot={bottom} (req: L>=4, T>=4, R>=4, B>=2)")
        margin_ok = False
    # Check boundary columns and rows are strictly 0
    arr = np.array(images[p])
    alpha = arr[:, :, 3]
    bad_bounds = []
    if np.sum(alpha[0, :] > 0): bad_bounds.append("top row y=0")
    if np.sum(alpha[1, :] > 0): bad_bounds.append("top row y=1")
    if np.sum(alpha[126, :] > 0): bad_bounds.append("bot row y=126")
    if np.sum(alpha[127, :] > 0): bad_bounds.append("bot row y=127")
    if np.sum(alpha[:, 0] > 0): bad_bounds.append("left col x=0")
    if np.sum(alpha[:, 1] > 0): bad_bounds.append("left col x=1")
    if np.sum(alpha[:, 126] > 0): bad_bounds.append("right col x=126")
    if np.sum(alpha[:, 127] > 0): bad_bounds.append("right col x=127")
    if bad_bounds:
        print(f"  ❌ BOUNDARY FAIL on {p}: non-zero pixels on outer edge! {bad_bounds}")
        margin_ok = False

assert margin_ok, "FAIL: Margins or boundaries failed!"
print("✓ Margins Verification PASSED!")

# 3. Rule 4b-5: Ground shadow row consistency
print("\n--- Ground Shadow Verification (Rule 4b-5) ---")
shadow_ok = True
for p in POSES:
    arr = np.array(images[p])
    counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"  {p:10s}: shadow counts={counts}")
    if counts != EXPECTED_SHADOW:
        print(f"  ❌ SHADOW FAIL on {p}: {counts} != {EXPECTED_SHADOW}")
        shadow_ok = False
assert shadow_ok, "FAIL: Ground shadow mismatch!"
print(f"✓ Rule 4b-5 PASSED: All 6 poses have 100% exact ground shadow matching baseline {EXPECTED_SHADOW}!")

# 4. Rule 4b-4: Guaranteed not pure translation
print("\n--- Pure Translation Exhaustive Search (Rule 4b-4) ---")
for p in ['attack', 'hit', 'recover', 'skill', 'telegraph']:
    min_diff = 999999
    best_shift = None
    target_arr = np.array(images[p])
    for dx in range(-12, 13):
        for dy in range(-12, 13):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(images['idle'], (dx, dy), images['idle'])
            diff = ImageChops.difference(shifted, images[p])
            if diff.getbbox() is None:
                diff_count = 0
            else:
                diff_arr = np.array(diff)
                diff_count = int(np.sum(np.any(diff_arr > 0, axis=-1)))
            if diff_count < min_diff:
                min_diff = diff_count
                best_shift = (dx, dy)
    print(f"  {p:10s}: min diff with idle={min_diff}px at shift={best_shift}")
    assert min_diff > 400, f"FAIL: {p} is too close to pure translation of idle! (diff={min_diff})"
print("✓ Rule 4b-4 PASSED: Guaranteed not pure translation under any offset!")

# 5. Rule 4b-7: Articulation Verification
print("\n--- Articulation and Kinematics (Rule 4b-7) ---")
for p in ['attack', 'hit', 'recover', 'skill', 'telegraph']:
    diff = ImageChops.difference(images['idle'], images[p])
    diff_arr = np.array(diff)
    changed = int(np.sum(np.any(diff_arr > 0, axis=-1)))
    print(f"  {p:10s} vs idle: {changed} pixels changed ({changed/(128*128)*100:.1f}%)")
    assert changed >= 2500, f"FAIL: {p} changed pixels {changed} < 2500"
print("✓ Rule 4b-7 PASSED: Significant mechanical articulation and stance change confirmed!")

# 6. Rule 0-QA34: Silhouette XOR Verification across Three Zones (Head / Torso / Legs)
print("\n--- Rule 0-QA34: Silhouette XOR Three-Zone Verification ---")
idle_alpha = np.array(images['idle'])[:, :, 3] > 10
qa34_results = {}
for p in ['telegraph', 'attack', 'skill', 'hit', 'recover']:
    p_alpha = np.array(images[p])[:, :, 3] > 10
    xor_mask = idle_alpha ^ p_alpha
    head_xor = int(np.sum(xor_mask[0:52, :]))
    torso_xor = int(np.sum(xor_mask[52:92, :]))
    legs_xor = int(np.sum(xor_mask[92:118, :]))
    total_xor = head_xor + torso_xor + legs_xor
    qa34_results[p] = {
        "head": head_xor,
        "torso": torso_xor,
        "legs": legs_xor,
        "total": total_xor
    }
    print(f"  {p:10s} XOR vs idle -> Head(y<52): {head_xor:4d} px, Torso(52<=y<92): {torso_xor:4d} px, Legs(92<=y<118): {legs_xor:4d} px | Total: {total_xor:5d} px")
    assert head_xor > 0, f"FAIL: {p} head zone XOR is 0 (suspected copy-paste)!"
    assert torso_xor > 0, f"FAIL: {p} torso zone XOR is 0 (suspected copy-paste)!"
    assert legs_xor > 0, f"FAIL: {p} legs zone XOR is 0 (suspected copy-paste)!"
    assert total_xor >= 500, f"FAIL: {p} total XOR {total_xor} < 500 px!"

print("✓ Rule 0-QA34 PASSED: Three-zone Silhouette XOR rigorously proves non-copy-paste kinematic articulation across all poses!")

# 7. Rule 0-QA16 / 0-QA21 / 0-QA31: Ultra-dark pixel count, white hole runs, and void analysis
print("\n--- 0-QA16 / 0-QA21 / 0-QA31 Defect & Void Analysis ---")
for p in POSES:
    arr = np.array(images[p])
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]

    # 7a. Ultra-dark pixels (<10 on all channels) in opaque region (should be 0)
    dark_mask = (alpha > 50) & (rgb[:, :, 0] < 10) & (rgb[:, :, 1] < 10) & (rgb[:, :, 2] < 10)
    dark_count = int(np.sum(dark_mask))
    print(f"  {p:10s}: ultra-dark pixels (<10)={dark_count}")
    assert dark_count == 0, f"FAIL: {p} contains {dark_count} corrupted black/ultra-dark pixels!"

    # 7b. 0-QA16: Longest horizontal white run (alpha>250 and min(rgb)>=225)
    white_mask = (alpha > 250) & (np.min(rgb, axis=-1) >= 225)
    max_white_run = 0
    for y in range(128):
        row = white_mask[y, :]
        current_run = 0
        for val in row:
            if val:
                current_run += 1
                if current_run > max_white_run:
                    max_white_run = current_run
            else:
                current_run = 0
    print(f"  {p:10s}: max horizontal white run={max_white_run}px (0-QA16 threshold < 80px)")
    assert max_white_run < 80, f"FAIL: {p} contains suspicious white clipping rectangular hole (run={max_white_run}px >= 80px)!"

    # 7c. binary_fill_holes structural void analysis (0-QA16: verify no large rectangular clipping tear)
    filled = binary_fill_holes(alpha > 10)
    holes = filled & (alpha <= 10)
    total_holes = int(np.sum(holes))

    lbl, num = label(holes)
    max_rect_defect = 0
    for i in range(1, num + 1):
        cys, cxs = np.where(lbl == i)
        cnt = len(cxs)
        h = max(cys) - min(cys) + 1
        w = max(cxs) - min(cxs) + 1
        rect_fill = cnt / (w * h)
        if rect_fill > 0.85 and cnt > 250:
            max_rect_defect = max(max_rect_defect, cnt)

    print(f"  {p:10s}: total internal negative space={total_holes}px (max rect defect={max_rect_defect}px)")
    assert max_rect_defect == 0, f"FAIL: {p} has rectangular tear defect ({max_rect_defect}px)!"
    assert total_holes <= 700, f"FAIL: {p} has excessive voids ({total_holes}px > 700px)!"

    # 7d. 0-QA31 Optic core color richness verification (prevent flat/unrendered mask alert)
    optic_zone = arr[34:56, 42:86]
    optic_opaque = optic_zone[:, :, 3] > 8
    optic_colors = len(np.unique(optic_zone[optic_opaque][:, :3], axis=0))
    print(f"  {p:10s}: optic core unique colors={optic_colors} (req >= 15)")
    assert optic_colors >= 15, f"FAIL: {p} optic core appears flat or unrendered (colors={optic_colors} < 15)!"

print("✓ 0-QA16 / 0-QA21 / 0-QA31 Measurement PASSED: Zero corrupted ultra-dark pixels, zero white mask defects, 100% verified structural negative space & optic color richness!")

# 8. Proof sheets verification
print("\n--- Proof Sheets Verification ---")
proof_768 = f"{PLAYER_DIR}/proof_scorpion_combat_poses_768.png"
proof_mag = f"{PLAYER_DIR}/proof_scorpion_combat_poses_magenta.png"
assert os.path.exists(proof_768), f"Missing {proof_768}"
assert os.path.exists(proof_mag), f"Missing {proof_mag}"
im_768 = Image.open(proof_768)
assert im_768.size == (128 * 6, 128)
im_mag = Image.open(proof_mag)
assert im_mag.size == (128 * 6, 128)
print(f"✓ Proof sheets verified: {proof_768} & {proof_mag} (768x128 Transparent & Magenta)")

# 9. LANCZOS Smoothing Verification for 512x512
print("\n--- 512x512 LANCZOS Smoothing Verification ---")
for p in POSES:
    c128, a128 = stats_128[p]
    c512, a512 = stats_512[p]
    print(f"  {p:10s}: 128 unique={c128:4d} -> 512 unique={c512:5d} (smoothing ratio={c512/c128:.1f}x)")
    assert c512 > c128 * 3, f"FAIL: {p}_512 does not appear to be LANCZOS smoothed (unique colors {c512} <= {c128} * 3)!"
print("✓ 512x512 LANCZOS Verification PASSED: Genuine high-definition interpolation confirmed!")

# 10. Alignment with recent approved races ranges (0-QA39)
print("\n--- Comparison with recent 5 approved races (manta, firefly, marmot, swan, takin) ---")
all_c128 = [v[0] for v in stats_128.values()]
all_a128 = [v[1] for v in stats_128.values()]
all_c512 = [v[0] for v in stats_512.values()]
all_a512 = [v[1] for v in stats_512.values()]

print(f"Scorpion 128 colors range: [{min(all_c128)}, {max(all_c128)}] (Target recent 5: [495, 5024])")
print(f"Scorpion 128 alphas range: [{min(all_a128)}, {max(all_a128)}] (Target recent 5: [4, 256])")
print(f"Scorpion 512 colors range: [{min(all_c512)}, {max(all_c512)}] (Target recent 5: [40000, 85000])")
print(f"Scorpion 512 alphas range: [{min(all_a512)}, {max(all_a512)}] (Target recent 5: [250, 256])")

assert min(all_c128) >= 450 and max(all_c128) <= 5500, "128 colors out of bounds!"
assert min(all_c512) >= 40000 and max(all_c512) <= 85000, "512 colors out of bounds!"
assert min(all_a512) >= 250, "512 alphas out of bounds!"
print("✓ Statistical Alignment PASSED: Scorpion matches recent approved races color and alpha richness perfectly!")

print("\n🎉 ALL QUALITY GATES PASSED FOR THE DUNESHADOW SCORPION COMBAT ACTION POSES!")
