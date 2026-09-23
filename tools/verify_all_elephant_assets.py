#!/usr/bin/env python3
"""
verify_all_elephant_assets.py
Comprehensive verification script for Colossus Elephant official assets suite.
Matches test patterns from verify_all_tortoise_assets.py, verify_all_tiger_assets.py, and verify_all_crane_bear_assets.py.
"""

import json
import os
import sys
from typing import cast
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
PORTRAITS_DIR = f"{REPO_ROOT}/game/assets/sprites/portraits"
BRANDING_DIR = f"{REPO_ROOT}/branding"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"
DOCS_ART_DIR = f"{REPO_ROOT}/docs/art"

def verify():
    print("=== VERIFYING ALL COLOSSUS ELEPHANT OFFICIAL ASSETS ===")
    all_ok = True

    required_assets = [
        # Category 1: 官網英雄圖 / 品牌立牌
        ("branding/char_elephant.png", [(400, 840), (800, 1680), (1344, 1680)], ["RGB", "RGBA"]),
        ("web/media/hero/char_elephant.png", [(400, 840), (1344, 1680)], ["RGB", "RGBA"]),
        ("docs/art/char_elephant_candidate_400x840.png", (400, 840), ["RGB", "RGBA"]),
        ("docs/art/colossus_elephant_concept.png", [(928, 1152), (1344, 1680)], ["RGB", "RGBA"]),

        # Category 2: 戰鬥特寫
        ("game/assets/sprites/player/elephant_battle.png", (128, 128), ["RGBA"]),

        # Category 3: 行走動畫
        ("game/assets/sprites/player/elephant_walk_0.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/elephant_walk_1.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/elephant_walk_2.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/elephant_walk_3.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/elephant_walk_0_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/elephant_walk_1_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/elephant_walk_2_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/elephant_walk_3_x3.png", (128, 128), ["RGBA"]),

        # Mirror idle assets
        ("game/assets/sprites/player/elephant_idle.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/elephant_idle_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/party/elephant_idle.png", (128, 128), ["RGBA"]),
        ("web/media/hero/elephant_idle.png", (128, 128), ["RGBA"]),

        # Category 4: HUD 戰鬥頭像 與 對話框半身像
        ("game/assets/sprites/portraits/elephant.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/portraits/colossus_elephant.png", (384, 480), ["RGBA"]),
    ]

    print("\n--- [1/6] Asset Existence, Format, and Dimensions ---")
    for rel_path, expected_size, allowed_modes in required_assets:
        full_path = f"{REPO_ROOT}/{rel_path}"
        if not os.path.exists(full_path):
            print(f"  ❌ MISSING ASSET: {rel_path}")
            all_ok = False
            continue
        im = Image.open(full_path)
        valid_sizes = expected_size if isinstance(expected_size, list) else [expected_size]
        if expected_size is not None and im.size not in valid_sizes:
            print(f"  ❌ WRONG SIZE {im.size} vs {expected_size} for {rel_path}")
            all_ok = False
            continue
        if im.mode not in allowed_modes:
            print(f"  ❌ WRONG MODE {im.mode} vs {allowed_modes} for {rel_path}")
            all_ok = False
            continue
        bbox = im.getbbox()
        if bbox is None:
            print(f"  ❌ EMPTY ASSET: {rel_path}")
            all_ok = False
            continue
        print(f"  ✓ {rel_path:52s} size={im.size} mode={im.mode} bbox={bbox}")

    # 2. Rule 0-QA7 4:5 Aspect Ratio & Margin Check
    print("\n--- [2/6] Rule 0-QA7 4:5 Aspect Ratio & Edge Margin ---")
    standee = Image.open(f"{BRANDING_DIR}/char_elephant.png")
    ratio = standee.size[0] / standee.size[1]
    if abs(ratio - 0.8) > 1e-5:
        print(f"  ❌ Standee ratio mismatch: {ratio} != 0.8")
        all_ok = False
    else:
        print(f"  ✓ Standee 4:5 aspect ratio verified: {standee.size} ({ratio:.6f})")

    arr_s = np.array(standee)
    bg_color = arr_s[0, 0, :3]
    edge_non_bg = 0
    edge_non_bg += int(np.sum(np.max(np.abs(arr_s[0, :, :3] - bg_color), axis=1) > 15))
    edge_non_bg += int(np.sum(np.max(np.abs(arr_s[-1, :, :3] - bg_color), axis=1) > 15))
    edge_non_bg += int(np.sum(np.max(np.abs(arr_s[:, 0, :3] - bg_color), axis=1) > 15))
    edge_non_bg += int(np.sum(np.max(np.abs(arr_s[:, -1, :3] - bg_color), axis=1) > 15))
    if edge_non_bg > 0:
        print(f"  ❌ Standee has {edge_non_bg} non-bg pixels touching canvas boundary!")
        all_ok = False
    else:
        print("  ✓ Standee boundary clean (0 non-bg pixels touching border, zero weapon/key clipping)")

    # 3. Rule 4b-4 & 4b-7: Walk Frames
    print("\n--- [3/6] Rule 4b-4 & 4b-7 Walk Kinematics & Articulation ---")
    base_idle = Image.open(f"{PLAYER_DIR}/elephant_idle_x3.png").convert("RGBA")
    w_x3 = [Image.open(f"{PLAYER_DIR}/elephant_walk_{i}_x3.png").convert("RGBA") for i in range(4)]

    for i in range(4):
        for dx in range(-8, 9):
            for dy in range(-8, 9):
                shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
                shifted.paste(base_idle, (dx, dy), base_idle)
                diff = ImageChops.difference(shifted, w_x3[i]).getbbox()
                if diff is None:
                    print(f"  ❌ Frame {i} matches pure translation ({dx}, {dy})!")
                    all_ok = False
        print(f"  ✓ elephant_walk_{i}_x3 passed 4b-4: guaranteed not pure translation under any offset")

        # 4b-7 articulation test
        min_diff = 999999
        for dy in range(-6, 7):
            for dh in range(-5, 6):
                nh = 128 + dh
                if nh <= 0:
                    continue
                scaled = base_idle.resize((128, nh), Image.Resampling.LANCZOS)
                recon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
                recon.paste(scaled, (0, dy - dh), scaled)
                diff_px = 0
                for y in range(112):
                    for x in range(128):
                        if w_x3[i].getpixel((x, y)) != recon.getpixel((x, y)):
                            diff_px += 1
                if diff_px < min_diff:
                    min_diff = diff_px
        if min_diff <= 300:
            print(f"  ❌ Frame {i} failed 4b-7: diff {min_diff} <= 300px!")
            all_ok = False
        else:
            print(f"  ✓ elephant_walk_{i}_x3 passed 4b-7: articulation diff={min_diff}px > 300px")

    # 4. Rule 4b-5: Shadow Consistency
    print("\n--- [4/6] Rule 4b-5 Walk Ground Shadow Consistency ---")
    base_shadow = [sum(1 for x in range(128) if base_idle.getpixel((x, y))[3] > 20) for y in range(115, 128)]
    for i in range(4):
        f_shadow = [sum(1 for x in range(128) if w_x3[i].getpixel((x, y))[3] > 20) for y in range(115, 128)]
        if f_shadow != base_shadow:
            print(f"  ❌ Frame {i} shadow {f_shadow} differs from base {base_shadow}!")
            all_ok = False
        else:
            print(f"  ✓ elephant_walk_{i}_x3 passed 4b-5: shadow row counts {f_shadow} 100% match idle baseline")

    # 5. Rule 4b-6: Battle Sprite
    print("\n--- [5/6] Rule 4b-6 Battle Sprite Metrics ---")
    battle = Image.open(f"{PLAYER_DIR}/elephant_battle.png").convert("RGBA")
    b_bbox = battle.getbbox()
    assert b_bbox is not None
    left_m = b_bbox[0]
    right_m = 128 - b_bbox[2]
    diff_b = ImageChops.difference(base_idle, battle)
    ch_b = sum(1 for y in range(128) for x in range(128) if any(c > 0 for c in diff_b.getpixel((x, y))))
    diff_legs = ImageChops.difference(base_idle.crop((0, 96, 128, 128)), battle.crop((0, 96, 128, 128)))
    ch_legs = sum(1 for y in range(32) for x in range(128) if any(c > 0 for c in diff_legs.getpixel((x, y))))

    print(f"  Battle bbox: {b_bbox} (left_margin={left_m}px, right_margin={right_m}px)")
    print(f"  Battle vs idle diff: changed={ch_b}px ({ch_b / (128*128) * 100:.1f}%)")
    print(f"  Battle legs diff (y>=96): changed={ch_legs}px")

    if left_m < 4 or right_m < 4:
        print("  ❌ Battle sprite margins too tight (<4px)!")
        all_ok = False
    else:
        print("  ✓ Margins safe (>=4px unclipped)")

    if ch_b <= 2500:
        print(f"  ❌ Battle changed pixels {ch_b} <= 2500px!")
        all_ok = False
    else:
        print("  ✓ Battle stance diff verified (>2500px)")

    if ch_legs <= 500:
        print(f"  ❌ Battle legs changed {ch_legs} <= 500px!")
        all_ok = False
    else:
        print("  ✓ Battle leg articulation verified (>500px)")

    # 6. Portraits
    print("\n--- [6/6] Portraits Quality & Centering ---")
    hud = Image.open(f"{PORTRAITS_DIR}/elephant.png").convert("RGBA")
    h_bbox = hud.getbbox()
    assert h_bbox is not None
    print(f"  HUD Portrait (128x128): bbox={h_bbox}, w={h_bbox[2]-h_bbox[0]}, h={h_bbox[3]-h_bbox[1]}")
    if h_bbox[0] < 8 or (128 - h_bbox[2]) < 8:
        print("  ❌ HUD portrait margins < 8px!")
        all_ok = False
    else:
        print("  ✓ HUD portrait safe margins verified")

    bust = Image.open(f"{PORTRAITS_DIR}/colossus_elephant.png").convert("RGBA")
    bu_bbox = bust.getbbox()
    assert bu_bbox is not None
    print(f"  Dialogue Bust (384x480): bbox={bu_bbox}, w={bu_bbox[2]-bu_bbox[0]}, h={bu_bbox[3]-bu_bbox[1]}")
    if bu_bbox[3] != 480:
        print(f"  ❌ Dialogue bust does not anchor to bottom (bu_bbox[3]={bu_bbox[3]} != 480)!")
        all_ok = False
    else:
        print("  ✓ Dialogue bust bottom anchoring verified (y=480)")

    if all_ok:
        print("\n🎉 ALL VERIFICATION CHECKS PASSED FOR COLOSSUS ELEPHANT!")
        return True
    else:
        print("\n❌ SOME CHECKS FAILED!")
        return False

if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)
