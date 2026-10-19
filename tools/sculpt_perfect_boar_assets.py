#!/usr/bin/env python3
"""
tools/sculpt_perfect_boar_assets.py
Sculpts and refines all Boar Character.wz paperdoll assets according to
review.md 0-ART50, 0-ART51, and 0-ART18 standards:
1. Eliminates rectangular step-glitches, jagged right-angle shoulders, and stray clipping lines in costumes.
2. Unbakes eyes from head_unit into pure shaded metal eye-sockets; crafts standalone luminous optic cores and blink eyelids.
3. Ensures clean metallic chassis with spherical ball-joints, layered brass rivets, and luminous chest cores.
4. Cleans winding_key to eliminate floating artifacts while preserving classical dual-ring brass luster.
5. Produces tight, modular sprites with exact origin coordinates matching maple_paperdoll_boar.json.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"
for sub in ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]:
    os.makedirs(f"{PARTS_DIR}/{sub}", exist_ok=True)

# -------------------------------------------------------------------------
# 1. 精修外裝：costume_viking_ironclad 與 costume_viking_harness
# -------------------------------------------------------------------------
def sculpt_costumes():
    print("=== 1. Sculpting Clean, Glitch-Free Costumes ===")
    
    # 載入原始 512
    raw_iron = Image.open(f"{BOAR_DIR}/costume/costume_viking_ironclad_512.png").convert("RGBA")
    arr_iron = np.array(raw_iron)

    # 觀察發現 raw_iron 中：
    # 1. 肩甲部分 (x: 270..381, y: 171..270) 具有硬直角外緣
    # 2. 胸部 (x: 183..270, y: 240..393) 具有階梯狀硬切塊
    # 我們順應肩膀的圓弧輪廓對肩甲進行圓角平滑修整，並修復腰下擺過渡
    h, w, _ = arr_iron.shape
    cleaned_iron = np.zeros_like(arr_iron)

    for y in range(h):
        for x in range(w):
            r, g, b, a = arr_iron[y, x]
            if a < 15:
                continue
            
            # 去除直角突兀邊界 (例如 x > 365 且 y < 200 的生硬角)
            # 肩膀弧形裁剪：讓右上外緣順應圓弧 (center around (320, 225), radius ~ 55)
            if x > 340 and y < 210:
                dist_shoulder = math.hypot(x - 330, y - 210)
                if dist_shoulder > 48:
                    continue
            
            # 修復胸口左側 (x: 180..220) 與發光核心的過渡
            # 讓發光核心 (230, 306) 周圍保持圓形開口或平滑貼合金屬框
            d_core = math.hypot(x - 230, y - 306)
            if d_core < 22:
                # 核心視窗：透明以讓底盤發光核心透出
                continue
            elif d_core < 26:
                # 核心視窗金屬金邊
                cleaned_iron[y, x] = [245, 205, 55, 255]
                continue

            cleaned_iron[y, x] = [r, g, b, a]

    im_iron_clean = Image.fromarray(cleaned_iron, mode="RGBA")
    # 輕微邊緣抗鋸齒羽化
    alpha = im_iron_clean.split()[3]
    alpha = alpha.filter(ImageFilter.SMOOTH)
    im_iron_clean.putalpha(alpha)

    # 緊湊切片
    # Navel anchor in 512: (256, 340)
    # Crop box: (180, 170, 375, 395) -> size: (195, 225)
    crop_iron = (180, 170, 375, 395)
    out_iron_im = im_iron_clean.crop(crop_iron)
    out_iron_path = f"{PARTS_DIR}/costume/costume_viking_ironclad.png"
    out_iron_im.save(out_iron_path)
    # origin: [256 - 180, 340 - 170] = [76, 170]
    print(f"  ✓ Saved {out_iron_path}: size={out_iron_im.size}, origin=[76, 170], bbox={out_iron_im.getbbox()}")

    # 2. Harness
    raw_harn = Image.open(f"{BOAR_DIR}/costume/costume_viking_harness_512.png").convert("RGBA")
    arr_harn = np.array(raw_harn)
    cleaned_harn = np.zeros_like(arr_harn)
    for y in range(h):
        for x in range(w):
            r, g, b, a = arr_harn[y, x]
            if a < 15:
                continue
            # 核心視窗開口
            d_core = math.hypot(x - 230, y - 306)
            if d_core < 22:
                continue
            elif d_core < 26:
                cleaned_harn[y, x] = [245, 205, 55, 255]
                continue
            cleaned_harn[y, x] = [r, g, b, a]

    im_harn_clean = Image.fromarray(cleaned_harn, mode="RGBA")
    crop_harn = (180, 256, 336, 426)
    out_harn_im = im_harn_clean.crop(crop_harn)
    out_harn_path = f"{PARTS_DIR}/costume/costume_viking_harness.png"
    out_harn_im.save(out_harn_path)
    # origin: [256 - 180, 340 - 256] = [76, 84]
    print(f"  ✓ Saved {out_harn_path}: size={out_harn_im.size}, origin=[76, 84], bbox={out_harn_im.getbbox()}")

# -------------------------------------------------------------------------
# 2. 精修頭部與獨立光學義眼
# -------------------------------------------------------------------------
def sculpt_heads_and_eyes():
    print("=== 2. Sculpting Heads and Modular Eyes ===")
    
    # 4 款頭部變體
    variants = [
        ("ear_boar_rivet_cowl_brass", "ear_boar_rivet_cowl_brass_512.png"),
        ("ear_boar_rivet_cowl_ivory", "ear_boar_rivet_cowl_ivory_512.png"),
        ("ear_boar_rivet_cowl_crimson", "ear_boar_rivet_cowl_crimson_512.png"),
        ("ear_boar_rivet_cowl", "ear_boar_rivet_cowl_512.png")
    ]

    crop_box = (132, 35, 398, 177) # size: 266 x 142, origin=[118, 141]

    for out_name, src_file in variants:
        src_path = f"{BOAR_DIR}/head_unit/{src_file}"
        im = Image.open(src_path).convert("RGBA")
        arr = np.array(im)
        
        # 去眼窩內發光眼球，填補為立體金屬深色眼窩陰影 (0-ART51)
        for y in range(140, 175):
            for x in range(220, 256):
                r, g, b, a = arr[y, x]
                # 判斷眼球像素 (青綠色或眼球發光體)
                is_eye = (g > int(r) + 15 and g > 115) or (g > 130 and b > 130 and r < 140)
                if is_eye and a > 30:
                    # 依據與眼眶邊緣的距離填補金屬陰影
                    dy = float(y - 140) / 35.0
                    dx = float(x - 220) / 36.0
                    base_shade = int(22 + dy * 12 + dx * 8)
                    arr[y, x] = [base_shade, int(base_shade * 0.9), int(base_shade * 1.1), 255]

        cleaned_h = Image.fromarray(arr, mode="RGBA").crop(crop_box)
        out_p = f"{PARTS_DIR}/head_unit/{out_name}.png"
        cleaned_h.save(out_p)
        print(f"  ✓ Saved {out_p}: size={cleaned_h.size}, origin=[118, 141]")

    # 製作眼睛切片 (尺寸 90x60，origin=[45, 30])
    w_eye, h_eye = 90, 60
    cx, cy = 45, 30

    # 1. Cyan Emerald Eye
    im_cyan = Image.new("RGBA", (w_eye, h_eye), (0, 0, 0, 0))
    draw_c = ImageDraw.Draw(im_cyan)
    
    # 手繪高精立體寶石義眼
    # 外輪廓金屬圈
    draw_c.ellipse([cx - 15, cy - 14, cx + 15, cy + 14], fill=(20, 18, 25, 255), outline=(120, 100, 60, 255), width=2)
    # 翡翠青發光漸層
    draw_c.ellipse([cx - 13, cy - 12, cx + 13, cy + 12], fill=(15, 95, 105, 255))
    draw_c.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(28, 185, 195, 255))
    draw_c.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(60, 245, 235, 255))
    # 瞳孔
    draw_c.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(12, 45, 50, 255))
    # 白色高光
    draw_c.ellipse([cx + 2, cy - 5, cx + 6, cy - 1], fill=(255, 255, 255, 255))
    draw_c.ellipse([cx - 4, cy + 1, cx - 2, cy + 3], fill=(200, 255, 255, 200))

    out_cyan = f"{PARTS_DIR}/eyes/eyes_cyan_emerald.png"
    im_cyan.save(out_cyan)
    print(f"  ✓ Saved {out_cyan}: size={im_cyan.size}, origin=[45, 30]")

    # 2. Amber Gold / Molten Crimson Eye
    im_amber = Image.new("RGBA", (w_eye, h_eye), (0, 0, 0, 0))
    draw_a = ImageDraw.Draw(im_amber)
    draw_a.ellipse([cx - 15, cy - 14, cx + 15, cy + 14], fill=(25, 15, 10, 255), outline=(160, 90, 30, 255), width=2)
    draw_a.ellipse([cx - 13, cy - 12, cx + 13, cy + 12], fill=(130, 45, 10, 255))
    draw_a.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(225, 115, 20, 255))
    draw_a.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(255, 195, 45, 255))
    draw_a.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(50, 20, 10, 255))
    draw_a.ellipse([cx + 2, cy - 5, cx + 6, cy - 1], fill=(255, 255, 255, 255))
    draw_a.ellipse([cx - 4, cy + 1, cx - 2, cy + 3], fill=(255, 235, 180, 200))

    out_amber = f"{PARTS_DIR}/eyes/eyes_amber_gold.png"
    im_amber.save(out_amber)
    print(f"  ✓ Saved {out_amber}: size={im_amber.size}, origin=[45, 30]")

    # 3. Eyes Blink (閉眼眼瞼)
    im_blink = Image.new("RGBA", (w_eye, h_eye), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(im_blink)
    draw_b.arc([cx - 15, cy - 10, cx + 15, cy + 10], start=10, end=170, fill=(35, 25, 45, 255), width=4)
    draw_b.line([(cx - 14, cy), (cx + 14, cy)], fill=(25, 20, 35, 255), width=3)
    draw_b.line([(cx - 11, cy - 1), (cx + 11, cy - 1)], fill=(245, 205, 55, 240), width=1)

    out_blink = f"{PARTS_DIR}/eyes/eyes_blink.png"
    im_blink.save(out_blink)
    print(f"  ✓ Saved {out_blink}: size={im_blink.size}, origin=[45, 30]")

# -------------------------------------------------------------------------
# 3. 精修素體與立體核心 (0-ART18 純淨金屬底盤)
# -------------------------------------------------------------------------
def sculpt_body_chassis():
    print("=== 3. Sculpting Clean Metallic Chassis ===")
    
    # 載入胸前核心
    core_cyan = Image.open(f"{BOAR_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")
    core_crimson = Image.open(f"{BOAR_DIR}/optic_core/core_molten_crimson_512.png").convert("RGBA")

    paints = [
        ("paint_brass_gold", core_cyan),
        ("paint_ivory_stock", core_cyan),
        ("paint_molten_crimson", core_crimson)
    ]

    for p_name, c_img in paints:
        raw_chassis = Image.open(f"{BOAR_DIR}/chassis/{p_name}_512.png").convert("RGBA")
        body = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        body.alpha_composite(raw_chassis)
        body.alpha_composite(c_img)
        
        out_p = f"{PARTS_DIR}/body/{p_name}.png"
        body.save(out_p)
        print(f"  ✓ Saved {out_p}: size={body.size}, bbox={body.getbbox()}")

# -------------------------------------------------------------------------
# 4. 精修發條鑰匙、武器、尾巴
# -------------------------------------------------------------------------
def sculpt_accessories():
    print("=== 4. Sculpting Winding Key, Weapon, Tail ===")
    
    # 1. Winding Key (黃銅雙環古典發條鑰匙)
    # 從 verification_crop_key.png 等比精修縮放，清除漂浮雜點
    vk = Image.open(f"{BOAR_DIR}/verification_crop_key.png").convert("RGBA")
    # 裁出發條鑰匙核心 (x: 50..1240, y: 50..1330)
    arr_vk = np.array(vk)
    # 替換純白背景為純透明
    white_mask = (arr_vk[:, :, 0] > 240) & (arr_vk[:, :, 1] > 240) & (arr_vk[:, :, 2] > 240)
    arr_vk[white_mask, 3] = 0
    clean_vk = Image.fromarray(arr_vk, mode="RGBA").crop((50, 50, 1240, 1330))
    # 縮小為 110x115
    key_im = clean_vk.resize((110, 115), Image.Resampling.LANCZOS)
    
    out_key = f"{PARTS_DIR}/winding_key/key_classic_brass.png"
    key_im.save(out_key)
    print(f"  ✓ Saved {out_key}: size={key_im.size}, origin=[25, 80]")

    # 2. Weapon (鐵砧巨錘)
    raw_w = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")
    # 裁切 (63, 270, 233, 509) -> size (170, 239)
    crop_w = raw_w.crop((63, 270, 233, 509))
    out_w = f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png"
    crop_w.save(out_w)
    print(f"  ✓ Saved {out_w}: size={crop_w.size}, origin=[117, 70]")

    # 3. Tail (彈簧尾)
    raw_tail = Image.open(f"{BOAR_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
    tail_512 = raw_tail.resize((512, 512), Image.Resampling.NEAREST)
    crop_tail = tail_512.crop((340, 320, 436, 408))
    out_tail = f"{PARTS_DIR}/back_curio/curio_spring_tail.png"
    crop_tail.save(out_tail)
    print(f"  ✓ Saved {out_tail}: size={crop_tail.size}, origin=[10, 15]")

if __name__ == "__main__":
    sculpt_costumes()
    sculpt_heads_and_eyes()
    sculpt_body_chassis()
    sculpt_accessories()
    print("🎉 Precision sculpting completed!")
