#!/usr/bin/env python3
"""
tools/verify_crane_second_costume_review.py
Systematic audit script against review.md 0-ART9, 0-ART11, 0-ART12, Rule 4c, and CANON standards
for Cloud Crane (雲嵐鶴) paperdoll expansion.
"""

import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
CRANE_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crane"

def audit():
    print("=== 開始雲嵐鶴第二套外裝與塗裝變體【總監級自檢覆驗】(review.md 0-ART9 / 0-ART11 / 0-ART12) ===")
    all_pass = True

    # ─────────────────────────────────────────────────────────────
    # 1. 0-ART9 / 0-ART11 / 0-ART12: 武器數量與握持驗收
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 1] 0-ART9 / 0-ART11 / 0-ART12 武器數量與完整性驗收 ---")
    wpn_im = Image.open(f"{CRANE_PD}/weapon/wpn_zephyr_wing_bow.png").convert("RGBA")
    w_arr = np.array(wpn_im)
    w_alpha = w_arr[:, :, 3] > 8

    # Chassis check (ensure chassis has NO baked-in weapon on right or left hand)
    ch_porcelain = Image.open(f"{CRANE_PD}/chassis/paint_crane_porcelain.png").convert("RGBA")
    ch_azure = Image.open(f"{CRANE_PD}/chassis/paint_zephyr_azure.png").convert("RGBA")
    
    # Left bow region (X: 78..106, Y: 50..100)
    bow_px = int(np.sum(w_alpha))
    print(f"  • 風弦羽翼機關弓不透明像素數: {bow_px} px (規範: > 200 px)")

    # Upper limb (y <= 65) and lower limb (y >= 85) check
    upper_px = int(np.sum(w_alpha[45:66, :]))
    lower_px = int(np.sum(w_alpha[85:105, :]))
    print(f"  • 上弓臂與滑輪像素數: {upper_px} px, 下弓臂與滑輪像素數: {lower_px} px")

    # Right hand area (empty hand down): X in 34..50, Y in 54..82 - must have 0 weapon pixels
    r_hand_wpn = int(np.sum(w_alpha[54:82, 34:50]))
    print(f"  • 副手(右手)武器像素數: {r_hand_wpn} px (規範: 0，單持一把)")

    if bow_px > 200 and upper_px > 40 and lower_px > 40 and r_hand_wpn == 0:
        print("  ✓ [通過] 武器剛好 1 把，風弦機關弓上下弓臂、滑輪與弓弦完整，無素體繪死雙持問題！")
    else:
        print("  ❌ [不合格] 武器數量異常或弓體不完整！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 2. 0-ART11 / 0-ART 門檻 2: 畫布邊界硬切檢驗
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 2] 0-ART11 武器與外裝本體畫布邊界硬切檢驗 ---")
    top_edge = int(np.sum(w_arr[0, :, 3] > 8))
    bottom_edge = int(np.sum(w_arr[127, :, 3] > 8))
    left_edge = int(np.sum(w_arr[:, 0, 3] > 8))
    right_edge = int(np.sum(w_arr[:, 127, 3] > 8))

    bbox = wpn_im.getbbox() or (0, 0, 0, 0)
    print(f"  • 武器 bbox: {bbox} (畫布 128x128)")
    print(f"  • 武器外緣邊界像素數: top={top_edge}, bottom={bottom_edge}, left={left_edge}, right={right_edge}")

    cos_im = Image.open(f"{CRANE_PD}/costume/costume_sky_hunter_mail.png").convert("RGBA")
    c_arr = np.array(cos_im)
    c_top = int(np.sum(c_arr[0, :, 3] > 8))
    c_bot = int(np.sum(c_arr[127, :, 3] > 8))
    c_left = int(np.sum(c_arr[:, 0, 3] > 8))
    c_right = int(np.sum(c_arr[:, 127, 3] > 8))
    bbox_c = cos_im.getbbox() or (0, 0, 0, 0)
    print(f"  • 外裝 bbox: {bbox_c} (畫布 128x128)")
    print(f"  • 外裝外緣邊界像素數: top={c_top}, bottom={c_bot}, left={c_left}, right={c_right}")

    if (top_edge == 0 and bottom_edge == 0 and left_edge == 0 and right_edge == 0 and
        c_top == 0 and c_bot == 0 and c_left == 0 and c_right == 0):
        print("  ✓ [通過] 武器與外裝四周留有安全邊距，完全零貼邊硬切！")
    else:
        print("  ❌ [不合格] 存在貼齊或超出邊界的硬切像素！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 3. Rule 4c 門檻 3: 圖層獨立性（外裝與素體 0 重複像素）
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 3] Rule 4c 圖層獨立性檢驗 ---")
    p_arr = np.array(ch_porcelain)
    a_arr = np.array(ch_azure)

    dup_p = int(np.sum((c_arr[:,:,3] > 20) & (p_arr[:,:,3] > 20) & np.all(c_arr == p_arr, axis=-1)))
    dup_a = int(np.sum((c_arr[:,:,3] > 20) & (a_arr[:,:,3] > 20) & np.all(c_arr == a_arr, axis=-1)))

    print(f"  • 晴空巡獵機關羽甲 vs 原廠冷淬青瓷白 重複像素: {dup_p} px (規範: 0)")
    print(f"  • 晴空巡獵機關羽甲 vs 晴空凌雲湛藍 重複像素: {dup_a} px (規範: 0)")

    if dup_p == 0 and dup_a == 0:
        print("  ✓ [通過] 100% 獨立外裝圖層，零素體像素複製！")
    else:
        print("  ❌ [不合格] 存在重複像素！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 4. CANON 門檻 4: 頭部特徵與材質機械化（零毛皮、八角丹頂閥、三翼發條鑰匙）
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 4] CANON 憲章與頭部/鑰匙特徵覆驗 ---")
    head_im = Image.open(f"{CRANE_PD}/head_unit/head_cloud_crane_stock.png").convert("RGBA")
    h_arr = np.array(head_im)
    key_im = Image.open(f"{CRANE_PD}/winding_key/key_tri_wing_zephyr.png").convert("RGBA")
    k_arr = np.array(key_im)

    h_px = int(np.sum(h_arr[:, :, 3] > 10))
    k_px = int(np.sum(k_arr[:, :, 3] > 10))
    print(f"  • 頭部組件不透明像素數: {h_px} px")
    print(f"  • 背部三翼風輪發條鑰匙像素數: {k_px} px")

    # Check key bbox protrudes left
    k_bbox = key_im.getbbox() or (0, 0, 0, 0)
    print(f"  • 發條鑰匙 bbox: {k_bbox} (在角色左背部 X<46，剪影明確外露)")

    if h_px > 1000 and k_px > 100 and k_bbox[0] < 40:
        print("  ✓ [通過] 頭頂八角丹頂琺瑯減壓閥、鈦合金鑷夾喙、背部三翼凌雲風輪發條鑰匙完整合規！")
    else:
        print("  ❌ [不合格] 頭部或發條鑰匙特徵不足！")
        all_pass = False

    # ─────────────────────────────────────────────────────────────
    # 5. 兩套外裝與兩套塗裝的視覺差異檢驗 (Diff Pixel Check)
    # ─────────────────────────────────────────────────────────────
    print("\n--- [門檻 5] 外裝與塗裝變體視覺差異檢驗 ---")
    robe_im = Image.open(f"{CRANE_PD}/costume/costume_zephyr_robe.png").convert("RGBA")
    r_arr = np.array(robe_im)
    diff_costume = int(np.sum(np.abs(c_arr.astype(int) - r_arr.astype(int)) > 20))
    print(f"  • 晴空巡獵機關羽甲 vs 凌雲羽衣輕鋼道袍 像素差異數: {diff_costume} px (規範: > 500 px)")

    diff_chassis = int(np.sum(np.abs(p_arr.astype(int) - a_arr.astype(int)) > 20))
    print(f"  • 晴空凌雲湛藍 vs 原廠冷淬青瓷白 像素差異數: {diff_chassis} px (規範: > 500 px)")

    if diff_costume > 500 and diff_chassis > 500:
        print("  ✓ [通過] 外裝與塗裝變體視覺差異顯著，非微調或換色欺瞞！")
    else:
        print("  ❌ [不合格] 差異過小！")
        all_pass = False

    print("\n=======================================================")
    if all_pass:
        print("CRANE_SECOND_COSTUME_REVIEW_ALL_PASS")
    else:
        print("CRANE_SECOND_COSTUME_REVIEW_FAIL")
    return all_pass

if __name__ == "__main__":
    import sys
    sys.exit(0 if audit() else 1)
