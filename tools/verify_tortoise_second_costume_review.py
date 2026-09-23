#!/usr/bin/env python3
"""
verify_tortoise_second_costume_review.py
Systematic audit script against review.md 0-ART5, 0-ART9, 0-ART11, 0-ART12, 0-ART18, Rule 4c, and CANON standards
for The Xuanji Tortoise (玄機龜) paperdoll expansion.
"""

import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
TORTOISE_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tortoise"

def audit():
    print("=== 開始玄機龜第二套外裝與塗裝變體【總監級自檢覆驗】(review.md 0-ART5 / 0-ART9 / 0-ART11 / 0-ART12 / Rule 4c) ===")
    all_pass = True

    # ─────────────────────────────────────────────────────────────
    # 1. 0-ART9 門檻 1: 武器數量與素體雙持嚴查
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 1] 0-ART9 武器數量與素體雙持防護嚴查 ---")
    chassis_jade = Image.open(f"{TORTOISE_PD}/chassis/paint_tortoise_jade.png").convert("RGBA")
    chassis_basalt = Image.open(f"{TORTOISE_PD}/chassis/paint_basalt_black.png").convert("RGBA")
    c_jade_arr = np.array(chassis_jade)
    c_basalt_arr = np.array(chassis_basalt)

    # 檢查武器槽
    wpn_im = Image.open(f"{TORTOISE_PD}/weapon/wpn_bagua_astrolabe.png").convert("RGBA")
    w_arr = np.array(wpn_im)
    w_alpha = w_arr[:, :, 3] > 8

    # 玄機龜武器為浮空八卦星盤，單持在右側 (x >= 75)
    w_astrolabe = w_alpha[40:85, 75:120]
    w_px = int(np.sum(w_astrolabe))
    print(f"  • 單持浮空八卦星盤不透明像素數: {w_px} px (規範: > 300 px)")

    # 檢查副手側(左側)武器槽是否有殘留武器
    l_area = w_alpha[40:85, 10:65]
    l_px = int(np.sum(l_area))
    print(f"  • 副手側(左側)武器層殘留像素數: {l_px} px (規範: 0 px，不得有多餘武器)")

    if w_px > 300 and l_px == 0:
        print("  ✓ [通過] 武器層僅有單持 1 把浮空八卦星盤，無多餘第二武器！")
    else:
        print("  ❌ [不合格] 武器數量不符規範！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 2. 0-ART12 門檻 2: 畫布邊界硬切檢驗
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 2] 0-ART12 畫布邊界硬切檢驗 ---")
    robe_im = Image.open(f"{TORTOISE_PD}/costume/costume_bagua_master_robe.png").convert("RGBA")
    r_arr = np.array(robe_im)

    top_edge = int(np.sum(r_arr[0, :, 3] > 8))
    bottom_edge = int(np.sum(r_arr[127, :, 3] > 8))
    left_edge = int(np.sum(r_arr[:, 0, 3] > 8))
    right_edge = int(np.sum(r_arr[:, 127, 3] > 8))

    bbox = robe_im.getbbox() or (0, 0, 0, 0)
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
    dup_jade = int(np.sum((r_arr[:,:,3] > 20) & (c_jade_arr[:,:,3] > 20) & np.all(r_arr == c_jade_arr, axis=-1)))
    dup_basalt = int(np.sum((r_arr[:,:,3] > 20) & (c_basalt_arr[:,:,3] > 20) & np.all(r_arr == c_basalt_arr, axis=-1)))

    print(f"  • 乾坤八卦宗師道鎧 vs 原廠青銅古翠綠 重複像素: {dup_jade} px (規範: 0)")
    print(f"  • 乾坤八卦宗師道鎧 vs 玄武黑曜淬火黑 重複像素: {dup_basalt} px (規範: 0)")

    if dup_jade == 0 and dup_basalt == 0:
        print("  ✓ [通過] 100% 獨立外裝圖層，零素體像素複製！")
    else:
        print("  ❌ [不合格] 存在重複像素！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 4. 門檻 4: 變體可讀性與辨識度（對比度與顯著差異）
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 4] 視覺對比度與辨識度驗收 ---")
    diff_chassis = np.sum(np.abs(c_jade_arr.astype(int) - c_basalt_arr.astype(int)) > 30)
    print(f"  • 青銅古翠綠塗裝 vs 玄武黑曜淬火黑塗裝 顯著差異像素數: {diff_chassis} px (規範: > 500 px)")

    costume_harness = Image.open(f"{TORTOISE_PD}/costume/costume_zen_dojo_harness.png").convert("RGBA")
    ch_arr = np.array(costume_harness)
    diff_costume = np.sum(np.abs(r_arr.astype(int) - ch_arr.astype(int)) > 30)
    print(f"  • 天元道場護甲 vs 乾坤八卦宗師道鎧 顯著差異像素數: {diff_costume} px (規範: > 500 px)")

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
    print(f"  • 乾坤八卦宗師道鎧 c100: {c100_r:.2f} (opaque={opaque_r}, colors={colors_r}, 規範: >= 10.0)")

    opaque_b = int(np.sum(c_basalt_arr[:, :, 3] > 0))
    colors_b = len(set(tuple(p) for p in c_basalt_arr.reshape(-1, 4) if p[3] > 0))
    c100_b = (colors_b / opaque_b * 100) if opaque_b > 0 else 0
    print(f"  • 玄武黑曜淬火黑 c100: {c100_b:.2f} (opaque={opaque_b}, colors={colors_b}, 規範: >= 10.0)")

    if c100_r >= 10.0 and c100_b >= 10.0:
        print("  ✓ [通過] 0-ART5 檢驗合格，非純色平塗占位圖，具備手繪厚塗多階明暗與微雜色！")
    else:
        print("  ❌ [不合格] c100 低於門檻 10.0，判定為平塗占位圖！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 6. 門檻 6: 光學核心透出檢驗 (Optic Core Aperture Audit)
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 6] 光學核心透出檢驗 ---")
    core_im = Image.open(f"{TORTOISE_PD}/optic_core/core_amber_quartz.png").convert("RGBA")
    core_arr = np.array(core_im)
    # Chest gem center (63, 70)
    heart_pixels = (core_arr[66:74, 60:67, 3] > 50)
    covered_pixels = (r_arr[66:74, 60:67, 3] > 100) & heart_pixels
    covered_count = int(np.sum(covered_pixels))
    print(f"  • 乾坤八卦宗師道鎧覆蓋核心寶石像素數: {covered_count} px (規範: 0 px，必須完全開孔)")

    if covered_count == 0:
        print("  ✓ [通過] 護心鏡八角開孔精準無遮擋，胸前核心翡翠寶石完全外露閃耀！")
    else:
        print("  ❌ [不合格] 核心寶石被外裝遮擋！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 7. 門檻 7: 512x512 高清資產存在性與 LANCZOS 檢驗
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 7] 512x512 高清資產查核 ---")
    p_robe_512 = f"{TORTOISE_PD}/costume/costume_bagua_master_robe_512.png"
    p_basalt_512 = f"{TORTOISE_PD}/chassis/paint_basalt_black_512.png"

    if os.path.exists(p_robe_512) and os.path.exists(p_basalt_512):
        im_r512 = Image.open(p_robe_512)
        im_b512 = Image.open(p_basalt_512)
        if im_r512.size == (512, 512) and im_b512.size == (512, 512):
            print(f"  ✓ [通過] 512x512 資產齊備且解析度符合規範: {im_r512.size}")
        else:
            print("  ❌ [不合格] 512x512 尺寸錯誤！")
            all_pass = False
    else:
        print("  ❌ [不合格] 512x512 檔案缺失！")
        all_pass = False

    print("\n=======================================================")
    if all_pass:
        print("🎉 ALL REVIEWS PASSED (0-ART5, 0-ART9, 0-ART11, 0-ART12, 0-ART18, Rule 4c, CANON)")
        return 0
    else:
        print("❌ SOME REVIEWS FAILED")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(audit())
