#!/usr/bin/env python3
"""
verify_penguin_poses.py
Comprehensive verification test suite for The Steam Penguin (蒸氣企鵝) combat action poses (128x128 RGBA).
Mirrors verify_bear_poses.py and verify_crane_poses.py.
"""
import os
import hashlib
from typing import cast
from PIL import Image, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/penguin"
BATTLE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/battle/penguin"
POSES = ['idle', 'attack', 'hit', 'recover', 'skill', 'telegraph']
lut = [0] * 11 + [1] * 245

print("=== VERIFYING THE STEAM PENGUIN COMBAT POSES (128x128 RGBA) ===")

# 1. Existence and RGBA format in both POSES_DIR and BATTLE_DIR
images: dict[str, Image.Image] = {}
md5s: dict[str, str] = {}
for p in POSES:
    for d in [POSES_DIR, BATTLE_DIR]:
        path = os.path.join(d, f"{p}.png")
        assert os.path.exists(path), f"FAIL: Missing pose {path}"
        im = Image.open(path)
        assert im.size == (128, 128), f"FAIL: {p} size {im.size} != (128, 128)"
        assert im.mode == "RGBA", f"FAIL: {p} mode {im.mode} != RGBA"
        if d == POSES_DIR:
            images[p] = im.convert("RGBA")
            with open(path, "rb") as f:
                h = hashlib.md5(f.read()).hexdigest()
            assert h not in md5s.values(), f"FAIL: Duplicate MD5 hash for {p}!"
            md5s[p] = h
            print(f"✓ {p:10s}: exists, size=(128, 128), mode=RGBA, md5={h[:10]}...")

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
    px = images[p].load()
    assert px is not None
    bad_bounds = []
    for x in range(128):
        if cast(tuple[int, int, int, int], px[x, 0])[3] > 0: bad_bounds.append(f"top row y=0 at x={x}")
        if cast(tuple[int, int, int, int], px[x, 1])[3] > 0: bad_bounds.append(f"top row y=1 at x={x}")
        if cast(tuple[int, int, int, int], px[x, 126])[3] > 0: bad_bounds.append(f"bot row y=126 at x={x}")
        if cast(tuple[int, int, int, int], px[x, 127])[3] > 0: bad_bounds.append(f"bot row y=127 at x={x}")
    for y in range(128):
        if cast(tuple[int, int, int, int], px[0, y])[3] > 0: bad_bounds.append(f"left col x=0 at y={y}")
        if cast(tuple[int, int, int, int], px[1, y])[3] > 0: bad_bounds.append(f"left col x=1 at y={y}")
        if cast(tuple[int, int, int, int], px[126, y])[3] > 0: bad_bounds.append(f"right col x=126 at y={y}")
        if cast(tuple[int, int, int, int], px[127, y])[3] > 0: bad_bounds.append(f"right col x=127 at y={y}")
    if bad_bounds:
        print(f"  ❌ BOUNDARY FAIL on {p}: {len(bad_bounds)} non-zero pixels on outer edge! {bad_bounds[:3]}")
        margin_ok = False

assert margin_ok, "FAIL: Margin check failed"
print("✓ Margins Verification PASSED!")

# 3. Rule 4b-5: Ground shadow row consistency
print("\n--- Ground Shadow Verification (Rule 4b-5) ---")
idle_shadow = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], images['idle'].getpixel((x, y)))[3] > 20) for y in range(118, 128)]
print(f"Benchmark Penguin shadow counts: {idle_shadow}")
shadow_ok = True
for p in POSES:
    counts = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], images[p].getpixel((x, y)))[3] > 20) for y in range(118, 128)]
    print(f"  {p:10s}: shadow counts={counts}")
    if counts != idle_shadow:
        print(f"  ❌ SHADOW FAIL on {p}: {counts} != {idle_shadow}")
        shadow_ok = False
assert shadow_ok, "FAIL: Ground shadow check failed!"
print("✓ Rule 4b-5 PASSED: All 6 poses have 100% exact ground shadow matching baseline!")

# 4. Rule 4b-4: Guaranteed not pure translation
print("\n--- Pure Translation Exhaustive Search (Rule 4b-4) ---")
for p in ['attack', 'hit', 'recover', 'skill', 'telegraph']:
    min_diff = 999999
    best_shift = None
    for dx in range(-12, 13):
        for dy in range(-12, 13):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(images['idle'], (dx, dy), images['idle'])
            diff = ImageChops.difference(shifted, images[p])
            r, g, b, a = diff.split()
            mask = ImageChops.lighter(ImageChops.lighter(r, g), ImageChops.lighter(b, a))
            ch = mask.point(lut).tobytes().count(b'\x01')
            if ch < min_diff:
                min_diff = ch
                best_shift = (dx, dy)
    pct = (min_diff / (128 * 128)) * 100
    print(f"✓ {p:10s}: best shift={best_shift}, min residual diff={min_diff} px ({pct:.1f}%)")
    assert min_diff > 3000, f"FAIL: {p} is too close to pure translation ({min_diff} <= 3000)!"

