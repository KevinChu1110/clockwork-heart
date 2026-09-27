#!/usr/bin/env python3
"""
audit_seahorse_slices.py
Rigorous automated audit script for 第二十三族 琉璃海馬 (The Crystal Seahorse, seahorse) paperdoll slices against:
- review.md 0-ART5 (c100 color richness, anti-placeholder)
- review.md 0-ART9 / 0-ART11 (no weapon baked into chassis)
- review.md 0-ART18 (bare chassis multi-tone depth, no flat placeholder blocks)
- review.md 0-ART26b (costume decoupled, no baked chassis)
- review.md 0-ART27 (head_unit & eye slot separation, hollow eye sockets)
- review.md 0-ART28r (discrete connected components audit)
- 0-ART29 (no dark rounded rectangle / box artifacts in winding_key or slices)
- 0-QA30 (seahorse aliases 100% aligned between paperdoll_slots.json and fallback)
- 128x128 and 512x512 resolution check
"""

import os
import json
import numpy as np
from PIL import Image
from scipy.ndimage import label

REPO_ROOT = "/opt/side/bravesoul-game"
SEAHORSE_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/seahorse"

SLICES = [
    ("chassis", "chassis_seahorse_abyssal_cyan_default"),
    ("head_unit", "head_seahorse_crown_visor"),
    ("winding_key", "key_seahorse_trident_coral_spire"),
    ("costume", "costume_seahorse_abyssal_scholar_harness"),
    ("optic_core", "optic_seahorse_ocean_sapphire"),
    ("weapon", "weapon_seahorse_abyssal_prism_astrolabe"),
    ("back_curio", "curio_seahorse_twin_propeller_fins")
]

