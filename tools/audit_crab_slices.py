#!/usr/bin/env python3
"""
audit_crab_slices.py
Rigorous automated audit script for 第五十二族 熔砧石蟹 (The Anvil Crab, crab) paperdoll slices against:
- review.md 0-ART5 (c100 color richness, anti-placeholder)
- review.md 0-ART9 / 0-ART11 (no weapon baked into chassis, strict x < 94)
- review.md 0-ART18 (bare chassis multi-tone depth, no flat placeholder blocks)
- review.md 0-ART25 (showcase HD RGBA mode, 4 corners transparent)
- review.md 0-ART26b (costume decoupled, no lower chassis baked, y >= 96 zero pixels)
- review.md 0-ART27 (head_unit & eye slot separation, hollow eye sockets)
- review.md 0-ART28n (MD5 查重: unique MD5 hashes across all 7 slices, zero duplicate placeholder assets)
- review.md 0-ART28q (色距量測: head_unit and chassis cast iron plate L2 color distance < 60.0)
- review.md 0-ART28r (連通元件: discrete connected components audit, zero undeclared fragments >= 50px)
- 0-ART29 (no dark rounded rectangle / box artifacts in winding_key, transparent corners, zero holes on magenta)
- 0-QA16 (quantitative white rectangle run test, dark block test, hole fill test)
- 0-QA30 (crab aliases 100% aligned between paperdoll_slots.json and fallback)
- 0-QA31 (quantitative verification of optic core / composite to prevent false vision alerts)
- 128x128 and 512x512 resolution check
"""

import os
import sys
import json
import hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes, label

REPO_ROOT = "/opt/side/bravesoul-game"
CRAB_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crab"

SLICES = [
    ("chassis", "chassis_crab_molten_iron_default"),
    ("head_unit", "head_crab_periscope_visor_cowl"),
    ("winding_key", "key_crab_quad_flue_crucible_t_bar"),
    ("costume", "costume_crab_furnace_sapper_cuirass"),
    ("optic_core", "face_crab_dual_gauge_convex_lens"),
    ("weapon", "weapon_crab_obsidian_stamping_fist"),
    ("back_curio", "curio_crab_pneumatic_exhaust_chimney")
]

