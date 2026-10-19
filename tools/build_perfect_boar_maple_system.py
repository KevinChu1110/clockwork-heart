#!/usr/bin/env python3
"""
tools/build_perfect_boar_maple_system.py
Creates the definitive, flawless Character.wz paperdoll assets for Boar (厚鎧野豬).
Fully compliant with review.md 0-ART50, 0-ART51, and 0-ART18.
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
# 1. BODY: 3 款素體塗裝，徹底消除胸口橙色小瓶，融合立體青綠/赤焰核心
# -----------------------------------------------------------------------------
def build_body_assets():
    print("--- 1. Building Body Assets ---")
    core_cyan = Image.open(f"{BOAR_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")
    core_crimson = Image.open(f"{BOAR_DIR}/optic_core/core_molten_crimson_512.png").convert("RGBA")

    paints = [
        ("paint_brass_gold", core_cyan, (140, 105, 45)),
        ("paint_ivory_stock", core_cyan, (90, 85, 95)),
        ("paint_molten_crimson", core_crimson, (140, 60, 40))
    ]

    for p_name, c_img, bg_metal in paints:
        ch = Image.open(f"{BOAR_DIR}/chassis/{p_name}_512.png").convert("RGBA")
        arr = np.array(ch)
        
        # 徹底清除 (x: 180..260, y: 250..340) 區域內的所有橙色瓶子與雜色
        for y in range(250, 340):
            for x in range(180, 260):
                r, g, b, a = arr[y, x]
                # 判斷是否為橙色小瓶或火焰色
                if (int(r) > 160 and int(g) < 150 and int(b) < 80) or math.hypot(x - 230, y - 306) < 28:
                    # 覆蓋為平滑金屬底盤底色
                    arr[y, x] = [bg_metal[0] // 3, bg_metal[1] // 3, bg_metal[2] // 3, 255]

        cleaned_ch = Image.fromarray(arr, mode="RGBA")
        body = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        body.alpha_composite(cleaned_ch)
        body.alpha_composite(c_img)
        
        out_p = f"{PARTS_DIR}/body/{p_name}.png"
        body.save(out_p)
        print(f"  ✓ {out_p}")

# -----------------------------------------------------------------------------
# 2. HEAD UNITS: 4 款頭部變體，徹底去除死眼，保留深色金屬眼窩 (0-ART51)
# -----------------------------------------------------------------------------
def build_head_assets():
    print("--- 2. Building Head Unit Assets ---")
    crop_box = (120, 24, 408, 188) # 288 x 164, origin=[130, 152]

    variants = [
        ("ear_boar_rivet_cowl_brass", "ear_boar_rivet_cowl_brass_512.png"),
        ("ear_boar_rivet_cowl_ivory", "ear_boar_rivet_cowl_ivory_512.png"),
        ("ear_boar_rivet_cowl_crimson", "ear_boar_rivet_cowl_crimson_512.png"),
        ("ear_boar_rivet_cowl", "ear_boar_rivet_cowl_512.png")
    ]

    for out_name, src_file in variants:
        im = Image.open(f"{BOAR_DIR}/head_unit/{src_file}").convert("RGBA")
        arr = np.array(im)
        
        # 眼窩 (x: 215..260, y: 135..176) 內去眼球
        for y in range(135, 177):
            for x in range(215, 261):
                r, g, b, a = arr[y, x]
                is_eye = (int(g) > int(r) + 10 and int(g) > 85) or (int(g) > 105 and int(b) > 105 and int(r) < 140)
                if is_eye and a > 20:
                    arr[y, x] = [28, 24, 32, 255]

        cleaned_h = Image.fromarray(arr, mode="RGBA").crop(crop_box)
        out_p = f"{PARTS_DIR}/head_unit/{out_name}.png"
        cleaned_h.save(out_p)
        print(f"  ✓ {out_p}")

# -----------------------------------------------------------------------------
# 3. EYES: 3 款獨立光學義眼 (翡翠青、琥珀金、眨眼)
# -----------------------------------------------------------------------------
def build_eye_assets():
    print("--- 3. Building Eye Assets ---")
    w_e, h_e = 90, 60
    cx, cy = 45, 30

    # 1. Cyan Emerald
    im_c = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
    dc = ImageDraw.Draw(im_c)
    dc.ellipse([cx - 15, cy - 14, cx + 15, cy + 14], fill=(20, 18, 25, 255), outline=(130, 105, 50, 255), width=2)
    dc.ellipse([cx - 13, cy - 12, cx + 13, cy + 12], fill=(12, 85, 95, 255))
    dc.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(25, 175, 185, 255))
    dc.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(55, 240, 230, 255))
    dc.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(10, 38, 42, 255))
    dc.ellipse([cx + 2, cy - 5, cx + 6, cy - 1], fill=(255, 255, 255, 255))
    dc.ellipse([cx - 4, cy + 1, cx - 2, cy + 3], fill=(210, 255, 255, 220))
    im_c.save(f"{PARTS_DIR}/eyes/eyes_cyan_emerald.png")

    # 2. Amber Gold
    im_a = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
    da = ImageDraw.Draw(im_a)
    da.ellipse([cx - 15, cy - 14, cx + 15, cy + 14], fill=(26, 15, 10, 255), outline=(165, 90, 25, 255), width=2)
    da.ellipse([cx - 13, cy - 12, cx + 13, cy + 12], fill=(125, 40, 10, 255))
    da.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(220, 110, 18, 255))
    da.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(255, 190, 40, 255))
    da.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(48, 18, 8, 255))
    da.ellipse([cx + 2, cy - 5, cx + 6, cy - 1], fill=(255, 255, 255, 255))
    da.ellipse([cx - 4, cy + 1, cx - 2, cy + 3], fill=(255, 230, 170, 220))
    im_a.save(f"{PARTS_DIR}/eyes/eyes_amber_gold.png")

    # 3. Blink
    im_b = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
    db = ImageDraw.Draw(im_b)
    db.arc([cx - 15, cy - 11, cx + 15, cy + 11], start=10, end=170, fill=(35, 25, 45, 255), width=4)
    db.line([(cx - 14, cy), (cx + 14, cy)], fill=(25, 20, 35, 255), width=3)
    db.line([(cx - 11, cy - 1), (cx + 11, cy - 1)], fill=(245, 205, 55, 240), width=1)
    im_b.save(f"{PARTS_DIR}/eyes/eyes_blink.png")
    print("  ✓ Eyes built")

# -----------------------------------------------------------------------------
# 4. COSTUMES: 束帶與重甲，徹底清除小瓶，核心開口金邊對齊 (0-ART50)
# -----------------------------------------------------------------------------
def build_costume_assets():
    print("--- 4. Building Costume Assets ---")
    
    # 1. Harness
    raw_h = Image.open(f"{BOAR_DIR}/costume/costume_viking_harness_512.png").convert("RGBA")
    arr_h = np.array(raw_h)
    
    for y in range(len(arr_h)):
        for x in range(len(arr_h[0])):
            # 徹底清除左上方所有發光橙色小藥瓶雜色
            r, g, b, a = arr_h[y, x]
            if (int(r) > 150 and int(g) < 145 and int(b) < 80 and 180 <= x <= 235 and 250 <= y <= 320):
                arr_h[y, x] = [0, 0, 0, 0]
                continue
            d = math.hypot(x - 230, y - 306)
            if d < 25:
                arr_h[y, x] = [0, 0, 0, 0]
            elif d < 29:
                arr_h[y, x] = [245, 205, 55, 255]

    clean_h = Image.fromarray(arr_h, mode="RGBA").crop((184, 260, 332, 424))
    clean_h.save(f"{PARTS_DIR}/costume/costume_viking_harness.png")

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
    clean_i.save(f"{PARTS_DIR}/costume/costume_viking_ironclad.png")
    print("  ✓ Costumes built")

# -----------------------------------------------------------------------------
# 5. WEAPON: 消除底部右側硬切線
# -----------------------------------------------------------------------------
def build_weapon_asset():
    print("--- 5. Building Weapon Asset ---")
    raw_w = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")
    arr_w = np.array(raw_w)
    
    # 平滑羽化右下角陰影垂直切線
    for y in range(460, 512):
        for x in range(60, 236):
            if arr_w[y, x, 3] > 0:
                if x < 85 and y > 495:
                    arr_w[y, x, 3] = 0
                elif x < 95 and y > 500:
                    arr_w[y, x, 3] = int(arr_w[y, x, 3] * 0.4)
                if x > 210 and y > 475:
                    fade = max(0.0, 1.0 - (x - 210) / 24.0)
                    arr_w[y, x, 3] = int(arr_w[y, x, 3] * fade)

    cleaned_w = Image.fromarray(arr_w, mode="RGBA").crop((60, 260, 236, 512))
    cleaned_w.save(f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png")
    print("  ✓ Weapon built")

# -----------------------------------------------------------------------------
# 6. WINDING KEY: 與背部發條軸自然銜接的立體古銅金屬發條手柄
# -----------------------------------------------------------------------------
def build_key_asset():
    print("--- 6. Building Winding Key Asset ---")
    w_k, h_k = 104, 108
    key_im = Image.new("RGBA", (w_k, h_k), (0, 0, 0, 0))
    draw = ImageDraw.Draw(key_im)

    # 軸心
    col_shaft = (135, 95, 35, 255)
    col_shaft_hi = (245, 205, 70, 255)
    col_shadow = (30, 22, 18, 255)

    draw.polygon([(16, 68), (38, 50), (46, 58), (24, 78)], fill=col_shaft, outline=col_shadow)
    draw.line([(19, 69), (40, 52)], fill=col_shaft_hi, width=2)
    draw.ellipse([26, 54, 42, 70], fill=(160, 120, 40, 255), outline=col_shadow, width=2)
    draw.ellipse([29, 57, 39, 67], fill=col_shaft_hi)

    # 手繪厚塗雙環發條翅膀
    draw.ellipse([18, 12, 62, 56], fill=(175, 130, 40, 255), outline=col_shadow, width=3)
    draw.ellipse([46, 12, 90, 56], fill=(175, 130, 40, 255), outline=col_shadow, width=3)
    draw.ellipse([21, 15, 59, 53], fill=(215, 170, 50, 255))
    draw.ellipse([49, 15, 87, 53], fill=(215, 170, 50, 255))
    draw.arc([21, 15, 59, 53], start=180, end=330, fill=(255, 240, 135, 255), width=3)
    draw.arc([49, 15, 87, 53], start=210, end=360, fill=(255, 240, 135, 255), width=3)
    draw.ellipse([36, 22, 66, 46], fill=(155, 115, 35, 255), outline=col_shadow, width=2)
    draw.ellipse([41, 27, 61, 41], fill=col_shaft_hi)

    # 內孔完全鏤空透明
    mask_hole = Image.new("L", (w_k, h_k), 0)
    draw_h = ImageDraw.Draw(mask_hole)
    draw_h.ellipse([28, 23, 48, 45], fill=255)
    draw_h.ellipse([58, 23, 78, 45], fill=255)

    arr_k = np.array(key_im)
    arr_h = np.array(mask_hole)
    arr_k[arr_h > 0, 3] = 0

    key_im = Image.fromarray(arr_k, mode="RGBA")
    draw = ImageDraw.Draw(key_im)
    draw.ellipse([28, 23, 48, 45], outline=col_shadow, width=2)
    draw.ellipse([58, 23, 78, 45], outline=col_shadow, width=2)

    key_im.save(f"{PARTS_DIR}/winding_key/key_classic_brass.png")
    print("  ✓ Key built")

# -----------------------------------------------------------------------------
# 7. BACK CURIO
# -----------------------------------------------------------------------------
def build_tail_asset():
    print("--- 7. Building Back Curio Asset ---")
    raw_tail = Image.open(f"{BOAR_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
    tail_512 = raw_tail.resize((512, 512), Image.Resampling.NEAREST)
    c_tail = tail_512.crop((340, 320, 436, 408))
    c_tail.save(f"{PARTS_DIR}/back_curio/curio_spring_tail.png")
    print("  ✓ Tail built")

if __name__ == "__main__":
    build_body_assets()
    build_head_assets()
    build_eye_assets()
    build_costume_assets()
    build_weapon_asset()
    build_key_asset()
    build_tail_asset()
    print("🎉 All Boar maple parts built flawlessly!")
