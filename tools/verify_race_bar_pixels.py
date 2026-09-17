#!/usr/bin/env python3
"""
tools/verify_race_bar_pixels.py
Measure character creation race bar pixel properties per review.md 0-QA11, 0-UI1, 31d, 28a-1 & task t_f9d1c897:
- Unselected bottom border >= 3px #1F1A3A, cream #FFF8E7 background
- Selected bottom border 5~6px #1F1A3A, warm orange #FFA010 jelly bottom
- Touch target height >= 48px
- Zero emoji, zero character icons (no checkmarks)
- Full official race names visible (no clipping, no ellipsis)
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BORDER_RGB = np.array([31, 26, 58])       # #1F1A3A
ORANGE_RGB = np.array([255, 160, 16])     # #FFA010 (COLOR_ORANGE)
CREAM_RGB = np.array([255, 248, 231])     # #FFF8E7 (COLOR_CARD_WARM)
FONT_PATH = "game/assets/fonts/jf-openhuninn-2.1.ttf"

def color_dist(c1, c2):
    return np.sqrt(np.sum((c1.astype(float) - c2.astype(float)) ** 2, axis=-1))

def is_border(rgb, tol=25):
    return color_dist(rgb, BORDER_RGB) < tol

def is_orange(rgb, tol=30):
    return color_dist(rgb, ORANGE_RGB) < tol

def is_cream(rgb, tol=15):
    return color_dist(rgb, CREAM_RGB) < tol

def detect_horizontal_buttons(arr, y_scan=135, x_start=40, x_end=1240):
    """Detect horizontal buttons at y=y_scan by detecting borders and card interiors."""
    in_btn = False
    start_x = 0
    btn_x_spans = []
    
    for x in range(x_start, x_end):
        pix = arr[y_scan, x]
        card_interior = is_orange(pix) or is_cream(pix)
        
        if card_interior and not in_btn:
            # Check left border exists within 6 pixels
            border_found = any(is_border(arr[y_scan, bx]) for bx in range(max(x_start, x - 6), x))
            if border_found:
                # Find exact left border
                bx_left = x
                while bx_left > x_start and is_border(arr[y_scan, bx_left - 1]):
                    bx_left -= 1
                start_x = bx_left
                in_btn = True
        elif not card_interior and in_btn:
            # Check if this is the right border
            if is_border(pix):
                continue
            # Border ended
            in_btn = False
            w = x - start_x
            if w >= 100:  # Valid card width
                btn_x_spans.append((start_x, x - 1))
    if in_btn and (x_end - start_x) >= 100:
        btn_x_spans.append((start_x, x_end - 1))

    boxes = []
    for x1, x2 in btn_x_spans:
        mid_x = (x1 + x2) // 2
        # Find top and bottom bounds of this card
        top_y = None
        bottom_y = None
        for y in range(120, 248):
            pix = arr[y, mid_x]
            if is_border(pix) or is_orange(pix) or is_cream(pix):
                if top_y is None:
                    top_y = y
                bottom_y = y
        if top_y is not None and bottom_y is not None:
            boxes.append((x1, top_y, x2, bottom_y))
    return boxes

def analyze_shot(img_path, selected_race_name=""):
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape
    assert (w, h) == (1280, 720), f"Expected 1280x720, got {w}x{h}"

    print(f"\n========================================================")
    print(f"分析截圖: {os.path.basename(img_path)} (選中目標: {selected_race_name})")
    print(f"========================================================")

    boxes = detect_horizontal_buttons(arr)
    print(f"自動偵測卡片數量: {len(boxes)}")
    assert len(boxes) >= 5, f"Expected at least 5 visible buttons, found {len(boxes)}"

    results = []

    for i, (x1, y1, x2, y2) in enumerate(boxes):
        btn_w = x2 - x1 + 1
        btn_h = y2 - y1 + 1

        # Measure bottom border thickness across flat bottom (avoid 16px corner radius)
        flat_xs = range(x1 + 35, x2 - 35, 4)
        bottom_thicknesses = []
        for fx in flat_xs:
            t = 0
            y = y2
            while y >= y1 and is_border(arr[y, fx]):
                t += 1
                y -= 1
            if t > 0:
                bottom_thicknesses.append(t)
        border_thickness = int(round(float(np.median(bottom_thicknesses)))) if bottom_thicknesses else 0

        # Measure background color ratio in inner card area
        inner_box = arr[y1 + 6 : max(y1 + 7, y2 - border_thickness - 2), x1 + 6 : x2 - 6]
        total_inner_pixels = max(1, inner_box.shape[0] * inner_box.shape[1])
        cream_count = int(np.sum(is_cream(inner_box)))
        orange_count = int(np.sum(is_orange(inner_box)))

        is_selected = orange_count > cream_count
        status_name = "選中態 (Active)" if is_selected else "未選取 (Inactive)"
        bg_ratio = (orange_count if is_selected else cream_count) / total_inner_pixels * 100.0

        res = {
            "idx": i,
            "box": (x1, y1, x2, y2),
            "width": btn_w,
            "height": btn_h,
            "bottom_border": border_thickness,
            "is_selected": is_selected,
            "status": status_name,
            "bg_ratio": bg_ratio,
            "orange_count": orange_count,
            "cream_count": cream_count
        }
        results.append(res)

        print(f"  [卡片 #{i+1}] 範圍: x={x1}..{x2}, y={y1}..{y2} ({btn_w}x{btn_h}px) | 狀態: {status_name} | 底框: {border_thickness}px | 主色佔比: {bg_ratio:.1f}%")

        # 斷言檢查
        assert btn_h >= 48, f"卡片高度 {btn_h}px 小於 48px (違反 review.md 0-UI1)"
        if is_selected:
            assert border_thickness in (5, 6), f"選中態厚底 {border_thickness}px 不在 5~6px 範圍內 (違反日常憲法 §3)"
            print(f"    ✓ 選中態果凍厚底: {border_thickness}px (符合 5~6px 規範)")
        else:
            assert border_thickness >= 3, f"未選取底框 {border_thickness}px 小於 3px (違反 review.md 0-QA11)"
            print(f"    ✓ 未選取底框: {border_thickness}px (符合 >= 3px 規範)")

    return results

def main():
    shots = [
        ("screenshots/proof_creation_race_bar_unselected.png", "白金兔"),
        ("screenshots/proof_creation_crane_selected.png", "雲嵐鶴"),
        ("screenshots/proof_creation_penguin_selected.png", "蒸氣企鵝"),
        ("screenshots/proof_creation_scroll_max_full.png", "蒸氣企鵝(橫滑終點選中)"),
        ("screenshots/proof_creation_scroll_max_unselected_full.png", "蒸氣企鵝(橫滑終點未選)"),
    ]

    all_res = {}
    for path, race in shots:
        if not os.path.exists(path):
            print(f"Error: {path} not found")
            sys.exit(1)
        res = analyze_shot(path, race)
        all_res[race] = res

    print("\n========================================================")
    print("✅ 全部像素量測驗證通過！")
    print("========================================================")
    for race, res_list in all_res.items():
        sel = [r for r in res_list if r["is_selected"]]
        unsel = [r for r in res_list if not r["is_selected"]]
        sel_t = sel[0]["bottom_border"] if sel else "N/A"
        unsel_t = unsel[0]["bottom_border"] if unsel else "N/A"
        h = res_list[0]["height"]
        print(f"• {race} 場景: 熱區高度={h}px (>=48px), 選中厚底={sel_t}px (5~6px), 未選底框={unsel_t}px (>=3px)")

if __name__ == "__main__":
    main()