def get_md5(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def get_average_plate_color(arr: np.ndarray, alpha_thresh=200, min_rgb=40, plate_ymin=0) -> np.ndarray:
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
    print("=== AUDITING ANVIL CRAB 7 PAPERDOLL SLICES ===")
    all_ok = True
    metrics = {}
    md5_128 = {}
    md5_512 = {}

    for slot, item_id in SLICES:
        path_128 = f"{CRAB_PD}/{slot}/{item_id}.png"
        path_512 = f"{CRAB_PD}/{slot}/{item_id}_512.png"

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

        # Audit 0-ART5: Color richness
        if unique_colors < 10 and slot not in ["optic_core"]:
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
    print("\n[0-ART28n Audit: MD5 查重與唯一性]")
    unique_hashes_128 = set(md5_128.values())
    unique_hashes_512 = set(md5_512.values())
    print(f"  128px 切片唯一 MD5 數: {len(unique_hashes_128)} / {len(SLICES)}")
    print(f"  512px 切片唯一 MD5 數: {len(unique_hashes_512)} / {len(SLICES)}")
    if len(unique_hashes_128) < len(SLICES) or len(unique_hashes_512) < len(SLICES):
        print("❌ FAILED 0-ART28n: 發現切片 MD5 重複，存在重複切片或複製佔位圖！")
        all_ok = False
    else:
        print("✓ PASSED 0-ART28n: 7 大切片 MD5 全數唯一獨立，零重複、零佔位複製圖！")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART28q: 色距量測 (Color Distance Coherence)
    # ─────────────────────────────────────────────────────────────
    print("\n[0-ART28q Audit: 鑄鐵板件 L2 色距量測 (Head Unit vs Chassis)]")
    head_im = Image.open(f"{CRAB_PD}/head_unit/head_crab_periscope_visor_cowl.png").convert("RGBA")
    chassis_im = Image.open(f"{CRAB_PD}/chassis/chassis_crab_molten_iron_default.png").convert("RGBA")
    head_arr = np.array(head_im)
    ch_arr = np.array(chassis_im)

    c_head = get_average_plate_color(head_arr, plate_ymin=36)
    c_chassis = get_average_plate_color(ch_arr)
    dist = color_distance(c_head, c_chassis)
    print(f"  Head Unit 平均色 (RGB):    ({c_head[0]:.1f}, {c_head[1]:.1f}, {c_head[2]:.1f})")
    print(f"  Chassis 底盤平均色 (RGB):  ({c_chassis[0]:.1f}, {c_chassis[1]:.1f}, {c_chassis[2]:.1f})")
    print(f"  L2 板件色距:              {dist:.2f} (規範上限: < 60.0)")
    if dist >= 60.0:
        print(f"❌ FAILED 0-ART28q: 頭部與底盤板件色距超標 ({dist:.2f} >= 60.0)！")
        all_ok = False
    else:
        print(f"✓ PASSED 0-ART28q: 色距符合規範 ({dist:.2f} < 60.0)，鑄鐵板件色調高度協調一致！")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART28r: 連通元件獨立區塊稽核 (Connected Components Audit)
    # ─────────────────────────────────────────────────────────────
    print("\n[0-ART28r Audit: 連通元件獨立區塊稽核 (alpha > 40)]")
    cc_ok = True
    for slot, item_id in SLICES:
        path_512 = f"{CRAB_PD}/{slot}/{item_id}_512.png"
        im_512 = Image.open(path_512).convert("RGBA")
        arr_512 = np.array(im_512)
        alpha_mask = arr_512[:, :, 3] > 40
        labeled, num_features = label(alpha_mask)
        num_features = int(num_features)

        components = []
        for i in range(1, num_features + 1):
            mask_i = (labeled == i)
            cnt = int(np.sum(mask_i))
            ys, xs = np.where(mask_i)
            bbox = (int(np.min(xs)), int(np.min(ys)), int(np.max(xs)), int(np.max(ys)))
            components.append({"count": cnt, "bbox": bbox, "id": i})

        components.sort(key=lambda c: c["count"], reverse=True)
        main_comp = components[0] if components else None
        undeclared_fragments = []

        for c in components[1:]:
            if c["count"] >= 50:
                if slot == "optic_core":
                    # Dual optic eye lenses
                    pass
                elif slot == "winding_key":
                    # Four cloverleaf vanes
                    pass
                elif slot == "back_curio":
                    # Dual chimneys
                    pass
                elif slot == "head_unit":
                    # Dual periscope rangefinder pods
                    pass
                else:
                    undeclared_fragments.append(c)

        if undeclared_fragments:
            print(f"  ❌ [{slot:<12}] 發現未交代異常獨立區塊 (>=50px): {len(undeclared_fragments)} 個")
            for c in undeclared_fragments:
                print(f"       - count={c['count']}px bbox={c['bbox']}")
            cc_ok = False
        else:
            main_cnt = main_comp["count"] if main_comp else 0
            print(f"  ✓ [{slot:<12}] 512px 主體面積: {main_cnt:6d}px, 獨立碎片查核合格")

    if not cc_ok:
        all_ok = False
    else:
        print("✓ PASSED 0-ART28r: 7 大切片連通元件查驗合格，無任何 >=50px 未交代孤立雜物或毛刺！")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART9/11: Chassis weapon baking check (strictly zero pixels at x >= 94)
    # ─────────────────────────────────────────────────────────────
    weapon_zone_pixels = int(np.sum(ch_arr[:, 94:128, 3] > 10))
    print(f"\n[0-ART9/11 Audit] Chassis pixels in weapon zone (x:94..128): {weapon_zone_pixels}")
    if weapon_zone_pixels > 0:
        print(f"❌ FAILED 0-ART9/11: Weapon baked into chassis ({weapon_zone_pixels} pixels at x>=94)!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART9/11: Chassis has strictly ZERO baked weapon pixels at x>=94!")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART18: Torso color depth
    # ─────────────────────────────────────────────────────────────
    torso_region = ch_arr[58:94, 44:84]
    torso_opaque = torso_region[:, :, 3] > 8
    torso_colors = len(np.unique(torso_region[torso_opaque][:, :3], axis=0))
    print(f"[0-ART18 Audit] Bare chassis torso unique colors: {torso_colors} (expected >= 20)")
    if torso_colors < 20:
        print(f"❌ FAILED 0-ART18: Torso has low multi-tone depth ({torso_colors} colors)!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART18: Torso has rich multi-tone depth and shading!")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART26b: Costume lower chassis baking check (strictly zero pixels at y >= 96)
    # ─────────────────────────────────────────────────────────────
    costume_im = Image.open(f"{CRAB_PD}/costume/costume_crab_furnace_sapper_cuirass.png").convert("RGBA")
    cos_arr = np.array(costume_im)
    lower_costume_pixels = int(np.sum(cos_arr[96:128, :, 3] > 30))
    print(f"[0-ART26b Audit] Costume pixels in lower leg zone (y:96..128): {lower_costume_pixels}")
    if lower_costume_pixels > 0:
        print(f"❌ FAILED 0-ART26b: Costume bakes lower chassis ({lower_costume_pixels} pixels)!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART26b: Costume is fully decoupled and does not bake lower chassis!")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART27: Optic core and head unit separation
    # ─────────────────────────────────────────────────────────────
    core_im = Image.open(f"{CRAB_PD}/optic_core/face_crab_dual_gauge_convex_lens.png").convert("RGBA")
    core_arr = np.array(core_im)

    # In head_unit, check that eye centers (54, 42) and (74, 42) are hollow (alpha == 0)
    left_socket_alpha = head_arr[41:44, 53:56, 3]
    right_socket_alpha = head_arr[41:44, 73:76, 3]
    max_socket_alpha = max(int(np.max(left_socket_alpha)), int(np.max(right_socket_alpha)))
    print(f"\n[0-ART27 Audit] Head unit eye sockets inner max alpha: {max_socket_alpha} (expected: 0)")
    if max_socket_alpha > 0:
        print("❌ FAILED 0-ART27: Head unit eye sockets are not hollow!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART27: Head unit has clean hollow eye sockets for optic_core insertion!")

    # In optic_core, check that eye centers have opaque lens content
    left_core_alpha = int(core_arr[42, 54, 3])
    right_core_alpha = int(core_arr[42, 74, 3])
    min_core_alpha = min(left_core_alpha, right_core_alpha)
    print(f"[0-ART27 Audit] Optic core lens center min alpha: {min_core_alpha} (expected: > 200)")
    if min_core_alpha < 200:
        print("❌ FAILED 0-ART27: Optic core eyes not centered properly in eye sockets!")
        all_ok = False
    else:
        print("✓ PASSED 0-ART27: Optic core precisely aligns with head unit eye sockets!")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-QA30: crab aliases 100% aligned
    # ─────────────────────────────────────────────────────────────
    with open(f"{REPO_ROOT}/game/data/tables/paperdoll_slots.json", "r", encoding="utf-8") as f:
        spec_data = json.load(f)
    races_list = spec_data.get("races_specification", {}).get("races", [])
    crab_spec = next((r for r in races_list if r.get("race_id") == "crab"), {})
    crab_aliases = crab_spec.get("aliases", [])
    expected_aliases = ["anvil_crab", "crucible_crab", "molten_crab", "boxer_crab", "clockwork_crab"]
    if crab_aliases != expected_aliases:
        print(f"❌ FAILED 0-QA30: paperdoll_slots.json crab aliases mismatch: {crab_aliases} vs {expected_aliases}")
        all_ok = False
    else:
        print(f"✓ PASSED 0-QA30: crab aliases perfectly aligned: {crab_aliases}")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-QA31: Quantitative verification of composite & optic core
    # ─────────────────────────────────────────────────────────────
    comp_im = Image.open(f"{CRAB_PD}/proof_paperdoll_crab_composite.png").convert("RGBA")
    comp_arr = np.array(comp_im)
    comp_alpha = comp_arr[:, :, 3] > 8
    opaque_comp = int(np.sum(comp_alpha))
    print(f"\n[0-QA31 Audit] Composite total opaque pixels: {opaque_comp:5d} (> 3000)")
    if opaque_comp < 3000:
        print("❌ FAILED 0-QA31: Composite character has insufficient pixel coverage!")
        all_ok = False
    else:
        print("✓ PASSED 0-QA31: Composite character has full volumetric coverage")

    # Optic core region on composite (x: 48..80, y: 36..48)
    optic_zone = comp_arr[36:49, 48:81]
    optic_opaque = optic_zone[:, :, 3] > 8
    optic_colors = len(np.unique(optic_zone[optic_opaque][:, :3], axis=0))
    print(f"[0-QA31 Audit] Composite optic core zone unique colors: {optic_colors} (expected >= 15)")
    if optic_colors < 15:
        print("❌ FAILED 0-QA31: Optic core appears flat or unrendered!")
        all_ok = False
    else:
        print("✓ PASSED 0-QA31: Optic core verified vibrant with rich color depth")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-QA16 & 0-ART29: 破圖量測與 winding_key 去背殘留
    # ─────────────────────────────────────────────────────────────
    print("\n[0-QA16 & 0-ART29 Audit: 破圖三項量測與發條鑰匙去背殘留查核]")
    # 1. White rectangle / hole test: alpha > 250 and min(RGB) >= 235
    white_mask = (comp_arr[:, :, 3] > 250) & (np.min(comp_arr[:, :, :3], axis=2) >= 235)
    max_white_run = 0
    for row in white_mask:
        current_run = 0
        for val in row:
            if val:
                current_run += 1
                if current_run > max_white_run:
                    max_white_run = current_run
            else:
                current_run = 0
    print(f"  Metric 1 (Max white horizontal run): {max_white_run} px (expected < 40)")
    if max_white_run >= 40:
        print(f"❌ FAILED 0-QA16 Metric 1: Abnormal white run detected ({max_white_run}px)!")
        all_ok = False
    else:
        print("  ✓ PASSED 0-QA16 Metric 1: Zero abnormal white rectangle artifacts")

    # 2. Dark block test on key (0-ART29 dark limit on winding key + transparent corners)
    key_im = Image.open(f"{CRAB_PD}/winding_key/key_crab_quad_flue_crucible_t_bar.png").convert("RGBA")
    key_arr = np.array(key_im)
    key_corners = [
        key_arr[0, 0, 3], key_arr[0, -1, 3],
        key_arr[-1, 0, 3], key_arr[-1, -1, 3]
    ]
    print(f"  0-ART29 Winding key 4角透明度: {key_corners} (expected all 0)")
    if any(c > 0 for c in key_corners):
        print(f"❌ FAILED 0-ART29: Winding key has opaque corners: {key_corners}!")
        all_ok = False
    else:
        print("  ✓ PASSED 0-ART29: Winding key 4 角完全透明 (alpha=0)")

    dark_mask = (key_arr[:, :, 3] > 8) & (np.max(key_arr[:, :, :3], axis=2) < 70)
    dark_pixels = int(np.sum(dark_mask))
    max_dark_run = 0
    for row in dark_mask:
        current_run = 0
        for val in row:
            if val:
                current_run += 1
                if current_run > max_dark_run:
                    max_dark_run = current_run
            else:
                current_run = 0
    print(f"  Metric 2 (Winding key dark pixels & max run): {dark_pixels} px, max run {max_dark_run} px (limit: < 260px, run < 13)")
    if dark_pixels >= 260 or max_dark_run >= 13:
        print(f"❌ FAILED 0-QA16 Metric 2 / 0-ART29: Winding key has dark plate artifact ({dark_pixels}px, run={max_dark_run})!")
        all_ok = False
    else:
        print("  ✓ PASSED 0-QA16 Metric 2 / 0-ART29: Winding key has zero dark plate artifact")

    # 3. Closed hole fill test (Magenta / 0-ART29 Hole Audit on core body x: 42..86, y: 35..95)
    core_mask = comp_alpha[35:95, 42:86]
    filled_core = np.asarray(binary_fill_holes(core_mask), dtype=bool)
    holes_in_core = filled_core & (~core_mask)
    num_holes = int(np.sum(holes_in_core))
    print(f"  Metric 3 (Holes in composite core body on magenta): {num_holes} px (expected: 0)")
    if num_holes > 0:
        y_indices, x_indices = np.where(holes_in_core)
        for y_idx, x_idx in zip(y_indices[:15], x_indices[:15]):
            print(f"     Hole at x={x_idx + 42}, y={y_idx + 35}")
        print(f"❌ FAILED 0-QA16 Metric 3 / 0-ART29: Detected {num_holes} hole pixels in composite core!")
        all_ok = False
    else:
        print("  ✓ PASSED 0-QA16 Metric 3: Zero internal holes in composite core on magenta background")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART25: Showcase HD check
    # ─────────────────────────────────────────────────────────────
    showcase_path = f"{REPO_ROOT}/game/assets/sprites/player/showcase/crab_idle_hd.png"
    if not os.path.exists(showcase_path):
        print(f"❌ FAILED 0-ART25: Missing showcase HD: {showcase_path}")
        all_ok = False
    else:
        sc_im = Image.open(showcase_path)
        if sc_im.size != (800, 1200) or sc_im.mode != "RGBA":
            print(f"❌ FAILED 0-ART25: Showcase HD has wrong spec {sc_im.size} {sc_im.mode}")
            all_ok = False
        else:
            sc_arr = np.array(sc_im)
            corners = [
                sc_arr[0, 0, 3], sc_arr[0, -1, 3],
                sc_arr[-1, 0, 3], sc_arr[-1, -1, 3]
            ]
            if any(c > 0 for c in corners):
                print(f"❌ FAILED 0-ART25: Showcase HD corners are not transparent: {corners}")
                all_ok = False
            else:
                print("✓ PASSED 0-ART25: Showcase HD 800x1200 RGBA with 100% transparent corners")

    print("\n" + ("🎉 ALL ANVIL CRAB AUDITS PASSED PERFECTLY!" if all_ok else "❌ SOME AUDITS FAILED!"))
    return all_ok

if __name__ == "__main__":
    success = audit()
    sys.exit(0 if success else 1)
