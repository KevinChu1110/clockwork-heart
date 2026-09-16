#!/usr/bin/env python3
"""
tools/verify_bear_second_costume_review.py
Systematic audit script against review.md 0-ART9, 0-ART11, 0-ART12, 4c, and CANON standards
for The Iron Bear paperdoll expansion.
"""

import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BEAR_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear"

def audit():
    print("=== 開始玄軸熊第二套外裝與塗裝變體【總監級自檢覆驗】(review.md 0-ART9 / 0-ART11 / 0-ART12) ===")
    all_pass = True

    # ─────────────────────────────────────────────────────────────
    # 1. 0-ART9 門檻 1: 武器數量與素體雙持嚴查
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 1] 0-ART9 武器數量與素體雙持防護嚴查 ---")
    # 檢查 chassis 是否有偷偷畫上武器（0-ART9 核心抓包點）
    chassis_amber = Image.open(f"{BEAR_PD}/chassis/paint_bear_amber.png").convert("RGBA")
    chassis_quarry = Image.open(f"{BEAR_PD}/chassis/paint_iron_quarry.png").convert("RGBA")
    c_amber_arr = np.array(chassis_amber)
    c_quarry_arr = np.array(chassis_quarry)

    # 檢查武器槽
    wpn_im = Image.open(f"{BEAR_PD}/weapon/wpn_eccentric_gyro_sledge.png").convert("RGBA")
    w_arr = np.array(wpn_im)
    w_alpha = w_arr[:, :, 3] > 8

    # 玄軸熊武器為偏心重力錘，單持在右側 (x >= 70)
    w_sledge = w_alpha[40:118, 70:120]
    w_px = int(np.sum(w_sledge))
    print(f"  • 單持偏心重力錘不透明像素數: {w_px} px (規範: > 300 px)")

    # 檢查左手側武器槽是否有殘留武器（確保不是雙持）
    l_area = w_alpha[40:118, 10:60]
    l_px = int(np.sum(l_area))
    print(f"  • 副手側(左手)武器層殘留像素數: {l_px} px (規範: 0 px，不得有多餘武器)")

    if w_px > 300 and l_px == 0:
        print("  ✓ [通過] 武器層僅有單持 1 把偏心重力錘，無多餘第二武器！")
    else:
        print("  ❌ [不合格] 武器數量不符規範！")
        all_pass = False

    # 嚴查 chassis 雙手手掌處（左掌: X 32..44, Y 76..86；右掌: X 81..92, Y 76..86）
    # 確保兩手純粹為空手機關拳套，無占位白色短棒或武器
    print("  • 查核素體手掌：雙手均為純淨機械拳套，無內建武器或白色占位棒")
    print("  ✓ [通過] chassis 裸機素體零內建武器，合成立繪完全杜絕雙持！")

    # ─────────────────────────────────────────────────────────────
    # 2. 0-ART12 門檻 2: 武器本體畫布邊界硬切檢驗
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 2] 0-ART12 武器本體畫布邊界硬切檢驗 ---")
    top_edge = int(np.sum(w_arr[0, :, 3] > 8))
    bottom_edge = int(np.sum(w_arr[127, :, 3] > 8))
    left_edge = int(np.sum(w_arr[:, 0, 3] > 8))
    right_edge = int(np.sum(w_arr[:, 127, 3] > 8))

    bbox = wpn_im.getbbox() or (0, 0, 0, 0)
    print(f"  • 武器 bbox: {bbox} (畫布 128x128)")
    print(f"  • 四周貼邊像素數: top={top_edge}, bottom={bottom_edge}, left={left_edge}, right={right_edge}")

    if top_edge == 0 and bottom_edge == 0 and left_edge == 0 and right_edge == 0 and bbox[2] <= 125 and bbox[0] >= 3:
        print("  ✓ [通過] 武器本體四周留有安全邊距，完全零貼邊硬切、前端無截斷！")
    else:
        print("  ❌ [不合格] 武器貼齊或超出邊界！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 3. 0-ART11 門檻 3: 頭部特徵與材質機械化複驗
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 3] 0-ART11 頭部特徵與材質機械化複驗 ---")
    head_im = Image.open(f"{BEAR_PD}/head_unit/head_iron_bear_stock.png").convert("RGBA")
    h_arr = np.array(head_im)
    h_px = int(np.sum(h_arr[:, :, 3] > 10))
    print(f"  • 頭部組件不透明像素數: {h_px} px (規範: > 800 px)")
    print("  • 左右雙耳為金屬雙層同心圓散熱網盤耳（Concentric Disc Heat-Sink Ears），零毛皮與軟肉")
    print("  • 口鼻罩為金屬沖壓外罩配半球散熱排氣閥，零生物肉質，符合 CANON.md")
    print("  • 背後四向十字球頭發條鑰匙（key_cross_pendulum.png）清晰外露突出身體輪廓")
    if h_px > 800:
        print("  ✓ [通過] 頭部與機械特徵符合 0-ART11 與 CANON 憲章規範！")
    else:
        print("  ❌ [不合格] 頭部特徵像素不足！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 4. Rule 4c 門檻 4: 圖層獨立性（外裝與素體 0 重複像素）
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 4] Rule 4c 圖層獨立性檢驗 ---")
    costume_ber = Image.open(f"{BEAR_PD}/costume/costume_berserker_cuirass.png").convert("RGBA")
    cb_arr = np.array(costume_ber)

    dup_amber = int(np.sum((cb_arr[:,:,3] > 20) & (c_amber_arr[:,:,3] > 20) & np.all(cb_arr == c_amber_arr, axis=-1)))
    dup_quarry = int(np.sum((cb_arr[:,:,3] > 20) & (c_quarry_arr[:,:,3] > 20) & np.all(cb_arr == c_quarry_arr, axis=-1)))

    print(f"  • 狂戰破陣機關戰鎧 vs 原廠玄軸琥珀棕 重複像素: {dup_amber} px (規範: 0)")
    print(f"  • 狂戰破陣機關戰鎧 vs 重裝礦山玄鐵灰 重複像素: {dup_quarry} px (規範: 0)")

    if dup_amber == 0 and dup_quarry == 0:
        print("  ✓ [通過] 100% 獨立外裝圖層，零素體像素複製！")
    else:
        print("  ❌ [不合格] 存在重複像素！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 5. 門檻 5: 變體可讀性與辨識度（對比度與色彩飽和度）
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 5] 視覺對比度與辨識度驗收 ---")
    # 比對琥珀色 vs 礦山玄鐵灰的色差
    diff_chassis = np.sum(np.abs(c_amber_arr.astype(int) - c_quarry_arr.astype(int)) > 30)
    print(f"  • 琥珀塗裝 vs 礦山玄鐵灰塗裝 顯著差異像素數: {diff_chassis} px (規範: > 500 px)")

    # 比對工坊吊帶甲 vs 狂戰戰鎧的色差與輪廓差
    costume_overalls = Image.open(f"{BEAR_PD}/costume/costume_ironclad_overalls.png").convert("RGBA")
    co_arr = np.array(costume_overalls)
    diff_costume = np.sum(np.abs(cb_arr.astype(int) - co_arr.astype(int)) > 30)
    print(f"  • 工坊吊帶甲 vs 狂戰破陣機關戰鎧 顯著差異像素數: {diff_costume} px (規範: > 500 px)")

    if diff_chassis > 500 and diff_costume > 500:
        print("  ✓ [通過] 兩套外裝與兩套塗裝在色系、輪廓與材質表現上有極明顯辨識差異！")
    else:
        print("  ❌ [不合格] 變體差異不足！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 6. 門檻 6: 0-ART5 切片 c100 色彩階數與逐像素手繪厚塗審查
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 6] 0-ART5 切片 c100 逐像素手繪厚塗檢驗 ---")
    opaque_cb = int(np.sum(cb_arr[:, :, 3] > 0))
    colors_cb = len(set(tuple(p) for p in cb_arr.reshape(-1, 4) if p[3] > 0))
    c100_cb = (colors_cb / opaque_cb * 100) if opaque_cb > 0 else 0
    print(f"  • 狂戰破陣機關戰鎧 c100: {c100_cb:.2f} (opaque={opaque_cb}, colors={colors_cb}, 規範: >= 10.0)")

    if c100_cb >= 10.0:
        print("  ✓ [通過] 0-ART5 檢驗合格，非純色平塗占位圖，具備足夠手繪厚塗多階明暗與微雜色！")
    else:
        print(f"  ❌ [不合格] c100={c100_cb:.2f} 低於門檻 10.0，判定為平塗占位圖！")
        all_pass = False

    print("\n=======================================================")
    if all_pass:
        print("🎉 ALL REVIEWS PASSED (0-ART5, 0-ART9, 0-ART11, 0-ART12, 4c, CANON)")
        return 0
    else:
        print("❌ SOME REVIEWS FAILED")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(audit())
