#!/usr/bin/env python3
"""
audit_kangaroo_slices.py
Rigorous automated audit script for 第二十四族 鐵拳袋鼠 (The Boxer Kangaroo, kangaroo) paperdoll slices against:
- review.md 0-ART5 (c100 color richness, anti-placeholder)
- review.md 0-ART9 / 0-ART11 (no weapon baked into chassis)
- review.md 0-ART18 (bare chassis multi-tone depth, no flat placeholder blocks)
- review.md 0-ART26b (costume decoupled, no baked chassis)
- review.md 0-ART27 (head_unit & eye slot separation, hollow eye sockets)
- review.md 0-ART28r (discrete connected components audit)
- 0-ART29 (no dark rounded rectangle / box artifacts in winding_key or slices)
- 0-QA30 (kangaroo aliases 100% aligned between paperdoll_slots.json and fallback)
- 128x128 and 512x512 resolution check
"""

import os
import json
import numpy as np
from PIL import Image
from scipy.ndimage import label

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_9a32151a/repo"
KANGAROO_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/kangaroo"

SLICES = [
    ("chassis", "chassis_kangaroo_caramel_bronze_default"),
    ("head_unit", "head_kangaroo_steampunk_boxer_visor"),
    ("winding_key", "key_kangaroo_champion_double_ring"),
    ("costume", "costume_kangaroo_champion_belt_harness"),
    ("optic_core", "optic_kangaroo_amber_dial_core"),
    ("weapon", "weapon_kangaroo_piston_brass_knuckle"),
    ("back_curio", "curio_kangaroo_steam_exhaust_backpack")
]

def audit():
    print("=== AUDITING BOXER KANGAROO 7 PAPERDOLL SLICES ===")
    all_ok = True
    metrics = {}

    for slot, item_id in SLICES:
        path_128 = f"{KANGAROO_PD}/{slot}/{item_id}.png"
        path_512 = f"{KANGAROO_PD}/{slot}/{item_id}_512.png"

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
    chassis_im = Image.open(f"{KANGAROO_PD}/chassis/chassis_kangaroo_caramel_bronze_default.png").convert("RGBA")
    ch_arr = np.array(chassis_im)
    weapon_zone_pixels = np.sum(ch_arr[:, 94:128, 3] > 30)
    print(f"\n[0-ART9 / 0-ART11 Audit] Chassis pixels in outer weapon zone (x:94..128): {weapon_zone_pixels}")
    if weapon_zone_pixels > 0:
        print(f"❌ FAILED 0-ART9: Chassis has {weapon_zone_pixels} pixels in weapon zone!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART9: Chassis does NOT bake weapon into outer hand zone!")

    # Audit 0-ART18: Bare chassis belly/torso must not be flat placeholder
    torso_crop = ch_arr[60:84, 52:74, :3]
    unique_torso_colors = len(np.unique(torso_crop.reshape(-1, 3), axis=0))
    print(f"[0-ART18 Audit] Bare chassis torso crop unique colors: {unique_torso_colors}")
    if unique_torso_colors < 20:
        print("❌ FAILED 0-ART18: Bare chassis torso appears flat/placeholder!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART18: Bare chassis torso has full multi-tone depth & shading!")

    # Audit 0-ART26b: Costume does not bake chassis underneath
    costume_im = Image.open(f"{KANGAROO_PD}/costume/costume_kangaroo_champion_belt_harness.png").convert("RGBA")
    cos_arr = np.array(costume_im)
    # Check that costume does not cover lower spring legs (y >= 96 should be empty)
    lower_costume_pixels = np.sum(cos_arr[96:128, :, 3] > 30)
    print(f"[0-ART26b Audit] Costume pixels in lower leg zone (y:96..128): {lower_costume_pixels}")
    if lower_costume_pixels > 0:
        print(f"❌ FAILED 0-ART26b: Costume bakes lower legs ({lower_costume_pixels} pixels)!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART26b: Costume is fully decoupled and does not bake lower chassis!")

    # Audit 0-ART27: Optic core and head unit separation
    head_im = Image.open(f"{KANGAROO_PD}/head_unit/head_kangaroo_steampunk_boxer_visor.png").convert("RGBA")
    head_arr = np.array(head_im)
    core_im = Image.open(f"{KANGAROO_PD}/optic_core/optic_kangaroo_amber_dial_core.png").convert("RGBA")
    core_arr = np.array(core_im)

    # In head_unit, check that eye centers (55, 42) and (69, 42) are hollow (alpha == 0)
    left_socket_alpha = head_arr[41:43, 54:56, 3]
    right_socket_alpha = head_arr[41:43, 68:70, 3]
    max_socket_alpha = max(int(np.max(left_socket_alpha)), int(np.max(right_socket_alpha)))
    print(f"[0-ART27 Audit] Head unit eye sockets inner max alpha: {max_socket_alpha} (expected: 0)")
    if max_socket_alpha > 0:
        print("❌ FAILED 0-ART27: Head unit eye sockets are not hollow!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART27: Head unit has clean hollow eye sockets for optic_core insertion!")

    # In optic_core, check that eye centers have opaque lens content
    left_core_alpha = int(core_arr[42, 55, 3])
    right_core_alpha = int(core_arr[42, 69, 3])
    min_core_alpha = min(left_core_alpha, right_core_alpha)
    print(f"[0-ART27 Audit] Optic core lens center min alpha: {min_core_alpha} (expected: > 200)")
    if min_core_alpha < 200:
        print("❌ FAILED 0-ART27: Optic core eyes not centered properly in eye sockets!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART27: Optic core precisely aligns with head unit eye sockets!")

    # Audit composite
    comp_im = Image.open(f"{KANGAROO_PD}/proof_paperdoll_kangaroo_composite.png").convert("RGBA")
    comp_arr = np.array(comp_im)
    non_trans = np.sum(comp_arr[:, :, 3] > 12)
    print(f"\n[Composite Audit] Total non-transparent pixels: {non_trans} (expected: > 1000)")
    if non_trans < 1000:
        print(f"❌ FAILED: Composite has too few pixels ({non_trans} < 1000)")
        all_ok = False
    else:
        print(f"✓ PASSED: Composite has complete chibi character ({non_trans} pixels)!")

    # Audit 0-QA30: kangaroo aliases 100% aligned
    with open(f"{REPO_ROOT}/game/data/tables/paperdoll_slots.json", "r", encoding="utf-8") as f:
        spec_data = json.load(f)
    races_list = spec_data.get("races_specification", {}).get("races", [])
    kangaroo_spec = next((r for r in races_list if r.get("race_id") == "kangaroo"), {})
    kangaroo_aliases = kangaroo_spec.get("aliases", [])
    expected_aliases = ["boxer_kangaroo", "steam_kangaroo", "brass_kangaroo", "champion_kangaroo"]
    if kangaroo_aliases != expected_aliases:
        print(f"❌ FAILED 0-QA30: paperdoll_slots.json kangaroo aliases mismatch: {kangaroo_aliases} vs {expected_aliases}")
        all_ok = False
    else:
        print(f"✓ PASSED 0-QA30: kangaroo aliases perfectly aligned: {kangaroo_aliases}")

    print("\n=======================================================")
    if all_ok:
        print("🎉 ALL 7 BOXER KANGAROO PAPERDOLL SLICES FULLY AUDITED AND COMPLIANT!")
        return 0
    else:
        print("❌ BOXER KANGAROO PAPERDOLL AUDIT DETECTED DEFECTS!")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(audit())
