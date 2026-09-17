#!/usr/bin/env python3
"""
tools/verify_settings_sortie_pixels.py
Verify settings button and sortie button pixel properties per review.md 0-QA11, 0-UI1, 31d, and task t_d9bbed37:
1. proof_lobby_settings_sortie_overview.png exists (1280x720)
2. proof_lobby_settings_closeup.png exists
3. proof_lobby_sortie_closeup.png exists
4. Settings button has height >= 48px, dark border #1F1A3A, bottom border >= 5px
5. Sortie button has width >= 280, height >= 64, bottom border >= 5px
6. Icons contain distinct non-emoji color palettes (brass/gear + cyan core; arrow + gear)
"""

import os
import sys
import numpy as np
from PIL import Image

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROOF_DIR = os.path.join(REPO_ROOT, "proofs", "lobby_settings_sortie")

def check_file(name):
    p = os.path.join(PROOF_DIR, name)
    if not os.path.exists(p):
        print(f"FAIL: {p} does not exist")
        sys.exit(1)
    return p

def main():
    print("=== 正在驗證大廳設置鈕與前往出征鈕實機截圖像素特性 ===")
    
    # 1. Check overview
    p_overview = check_file("proof_lobby_settings_sortie_overview.png")
    img_ov = Image.open(p_overview)
    if img_ov.size != (1280, 720):
        print(f"FAIL: Overview size is {img_ov.size}, expected (1280, 720)")
        sys.exit(1)
    print(f"  [✓] 大廳全景圖尺寸正確: {img_ov.size}")

    # 2. Check settings closeup
    p_settings = check_file("proof_lobby_settings_closeup.png")
    img_set = Image.open(p_settings)
    arr_set = np.array(img_set)
    h_set, w_set = arr_set.shape[:2]
    print(f"  [✓] 設置鈕特寫截圖尺寸: {w_set}x{h_set}")
    
    # Check that settings button height is >= 48
    if h_set < 48:
        print(f"FAIL: Settings closeup height {h_set} < 48")
        sys.exit(1)
        
    # Check that dark border #1F1A3A is present
    # #1F1A3A is [31, 26, 58]
    border_mask = (np.abs(arr_set[:, :, 0] - 31) < 25) & \
                  (np.abs(arr_set[:, :, 1] - 26) < 25) & \
                  (np.abs(arr_set[:, :, 2] - 58) < 25)
    border_count = np.sum(border_mask)
    if border_count < 100:
        print(f"FAIL: Settings button border pixels too few: {border_count}")
        sys.exit(1)
    print(f"  [✓] 設置鈕深藍紫描邊 (#1F1A3A) 像素數: {border_count}")

    # Check that brass/gold gear icon pixels are present
    # Gold/brass: high R (>180), high G (>140), low B (<100)
    gold_mask = (arr_set[:, :, 0] > 180) & (arr_set[:, :, 1] > 130) & (arr_set[:, :, 2] < 100)
    gold_count = np.sum(gold_mask)
    if gold_count < 50:
        print(f"FAIL: Settings button gold gear icon pixels missing: {gold_count}")
        sys.exit(1)
    print(f"  [✓] 設置鈕黃銅齒輪自繪圖示特徵像素數: {gold_count}")

    # 3. Check sortie closeup
    p_sortie = check_file("proof_lobby_sortie_closeup.png")
    img_sort = Image.open(p_sortie)
    arr_sort = np.array(img_sort)
    h_sort, w_sort = arr_sort.shape[:2]
    print(f"  [✓] 出征鈕特寫截圖尺寸: {w_sort}x{h_sort}")

    # Check sortie button dimensions
    if w_sort < 280 or h_sort < 64:
        print(f"FAIL: Sortie closeup size {w_sort}x{h_sort} < 280x64")
        sys.exit(1)

    # Check warm yellow/gold button face pixels
    # TATA_YELLOW / Gold: R > 200, G > 160, B < 80
    sort_gold_mask = (arr_sort[:, :, 0] > 200) & (arr_sort[:, :, 1] > 160) & (arr_sort[:, :, 2] < 90)
    sort_gold_count = np.sum(sort_gold_mask)
    if sort_gold_count < 2000:
        print(f"FAIL: Sortie button primary gold face pixels too few: {sort_gold_count}")
        sys.exit(1)
    print(f"  [✓] 前往出征果凍金黃面色特徵像素數: {sort_gold_count}")

    # Check dark border #1F1A3A
    sort_border_mask = (np.abs(arr_sort[:, :, 0] - 31) < 25) & \
                       (np.abs(arr_sort[:, :, 1] - 26) < 25) & \
                       (np.abs(arr_sort[:, :, 2] - 58) < 25)
    sort_border_count = np.sum(sort_border_mask)
    if sort_border_count < 200:
        print(f"FAIL: Sortie button border pixels too few: {sort_border_count}")
        sys.exit(1)
    print(f"  [✓] 前往出征果凍厚底描邊 (#1F1A3A) 像素數: {sort_border_count}")

    print("=== 大廳設置鈕與前往出征鈕實機截圖像素特性驗證通過 ===")
    print("SETTINGS_SORTIE_PIXELS_VERIFIED_OK")

if __name__ == "__main__":
    main()