# 5. Rule 4b-7: Whole-image vertical resize + translation
print("\n--- Whole-image Resize+Translate Verification (Rule 4b-7) ---")
w, h = 128, 128
for p in ['attack', 'hit', 'recover', 'skill', 'telegraph']:
    im_crop = images[p].crop((0, 0, 128, 115))
    best_resid = 999999
    best_param: tuple[int, int] = (0, 0)
    for dh in range(-8, 9):
        new_h = h + dh
        resized = images['idle'].resize((w, new_h), Image.Resampling.BICUBIC)
        for dy in range(-10, 11):
            recon = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            recon.paste(resized, (0, dy), resized)
            recon_crop = recon.crop((0, 0, 128, 115))
            diff = ImageChops.difference(recon_crop, im_crop)
            r, g, b, a = diff.split()
            mask = ImageChops.lighter(ImageChops.lighter(r, g), ImageChops.lighter(b, a))
            ch = mask.point(lut).tobytes().count(b'\x01')
            if ch < best_resid:
                best_resid = ch
                best_param = (dh, dy)
    print(f"✓ {p:10s}: best dh={best_param[0]:+2d}, dy={best_param[1]:+2d} | residual diff (y<115)={best_resid} px")
    assert best_resid > 2500, f"FAIL: {p} resembles vertical resize ({best_resid} <= 2500)!"

# 6. Rule 4b-10: Pairwise Difference Matrix across all 15 pairs
print("\n--- Pairwise Difference Matrix (Rule 4b-10: all >= 6000 px) ---")
pairwise_min = 999999
for i in range(len(POSES)):
    for j in range(i + 1, len(POSES)):
        p1, p2 = POSES[i], POSES[j]
        # Compare torso area y < 118
        c1 = images[p1].crop((0, 0, 128, 118))
        c2 = images[p2].crop((0, 0, 128, 118))
        diff = ImageChops.difference(c1, c2)
        r, g, b, a = diff.split()
        mask = ImageChops.lighter(ImageChops.lighter(r, g), ImageChops.lighter(b, a))
        ch = mask.point(lut).tobytes().count(b'\x01')
        print(f"  {p1:9s} <-> {p2:9s}: {ch:5d} px")
        if ch < pairwise_min:
            pairwise_min = ch
print(f"✓ Minimum pairwise diff across all 15 pairs: {pairwise_min} px (threshold: >= 6000 px)")
assert pairwise_min >= 6000, f"FAIL: Minimum pairwise diff {pairwise_min} < 6000 px!"

# 7. Rule 4b-9: Unified Scale Verification
print("\n--- Unified Scale Verification (Rule 4b-9) ---")
idle_bbox = images['idle'].getbbox()
assert idle_bbox is not None
idle_h = idle_bbox[3] - idle_bbox[1]
for p in POSES:
    bbox = images[p].getbbox()
    assert bbox is not None
    h_curr = bbox[3] - bbox[1]
    diff_pct = abs(h_curr - idle_h) / float(idle_h) * 100
    print(f"  {p:10s}: height={h_curr} (diff vs idle: {diff_pct:.2f}%)")
    assert diff_pct <= 5.5, f"FAIL: {p} height diff {diff_pct:.2f}% > 5.5%"

# Check body pixel volume (y < 115)
idle_vol = sum(1 for y in range(115) for x in range(128) if cast(tuple[int, int, int, int], images['idle'].getpixel((x, y)))[3] > 8)
print(f"\n--- Body Pixel Volume Verification (y<115, idle={idle_vol} px) ---")
for p in POSES:
    vol = sum(1 for y in range(115) for x in range(128) if cast(tuple[int, int, int, int], images[p].getpixel((x, y)))[3] > 8)
    ratio = vol / float(idle_vol) * 100
    print(f"  {p:10s}: vol={vol:5d} px ({ratio:.1f}% of idle)")
    assert 80.0 <= ratio <= 125.0, f"FAIL: {p} body volume {ratio:.1f}% outside 80..125%"

print("\n=== ALL 7 AUTOMATED METRIC VERIFICATIONS PASSED SUCCESSFULLY! ===")
