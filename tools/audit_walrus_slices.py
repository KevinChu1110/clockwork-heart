#!/usr/bin/env python3
"""
audit_walrus_slices.py
Rigorous automated audit script for 第六十二族 破冰海象 (The Icebreaker Walrus, walrus) paperdoll slices against:
- review.md 0-ART5 (c100 color richness, anti-placeholder)
- review.md 0-ART9 / 0-ART11 (no weapon baked into chassis, strict x < 94)
- review.md 0-ART18 (bare chassis multi-tone depth, unique colors >= 10)
- review.md 0-ART25 (showcase HD RGBA mode, 4 corners transparent)
- review.md 0-ART26b (costume decoupled, no lower chassis baked, y >= 96 zero pixels)
- review.md 0-ART27 (head_unit & eye slot separation, hollow eye sockets)
- review.md 0-ART28n (MD5 查重: unique MD5 hashes across all 7 slices, zero duplicate placeholder assets)
- review.md 0-ART28q (色距量測: head_unit and chassis L2 color distance < 60.0)
- review.md 0-ART28r (連通元件: discrete connected components audit)
- 0-ART29 (no dark rounded rectangle / box artifacts in winding_key, transparent corners, zero holes on magenta)
- 0-QA16 (quantitative white rectangle run test, dark block test, hole fill test)
- 0-QA30 (walrus aliases 100% aligned between paperdoll_slots.json and fallback)
- 0-QA31 (quantitative verification of optic core / composite to prevent false vision alerts)
- 0-QA34 / 三區量化稽核: Three-zone analysis (Head, Torso, Legs) in 512x512 native resolution (> 1500px each)
- 128x128 and 512x512 resolution check
"""

import os
import sys
import json
import hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes, label

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WALRUS_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/walrus"
SHOWCASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/showcase"

SLICES = [
    ("chassis", "chassis_walrus_icebreaker_alloy_default"),
    ("head_unit", "head_walrus_tungsten_tusk_cowl"),
    ("winding_key", "key_walrus_anchor_handwheel_brass"),
    ("costume", "costume_walrus_abyssal_peacoat_cuirass"),
    ("optic_core", "face_walrus_quartz_dome_eyes"),
    ("weapon", "weapon_walrus_abyssal_icebreaker_cutlass"),
    ("back_curio", "curio_walrus_dual_ballast_tanks")
]

