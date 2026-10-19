#!/usr/bin/env python3
"""
tools/craft_masterpiece_boar_assets.py
Crafts museum-grade Character.wz tight slice assets for Boar (厚鎧野豬).
Eliminates:
1. Strange orange vial/potion glitch and blurry overlays on costume.
2. Rectangular un-cutout blocks in winding_key holes and edges.
3. Stone hammer bottom clipping lines.
4. Glitched shoulder squares.
Ensures:
1. Pure metallic chassis (paint_brass_gold, paint_ivory_stock, paint_molten_crimson)
   with spherical joints, layered rivets, and glowing chest core (0-ART18).
2. Head unit (4 variants) with unbaked eyes; eye sockets are cleanly shaded dark metal (0-ART51).
3. Independent optic cores (eyes_cyan_emerald, eyes_amber_gold, eyes_blink).
4. Costumes (costume_viking_ironclad, costume_viking_harness) cleanly cut, perfectly aligned,
   with gold-bezeled core windows (0-ART50).
5. Weapon and key cleanly keyed and anchored.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"

for sub in ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]:
    os.makedirs(f"{PARTS_DIR}/{sub}", exist_ok=True)

# -----------------------------------------------------------------------------
# 1. WINDING KEY (古典黃銅雙環發條鑰匙)
# -----------------------------------------------------------------------------
def craft_winding_key():
    print("--- 1. Crafting Clean Winding Key ---")
    # 尺寸 110 x 115，origin=[25, 80]
    # 使用雄獅的經典黃銅金屬材質與風格，重新生成野豬右背專屬的完美雙環發條鑰匙
    w_k, h_k = 110, 115
    key_im = Image.new("RGBA", (w_k, h_k), (0, 0, 0, 0))
    draw = ImageDraw.Draw(key_im)

    # 軸心 (從 center-left 向下插入背部)
    # 軸心起點 (40, 65) -> 插入點 (25, 80)
    col_shaft = (130, 95, 35, 255)
    col_shaft_hi = (235, 195, 65, 255)
    col_shadow = (35, 25, 20, 255)

    # 繪製插軸
    draw.polygon([(20, 75), (45, 55), (55, 65), (28, 87)], fill=col_shaft, outline=col_shadow)
    draw.line([(24, 76), (48, 57)], fill=col_shaft_hi, width=2)

    # 軸環 (Collar ring)
    draw.ellipse([30, 60, 48, 76], fill=(160, 120, 40, 255), outline=col_shadow, width=2)
    draw.ellipse([33, 63, 44, 73], fill=col_shaft_hi)

    # 雙環發條手柄 (Dual-ring butterfly handle)
    # 環1 (左上環，中心 (48, 38), 半徑 24)
    # 環2 (右上環，中心 (76, 38), 半徑 24)
    # 外輪廓 (加深外邊緣)
    draw.ellipse([24, 14, 72, 62], fill=(180, 135, 45, 255), outline=col_shadow, width=3)
    draw.ellipse([52, 14, 100, 62], fill=(180, 135, 45, 255), outline=col_shadow, width=3)
    
    # 內部過渡填充與高光
    draw.ellipse([27, 17, 69, 59], fill=(215, 170, 55, 255))
    draw.ellipse([55, 17, 97, 59], fill=(215, 170, 55, 255))

    # 頂部反光弧線
    draw.arc([27, 17, 69, 59], start=180, end=330, fill=(255, 240, 140, 255), width=3)
    draw.arc([55, 17, 97, 59], start=210, end=360, fill=(255, 240, 140, 255), width=3)

    # 核心金屬實心連接塊
    draw.ellipse([45, 25, 75, 52], fill=(160, 120, 40, 255), outline=col_shadow, width=2)
    draw.ellipse([50, 30, 70, 47], fill=col_shaft_hi)

    # 清空兩顆指孔內部 (完全透明！徹底解決未去背問題)
    mask_hole = Image.new("L", (w_k, h_k), 0)
    draw_h = ImageDraw.Draw(mask_hole)
    draw_h.ellipse([35, 26, 56, 50], fill=255)
    draw_h.ellipse([64, 26, 85, 50], fill=255)

    arr_k = np.array(key_im)
    arr_h = np.array(mask_hole)
    arr_k[arr_h > 0, 3] = 0

    # 內孔深色邊框線
    key_im = Image.fromarray(arr_k, mode="RGBA")
    draw = ImageDraw.Draw(key_im)
    draw.ellipse([35, 26, 56, 50], outline=col_shadow, width=2)
    draw.ellipse([64, 26, 85, 50], outline=col_shadow, width=2)

    out_p = f"{PARTS_DIR}/winding_key/key_classic_brass.png"
    key_im.save(out_p)
    print(f"  ✓ Saved {out_p}: size={key_im.size}, origin=[25, 80]")

# -----------------------------------------------------------------------------
# 2. WEAPON (鐵砧巨錘，清除接地切邊與雜點)
# -----------------------------------------------------------------------------
def craft_weapon():
    print("--- 2. Crafting Clean Warhammer ---")
    raw_w = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")
    arr_w = np.array(raw_w)
    
    # 戰錘在 (63, 270, 233, 509)
    # 清除錘頭底部左下角 (y > 490, x < 120) 的生硬直線切邊，給予自然風化石質倒角
    for y in range(485, 510):
        for x in range(63, 115):
            if arr_w[y, x, 3] > 0:
                # 倒角修剪
                dist = math.hypot(x - 110, y - 485)
                if x < 80 and y > 498:
                    arr_w[y, x, 3] = 0
                elif x < 90 and y > 502:
                    arr_w[y, x, 3] = int(arr_w[y, x, 3] * 0.5)

    cleaned_w = Image.fromarray(arr_w, mode="RGBA")
    crop_w = cleaned_w.crop((63, 270, 233, 509))
    out_p = f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png"
    crop_w.save(out_p)
    print(f"  ✓ Saved {out_p}: size={crop_w.size}, origin=[117, 70]")

# -----------------------------------------------------------------------------
# 3. TAIL (彈簧尾)
# -----------------------------------------------------------------------------
def craft_tail():
    print("--- 3. Crafting Spring Tail ---")
    raw_tail = Image.open(f"{BOAR_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
    tail_512 = raw_tail.resize((512, 512), Image.Resampling.NEAREST)
    c_tail = tail_512.crop((340, 320, 436, 408))
    out_p = f"{PARTS_DIR}/back_curio/curio_spring_tail.png"
    c_tail.save(out_p)
    print(f"  ✓ Saved {out_p}: size={c_tail.size}, origin=[10, 15]")

# -----------------------------------------------------------------------------
# 4. HEAD UNIT (4 款頭部變體，徹底去除死眼，保持純淨眼窩)
# -----------------------------------------------------------------------------
def craft_head_units():
    print("--- 4. Crafting Head Units (Eyes completely unbaked) ---")
    crop_box = (132, 35, 398, 177) # size (266, 142), origin=[118, 141]

    variants = [
        ("ear_boar_rivet_cowl_brass", "ear_boar_rivet_cowl_brass_512.png"),
        ("ear_boar_rivet_cowl_ivory", "ear_boar_rivet_cowl_ivory_512.png"),
        ("ear_boar_rivet_cowl_crimson", "ear_boar_rivet_cowl_crimson_512.png"),
        ("ear_boar_rivet_cowl", "ear_boar_rivet_cowl_512.png")
    ]

    for out_name, src_file in variants:
        src_path = f"{BOAR_DIR}/head_unit/{src_file}"
        im = Image.open(src_path).convert("RGBA")
        arr = np.array(im)
        
        # 仔細覆蓋眼窩區域 (x: 215..258, y: 138..175) 內的發光像素
        for y in range(138, 176):
            for x in range(215, 259):
                r, g, b, a = arr[y, x]
                # 判斷是否為眼睛青綠或亮色
                is_eye_px = (int(g) > int(r) + 12 and int(g) > 90) or (int(g) > 110 and int(b) > 110 and int(r) < 140)
                if is_eye_px and a > 20:
                    # 替換為眼窩金屬暗面底色 (與周圍金屬眼窩邊緣平滑過渡)
                    arr[y, x] = [28, 24, 32, 255]

        cleaned_h = Image.fromarray(arr, mode="RGBA").crop(crop_box)
        out_p = f"{PARTS_DIR}/head_unit/{out_name}.png"
        cleaned_h.save(out_p)
        print(f"  ✓ Saved {out_p}: size={cleaned_h.size}, origin=[118, 141]")

# -----------------------------------------------------------------------------
# 5. MODULAR EYES (獨立光學義眼與眨眼眼瞼)
# -----------------------------------------------------------------------------
def craft_eyes():
    print("--- 5. Crafting Standalone Optic Cores & Blink ---")
    w_e, h_e = 90, 60
    cx, cy = 45, 30

    # 1. Cyan Emerald Eye (高階手繪賽璐珞發光義眼)
    im_cyan = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
    draw_c = ImageDraw.Draw(im_cyan)
    
    # 金屬外框
    draw_c.ellipse([cx - 16, cy - 15, cx + 16, cy + 15], fill=(22, 18, 28, 255), outline=(135, 110, 50, 255), width=2)
    # 發光虹膜漸層 (青藍色)
    draw_c.ellipse([cx - 14, cy - 13, cx + 14, cy + 13], fill=(12, 85, 95, 255))
    draw_c.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(25, 175, 185, 255))
    draw_c.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(55, 240, 230, 255))
    # 瞳孔
    draw_c.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(10, 38, 42, 255))
    # 雙高光
    draw_c.ellipse([cx + 2, cy - 5, cx + 6, cy - 1], fill=(255, 255, 255, 255))
    draw_c.ellipse([cx - 4, cy + 1, cx - 2, cy + 3], fill=(210, 255, 255, 220))

    out_cyan = f"{PARTS_DIR}/eyes/eyes_cyan_emerald.png"
    im_cyan.save(out_cyan)
    print(f"  ✓ Saved {out_cyan}: size={im_cyan.size}, origin=[45, 30]")

    # 2. Amber Gold Eye (赤焰琥珀金義眼)
    im_amber = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
    draw_a = ImageDraw.Draw(im_amber)
    draw_a.ellipse([cx - 16, cy - 15, cx + 16, cy + 15], fill=(28, 16, 12, 255), outline=(170, 95, 30, 255), width=2)
    draw_a.ellipse([cx - 14, cy - 13, cx + 14, cy + 13], fill=(125, 40, 10, 255))
    draw_a.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(220, 110, 18, 255))
    draw_a.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(255, 190, 40, 255))
    draw_a.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(48, 18, 8, 255))
    draw_a.ellipse([cx + 2, cy - 5, cx + 6, cy - 1], fill=(255, 255, 255, 255))
    draw_a.ellipse([cx - 4, cy + 1, cx - 2, cy + 3], fill=(255, 230, 170, 220))

    out_amber = f"{PARTS_DIR}/eyes/eyes_amber_gold.png"
    im_amber.save(out_amber)
    print(f"  ✓ Saved {out_amber}: size={im_amber.size}, origin=[45, 30]")

    # 3. Eyes Blink (金屬眼瞼閉合線)
    im_blink = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(im_blink)
    draw_b.arc([cx - 16, cy - 12, cx + 16, cy + 12], start=10, end=170, fill=(35, 25, 45, 255), width=4)
    draw_b.line([(cx - 15, cy), (cx + 15, cy)], fill=(25, 20, 35, 255), width=3)
    draw_b.line([(cx - 12, cy - 1), (cx + 12, cy - 1)], fill=(245, 205, 55, 240), width=1)

    out_blink = f"{PARTS_DIR}/eyes/eyes_blink.png"
    im_blink.save(out_blink)
    print(f"  ✓ Saved {out_blink}: size={im_blink.size}, origin=[45, 30]")

# -----------------------------------------------------------------------------
# 6. BODY (純淨金屬底盤，立體核心，0-ART18 合規)
# -----------------------------------------------------------------------------
def craft_bodies():
    print("--- 6. Crafting Pure Metallic Chassis Bodies (0-ART18) ---")
    core_cyan = Image.open(f"{BOAR_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")
    core_crimson = Image.open(f"{BOAR_DIR}/optic_core/core_molten_crimson_512.png").convert("RGBA")

    paints = [
        ("paint_brass_gold", core_cyan),
        ("paint_ivory_stock", core_cyan),
        ("paint_molten_crimson", core_crimson)
    ]

    for p_name, c_img in paints:
        ch = Image.open(f"{BOAR_DIR}/chassis/{p_name}_512.png").convert("RGBA")
        body = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        body.alpha_composite(ch)
        body.alpha_composite(c_img)
        
        out_p = f"{PARTS_DIR}/body/{p_name}.png"
        body.save(out_p)
        print(f"  ✓ Saved {out_p}: size={body.size}, bbox={body.getbbox()}")

# -----------------------------------------------------------------------------
# 7. COSTUMES (手工精修：徹底消除生硬方塊、小藥瓶雜項與肩甲直角)
# -----------------------------------------------------------------------------
def craft_costumes():
    print("--- 7. Crafting Clean, Form-Fitting Costumes ---")
    
    # 1. Harness (鍛爐工坊束帶：圍繞能量核心的立體皮帶與金屬扣環，絕無模糊小藥瓶)
    # Navel anchor in 512: (256, 340)
    # Crop box: (180, 256, 336, 426) -> size: (156, 170), origin=[76, 84]
    raw_harn = Image.open(f"{BOAR_DIR}/costume/costume_viking_harness_512.png").convert("RGBA")
    arr_h = np.array(raw_harn)
    h, w, _ = arr_h.shape

    clean_h = np.zeros_like(arr_h)
    for y in range(h):
        for x in range(w):
            r, g, b, a = arr_h[y, x]
            if a < 20:
                continue
            
            # 清除左上懸掛的橙紅色小瓶雜訊 (x: 185..215, y: 260..295)
            is_orange_vial = (int(r) > 170 and int(g) < 140 and int(b) < 60)
            if is_orange_vial and (180 <= x <= 220 and 260 <= y <= 305):
                continue
            
            # 核心視窗中心 (230, 306) 保持透明以露出底盤核心
            d_core = math.hypot(x - 230, y - 306)
            if d_core < 22:
                continue
            elif d_core < 26:
                clean_h[y, x] = [245, 205, 55, 255] # 金色邊框
                continue

            clean_h[y, x] = [r, g, b, a]

    im_h_clean = Image.fromarray(clean_h, mode="RGBA").crop((180, 256, 336, 426))
    out_h = f"{PARTS_DIR}/costume/costume_viking_harness.png"
    im_h_clean.save(out_h)
    print(f"  ✓ Saved {out_h}: size={im_h_clean.size}, origin=[76, 84]")

    # 2. Ironclad (維京重裝鐵甲：深鋼藍板甲、金色鉚釘、圓弧肩甲、核心視窗金框)
    # Navel anchor in 512: (256, 340)
    # Crop box: (180, 170, 375, 395) -> size: (195, 225), origin=[76, 170]
    raw_iron = Image.open(f"{BOAR_DIR}/costume/costume_viking_ironclad_512.png").convert("RGBA")
    arr_i = np.array(raw_iron)

    clean_i = np.zeros_like(arr_i)
    for y in range(h):
        for x in range(w):
            r, g, b, a = arr_i[y, x]
            if a < 20:
                continue
            
            # 消除肩膀外緣生硬直角 (x > 340 且 y < 215)
            # 依圓弧半徑裁剪
            if x > 335 and y < 215:
                d_sh = math.hypot(x - 330, y - 215)
                if d_sh > 46:
                    continue

            # 核心視窗中心 (230, 306)
            d_core = math.hypot(x - 230, y - 306)
            if d_core < 22:
                continue
            elif d_core < 26:
                clean_i[y, x] = [245, 205, 55, 255]
                continue

            clean_i[y, x] = [r, g, b, a]

    im_i_clean = Image.fromarray(clean_i, mode="RGBA").crop((180, 170, 375, 395))
    out_i = f"{PARTS_DIR}/costume/costume_viking_ironclad.png"
    im_i_clean.save(out_i)
    print(f"  ✓ Saved {out_i}: size={im_i_clean.size}, origin=[76, 170]")

if __name__ == "__main__":
    craft_winding_key()
    craft_weapon()
    craft_tail()
    craft_head_units()
    craft_eyes()
    craft_bodies()
    craft_costumes()
    print("🎉 All masterpiece Boar assets crafted successfully!")
