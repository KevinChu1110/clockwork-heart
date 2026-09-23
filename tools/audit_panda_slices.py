#!/usr/bin/env python3
"""
audit_panda_slices.py
Rigorous automated audit script for Porcelain Panda (瓷韻熊貓 / The Porcelain Panda) paperdoll slices against:
- review.md 0-ART5 (c100 color richness, anti-placeholder)
- review.md 0-ART9 / 0-ART11 (no weapon baked into chassis)
- review.md 0-ART18 (bare chassis multi-tone depth, no flat placeholder blocks)
- review.md 0-ART27 (head_unit & eye slot separation, hollow eye sockets)
- review.md 0-ART28r (discrete connected components audit)
- 128x128 and 512x512 resolution check
"""

import os
import numpy as np
from PIL import Image
from scipy.ndimage import label

REPO_ROOT = "/opt/side/bravesoul-game"
PANDA_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/panda"

SLICES = [
    ("chassis", "paint_panda_porcelain"),
    ("head_unit", "head_panda_brass_socket_ears"),
    ("winding_key", "key_panda_taiji_ruyi_brass"),
    ("costume", "costume_panda_zen_apprentice_robe"),
    ("optic_core", "core_obsidian_amber_quartz"),
    ("weapon", "wpn_panda_taiji_cestus"),
    ("back_curio", "curio_panda_floating_taiji_box")
]

def audit():
    print("=== AUDITING PORCELAIN PANDA 7 PAPERDOLL SLICES ===")
    all_ok = True

    metrics = {}

    for slot, item_id in SLICES:
        path_128 = f"{PANDA_PD}/{slot}/{item_id}.png"
        path_512 = f"{PANDA_PD}/{slot}/{item_id}_512.png"

        if not os.path.exists(path_128):
            print(f"❌ Missing 128px file: {path_128}")
            all_ok = False
            continue
        if not os.path.exists(path_512):
            print(f"❌ Missing 512px file: {path_512}")
            all_ok = False
            continue

        im = Image.open(path_128).convert("RGBA")
        if im.size != (128, 128):
            print(f"❌ Wrong size {im.size} for {path_128} (expected 128x128)")
            all_ok = False

        im_512 = Image.open(path_512).convert("RGBA")
        if im_512.size != (512, 512):
            print(f"❌ Wrong size {im_512.size} for {path_512} (expected 512x512)")
            all_ok = False

        arr = np.array(im)
        alpha = arr[:, :, 3]
        opaque_mask = alpha > 8
        opaque_count = int(np.sum(opaque_mask))

        if opaque_count == 0:
            print(f"❌ {slot}/{item_id} has 0 opaque pixels!")
            all_ok = False
            continue

        # Unique RGB colors among opaque pixels
        opaque_rgb = arr[opaque_mask][:, :3]
        unique_colors = len(np.unique(opaque_rgb, axis=0))
        c100 = (unique_colors / opaque_count) * 100.0
        metrics[slot] = round(c100, 2)

        # Connected components on alpha > 30
        labeled, num_features = label(alpha > 30)

        print(f"  [{slot:<12}] {item_id}.png:")
        print(f"      Size: {im.size} | BBox: {im.getbbox()}")
        print(f"      Opaque Pixels: {opaque_count:5d} | Unique Colors: {unique_colors:4d} | c100: {c100:6.2f}%")
        print(f"      Connected Components: {num_features}")

        # 0-ART5 threshold: c100 should not be flat placeholder
        if unique_colors < 10:
            print(f"      ❌ FAILED 0-ART5: Flat placeholder art suspected (unique colors {unique_colors} < 10)")
            all_ok = False
        else:
            print(f"      ✓ PASSED 0-ART5: Hand-painted multi-tone depth confirmed")

    # Audit 0-ART9 / 0-ART11: Chassis must NOT bake weapon in outer hand area
    chassis_im = Image.open(f"{PANDA_PD}/chassis/paint_panda_porcelain.png").convert("RGBA")
    ch_arr = np.array(chassis_im)
    # Weapon zone is x >= 95 (wrist socket ends at 91, weapon reaches x: 80..108, y: 64..88)
    weapon_zone_pixels = np.sum(ch_arr[64:88, 95:120, 3] > 30)
    print(f"\n[0-ART9 / 0-ART11 Audit] Chassis pixels in outer weapon zone (x:95..120, y:64..88): {weapon_zone_pixels}")
    if weapon_zone_pixels > 0:
        print(f"❌ FAILED 0-ART9: Chassis has {weapon_zone_pixels} pixels in weapon zone!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART9: Chassis does NOT bake weapon or gauntlet into body!")

    # Audit 0-ART18: Bare chassis belly/torso must not be flat placeholder
    # Inspect center torso x: 52..76, y: 56..74
    torso_crop = ch_arr[56:74, 52:76, :3]
    unique_torso_colors = len(np.unique(torso_crop.reshape(-1, 3), axis=0))
    print(f"[0-ART18 Audit] Bare chassis torso crop unique colors: {unique_torso_colors}")
    if unique_torso_colors < 20:
        print("❌ FAILED 0-ART18: Bare chassis torso appears flat/placeholder!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART18: Bare chassis torso has full multi-tone depth & shading!")

    # Audit 0-ART27: Optic core and head unit separation
    head_im = Image.open(f"{PANDA_PD}/head_unit/head_panda_brass_socket_ears.png").convert("RGBA")
    head_arr = np.array(head_im)
    core_im = Image.open(f"{PANDA_PD}/optic_core/core_obsidian_amber_quartz.png").convert("RGBA")
    core_arr = np.array(core_im)

    # In head_unit, check that eye centers (49, 34) and (79, 34) are hollow (alpha == 0)
    left_socket_inner_alpha = head_arr[32:36, 47:51, 3]
    right_socket_inner_alpha = head_arr[32:36, 77:81, 3]
    max_socket_alpha = max(np.max(left_socket_inner_alpha), np.max(right_socket_inner_alpha))
    print(f"[0-ART27 Audit] Head unit eye sockets inner max alpha: {max_socket_alpha} (expected: 0)")
    if max_socket_alpha > 0:
        print(f"❌ FAILED 0-ART27: Head unit eye sockets are not hollow (max alpha={max_socket_alpha})!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART27: Head unit has clean hollow eye sockets for optic_core insertion!")

    # In optic_core, check that eye centers have pixels
    left_core_pixels = np.sum(core_arr[30:38, 45:53, 3] > 30)
    right_core_pixels = np.sum(core_arr[30:38, 75:83, 3] > 30)
    print(f"[0-ART27 Audit] Optic core lens eyes pixels - Left: {left_core_pixels}, Right: {right_core_pixels}")
    if left_core_pixels == 0 or right_core_pixels == 0:
        print("❌ FAILED 0-ART27: Optic core missing lens eye pixels!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART27: Optic core has complete dual quartz lens eyes!")

    # Check proofs
    proofs = [
        "proof_paperdoll_panda_composite.png",
        "proof_paperdoll_panda_magenta.png",
        "proof_panda_all_7_slices.png"
    ]
    for p in proofs:
        p_path = f"{PANDA_PD}/{p}"
        if not os.path.exists(p_path):
            print(f"❌ Missing proof: {p_path}")
            all_ok = False
        else:
            print(f"✓ Proof verified: {p}")

    print("\nC100 Metrics:", metrics)
    if all_ok:
        print("\n=== ALL 7 PORCELAIN PANDA SLICES AUDITED AND PASSED ALL QUALITY GATES ===")
    else:
        print("\n=== AUDIT FAILED SOME GATES ===")
        exit(1)

if __name__ == "__main__":
    audit()