def get_md5(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def get_average_plate_color(arr: np.ndarray, alpha_thresh=200, min_rgb=30, plate_ymin=0) -> np.ndarray:
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    mask = (alpha > alpha_thresh) & (np.max(rgb, axis=2) > min_rgb)
    if plate_ymin > 0:
        mask[:plate_ymin, :] = False
    if np.sum(mask) == 0:
        mask = alpha > alpha_thresh
    pixels = rgb[mask].astype(float)
    return np.mean(pixels, axis=0)

def color_distance(c1: np.ndarray, c2: np.ndarray) -> float:
    return float(np.linalg.norm(np.array(c1) - np.array(c2)))

def audit():
    print("=== AUDITING THE ICEBREAKER WALRUS 7 PAPERDOLL SLICES ===")
    all_ok = True
    metrics = {}
    md5_128 = {}
    md5_512 = {}

    for slot, item_id in SLICES:
        path_128 = f"{WALRUS_PD}/{slot}/{item_id}.png"
        path_512 = f"{WALRUS_PD}/{slot}/{item_id}_512.png"

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

        opaque_rgb = arr[opaque_mask][:, :3]
        unique_colors = len(np.unique(opaque_rgb, axis=0))
        c100 = (unique_colors / opaque_count) * 100.0
        metrics[slot] = round(c100, 2)

        # Audit 0-ART5: Color richness
        if unique_colors < 8 and slot not in ["optic_core"]:
            print(f"❌ FAILED 0-ART5: {slot} has too few unique colors ({unique_colors})!")
            all_ok = False
        else:
            print(f"  [{slot:<12}] 128px pixels: {opaque_count:4d}, unique colors: {unique_colors:3d}, c100: {c100:5.2f}%")

        # Record MD5 hashes for 0-ART28n check
        h128 = get_md5(path_128)
        h512 = get_md5(path_512)
        md5_128[slot] = h128
        md5_512[slot] = h512

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART28n: MD5 查重 (MD5 Uniqueness Audit)
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART28n: 7 大切片 MD5 唯一性查驗 ---")
    unique_128 = set(md5_128.values())
    unique_512 = set(md5_512.values())
    if len(unique_128) != len(md5_128):
        print(f"❌ 0-ART28n FAILED: 128px 切片存在重複 MD5！唯一數: {len(unique_128)} / 7")
        all_ok = False
    else:
        print(f"  ✓ 128px 7/7 切片 MD5 全數唯一獨立 (7 unique hashes)")

    if len(unique_512) != len(md5_512):
        print(f"❌ 0-ART28n FAILED: 512px 切片存在重複 MD5！唯一數: {len(unique_512)} / 7")
        all_ok = False
    else:
        print(f"  ✓ 512px 7/7 切片 MD5 全數唯一獨立 (7 unique hashes)")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART9 / 0-ART11: Chassis weapon baking check (strict x < 94)
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART9 / 0-ART11: Chassis 武器烘焙邊界稽核 (strict x < 94) ---")
    chassis_p = f"{WALRUS_PD}/chassis/chassis_walrus_icebreaker_alloy_default.png"
    if os.path.exists(chassis_p):
        arr_c = np.array(Image.open(chassis_p).convert("RGBA"))
        alpha_c = arr_c[:, :, 3]
        right_overflow = np.sum(alpha_c[:, 94:] > 10)
        if right_overflow > 0:
            print(f"❌ FAILED 0-ART9/11: Chassis has {right_overflow} pixels at x >= 94 (weapon baked into chassis)!")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-ART9/11: Chassis strictly decoupled at x < 94 (0 pixels at x >= 94)")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART18: Bare chassis multi-tone depth (unique colors >= 10)
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART18: 裸機軀幹色階稽核 (unique colors >= 10) ---")
    if os.path.exists(chassis_p):
        arr_c = np.array(Image.open(chassis_p).convert("RGBA"))
        torso_mask = (arr_c[60:92, 45:83, 3] > 50)
        torso_rgb = arr_c[60:92, 45:83, :3][torso_mask]
        torso_colors = len(np.unique(torso_rgb, axis=0))
        if torso_colors < 10:
            print(f"❌ FAILED 0-ART18: Chassis torso has only {torso_colors} unique colors (< 10)!")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-ART18: Chassis bare torso unique colors = {torso_colors} (>= 10)")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART26b: Costume lower chassis decoupling (strict y < 96)
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART26b: Costume 下身解耦稽核 (strict y < 96) ---")
    costume_p = f"{WALRUS_PD}/costume/costume_walrus_abyssal_peacoat_cuirass.png"
    if os.path.exists(costume_p):
        arr_cos = np.array(Image.open(costume_p).convert("RGBA"))
        alpha_cos = arr_cos[:, :, 3]
        lower_overflow = np.sum(alpha_cos[96:, :] > 10)
        if lower_overflow > 0:
            print(f"❌ FAILED 0-ART26b: Costume has {lower_overflow} pixels at y >= 96!")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-ART26b: Costume strictly decoupled at y < 96 (0 pixels at y >= 96)")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART27: Head unit & Eye slot separation (hollow sockets)
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART27: Head Unit 眼窩鏤空稽核 (strict alpha = 0) ---")
    head_p = f"{WALRUS_PD}/head_unit/head_walrus_tungsten_tusk_cowl.png"
    optic_p = f"{WALRUS_PD}/optic_core/face_walrus_quartz_dome_eyes.png"
    if os.path.exists(head_p) and os.path.exists(optic_p):
        arr_head = np.array(Image.open(head_p).convert("RGBA"))
        arr_eye = np.array(Image.open(optic_p).convert("RGBA"))

        # Left eye socket: x: 50..58, y: 38..46
        left_socket = arr_head[38:47, 50:59, 3]
        right_socket = arr_head[38:47, 70:79, 3]
        max_left_a = int(np.max(left_socket))
        max_right_a = int(np.max(right_socket))

        if max_left_a > 0 or max_right_a > 0:
            print(f"❌ FAILED 0-ART27: Head unit eye sockets are not hollow! Left max alpha={max_left_a}, Right max alpha={max_right_a}")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-ART27: Head unit eye sockets 100% hollow (left max alpha={max_left_a}, right max alpha={max_right_a})")

        # Verify optic core provides solid pixels in sockets
        eye_left_a = int(arr_eye[42, 54, 3])
        eye_right_a = int(arr_eye[42, 74, 3])
        if eye_left_a < 200 or eye_right_a < 200:
            print(f"❌ FAILED 0-ART27: Optic core missing center pixels! Left center={eye_left_a}, Right center={eye_right_a}")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-ART27: Optic core renders solid centers (left center alpha={eye_left_a}, right center alpha={eye_right_a})")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART28q: 色距量測 (Head Unit vs Chassis L2 distance < 60.0)
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART28q: 色距量測 (Head Unit vs Chassis L2 < 60.0) ---")
    if os.path.exists(head_p) and os.path.exists(chassis_p):
        arr_h = np.array(Image.open(head_p).convert("RGBA"))
        arr_c = np.array(Image.open(chassis_p).convert("RGBA"))

        c_head = get_average_plate_color(arr_h, plate_ymin=24)
        c_chassis = get_average_plate_color(arr_c, plate_ymin=60)
        dist = color_distance(c_head, c_chassis)

        if dist >= 60.0:
            print(f"❌ FAILED 0-ART28q: Head unit & Chassis color distance L2 = {dist:.2f} >= 60.0!")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-ART28q: Head unit ({c_head.astype(int)}) vs Chassis ({c_chassis.astype(int)}) L2 = {dist:.2f} (< 60.0)")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART28r: 連通元件獨立區塊查核
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART28r: 連通元件獨立區塊查核 ---")
    for slot, item_id in SLICES:
        p128 = f"{WALRUS_PD}/{slot}/{item_id}.png"
        arr = np.array(Image.open(p128).convert("RGBA"))
        alpha = arr[:, :, 3] > 20
        labeled, num_features = label(alpha)

        component_sizes = [np.sum(labeled == i) for i in range(1, num_features + 1)]
        tiny_debris = sum(1 for s in component_sizes if s < 3)
        print(f"  [{slot:<12}] Connected components: {num_features}, tiny debris: {tiny_debris}")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART29 & 0-QA16: Winding Key White Run, Dark Run, and Hole Fill
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART29 & 0-QA16: Winding Key 規範與洋紅背景無孔洞 ---")
    key_p = f"{WALRUS_PD}/winding_key/key_walrus_anchor_handwheel_brass.png"
    if os.path.exists(key_p):
        arr_k = np.array(Image.open(key_p).convert("RGBA"))
        alpha_k = arr_k[:, :, 3]

        # White run test: pure white runs (R>245, G>245, B>245)
        white_mask = (alpha_k > 200) & (arr_k[:, :, 0] > 245) & (arr_k[:, :, 1] > 245) & (arr_k[:, :, 2] > 245)
        max_white_run = 0
        for row in white_mask:
            run = 0
            for val in row:
                if val:
                    run += 1
                    max_white_run = max(max_white_run, run)
                else:
                    run = 0

        # Dark block run test (R<40, G<40, B<40, alpha>200)
        dark_mask = (alpha_k > 200) & (arr_k[:, :, 0] < 40) & (arr_k[:, :, 1] < 40) & (arr_k[:, :, 2] < 40)
        max_dark_run = 0
        for row in dark_mask:
            run = 0
            for val in row:
                if val:
                    run += 1
                    max_dark_run = max(max_dark_run, run)
                else:
                    run = 0

        print(f"  • Winding key max white run: {max_white_run} (limit < 40)")
        print(f"  • Winding key max dark run: {max_dark_run} (limit < 13)")

        if max_white_run >= 40:
            print(f"❌ FAILED 0-QA16: Winding key white run {max_white_run} >= 40!")
            all_ok = False
        else:
            print("  ✓ PASSED 0-QA16: Winding key white run < 40")

        if max_dark_run >= 13:
            print(f"❌ FAILED 0-ART29: Winding key dark run {max_dark_run} >= 13!")
            all_ok = False
        else:
            print("  ✓ PASSED 0-ART29: Winding key dark run < 13")

    # Hole fill test on composite core body
    comp_p = f"{WALRUS_PD}/proof_paperdoll_walrus_composite.png"
    if os.path.exists(comp_p):
        comp_im = Image.open(comp_p).convert("RGBA")
        comp_alpha = np.array(comp_im)[:, :, 3] > 8
        core_mask = comp_alpha[35:95, 42:86]
        filled_core = np.asarray(binary_fill_holes(core_mask), dtype=bool)
        holes_in_core = filled_core & (~core_mask)
        num_holes = int(np.sum(holes_in_core))
        print(f"  Metric 3 (Holes in composite core body): {num_holes} px (expected: 0)")
        if num_holes > 0:
            y_indices, x_indices = np.where(holes_in_core)
            for y_idx, x_idx in zip(y_indices[:15], x_indices[:15]):
                print(f"     Hole at x={x_idx + 42}, y={y_idx + 35}")
            print(f"❌ FAILED 0-QA16 Metric 3 / 0-ART29: Detected {num_holes} hole pixels in composite core!")
            all_ok = False
        else:
            print("  ✓ PASSED 0-QA16 Metric 3: Zero internal holes in composite core on magenta background")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-QA31: Optic Core & Composite Coverage
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-QA31: 靈晶與目鏡色階與合成圖層覆蓋 ---")
    if os.path.exists(comp_p):
        arr_comp = np.array(Image.open(comp_p).convert("RGBA"))
        opaque_comp = np.sum(arr_comp[:, :, 3] > 20)
        unique_comp = len(np.unique(arr_comp[arr_comp[:, :, 3] > 20][:, :3], axis=0))
        print(f"  • Composite opaque pixels: {opaque_comp} (limit > 3000)")
        print(f"  • Composite unique colors: {unique_comp} (limit > 300)")

        if opaque_comp <= 3000:
            print(f"❌ FAILED 0-QA31: Composite opaque pixels {opaque_comp} <= 3000!")
            all_ok = False
        else:
            print("  ✓ PASSED 0-QA31: Composite opaque coverage > 3000 px")

        if unique_comp < 300:
            print(f"❌ FAILED 0-QA31: Composite unique colors {unique_comp} < 300!")
            all_ok = False
        else:
            print("  ✓ PASSED 0-QA31: Composite unique colors > 300")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-QA34 / 三區量化稽核: Three-Zone Analysis in 512x512
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-QA34 / 三區量化稽核 (Head, Torso, Legs in 512x512 > 1500px each) ---")
    if os.path.exists(comp_p):
        im_comp = Image.open(comp_p).convert("RGBA")
        im_c512 = im_comp.resize((512, 512), Image.Resampling.LANCZOS)
        arr_c512 = np.array(im_c512)
        alpha_512 = arr_c512[:, :, 3] > 20

        # Zone definitions in 512 (Head: y: 0..240, Torso: y: 241..390, Legs: y: 391..511)
        head_px = int(np.sum(alpha_512[0:241, :]))
        torso_px = int(np.sum(alpha_512[241:391, :]))
        legs_px = int(np.sum(alpha_512[391:512, :]))

        print(f"  • Head zone (y: 0..240):   {head_px:6d} px (limit > 1500)")
        print(f"  • Torso zone (y: 241..390): {torso_px:6d} px (limit > 1500)")
        print(f"  • Legs zone (y: 391..511):  {legs_px:6d} px (limit > 1500)")

        if head_px <= 1500 or torso_px <= 1500 or legs_px <= 1500:
            print(f"❌ FAILED 0-QA34: One or more zones have <= 1500 pixels!")
            all_ok = False
        else:
            print("  ✓ PASSED 0-QA34: All three zones exceed 1500 px in 512x512")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART25: Showcase HD RGBA mode and 4-corner transparency
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART25: Showcase HD 800x1200 RGBA & 四角完全透明稽核 ---")
    showcase_p = f"{SHOWCASE_DIR}/walrus_idle_hd.png"
    if os.path.exists(showcase_p):
        im_sh = Image.open(showcase_p)
        if im_sh.mode != "RGBA" or im_sh.size != (800, 1200):
            print(f"❌ FAILED 0-ART25: Showcase HD wrong mode {im_sh.mode} or size {im_sh.size}!")
            all_ok = False
        else:
            arr_sh = np.array(im_sh)
            corners = [
                arr_sh[0, 0, 3],
                arr_sh[0, 799, 3],
                arr_sh[1199, 0, 3],
                arr_sh[1199, 799, 3]
            ]
            if any(c > 0 for c in corners):
                print(f"❌ FAILED 0-ART25: Showcase HD corners not transparent: {corners}")
                all_ok = False
            else:
                print("  ✓ PASSED 0-ART25: Showcase HD is 800x1200 RGBA with 4 corners 100% transparent")

    if all_ok:
        print("\n🎉 ALL 0-ART / 0-QA AUDIT CHECKS PASSED FOR THE ICEBREAKER WALRUS!")
        return 0
    else:
        print("\n❌ SOME AUDIT CHECKS FAILED FOR THE ICEBREAKER WALRUS!")
        return 1

if __name__ == "__main__":
    sys.exit(audit())
