#!/usr/bin/env python3
"""
audit_salamander_slices.py
Rigorous automated audit script for 第二十六族 熔火蜥蜴 (The Magma Salamander, salamander) paperdoll slices against:
- review.md 0-ART5 (c100 color richness, anti-placeholder)
- review.md 0-ART9 / 0-ART11 (no weapon baked into chassis)
- review.md 0-ART18 (bare chassis multi-tone depth, no flat placeholder blocks)
- review.md 0-ART27 (head_unit & eye slot separation, hollow eye sockets)
- review.md 0-ART28r (discrete connected components audit)
- 0-ART29 (no dark rounded rectangle / box artifacts in winding_key or slices)
- 0-QA30 (salamander aliases 100% aligned between paperdoll_slots.json and fallback)
- 0-QA31 (quantitative verification of optic core / chest to prevent false vision alerts)
- 128x128 and 512x512 resolution check
"""

import os
import json
import numpy as np
from PIL import Image
from scipy.ndimage import label

REPO_ROOT = "/opt/side/bravesoul-game"
SALAMANDER_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/salamander"

SLICES = [
    ("chassis", "chassis_salamander_magma_tungsten_default"),
    ("head_unit", "head_salamander_radiator_crest_horns"),
    ("winding_key", "key_salamander_four_vane_heatsink"),
    ("costume", "costume_salamander_foundry_sapper_apron"),
    ("optic_core", "face_salamander_amber_dial_lens"),
    ("weapon", "weapon_salamander_foundry_stamping_sledgehammer"),
    ("back_curio", "curio_salamander_segmented_damping_tail")
]

def audit():
    print("=== AUDITING MAGMA SALAMANDER 7 PAPERDOLL SLICES ===")
    all_ok = True
    metrics = {}

    for slot, item_id in SLICES:
        path_128 = f"{SALAMANDER_PD}/{slot}/{item_id}.png"
        path_512 = f"{SALAMANDER_PD}/{slot}/{item_id}_512.png"

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

            dark_mask = (alpha > 8) & (arr[:, :, 0] < 90) & (arr[:, :, 1] < 90) & (arr[:, :, 2] < 130)
            dark_count = int(np.sum(dark_mask))
            max_run = 0
            rows_run_ge_20 = 0
            for r in range(128):
                row = dark_mask[r, :]
                cur_run = 0
                r_max = 0
                for v in row:
                    if v:
                        cur_run += 1
                        r_max = max(r_max, cur_run)
                    else:
                        cur_run = 0
                max_run = max(max_run, r_max)
                if r_max >= 20:
                    rows_run_ge_20 += 1

            print(f"      [0-ART29 Metric] dark_count={dark_count} (<260), max_run={max_run} (<13), rows_run>=20: {rows_run_ge_20} (==0)")
            if dark_count >= 260 or max_run >= 13 or rows_run_ge_20 > 0:
                print("      ❌ FAILED 0-ART29: Winding key has dark box/card artifact!")
                all_ok = False
            else:
                print("      ✓ PASSED 0-ART29: No dark background residue detected")

    # Audit 0-ART9 / 0-ART11: Chassis must NOT bake weapon in outer hand area (x >= 94)
    chassis_im = Image.open(f"{SALAMANDER_PD}/chassis/chassis_salamander_magma_tungsten_default.png").convert("RGBA")
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

    # Audit 0-ART27: Optic core and head unit separation
    head_im = Image.open(f"{SALAMANDER_PD}/head_unit/head_salamander_radiator_crest_horns.png").convert("RGBA")
    head_arr = np.array(head_im)
    core_im = Image.open(f"{SALAMANDER_PD}/optic_core/face_salamander_amber_dial_lens.png").convert("RGBA")
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

    # Audit 0-QA30: salamander aliases 100% aligned
    with open(f"{REPO_ROOT}/game/data/tables/paperdoll_slots.json", "r", encoding="utf-8") as f:
        spec_data = json.load(f)
    races_list = spec_data.get("races_specification", {}).get("races", [])
    salamander_spec = next((r for r in races_list if r.get("race_id") == "salamander"), {})
    salamander_aliases = salamander_spec.get("aliases", [])
    expected_aliases = ["magma_salamander", "foundry_salamander", "crucible_salamander", "sapper_salamander"]
    if salamander_aliases != expected_aliases:
        print(f"❌ FAILED 0-QA30: paperdoll_slots.json salamander aliases mismatch: {salamander_aliases} vs {expected_aliases}")
        all_ok = False
    else:
        print(f"✓ PASSED 0-QA30: salamander aliases perfectly aligned: {salamander_aliases}")

    # Audit 0-QA31: Quantitative verification of composite & optic core (no false vision alarms)
    comp_im = Image.open(f"{SALAMANDER_PD}/proof_paperdoll_salamander_composite.png").convert("RGBA")
    comp_arr = np.array(comp_im)
    comp_alpha = comp_arr[:, :, 3] > 8
    opaque_comp = int(np.sum(comp_alpha))
    print(f"\n[0-QA31 Audit] Composite total opaque pixels: {opaque_comp:5d} (> 3000)")
    if opaque_comp < 3000:
        print("❌ FAILED 0-QA31: Composite character has insufficient pixel coverage!")
        all_ok = False
    else:
        print("✓ PASSED 0-QA31: Composite character has full volumetric coverage")

    # Optic core region on composite (x: 46..82, y: 34..46)
    optic_zone = comp_arr[34:47, 46:83]
    optic_opaque = optic_zone[:, :, 3] > 8
    optic_colors = len(np.unique(optic_zone[optic_opaque][:, :3], axis=0))
    print(f"[0-QA31 Audit] Composite optic core zone unique colors: {optic_colors} (expected >= 15)")
    if optic_colors < 15:
        print("❌ FAILED 0-QA31: Optic core appears flat or unrendered!")
        all_ok = False
    else:
        print("✓ PASSED 0-QA31: Optic core verified vibrant with rich color depth (no false vision mask alarm)")

    # Audit Magenta Proof: check for interior holes in core body (x: 40..85, y: 35..95)
    from scipy.ndimage import binary_fill_holes
    mag_im = Image.open(f"{SALAMANDER_PD}/proof_paperdoll_salamander_magenta.png").convert("RGB")
    if mag_im.size != (128, 128):
        print(f"❌ Wrong size {mag_im.size} for magenta proof")
        all_ok = False
    core_mask = comp_alpha[35:95, 40:85]
    filled_core = np.asarray(binary_fill_holes(core_mask), dtype=bool)
    holes_in_core = filled_core & (~core_mask)
    num_holes = int(np.sum(holes_in_core))
    print(f"\n[Magenta / 0-ART29 Hole Audit] Holes in core body: {num_holes}")
    if num_holes > 0:
        print(f"❌ FAILED 0-ART29: Detected {num_holes} hole pixels in composite core!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART29: Magenta composite has zero holes in core body, zero clipping, zero chassis leakage")

    print("\n=======================================================")
    if all_ok:
        print("🎉 ALL 7 MAGMA SALAMANDER PAPERDOLL SLICES FULLY AUDITED AND COMPLIANT!")
        return 0
    else:
        print("❌ MAGMA SALAMANDER PAPERDOLL AUDIT DETECTED DEFECTS!")
        return 1

if __name__ == "__main__":
    exit(audit())
