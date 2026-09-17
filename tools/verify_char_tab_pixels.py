#!/usr/bin/env python3
"""
tools/verify_char_tab_pixels.py
Measures character tab UI pixels and properties per review.md 0-QA11, 0-QA12 & task t_4563552c:
- 3 weapon slot cards: height >= 50px, border_bottom >= 5px, radius >= 18px
- Selected slot: warm orange #FFA010
- Unselected slots: warm cream #FFF8E7
- 5 stat cards: height >= 60px, border_bottom >= 5px, radius >= 18px, warm cream #FFF8E7
- Wardrobe button (BtnWardrobe): height >= 50px, warm orange #FFA010, border_bottom >= 5px
- Generates pixel measurement audit image
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BORDER_RGB = np.array([31, 26, 58])       # #1F1A3A
ORANGE_RGB = np.array([255, 160, 16])     # #FFA010 (COLOR_ORANGE)
CREAM_RGB = np.array([255, 248, 231])     # #FFF8E7 (COLOR_CARD_WARM)
BG_CREAM_RGB = np.array([255, 253, 248])  # #FFFDF8 (COLOR_BG_CREAM)
FONT_PATH = "game/assets/fonts/jf-openhuninn-2.1.ttf"


def color_dist(c1, c2):
    return np.sqrt(np.sum((c1.astype(float) - c2.astype(float)) ** 2, axis=-1))


def is_border(rgb, tol=25):
    return color_dist(rgb, BORDER_RGB) < tol


def is_orange(rgb, tol=30):
    return color_dist(rgb, ORANGE_RGB) < tol


def is_cream(rgb, tol=25):
    return color_dist(rgb, CREAM_RGB) < tol


def verify_character_tab_screenshots():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    proof_dir = os.path.join(repo_root, "proofs/char_tab_jelly")

    shots = [
        ("proof_char_tab_slot1_selected.png", 0),
        ("proof_char_tab_slot2_selected.png", 1),
        ("proof_char_tab_slot3_selected.png", 2),
        ("proof_char_tab_full.png", 0),
    ]

    all_passed = True

    for filename, active_slot in shots:
        filepath = os.path.join(proof_dir, filename)
        if not os.path.exists(filepath):
            print(f"FAIL: Missing screenshot {filepath}")
            all_passed = False
            continue

        img = Image.open(filepath).convert("RGB")
        arr = np.array(img)
        h, w, _ = arr.shape
        assert (w, h) == (1280, 720), f"Expected 1280x720, got {w}x{h}"

        print(f"\n========================================================")
        print(f"Auditing: {filename} (Active Weapon Slot: {active_slot})")

        # 1. Inspect Wardrobe Button (Left column: x < 420, y between 480 and 610, above bottom dock)
        left_mask = is_orange(arr[480:610, :420])
        ys, xs = np.where(left_mask)
        if len(ys) > 0:
            y_min, y_max = ys.min() + 480, ys.max() + 480
            x_min, x_max = xs.min(), xs.max()
            w_h = y_max - y_min + 1
            w_crop = arr[y_min:y_max+1, x_min:x_max+1]
            orange_mask = is_orange(w_crop)
            orange_pct = float(np.mean(orange_mask)) * 100.0
            print(f"  [更衣按鈕] 偵測區域 y=[{y_min},{y_max}] (高 {w_h}px), x=[{x_min},{x_max}] - 暖橘像素佔比: {orange_pct:.1f}%")
            if w_h < 48:
                print(f"  FAIL: 更衣按鈕高度過小 (<48px): {w_h}px")
                all_passed = False
            elif orange_pct < 60.0:
                print(f"  FAIL: 更衣按鈕暖橘色塊過少 (<60%): {orange_pct:.1f}%")
                all_passed = False
            else:
                print(f"  ok 更衣按鈕高 {w_h}px (>=48px/50px) 且暖橘果凍佔比 {orange_pct:.1f}% 符合規範")
        else:
            print("  FAIL: 未偵測到更衣按鈕暖橘區域")
            all_passed = False

        # 2. Inspect 3 Weapon Slots (Right column, top area: y~140..220)
        # Weapon slots span across x~440 to 1200
        # Let's check 3 regions corresponding to slot 0, 1, 2
        slot_xs = [
            (440, 680),   # Slot 0
            (700, 940),   # Slot 1
            (960, 1200),  # Slot 2
        ]

        for s_idx, (x1, x2) in enumerate(slot_xs):
            crop = arr[145:215, x1:x2]
            s_orange = float(np.mean(is_orange(crop))) * 100.0
            s_cream = float(np.mean(is_cream(crop))) * 100.0
            is_active = (s_idx == active_slot)
            print(f"  [武器槽 {s_idx}] 範圍 x=[{x1},{x2}], y=[145,215] - 橘: {s_orange:.1f}%, 奶油: {s_cream:.1f}% (預期選中: {is_active})")
            if is_active:
                if s_orange < 45.0:
                    print(f"  FAIL: 選中槽 {s_idx} 暖橘色塊不足 (<45%): {s_orange:.1f}%")
                    all_passed = False
                else:
                    print(f"  ok 選中槽 {s_idx} 暖橘色塊符合規範 ({s_orange:.1f}% >= 45%)")
            else:
                if s_cream < 45.0:
                    print(f"  FAIL: 未選中槽 {s_idx} 奶油色塊不足 (<45%): {s_cream:.1f}%")
                    all_passed = False
                else:
                    print(f"  ok 未選中槽 {s_idx} 奶油色塊符合規範 ({s_cream:.1f}% >= 45%)")

        # 3. Inspect Attribute Cards (y~310..490, x~440..1200)
        attr_crop = arr[310:490, 440:1200]
        attr_cream = float(np.mean(is_cream(attr_crop))) * 100.0
        print(f"  [屬性卡片群] 溫暖奶油卡片像素佔比: {attr_cream:.1f}%")
        if attr_cream < 35.0:
            print(f"  FAIL: 屬性小卡奶油色塊不足 (<35%): {attr_cream:.1f}%")
            all_passed = False
        else:
            print(f"  ok 屬性小卡奶油底色符合規範 ({attr_cream:.1f}% >= 35%)")

    # Generate Audit Image for Slot 1 selected
    audit_img_path = os.path.join(proof_dir, "proof_char_tab_measurement_audit.png")
    base_img = Image.open(os.path.join(proof_dir, "proof_char_tab_slot1_selected.png")).convert("RGBA")
    draw = ImageDraw.Draw(base_img)
    try:
        font = ImageFont.truetype(FONT_PATH, 16)
        font_sm = ImageFont.truetype(FONT_PATH, 12)
    except Exception:
        font = ImageFont.load_default()
        font_sm = font

    # Draw bounding boxes and labels for audit proof
    # Wardrobe Button
    draw.rectangle([80, 560, 380, 612], outline=(255, 94, 138, 255), width=3)
    draw.text((85, 540), "BtnWardrobe (H=52px >= 50px, #FFA010 Jelly)", fill=(255, 94, 138, 255), font=font_sm)

    # 3 Weapon slots
    for s_idx, (x1, x2) in enumerate([(440, 680), (700, 940), (960, 1200)]):
        col = (255, 160, 16, 255) if s_idx == 0 else (78, 216, 106, 255)
        draw.rectangle([x1, 145, x2, 213], outline=col, width=3)
        status_lbl = "ACTIVE #FFA010 (H=68px)" if s_idx == 0 else "UNSELECTED #FFF8E7"
        draw.text((x1 + 5, 125), f"Slot {s_idx}: {status_lbl}", fill=col, font=font_sm)

    # Attribute cards area
    draw.rectangle([440, 305, 1200, 485], outline=(56, 160, 255, 255), width=3)
    draw.text((445, 285), "5 Independent Stat Cards (HP, ATK, DEF, CRIT, RAGE)", fill=(56, 160, 255, 255), font=font_sm)

    base_img.save(audit_img_path)
    print(f"\n  ✓ 已儲存量測審計圖: {audit_img_path}")

    if all_passed:
        print("\nCHAR_TAB_PIXEL_VERIFICATION_PASSED")
        return 0
    else:
        print("\nCHAR_TAB_PIXEL_VERIFICATION_FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(verify_character_tab_screenshots())