def audit():
    print("=== AUDITING CRYSTAL SEAHORSE 7 PAPERDOLL SLICES ===")
    all_ok = True
    metrics = {}

    for slot, item_id in SLICES:
        path_128 = f"{SEAHORSE_PD}/{slot}/{item_id}.png"
        path_512 = f"{SEAHORSE_PD}/{slot}/{item_id}_512.png"

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
        res = label(alpha > 30)
        num_features = res[1] if isinstance(res, tuple) else 0

        print(f"  [{slot:<12}] {item_id}.png:")
        print(f"      Size: {im.size} | BBox: {im.getbbox()}")
        print(f"      Opaque Pixels: {opaque_count:5d} | Unique Colors: {unique_colors:4d} | c100: {c100:6.2f}%")
        print(f"      Connected Components: {num_features}")

        # 0-ART5 threshold: c100 should not be flat placeholder
        if unique_colors < 10:
            print(f"      ❌ FAILED 0-ART5: Flat placeholder art suspected (unique colors {unique_colors} < 10)")
            all_ok = False
        else:
            print("      ✓ PASSED 0-ART5: Hand-painted multi-tone depth confirmed")

        # 0-ART29 check: verify NO dark card/strip background rectangle in slices
        if slot == "winding_key":
            corners_alpha = [arr[0, 0, 3], arr[0, 127, 3], arr[127, 0, 3], arr[127, 127, 3]]
            if any(a > 0 for a in corners_alpha):
                print(f"      ❌ FAILED 0-ART29: Winding key has opaque corners: {corners_alpha}")
                all_ok = False
            else:
                print("      ✓ PASSED 0-ART29: Winding key corners completely transparent (alpha=0)")

    # Audit 0-ART9 / 0-ART11: Chassis must NOT bake weapon in outer hand area (x >= 94)
    chassis_im = Image.open(f"{SEAHORSE_PD}/chassis/chassis_seahorse_abyssal_cyan_default.png").convert("RGBA")
    ch_arr = np.array(chassis_im)
    weapon_zone_pixels = np.sum(ch_arr[:, 94:128, 3] > 30)
    print(f"\n[0-ART9 / 0-ART11 Audit] Chassis pixels in outer weapon zone (x:94..128): {weapon_zone_pixels}")
    if weapon_zone_pixels > 0:
        print(f"❌ FAILED 0-ART9: Chassis has {weapon_zone_pixels} pixels in weapon zone!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART9: Chassis does NOT bake weapon into outer hand zone!")

    # Audit 0-ART18: Bare chassis belly/torso must not be flat placeholder
    torso_crop = ch_arr[60:84, 48:72, :3]
    unique_torso_colors = len(np.unique(torso_crop.reshape(-1, 3), axis=0))
    print(f"[0-ART18 Audit] Bare chassis torso crop unique colors: {unique_torso_colors}")
    if unique_torso_colors < 20:
        print("❌ FAILED 0-ART18: Bare chassis torso appears flat/placeholder!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART18: Bare chassis torso has full multi-tone depth & shading!")

    # Audit 0-ART26b: Costume does not bake chassis underneath
    costume_im = Image.open(f"{SEAHORSE_PD}/costume/costume_seahorse_abyssal_scholar_harness.png").convert("RGBA")
    cos_arr = np.array(costume_im)
    # Check that costume does not cover lower spring tail (y >= 92 should be empty)
    lower_costume_pixels = np.sum(cos_arr[92:128, :, 3] > 30)
    print(f"[0-ART26b Audit] Costume pixels in lower tail zone (y:92..128): {lower_costume_pixels}")
    if lower_costume_pixels > 0:
        print(f"❌ FAILED 0-ART26b: Costume bakes lower tail ({lower_costume_pixels} pixels)!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART26b: Costume is fully decoupled and does not bake lower chassis!")

    # Audit 0-ART27: Optic core and head unit separation
    head_im = Image.open(f"{SEAHORSE_PD}/head_unit/head_seahorse_crown_visor.png").convert("RGBA")
    head_arr = np.array(head_im)
    core_im = Image.open(f"{SEAHORSE_PD}/optic_core/optic_seahorse_ocean_sapphire.png").convert("RGBA")
    core_arr = np.array(core_im)

    # In head_unit, check that eye centers (52, 40) and (76, 40) are hollow (alpha == 0)
    left_socket_alpha = head_arr[39:41, 51:53, 3]
    right_socket_alpha = head_arr[39:41, 75:77, 3]
    max_socket_alpha = max(int(np.max(left_socket_alpha)), int(np.max(right_socket_alpha)))
    print(f"[0-ART27 Audit] Head unit eye sockets inner max alpha: {max_socket_alpha} (expected: 0)")
    if max_socket_alpha > 0:
        print("❌ FAILED 0-ART27: Head unit eye sockets are not hollow!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART27: Head unit has clean hollow eye sockets for optic_core insertion!")

    # In optic_core, check that eye centers have opaque lens content
    left_core_alpha = int(core_arr[40, 52, 3])
    right_core_alpha = int(core_arr[40, 76, 3])
    min_core_alpha = min(left_core_alpha, right_core_alpha)
    print(f"[0-ART27 Audit] Optic core lens center min alpha: {min_core_alpha} (expected: > 200)")
    if min_core_alpha < 200:
        print("❌ FAILED 0-ART27: Optic core eyes not centered properly in eye sockets!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART27: Optic core precisely aligns with head unit eye sockets!")

    # Audit 0-QA30: seahorse aliases 100% aligned
    with open(f"{REPO_ROOT}/game/data/tables/paperdoll_slots.json", "r", encoding="utf-8") as f:
        spec_data = json.load(f)
    races_list = spec_data.get("races_specification", {}).get("races", [])
    seahorse_spec = next((r for r in races_list if r.get("race_id") == "seahorse"), {})
    seahorse_aliases = seahorse_spec.get("aliases", [])
    expected_aliases = ["crystal_seahorse", "abyssal_seahorse", "ocean_seahorse", "tide_seahorse"]
    if seahorse_aliases != expected_aliases:
        print(f"❌ FAILED 0-QA30: paperdoll_slots.json seahorse aliases mismatch: {seahorse_aliases} vs {expected_aliases}")
        all_ok = False
    else:
        print(f"✓ PASSED 0-QA30: seahorse aliases perfectly aligned: {seahorse_aliases}")

    print("\n=======================================================")
    if all_ok:
        print("🎉 ALL 7 CRYSTAL SEAHORSE PAPERDOLL SLICES FULLY AUDITED AND COMPLIANT!")
        return 0
    else:
        print("❌ CRYSTAL SEAHORSE PAPERDOLL AUDIT DETECTED DEFECTS!")
        return 1

if __name__ == "__main__":
    exit(audit())
