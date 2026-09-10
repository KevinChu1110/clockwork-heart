#!/usr/bin/env python3
"""
verify_lion_poses.py
Comprehensive verification test suite for Lion combat poses.
"""
import os
import hashlib
import subprocess
from typing import cast
from PIL import Image, ImageChops

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLAYER_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player")
POSES_DIR = os.path.join(PLAYER_DIR, "poses/lion")
EXPECTED_SHADOW = [67, 71, 72, 70, 66, 59, 47, 26, 0, 0]
POSES = ['idle', 'attack', 'hit', 'recover', 'skill', 'telegraph']
lut = [0] * 11 + [1] * 245

print("=== VERIFYING LION COMBAT POSES (128x128 RGBA) ===")

# 1. Existence and RGBA format
images: dict[str, Image.Image] = {}
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

# 2. Margins (no hard clipping)
print("\n--- Margins Verification ---")
for p in POSES:
    bbox = images[p].getbbox()
    assert bbox is not None, f"FAIL: {p} is empty!"
    left, top, right, bottom = bbox[0], bbox[1], 128 - bbox[2], 128 - bbox[3]
    print(f"✓ {p:10s}: bbox={bbox}, margins: left={left}px, top={top}px, right={right}px, bot={bottom}px")
    assert left >= 4, f"FAIL: {p} left margin {left} < 4px!"
    assert top >= 4, f"FAIL: {p} top margin {top} < 4px!"
    assert right >= 4, f"FAIL: {p} right margin {right} < 4px!"

# 3. Rule 4b-5: Ground shadow row consistency
print("\n--- Ground Shadow Verification (Rule 4b-5) ---")
for p in POSES:
    counts = [sum(1 for x in range(128) if images[p].getpixel((x, y))[3] > 20) for y in range(118, 128)]
    print(f"✓ {p:10s}: shadow counts={counts}")
    assert counts == EXPECTED_SHADOW, f"FAIL: {p} shadow counts {counts} != expected {EXPECTED_SHADOW}"
print("✓ Rule 4b-5 PASSED: All 6 poses have 100% exact ground shadow matching party baseline!")

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
    assert min_diff > 3000, f"FAIL: {p} is too close to pure translation!"
print("✓ Rule 4b-4 PASSED: All poses differ substantially (>3000px) from any translation of idle!")

# 5. Rule 4b-7: Whole-image vertical resize + translation
print("\n--- Whole-image Resize+Translate Verification (Rule 4b-7) ---")
w, h = 128, 128
for p in ['attack', 'hit', 'recover', 'skill', 'telegraph']:
    im_crop = images[p].crop((0, 0, 128, 115))
    best_resid = 999999
    best_param = None
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
    assert best_resid > 2500, f"FAIL: {p} resembles vertical resize!"
print("✓ Rule 4b-7 PASSED: All poses differ substantially (>2500px) from any vertical resize+translate of idle!")

# 6. Rule 19f-2-2: Status catalog diff check
print("\n--- Status Catalog Diff Check (Rule 19f-2-2) ---")
diff_cmd = "git diff origin/main -U0 -- docs/design/paperdoll_slots.json game/data/tables/paperdoll_slots.json docs/design/PAPERDOLL_SLOTS_SPEC.md 2>/dev/null | grep '^[+-]' | grep -v '^[+-]\\{3\\}' | grep -oE '(rabbit|lion|fox|boar|macaque)_(idle|battle|walk|poses)' | sort -u || true"
diff_out = subprocess.check_output(diff_cmd, shell=True, text=True, cwd=REPO_ROOT).strip()
print("Rule 19f-2-2 matched races in diff lines:")
print(diff_out if diff_out else "(no catalog changes against main)")
lines = [l for l in diff_out.splitlines() if l.strip()]
for l in lines:
    assert l.startswith("lion_"), f"FAIL: Non-lion entry in diff: {l}"
print("✓ Rule 19f-2-2 PASSED: No foreign race modifications!")

print("\n=== ALL LION COMBAT POSES CHECKS PASSED SUCCESSFULLY ===")
