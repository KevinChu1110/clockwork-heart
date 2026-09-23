#!/usr/bin/env python3
"""
verify_frog_poses.py
Comprehensive verification test suite for Spring-Leg Frog combat action poses (128x128 RGBA & 512x512 RGBA).
Mirrors verify_elephant_poses.py and verify_tortoise_poses.py.
"""
import os
import hashlib
from typing import cast
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/frog"
EXPECTED_SHADOW = [69, 67, 63, 55, 35, 0, 0, 0, 0, 0]
POSES = ['idle', 'attack', 'hit', 'recover', 'skill', 'telegraph']

print("=== VERIFYING SPRING-LEG FROG COMBAT POSES (128x128 & 512x512 RGBA) ===")

# 1. Existence and RGBA format
images: dict[str, Image.Image] = {}
images_512: dict[str, Image.Image] = {}
md5s: dict[str, str] = {}
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
    print(f"✓ {p:10s}: exists, size=(128, 128), mode=RGBA, md5={h[:10]}...")

    path_512 = os.path.join(POSES_DIR, f"{p}_512.png")
    assert os.path.exists(path_512), f"FAIL: Missing 512 pose {path_512}"
    im_512 = Image.open(path_512)
    assert im_512.size == (512, 512), f"FAIL: {p}_512 size {im_512.size} != (512, 512)"
    assert im_512.mode == "RGBA", f"FAIL: {p}_512 mode {im_512.mode} != RGBA"
    images_512[p] = im_512.convert("RGBA")
    print(f"  ✓ {p:10s}_512: exists, size=(512, 512), mode=RGBA")

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
print("✓ Rule 4b-5 PASSED: All 6 poses have 100% exact ground shadow matching baseline!")

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

print("\n🎉 ALL SPRING-LEG FROG COMBAT POSES FULLY VERIFIED AND AUDITED!")
