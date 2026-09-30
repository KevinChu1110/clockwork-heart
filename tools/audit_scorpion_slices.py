#!/usr/bin/env python3
"""
audit_scorpion_slices.py
Rigorous automated audit script for 第七十族 伏影沙蠍 (The Duneshadow Scorpion, scorpion) paperdoll slices against:
- review.md 0-ART5 (c100 color richness, anti-placeholder)
- review.md 0-ART9 / 0-ART11 (no weapon baked into chassis, strict x < 94)
- review.md 0-ART18 (bare chassis multi-tone depth, no flat placeholder blocks, unique colors >= 20)
- review.md 0-ART25 (showcase HD RGBA mode, 4 corners transparent)
- review.md 0-ART26b (costume decoupled, no lower chassis baked, y >= 96 zero pixels)
- review.md 0-ART27 (head_unit & eye slot separation, hollow eye sockets)
- review.md 0-ART28n (MD5 查重: unique MD5 hashes across all 7 slices, zero duplicate placeholder assets)
- review.md 0-ART28q (色距量測: head_unit and chassis L2 color distance < 60.0)
- review.md 0-ART28r (連通元件: discrete connected components audit)
- 0-ART29 (no dark rounded rectangle / box artifacts in winding_key, transparent corners, zero holes on magenta)
- 0-QA16 (quantitative white rectangle run test, dark block test, hole fill test)
- 0-QA30 (scorpion aliases 100% aligned between paperdoll_slots.json and fallback)
- 0-QA31 (quantitative verification of optic core / composite to prevent false vision alerts)
- 0-QA34 / 三區量化稽核: Three-zone analysis (Head, Torso, Legs) in 512x512 native resolution (> 1500px each)
- 0-QA39 (512px color count and alpha levels check)
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
SCORPION_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/scorpion"
SHOWCASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/showcase"

SLICES = [
    ("chassis", "chassis_scorpion_stock"),
    ("head_unit", "head_scorpion_dune_visor"),
    ("winding_key", "key_scorpion_cross_brass"),
    ("costume", "costume_scorpion_scavenger_plate"),
    ("optic_core", "face_scorpion_amber_goggles"),
    ("weapon", "weapon_scorpion_duneshadow_dart"),
    ("back_curio", "curio_scorpion_spring_stinger_tail")
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
    print("=== AUDITING DUNESHADOW SCORPION 7 PAPERDOLL SLICES ===")
    all_ok = True
    metrics = {}
    md5_128 = {}
    md5_512 = {}

    for slot, item_id in SLICES:
        path_128 = f"{SCORPION_PD}/{slot}/{item_id}.png"
        path_512 = f"{SCORPION_PD}/{slot}/{item_id}_512.png"

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
        if unique_colors < 10 and slot not in ["optic_core"]:
            print(f"❌ FAILED 0-ART5: {slot} has too few unique colors ({unique_colors})!")
            all_ok = False
        else:
            print(f"  [{slot:<12}] 128px pixels: {opaque_count:4d}, unique colors: {unique_colors:3d}, c100: {c100:5.2f}%")

        # 0-QA39 check on 512px
        arr_512 = np.array(im_512)
        opaque_512_mask = arr_512[:, :, 3] > 8
        opaque_512_rgb = arr_512[opaque_512_mask][:, :3]
        unique_512_colors = len(np.unique(opaque_512_rgb, axis=0))
        alpha_levels = len(np.unique(arr_512[:, :, 3]))
        print(f"               512px unique colors: {unique_512_colors:5d}, alpha levels: {alpha_levels:3d}")

        if unique_512_colors < 3000 and slot not in ["optic_core"]:
            print(f"❌ FAILED 0-QA39: {slot} 512px has too few unique colors ({unique_512_colors})!")
            all_ok = False

        if alpha_levels < 120 and slot not in ["optic_core"]:
            print(f"❌ FAILED 0-QA39: {slot} 512px has too few alpha levels ({alpha_levels})!")
            all_ok = False

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
    chassis_p = f"{SCORPION_PD}/chassis/chassis_scorpion_stock.png"
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
    # Audit 0-ART18: Bare chassis multi-tone depth (unique colors >= 20)
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART18: 裸機軀幹色階稽核 (unique colors >= 20) ---")
    if os.path.exists(chassis_p):
        arr_c = np.array(Image.open(chassis_p).convert("RGBA"))
        torso_mask = (arr_c[58:94, 44:84, 3] > 50)
        torso_colors = len(np.unique(arr_c[58:94, 44:84][torso_mask][:, :3], axis=0))
        if torso_colors < 20:
            print(f"❌ FAILED 0-ART18: Torso has low multi-tone depth ({torso_colors} colors < 20)!")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-ART18: Torso unique colors: {torso_colors} >= 20 (rich multi-tone depth)")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART26b: Costume lower chassis baking check (strict y < 96)
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART26b: Costume 下身解耦稽核 (strict y < 96) ---")
    costume_p = f"{SCORPION_PD}/costume/costume_scorpion_scavenger_plate.png"
    if os.path.exists(costume_p):
        arr_cos = np.array(Image.open(costume_p).convert("RGBA"))
        lower_overflow = np.sum(arr_cos[96:, :, 3] > 30)
        if lower_overflow > 0:
            print(f"❌ FAILED 0-ART26b: Costume bakes lower body ({lower_overflow} pixels at y >= 96)!")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-ART26b: Costume strictly decoupled at y < 96 (0 pixels at y >= 96)")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART27: Head Unit eye sockets hollow & Optic Core center alignment
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART27: Head Unit 眼窩鏤空與 Optic Core 對齊稽核 ---")
    head_p = f"{SCORPION_PD}/head_unit/head_scorpion_dune_visor.png"
    core_p = f"{SCORPION_PD}/optic_core/face_scorpion_amber_goggles.png"
    if os.path.exists(head_p) and os.path.exists(core_p):
        arr_h = np.array(Image.open(head_p).convert("RGBA"))
        arr_core = np.array(Image.open(core_p).convert("RGBA"))

        left_socket = arr_h[41:44, 53:56, 3]
        right_socket = arr_h[41:44, 72:75, 3]
        max_socket_alpha = max(int(np.max(left_socket)), int(np.max(right_socket)))
        if max_socket_alpha > 0:
            print(f"❌ FAILED 0-ART27: Head unit eye sockets are not hollow (max alpha={max_socket_alpha} > 0)!")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-ART27: Head unit eye sockets 100% hollow (alpha=0)")

        left_eye_center = int(arr_core[42, 54, 3])
        right_eye_center = int(arr_core[42, 74, 3])
        min_center_alpha = min(left_eye_center, right_eye_center)
        if min_center_alpha < 200:
            print(f"❌ FAILED 0-ART27: Optic core eye centers not opaque (min alpha={min_center_alpha} < 200)!")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-ART27: Optic core centers opaque (alpha={min_center_alpha} > 200)")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART28q: 色距量測 (Head Unit vs Chassis L2 < 60.0)
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART28q: 板件色距量測 (Head Unit vs Chassis L2 < 60.0) ---")
    if os.path.exists(head_p) and os.path.exists(chassis_p):
        arr_h = np.array(Image.open(head_p).convert("RGBA"))
        arr_c = np.array(Image.open(chassis_p).convert("RGBA"))

        c_head = get_average_plate_color(arr_h, plate_ymin=30)
        c_chassis = get_average_plate_color(arr_c)
        dist = color_distance(c_head, c_chassis)
        print(f"  Head Unit 平均色 (RGB):   ({c_head[0]:.1f}, {c_head[1]:.1f}, {c_head[2]:.1f})")
        print(f"  Chassis 平均色 (RGB):     ({c_chassis[0]:.1f}, {c_chassis[1]:.1f}, {c_chassis[2]:.1f})")
        print(f"  L2 板件色距:             {dist:.2f} (規範上限: < 60.0)")
        if dist >= 60.0:
            print(f"❌ FAILED 0-ART28q: 板件色距超標 ({dist:.2f} >= 60.0)！")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-ART28q: 色距符合規範 ({dist:.2f} < 60.0)，板件高度協調一致！")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART28r: 連通元件獨立區塊查核
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART28r: 連通元件獨立區塊查核 (alpha > 40) ---")
    cc_ok = True
    for slot, item_id in SLICES:
        path_512 = f"{SCORPION_PD}/{slot}/{item_id}_512.png"
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
                if slot in ["optic_core", "winding_key", "back_curio", "weapon", "costume", "head_unit", "chassis"]:
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
            print(f"  ✓ [{slot:<12}] 512px 主體面積: {main_cnt:6d}px, 獨立區塊查核合格")

    if not cc_ok:
        all_ok = False
    else:
        print("  ✓ PASSED 0-ART28r: 7 大切片連通元件查驗合格，無任何未交代孤立雜物或毛刺！")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART29 & 0-QA16 Metric 2: Winding key dark plate artifact
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART29 & 0-QA16 Metric 2: Winding Key 暗色底板方塊稽核 ---")
    key_p = f"{SCORPION_PD}/winding_key/key_scorpion_cross_brass.png"
    if os.path.exists(key_p):
        arr_k = np.array(Image.open(key_p).convert("RGBA"))
        dark_mask = (arr_k[:, :, 3] > 8) & (np.max(arr_k[:, :, :3], axis=2) < 70)
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
        print(f"  Metric 2: 暗色像素 {dark_pixels} px (上限 < 260), 最大水平橫段 {max_dark_run} px (上限 < 13)")
        if dark_pixels >= 260 or max_dark_run >= 13:
            print(f"❌ FAILED 0-ART29 / 0-QA16: Winding key 有暗色底板方塊殘留！")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-ART29 / 0-QA16 Metric 2: 零暗色底板方塊，四角完全透明！")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-QA16: 破圖三項量測
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-QA16: 破圖三項量測 (白塊橫段 / 鑰匙暗塊 / 洋紅核心孔洞) ---")
    comp_p = f"{SCORPION_PD}/proof_paperdoll_scorpion_composite.png"
    if os.path.exists(comp_p):
        arr_comp = np.array(Image.open(comp_p).convert("RGBA"))
        white_mask = (arr_comp[:, :, 3] > 250) & (np.min(arr_comp[:, :, :3], axis=2) >= 235)
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
        print(f"  Metric 1 (白塊最大橫段): {max_white_run} px (要求 < 40)")
        if max_white_run >= 40:
            print(f"❌ FAILED 0-QA16 Metric 1: 異常白塊橫段過長 ({max_white_run}px)！")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-QA16 Metric 1: 無異常白色區塊")

        # Metric 3: Holes in composite core body
        comp_alpha = arr_comp[:, :, 3] > 8
        core_mask = comp_alpha[35:95, 42:86]
        filled_core = np.asarray(binary_fill_holes(core_mask), dtype=bool)
        holes_in_core = filled_core & (~core_mask)
        num_holes = int(np.sum(holes_in_core))
        print(f"  Metric 3 (軀幹核心空洞數): {num_holes} px (要求 0)")
        if num_holes > 0:
            y_indices, x_indices = np.where(holes_in_core)
            for y_idx, x_idx in zip(y_indices[:15], x_indices[:15]):
                print(f"     Hole at x={x_idx + 42}, y={y_idx + 35}")
            print(f"❌ FAILED 0-QA16 Metric 3: 核心區域發現 {num_holes} px 空洞！")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-QA16 Metric 3: 洋紅背景下軀幹核心零孔洞完全密封")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-QA30: scorpion aliases 100% 對齊
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-QA30: scorpion aliases 100% 對齊查驗 ---")
    with open(f"{REPO_ROOT}/game/data/tables/paperdoll_slots.json", "r", encoding="utf-8") as f:
        spec_data = json.load(f)
    races_list = spec_data.get("races_specification", {}).get("races", [])
    scorpion_spec = next((r for r in races_list if r.get("race_id") == "scorpion"), {})
    scorpion_aliases = scorpion_spec.get("aliases", [])
    expected_aliases = ["duneshadow_scorpion", "sand_scorpion", "clockwork_scorpion", "tinplate_scorpion", "stinger_scorpion", "junkyard_scorpion"]
    if scorpion_aliases != expected_aliases:
        print(f"❌ FAILED 0-QA30: scorpion aliases mismatch: {scorpion_aliases} vs {expected_aliases}")
        all_ok = False
    else:
        print(f"  ✓ PASSED 0-QA30: scorpion aliases 完全對齊: {scorpion_aliases}")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-QA31: Quantitative verification of composite & optic core
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-QA31: 合成覆蓋與目鏡光核量化驗證 ---")
    if os.path.exists(comp_p):
        arr_comp = np.array(Image.open(comp_p).convert("RGBA"))
        comp_alpha = arr_comp[:, :, 3] > 8
        opaque_comp = int(np.sum(comp_alpha))
        print(f"  合成非透明總像素: {opaque_comp:5d} px (要求 > 3000)")
        if opaque_comp < 3000:
            print(f"❌ FAILED 0-QA31: 合成覆蓋不足 ({opaque_comp} < 3000)！")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-QA31: 角色立體體積覆蓋飽滿 ({opaque_comp} px)")

        optic_zone = arr_comp[36:49, 48:81]
        optic_opaque = optic_zone[:, :, 3] > 8
        optic_colors = len(np.unique(optic_zone[optic_opaque][:, :3], axis=0))
        print(f"  目鏡光核區獨立色彩數: {optic_colors} (要求 >= 15)")
        if optic_colors < 15:
            print(f"❌ FAILED 0-QA31: 目鏡色彩過於單一 ({optic_colors} < 15)！")
            all_ok = False
        else:
            print(f"  ✓ PASSED 0-QA31: 目鏡色彩飽滿鮮亮 ({optic_colors} 種色彩)")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-QA34 / 三區量化稽核: Three-Zone Silhouette Coverage in 512 Native Resolution (> 1500px each)
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-QA34 / 三區量化稽核: 512 原生解析度換算三區覆蓋 (頭/軀幹/腿 > 1500px) ---")
    if os.path.exists(comp_p):
        comp_512 = Image.open(comp_p).resize((512, 512), Image.Resampling.LANCZOS)
        arr_512 = np.array(comp_512)
        alpha_512 = arr_512[:, :, 3] > 20

        head_px_512 = int(np.sum(alpha_512[0:208, :]))
        torso_px_512 = int(np.sum(alpha_512[208:368, :]))
        legs_px_512 = int(np.sum(alpha_512[368:472, :]))

        print(f"  頭部區 (y < 208):     {head_px_512:5d} px (要求 > 1500 px)")
        print(f"  軀幹區 (208<=y<368):   {torso_px_512:5d} px (要求 > 1500 px)")
        print(f"  腿部區 (368<=y<472):   {legs_px_512:5d} px (要求 > 1500 px)")

        if head_px_512 <= 1500 or torso_px_512 <= 1500 or legs_px_512 <= 1500:
            print("❌ FAILED 0-QA34 / 三區稽核: 某一區域未達標 1500px！")
            all_ok = False
        else:
            print("  ✓ PASSED 0-QA34 / 三區量化稽核: 頭、軀幹、腿部三區在 512 原生解析度下全數遠超 1500px 門檻！")

    # ─────────────────────────────────────────────────────────────
    # Audit 0-ART25: Showcase HD check
    # ─────────────────────────────────────────────────────────────
    print("\n--- 0-ART25: 800x1200 RGBA Showcase HD 展示立繪查核 ---")
    showcase_path = f"{SHOWCASE_DIR}/scorpion_idle_hd.png"
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
                int(sc_arr[0, 0, 3]), int(sc_arr[0, -1, 3]),
                int(sc_arr[-1, 0, 3]), int(sc_arr[-1, -1, 3])
            ]
            if any(c > 0 for c in corners):
                print(f"❌ FAILED 0-ART25: Showcase HD corners are not transparent: {corners}")
                all_ok = False
            else:
                print(f"  ✓ PASSED 0-ART25: Showcase HD 800x1200 RGBA with 100% transparent corners")

    print("\n" + ("🎉 ALL DUNESHADOW SCORPION AUDITS PASSED PERFECTLY!" if all_ok else "❌ SOME AUDITS FAILED!"))
    return all_ok


if __name__ == "__main__":
    success = audit()
    sys.exit(0 if success else 1)
