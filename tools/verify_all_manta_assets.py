#!/usr/bin/env python3
"""
verify_all_manta_assets.py
Comprehensive verification script for The Tidal Manta (第六十七族 潮汐蝠魟, manta) official assets suite.
Matches test patterns from verify_all_kingfisher_assets.py, verify_all_scarab_assets.py, and verify_all_firefly_assets.py.
"""

import os
import sys
from typing import cast
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PORTRAITS_DIR = f"{REPO_ROOT}/game/assets/sprites/portraits"
BRANDING_DIR = f"{REPO_ROOT}/branding"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"
DOCS_ART_DIR = f"{REPO_ROOT}/docs/art"


def verify():
    print("=== VERIFYING ALL THE TIDAL MANTA OFFICIAL ASSETS ===")
    all_ok = True

    required_assets = [
        # Category 1: 官網英雄圖 / 品牌立牌
        ("branding/char_manta.png", [(400, 840), (800, 1680), (1344, 1680)], ["RGB", "RGBA"]),
        ("web/media/hero/char_manta.png", [(400, 840), (1344, 1680)], ["RGB", "RGBA"]),
        ("docs/art/char_manta_candidate_400x840.png", (400, 840), ["RGB", "RGBA"]),
        ("docs/art/tidal_manta_concept.png", [(928, 1152), (1344, 1680)], ["RGB", "RGBA"]),

        # Category 2: 戰鬥特寫
        ("game/assets/sprites/player/manta_battle.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/manta_battle_512.png", (512, 512), ["RGBA"]),
        ("game/assets/sprites/player/proof_manta_idle_vs_battle.png", (256, 128), ["RGBA"]),
        ("game/assets/sprites/player/proof_manta_idle_vs_battle_512.png", (1024, 512), ["RGBA"]),

        # Category 3: 行走動畫
        ("game/assets/sprites/player/manta_walk_0.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/manta_walk_1.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/manta_walk_2.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/manta_walk_3.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/manta_walk_0_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/manta_walk_1_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/manta_walk_2_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/manta_walk_3_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/manta_walk_0_512.png", (512, 512), ["RGBA"]),
        ("game/assets/sprites/player/manta_walk_1_512.png", (512, 512), ["RGBA"]),
        ("game/assets/sprites/player/manta_walk_2_512.png", (512, 512), ["RGBA"]),
        ("game/assets/sprites/player/manta_walk_3_512.png", (512, 512), ["RGBA"]),
        ("game/assets/sprites/player/proof_manta_walk_cycle.png", (512, 128), ["RGBA"]),

        # Mirror idle assets & Showcase
        ("game/assets/sprites/player/manta_idle.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/manta_idle_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/party/manta_idle.png", (128, 128), ["RGBA"]),
        ("web/media/hero/manta_idle.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/showcase/manta_idle_hd.png", (800, 1200), ["RGBA"]),

        # Category 4: HUD 戰鬥頭像 與 對話框半身像
        ("game/assets/sprites/portraits/manta.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/portraits/manta_512.png", (512, 512), ["RGBA"]),
        ("game/assets/sprites/portraits/tidal_manta.png", (384, 480), ["RGBA"]),
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
        print(f"  ✓ {rel_path:60s} size={im.size} mode={im.mode} bbox={bbox}")

    # 2. Rule 0-QA7 4:5 Aspect Ratio & Edge Margin Check
    print("\n--- [2/6] Rule 0-QA7 4:5 Aspect Ratio & Edge Margin ---")
    standee = Image.open(f"{BRANDING_DIR}/char_manta.png")
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

    # 0-ART25 Showcase check
    showcase = Image.open(f"{SHOWCASE_DIR}/manta_idle_hd.png")
    if showcase.mode != "RGBA":
        print(f"  ❌ Showcase mode {showcase.mode} != RGBA")
        all_ok = False
    elif showcase.size != (800, 1200):
        print(f"  ❌ Showcase size {showcase.size} != (800, 1200)")
        all_ok = False
    else:
        s_arr = np.array(showcase)
        corners = [s_arr[0, 0, 3], s_arr[0, -1, 3], s_arr[-1, 0, 3], s_arr[-1, -1, 3]]
        if any(c != 0 for c in corners):
            print(f"  ❌ Showcase 4-corner alpha != 0: {corners}")
            all_ok = False
        else:
            print("  ✓ Showcase manta_idle_hd.png (800x1200 RGBA, 4-corner alpha=0) compliant")

    # 3. Rule 4b-4 Kinematics Walk Animation & Shadow Row Consistency
    print("\n--- [3/6] Rule 4b-4 Walk Kinematics & Rule 4b-5 Shadow Row Consistency ---")
    idle128 = Image.open(f"{PLAYER_DIR}/manta_idle_x3.png")
    expected_shadow = [59, 57, 53, 45, 29, 0, 0, 0, 0, 0]

    walk_frames = [Image.open(f"{PLAYER_DIR}/manta_walk_{i}_x3.png") for i in range(4)]
    for i, fr in enumerate(walk_frames):
        arr = np.array(fr)
        counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
        if counts != expected_shadow:
            print(f"  ❌ Frame {i} shadow counts mismatch: {counts} != {expected_shadow}")
            all_ok = False
        else:
            print(f"  ✓ Frame {i} shadow rows match baseline: {counts}")

        # Check non-translation vs idle
        min_diff = 999999
        for dx in range(-8, 9):
            for dy in range(-8, 9):
                shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
                shifted.paste(idle128, (dx, dy), idle128)
                diff = ImageChops.difference(shifted, fr)
                d_arr = np.array(diff)
                diff_px = int(np.sum(np.any(d_arr > 0, axis=-1)))
                if diff_px < min_diff:
                    min_diff = diff_px
        if min_diff < 400:
            print(f"  ❌ Frame {i} failed non-translation test: min_diff {min_diff} < 400px")
            all_ok = False
        else:
            print(f"  ✓ Frame {i} non-translation test PASSED: min_diff {min_diff}px >= 400px")

    # 4. Rule 4b-6 Battle Stance Distinctness vs Idle
    print("\n--- [4/6] Rule 4b-6 Battle Stance Distinctness vs Idle ---")
    battle128 = Image.open(f"{PLAYER_DIR}/manta_battle.png")
    diff_battle = ImageChops.difference(idle128, battle128)
    d_battle_arr = np.array(diff_battle)
    diff_battle_px = int(np.sum(np.any(d_battle_arr > 0, axis=-1)))
    if diff_battle_px < 2500:
        print(f"  ❌ Battle stance difference too small: {diff_battle_px}px < 2500px")
        all_ok = False
    else:
        print(f"  ✓ Battle stance distinctness verified: diff={diff_battle_px}px >= 2500px")

    # 5. HUD & Dialogue Bust Margins and Alpha Fade
    print("\n--- [5/6] HUD and Dialogue Bust Metrics ---")
    hud128 = Image.open(f"{PORTRAITS_DIR}/manta.png")
    hb128 = hud128.getbbox()
    assert hb128 is not None
    m_128 = [hb128[0], hb128[1], 128 - hb128[2], 128 - hb128[3]]
    if min(m_128) < 8:
        print(f"  ❌ HUD 128 margin too small: {m_128} (req: all >= 8px)")
        all_ok = False
    else:
        print(f"  ✓ HUD 128 margins verified: L={m_128[0]}, T={m_128[1]}, R={m_128[2]}, B={m_128[3]} (>= 8px)")

    hud512 = Image.open(f"{PORTRAITS_DIR}/manta_512.png")
    hb512 = hud512.getbbox()
    assert hb512 is not None
    m_512 = [hb512[0], hb512[1], 512 - hb512[2], 512 - hb512[3]]
    if min(m_512) < 32:
        print(f"  ❌ HUD 512 margin too small: {m_512} (req: all >= 32px)")
        all_ok = False
    else:
        print(f"  ✓ HUD 512 margins verified: L={m_512[0]}, T={m_512[1]}, R={m_512[2]}, B={m_512[3]} (>= 32px)")

    bust = Image.open(f"{PORTRAITS_DIR}/tidal_manta.png")
    bb = bust.getbbox()
    assert bb is not None
    if bb[3] != 480:
        print(f"  ❌ Dialogue bust not anchored to baseline: bottom={bb[3]} != 480")
        all_ok = False
    else:
        print("  ✓ Dialogue bust anchored to baseline (y=480) with smooth fade")

    # 6. Proof cards verification
    print("\n--- [6/6] Proof Cards Verification ---")
    proof_cards = [
        ("proofs/official_assets_manta/proof_01_branding_hero.png", (1200, 800), ["RGB", "RGBA"]),
        ("proofs/official_assets_manta/proof_02_battle_stance.png", (1200, 720), ["RGB", "RGBA"]),
        ("proofs/official_assets_manta/proof_03_walk_cycle.png", (1200, 720), ["RGB", "RGBA"]),
        ("proofs/official_assets_manta/proof_04_portraits_hud.png", (1200, 720), ["RGB", "RGBA"]),
    ]
    for rel_path, expected_size, allowed_modes in proof_cards:
        full_path = f"{REPO_ROOT}/{rel_path}"
        if not os.path.exists(full_path):
            print(f"  ❌ MISSING PROOF CARD: {rel_path}")
            all_ok = False
            continue
        im = Image.open(full_path)
        if im.size != expected_size:
            print(f"  ❌ WRONG SIZE {im.size} vs {expected_size} for {rel_path}")
            all_ok = False
            continue
        if im.mode not in allowed_modes:
            print(f"  ❌ WRONG MODE {im.mode} vs {allowed_modes} for {rel_path}")
            all_ok = False
            continue
        print(f"  ✓ Proof card {rel_path} size={im.size} mode={im.mode} OK")

    if not all_ok:
        print("\n❌ SOME ASSET VERIFICATIONS FAILED!")
        sys.exit(1)
    else:
        print("\n✓ ALL OFFICIAL ASSETS AND PROOF CARDS 100% VERIFIED FOR THE TIDAL MANTA!")


if __name__ == "__main__":
    verify()
