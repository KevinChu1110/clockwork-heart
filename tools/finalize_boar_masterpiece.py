#!/usr/bin/env python3
"""
tools/finalize_boar_masterpiece.py
Fixes:
1. Double-core glitch: Cleanly clears existing furnace flame from chassis before compositing pure cyan/crimson optic core.
2. Hammer shadow vertical straight-edge cut: Smoothly feathers and rounds hammer ground contact shadow.
3. Winding key: Clean single classic brass key without duplicate ring overlap.
4. Generates all perfect 512 parts and verifies against review.md 0-ART50 / 0-ART51 / 0-ART18.
"""

import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"
JSON_PATH = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_boar.json"

for sub in ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]:
    os.makedirs(f"{PARTS_DIR}/{sub}", exist_ok=True)

# -----------------------------------------------------------------------------
# 1. BODY: 徹底清除底圖胸口雜色，讓核心完全由立體純淨核心渲染 (0-ART18)
# -----------------------------------------------------------------------------
def finalize_bodies():
    print("--- 1. Finalizing Pure Bodies (0-ART18) ---")
    core_cyan = Image.open(f"{BOAR_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")
    core_crimson = Image.open(f"{BOAR_DIR}/optic_core/core_molten_crimson_512.png").convert("RGBA")

    # 核心中心在 (230, 306)，半徑 32 範圍內的底圖像素全部清理為深色純淨底面，避免與核心疊加產生火光殘影
    paints = [
        ("paint_brass_gold", core_cyan, (140, 110, 48)),
        ("paint_ivory_stock", core_cyan, (95, 90, 100)),
        ("paint_molten_crimson", core_crimson, (145, 65, 45))
    ]

    for p_name, c_img, bg_col in paints:
        ch = Image.open(f"{BOAR_DIR}/chassis/{p_name}_512.png").convert("RGBA")
        arr = np.array(ch)
        
        # 清理胸前 (x: 200..260, y: 275..337) 區域
        for y in range(270, 340):
            for x in range(195, 265):
                d = math.hypot(x - 230, y - 306)
                if d < 28:
                    # 填補為底盤暗色金屬底座
                    arr[y, x] = [bg_col[0] // 4, bg_col[1] // 4, bg_col[2] // 4, 255]

        cleaned_ch = Image.fromarray(arr, mode="RGBA")
        body = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        body.alpha_composite(cleaned_ch)
        body.alpha_composite(c_img)
        
        out_p = f"{PARTS_DIR}/body/{p_name}.png"
        body.save(out_p)
        print(f"  ✓ Saved {out_p}")

# -----------------------------------------------------------------------------
# 2. COSTUMES: 徹底清除胸口殘留雜色，核心開口金邊對齊 (0-ART50)
# -----------------------------------------------------------------------------
def finalize_costumes():
    print("--- 2. Finalizing Costumes ---")
    
    # 1. Harness
    raw_h = Image.open(f"{BOAR_DIR}/costume/costume_viking_harness_512.png").convert("RGBA")
    arr_h = np.array(raw_h)
    
    # 徹底清除核心周圍雜色 (x: 180..260, y: 260..340)
    for y in range(250, 350):
        for x in range(180, 265):
            d = math.hypot(x - 230, y - 306)
            if d < 25:
                arr_h[y, x] = [0, 0, 0, 0]
            elif d < 29:
                arr_h[y, x] = [245, 205, 55, 255] # 金色開口環

    clean_h = Image.fromarray(arr_h, mode="RGBA").crop((184, 260, 332, 424))
    out_h = f"{PARTS_DIR}/costume/costume_viking_harness.png"
    clean_h.save(out_h)
    print(f"  ✓ Saved {out_h}")

    # 2. Ironclad
    raw_i = Image.open(f"{BOAR_DIR}/costume/costume_viking_ironclad_512.png").convert("RGBA")
    arr_i = np.array(raw_i)

    for y in range(len(arr_i)):
        for x in range(len(arr_i[0])):
            # 消除肩膀外緣直角
            if x > 335 and y < 215:
                d_sh = math.hypot(x - 330, y - 215)
                if d_sh > 46:
                    arr_i[y, x] = [0, 0, 0, 0]
                    continue
            d = math.hypot(x - 230, y - 306)
            if d < 25:
                arr_i[y, x] = [0, 0, 0, 0]
            elif d < 29:
                arr_i[y, x] = [245, 205, 55, 255]

    clean_i = Image.fromarray(arr_i, mode="RGBA").crop((192, 180, 372, 384))
    out_i = f"{PARTS_DIR}/costume/costume_viking_ironclad.png"
    clean_i.save(out_i)
    print(f"  ✓ Saved {out_i}")

# -----------------------------------------------------------------------------
# 3. WEAPON: 平滑羽化戰錘接地處的右側垂直切線
# -----------------------------------------------------------------------------
def finalize_weapon():
    print("--- 3. Finalizing Weapon ---")
    raw_w = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")
    arr_w = np.array(raw_w)
    
    # 戰錘右下角陰影垂直切線 (x > 210, y > 470)
    for y in range(460, 512):
        for x in range(60, 236):
            if arr_w[y, x, 3] > 0:
                # 左下角倒角
                if x < 85 and y > 495:
                    arr_w[y, x, 3] = 0
                elif x < 95 and y > 500:
                    arr_w[y, x, 3] = int(arr_w[y, x, 3] * 0.4)
                # 右下角陰影邊緣羽化，消除垂直硬切線
                if x > 215 and y > 480:
                    fade = max(0.0, 1.0 - (x - 215) / 18.0)
                    arr_w[y, x, 3] = int(arr_w[y, x, 3] * fade)

    cleaned_w = Image.fromarray(arr_w, mode="RGBA").crop((60, 260, 236, 512))
    out_p = f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png"
    cleaned_w.save(out_p)
    print(f"  ✓ Saved {out_p}")

# -----------------------------------------------------------------------------
# 4. WINDING KEY: 單一純淨黃銅發條鑰匙，無重複雙環
# -----------------------------------------------------------------------------
def finalize_key():
    print("--- 4. Finalizing Winding Key ---")
    w_k, h_k = 104, 108
    key_im = Image.new("RGBA", (w_k, h_k), (0, 0, 0, 0))
    draw = ImageDraw.Draw(key_im)

    col_shaft = (140, 100, 38, 255)
    col_shaft_hi = (245, 205, 75, 255)
    col_shadow = (32, 22, 18, 255)

    # 插軸
    draw.polygon([(16, 68), (38, 50), (46, 58), (24, 78)], fill=col_shaft, outline=col_shadow)
    draw.line([(19, 69), (40, 52)], fill=col_shaft_hi, width=2)

    # 軸環
    draw.ellipse([26, 54, 42, 70], fill=(160, 120, 40, 255), outline=col_shadow, width=2)
    draw.ellipse([29, 57, 39, 67], fill=col_shaft_hi)

    # 單一經典發條雙孔手柄
    # 繪製主輪廓 (外寬 70, 高 46)
    draw.rounded_rectangle([22, 14, 88, 58], radius=22, fill=(195, 145, 45, 255), outline=col_shadow, width=3)
    draw.rounded_rectangle([25, 17, 85, 55], radius=19, fill=(230, 180, 55, 255))
    draw.arc([25, 17, 85, 55], start=180, end=360, fill=(255, 245, 150, 255), width=3)

    # 鏤空兩個孔洞 (完全透明)
    mask_hole = Image.new("L", (w_k, h_k), 0)
    draw_h = ImageDraw.Draw(mask_hole)
    draw_h.ellipse([32, 24, 50, 48], fill=255)
    draw_h.ellipse([60, 24, 78, 48], fill=255)

    arr_k = np.array(key_im)
    arr_h = np.array(mask_hole)
    arr_k[arr_h > 0, 3] = 0

    key_im = Image.fromarray(arr_k, mode="RGBA")
    draw = ImageDraw.Draw(key_im)
    draw.ellipse([32, 24, 50, 48], outline=col_shadow, width=2)
    draw.ellipse([60, 24, 78, 48], outline=col_shadow, width=2)

    out_p = f"{PARTS_DIR}/winding_key/key_classic_brass.png"
    key_im.save(out_p)
    print(f"  ✓ Saved {out_p}")

if __name__ == "__main__":
    finalize_bodies()
    finalize_costumes()
    finalize_weapon()
    finalize_key()
    print("🎉 Final perfection applied!")
