#!/usr/bin/env python3
"""
verify_elephant_second_costume_review.py
Systematic audit script against review.md 0-ART5, 0-ART9, 0-ART11, 0-ART12, 0-ART18, Rule 4c, and CANON standards
for The Colossus Elephant (鋼岳象 - 第十一族) paperdoll expansion.
"""

import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
ELEPHANT_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/elephant"

def audit():
    print("=== 開始鋼岳象第二套外裝與塗裝變體【總監級自檢覆驗】(review.md 0-ART5 / 0-ART9 / 0-ART11 / 0-ART12 / Rule 4c) ===")
    all_pass = True

    # ─────────────────────────────────────────────────────────────
    # 1. 0-ART9 門檻 1: 武器數量與素體雙持防護嚴查
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 1] 0-ART9 武器數量與素體雙持防護嚴查 ---")
    chassis_brass = Image.open(f"{ELEPHANT_PD}/chassis/paint_elephant_brass.png").convert("RGBA")
    chassis_tungsten = Image.open(f"{ELEPHANT_PD}/chassis/paint_tungsten_iron.png").convert("RGBA")
    c_brass_arr = np.array(chassis_brass)
    c_tungsten_arr = np.array(chassis_tungsten)

    # 檢查武器槽
    wpn_im = Image.open(f"{ELEPHANT_PD}/weapon/wpn_colossus_cleaver_axe.png").convert("RGBA")
    w_arr = np.array(wpn_im)
    w_alpha = w_arr[:, :, 3] > 8

    # 鋼岳象武器為巨輪開山重斧，右手單持在右側 (x >= 80)
    w_axe = w_alpha[35:105, 80:128]
    w_px = int(np.sum(w_axe))
    print(f"  • 單持巨輪開山重斧不透明像素數: {w_px} px (規範: > 300 px)")

    # 檢查左手側(副手側)武器層是否有殘留武器
    l_area = w_alpha[40:85, 10:60]
    l_px = int(np.sum(l_area))
    print(f"  • 副手側(左側)武器層殘留像素數: {l_px} px (規範: 0 px，不得有多餘武器)")

    # 檢查底盤在武器區是否有畫死武器
    w_blade_zone = c_tungsten_arr[35:80, 90:125, 3] > 8
    wbz_px = int(np.sum(w_blade_zone))
    print(f"  • 鎢鋼底盤在武器刃區 (x:90..125, y:35..80) 殘留像素數: {wbz_px} px (規範: 0 px)")

    if w_px > 300 and l_px == 0 and wbz_px == 0:
        print("  ✓ [通過] 武器層僅有單持 1 把重斧，底盤無武器畫死，零多餘武器！")
    else:
        print("  ❌ [不合格] 武器數量或底盤畫死檢驗失敗！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 2. 0-ART12 門檻 2: 畫布邊界硬切檢驗
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 2] 0-ART12 畫布邊界硬切檢驗 ---")
    plate_im = Image.open(f"{ELEPHANT_PD}/costume/costume_colossus_bastion_plate.png").convert("RGBA")
    r_arr = np.array(plate_im)

    top_edge = int(np.sum(r_arr[0, :, 3] > 8))
    bottom_edge = int(np.sum(r_arr[127, :, 3] > 8))
    left_edge = int(np.sum(r_arr[:, 0, 3] > 8))
    right_edge = int(np.sum(r_arr[:, 127, 3] > 8))

    bbox = plate_im.getbbox() or (0, 0, 0, 0)
    print(f"  • 外裝 bbox: {bbox} (畫布 128x128)")
    print(f"  • 四周貼邊像素數: top={top_edge}, bottom={bottom_edge}, left={left_edge}, right={right_edge}")

    if top_edge == 0 and bottom_edge == 0 and left_edge == 0 and right_edge == 0 and bbox[2] <= 125 and bbox[0] >= 3:
        print("  ✓ [通過] 外裝四周留有安全邊距，完全零貼邊硬切、無截斷！")
    else:
        print("  ❌ [不合格] 外裝貼齊或超出邊界！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 3. Rule 4c 門檻 3: 圖層獨立性（外裝與素體 0 重複像素）
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 3] Rule 4c 圖層獨立性檢驗 ---")
    dup_brass = int(np.sum((r_arr[:,:,3] > 20) & (c_brass_arr[:,:,3] > 20) & np.all(r_arr == c_brass_arr, axis=-1)))
    dup_tungsten = int(np.sum((r_arr[:,:,3] > 20) & (c_tungsten_arr[:,:,3] > 20) & np.all(r_arr == c_tungsten_arr, axis=-1)))

    print(f"  • 鋼岳要塞重裝戰鎧 vs 原廠巨輪工坊黃銅原金 重複像素: {dup_brass} px (規範: 0)")
    print(f"  • 鋼岳要塞重裝戰鎧 vs 高爐鎢鋼淬火黑 重複像素: {dup_tungsten} px (規範: 0)")

    if dup_brass == 0 and dup_tungsten == 0:
        print("  ✓ [通過] 100% 獨立外裝圖層，零素體像素複製！")
    else:
        print("  ❌ [不合格] 存在重複像素！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 4. 門檻 4: 變體可讀性與辨識度（顯著差異）
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 4] 視覺對比度與辨識度驗收 ---")
    diff_chassis = np.sum(np.abs(c_brass_arr.astype(int) - c_tungsten_arr.astype(int)) > 30)
    print(f"  • 黃銅原金塗裝 vs 鎢鋼淬火黑塗裝 顯著差異像素數: {diff_chassis} px (規範: > 500 px)")

    costume_overalls = Image.open(f"{ELEPHANT_PD}/costume/costume_cog_workshop_overalls.png").convert("RGBA")
    co_arr = np.array(costume_overalls)
    diff_costume = np.sum(np.abs(r_arr.astype(int) - co_arr.astype(int)) > 30)
    print(f"  • 巨輪工坊厚鋼工裝 vs 鋼岳要塞重裝戰鎧 顯著差異像素數: {diff_costume} px (規範: > 500 px)")

    if diff_chassis > 500 and diff_costume > 500:
        print("  ✓ [通過] 兩套外裝與兩套塗裝在色系、輪廓與材質表現上有極明顯辨識差異！")
    else:
        print("  ❌ [不合格] 變體差異不足！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 5. 門檻 5: 0-ART5 切片 c100 色彩階數與逐像素手繪厚塗審查
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 5] 0-ART5 切片 c100 逐像素手繪厚塗檢驗 ---")
    opaque_r = int(np.sum(r_arr[:, :, 3] > 0))
    colors_r = len(set(tuple(p) for p in r_arr.reshape(-1, 4) if p[3] > 0))
    c100_r = (colors_r / opaque_r * 100) if opaque_r > 0 else 0
    print(f"  • 鋼岳要塞重裝戰鎧 c100: {c100_r:.2f}% (opaque={opaque_r}, colors={colors_r}, 規範: >= 10.0%)")

    opaque_t = int(np.sum(c_tungsten_arr[:, :, 3] > 0))
    colors_t = len(set(tuple(p) for p in c_tungsten_arr.reshape(-1, 4) if p[3] > 0))
    c100_t = (colors_t / opaque_t * 100) if opaque_t > 0 else 0
    print(f"  • 高爐鎢鋼淬火黑 c100: {c100_t:.2f}% (opaque={opaque_t}, colors={colors_t}, 規範: >= 10.0%)")

    if c100_r >= 10.0 and c100_t >= 10.0:
        print("  ✓ [通過] 0-ART5 檢驗合格，非純色平塗占位圖，具備手繪厚塗多階明暗與微雜色！")
    else:
        print("  ❌ [不合格] 色彩階數不足！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 6. 門檻 6: 0-ART27 核心與外裝中心鏤空檢驗（發條之心晶石無遮擋）
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 6] 0-ART27 核心寶石與外裝胸口鏤空檢驗 ---")
    core_im = Image.open(f"{ELEPHANT_PD}/optic_core/core_sky_quartz.png").convert("RGBA")
    core_arr = np.array(core_im)
    # 胸口薄荷綠晶石位置 centered around (63, 70)
    heart_gem_px = int(np.sum(core_arr[65:75, 59:67, 3] > 30))
    costume_overlap_px = int(np.sum(r_arr[66:74, 60:66, 3] > 30))
    print(f"  • 胸口發條之心晶石有效像素: {heart_gem_px} px")
    print(f"  • 新外裝在發條之心核心區遮擋像素: {costume_overlap_px} px (規範: 0 px，必須完全鏤空露出)")

    if heart_gem_px > 20 and costume_overlap_px == 0:
        print("  ✓ [通過] 新外裝胸口完美鏤空，發條之心晶石 100% 毫無遮擋！")
    else:
        print("  ❌ [不合格] 新外裝遮擋胸口發條之心晶石！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 7. 門檻 7: 512 高清切片規格與檔案存在檢驗
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 7] 512 高清切片尺寸與規格檢驗 ---")
    plate_512 = Image.open(f"{ELEPHANT_PD}/costume/costume_colossus_bastion_plate_512.png")
    tungsten_512 = Image.open(f"{ELEPHANT_PD}/chassis/paint_tungsten_iron_512.png")
    print(f"  • costume_colossus_bastion_plate_512 尺寸: {plate_512.size}")
    print(f"  • paint_tungsten_iron_512 尺寸: {tungsten_512.size}")

    if plate_512.size == (512, 512) and tungsten_512.size == (512, 512):
        print("  ✓ [通過] 512 高清切片尺寸精確為 512x512！")
    else:
        print("  ❌ [不合格] 512 切片尺寸錯誤！")
        all_pass = False

    print("\n=======================================================")
    if all_pass:
        print("🎉 [ALL PASS] 鋼岳象第二套外裝與塗裝變體通過所有總監級檢驗門檻！")
        return 0
    else:
        print("❌ [FAIL] 有檢驗項目未通過！")
        return 1

if __name__ == "__main__":
    exit(audit())
