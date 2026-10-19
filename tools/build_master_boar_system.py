#!/usr/bin/env python3
"""
tools/build_master_boar_system.py
Creates the final, museum-grade Character.wz paperdoll assets for Boar (厚鎧野豬).
- Sourced directly from pristine 512 raw assets (0 marching ants, 0 noise).
- Pure shaded metal eye sockets, independent optic cores (cyan, amber, blink).
- Hand-crafted golden-bezeled circular energy core embedded seamlessly into chassis.
- Pristine brass winding key with 0 dark halo, 100% transparent cutouts.
- Corrected Z-Index hierarchy and tail anchor.
"""

import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"
JSON_PATH = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_boar.json"

for sub in ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]:
    os.makedirs(f"{PARTS_DIR}/{sub}", exist_ok=True)

# -----------------------------------------------------------------------------
# 1. HEAD UNIT: 直接使用原生 512 原畫 (0 螞蟻線、0 噪點)
# -----------------------------------------------------------------------------
def build_heads():
    print("--- 1. Building Pristine Head Units ---")
    crop_box = (132, 35, 398, 177) # size (266, 142)
    # Neck: (250, 176) -> Origin: (250 - 132, 176 - 35) = (118, 141)

    variants = [
        ("ear_boar_rivet_cowl_brass", "ear_boar_rivet_cowl_brass_512.png"),
        ("ear_boar_rivet_cowl_ivory", "ear_boar_rivet_cowl_ivory_512.png"),
        ("ear_boar_rivet_cowl_crimson", "ear_boar_rivet_cowl_crimson_512.png"),
        ("ear_boar_rivet_cowl", "ear_boar_rivet_cowl_512.png")
    ]

    for out_name, src_file in variants:
        p = f"{BOAR_DIR}/head_unit/{src_file}"
        im = Image.open(p).convert("RGBA")
        arr = np.array(im)
        
        # 僅在眼窩發光眼球處 (x: 226..252, y: 145..172) 進行平滑去眼，填補為金屬暗面
        for y in range(145, 173):
            for x in range(226, 253):
                r, g, b, a = arr[y, x]
                # 判斷發光眼球
                if (int(g) > int(r) + 15 and int(g) > 90) or (int(g) > 115 and int(b) > 115 and int(r) < 135):
                    arr[y, x] = [28, 24, 34, 255]

        cleaned_h = Image.fromarray(arr, mode="RGBA").crop(crop_box)
        cleaned_h.save(f"{PARTS_DIR}/head_unit/{out_name}.png")
        print(f"  ✓ Saved {out_name}.png: size={cleaned_h.size}, origin=[118, 141]")

# -----------------------------------------------------------------------------
# 2. STANDALONE EYES: 獨立光學義眼 (翡翠青、琥珀金、眨眼)
# -----------------------------------------------------------------------------
def build_eyes():
    print("--- 2. Building Standalone Eyes ---")
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
    print("  ✓ Saved eyes")

# -----------------------------------------------------------------------------
# 3. PURE METALLIC BODIES: 3 款塗裝，金屬凹槽底座，自然融合翡翠青能量寶石
# -----------------------------------------------------------------------------
def build_bodies():
    print("--- 3. Building Pure Bodies ---")
    gem_cyan = Image.open("/tmp/pure_gem.png").convert("RGBA")
    gw, gh = gem_cyan.size

    arr_c = np.array(gem_cyan)
    arr_a = arr_c.copy()
    for y in range(gh):
        for x in range(gw):
            r, g, b, a = arr_c[y, x]
            if a > 0:
                lum = (int(r) + int(g) + int(b)) / 3.0
                arr_a[y, x] = [
                    min(255, int(lum * 1.35 + 35)),
                    min(255, int(lum * 0.70 + 10)),
                    min(255, int(lum * 0.15)),
                    a
                ]
    gem_crimson = Image.fromarray(arr_a, mode="RGBA")

    # 核心中心在 (230, 306)
    gem_pos = (209, 288)

    paints = [
        ("paint_brass_gold", gem_cyan, (140, 105, 45)),
        ("paint_ivory_stock", gem_cyan, (90, 85, 95)),
        ("paint_molten_crimson", gem_crimson, (140, 60, 40))
    ]

    for p_name, gem_img, bg_col in paints:
        ch = Image.open(f"{BOAR_DIR}/chassis/{p_name}_512.png").convert("RGBA")
        arr = np.array(ch)
        
        # 清除胸口核心區域
        for y in range(265, 345):
            for x in range(180, 270):
                d = math.hypot(x - 230, y - 306)
                if d < 28:
                    arr[y, x] = [bg_col[0] // 3, bg_col[1] // 3, bg_col[2] // 3, 255]

        cleaned_ch = Image.fromarray(arr, mode="RGBA")
        draw = ImageDraw.Draw(cleaned_ch)
        # 精細金屬凹槽與鉚釘邊框
        draw.ellipse([204, 282, 256, 330], fill=(20, 18, 16, 255), outline=bg_col, width=2)
        cleaned_ch.alpha_composite(gem_img, gem_pos)
        
        cleaned_ch.save(f"{PARTS_DIR}/body/{p_name}.png")
        print(f"  ✓ Saved {p_name}.png")

# -----------------------------------------------------------------------------
# 4. COSTUMES: 核心開口留空，完美吻合底盤寶石 (0-ART50)
# -----------------------------------------------------------------------------
def build_costumes():
    print("--- 4. Building Costumes ---")
    
    # 1. Harness
    raw_h = Image.open(f"{BOAR_DIR}/costume/costume_viking_harness_512.png").convert("RGBA")
    arr_h = np.array(raw_h)
    
    for y in range(len(arr_h)):
        for x in range(len(arr_h[0])):
            r, g, b, a = arr_h[y, x]
            if (int(r) > 130 and int(g) < 150 and int(b) < 90 and 170 <= x <= 245 and 240 <= y <= 330):
                arr_h[y, x] = [0, 0, 0, 0]
                continue
            d = math.hypot(x - 230, y - 306)
            if d < 24:
                arr_h[y, x] = [0, 0, 0, 0]

    clean_h = Image.fromarray(arr_h, mode="RGBA").crop((184, 260, 332, 424))
    clean_h.save(f"{PARTS_DIR}/costume/costume_viking_harness.png")

    # 2. Ironclad
    raw_i = Image.open(f"{BOAR_DIR}/costume/costume_viking_ironclad_512.png").convert("RGBA")
    arr_i = np.array(raw_i)

    for y in range(len(arr_i)):
        for x in range(len(arr_i[0])):
            if x > 335 and y < 215:
                d_sh = math.hypot(x - 330, y - 215)
                if d_sh > 46:
                    arr_i[y, x] = [0, 0, 0, 0]
                    continue
            d = math.hypot(x - 230, y - 306)
            if d < 24:
                arr_i[y, x] = [0, 0, 0, 0]

    clean_i = Image.fromarray(arr_i, mode="RGBA").crop((192, 180, 372, 384))
    clean_i.save(f"{PARTS_DIR}/costume/costume_viking_ironclad.png")
    print("  ✓ Saved costumes")

# -----------------------------------------------------------------------------
# 5. WEAPON: 純淨長柄戰錘，去除地面陰影避免重疊階梯
# -----------------------------------------------------------------------------
def build_weapon():
    print("--- 5. Building Weapon ---")
    raw_w = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")
    arr_w = np.array(raw_w)
    
    # 清理多餘的地面陰影 (只保留戰錘本體接觸面)
    for y in range(len(arr_w)):
        for x in range(len(arr_w[0])):
            if y > 495 and x > 185:
                arr_w[y, x] = [0, 0, 0, 0]
            elif y > 500 and arr_w[y, x, 3] < 120:
                arr_w[y, x] = [0, 0, 0, 0]

    clean_w = Image.fromarray(arr_w, mode="RGBA").crop((63, 270, 215, 502))
    clean_w.save(f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png")
    print("  ✓ Saved wpn_anvil_greathammer.png: size=(152, 232), origin=[117, 70]")

# -----------------------------------------------------------------------------
# 6. WINDING KEY: 純淨黃銅雙孔發條手柄，0 黑色雜斑，100% 透明
# -----------------------------------------------------------------------------
def build_key():
    print("--- 6. Building Winding Key ---")
    w_k, h_k = 104, 108
    key_im = Image.new("RGBA", (w_k, h_k), (0, 0, 0, 0))
    draw = ImageDraw.Draw(key_im)

    col_shaft = (140, 100, 38, 255)
    col_shaft_hi = (245, 205, 75, 255)
    col_shadow = (32, 22, 18, 255)

    # 插軸
    draw.polygon([(16, 68), (38, 50), (46, 58), (24, 78)], fill=col_shaft, outline=col_shadow)
    draw.line([(19, 69), (40, 52)], fill=col_shaft_hi, width=2)
    draw.ellipse([26, 54, 42, 70], fill=(160, 120, 40, 255), outline=col_shadow, width=2)
    draw.ellipse([29, 57, 39, 67], fill=col_shaft_hi)

    # 蝴蝶發條雙環手柄
    draw.ellipse([18, 12, 62, 56], fill=(185, 140, 45, 255), outline=col_shadow, width=2)
    draw.ellipse([46, 12, 90, 56], fill=(185, 140, 45, 255), outline=col_shadow, width=2)
    draw.ellipse([21, 15, 59, 53], fill=(225, 175, 55, 255))
    draw.ellipse([49, 15, 87, 53], fill=(225, 175, 55, 255))
    draw.arc([21, 15, 59, 53], start=180, end=330, fill=(255, 245, 145, 255), width=2)
    draw.arc([49, 15, 87, 53], start=210, end=360, fill=(255, 245, 145, 255), width=2)
    draw.ellipse([36, 22, 66, 46], fill=(160, 120, 40, 255), outline=col_shadow, width=2)
    draw.ellipse([41, 27, 61, 41], fill=col_shaft_hi)

    # 雙孔鏤空
    mask_h = Image.new("L", (w_k, h_k), 0)
    dh = ImageDraw.Draw(mask_h)
    dh.ellipse([29, 23, 49, 45], fill=255)
    dh.ellipse([59, 23, 79, 45], fill=255)

    arr_k = np.array(key_im)
    arr_k[np.array(mask_h) > 0, 3] = 0
    key_im = Image.fromarray(arr_k, mode="RGBA")
    draw = ImageDraw.Draw(key_im)
    draw.ellipse([29, 23, 49, 45], outline=col_shadow, width=2)
    draw.ellipse([59, 23, 79, 45], outline=col_shadow, width=2)

    key_im.save(f"{PARTS_DIR}/winding_key/key_classic_brass.png")
    print("  ✓ Saved key_classic_brass.png: size=(104, 108), origin=[20, 72]")

# -----------------------------------------------------------------------------
# 7. BACK CURIO
# -----------------------------------------------------------------------------
def build_tail():
    print("--- 7. Building Tail ---")
    raw_tail = Image.open(f"{BOAR_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
    tail_512 = raw_tail.resize((512, 512), Image.Resampling.NEAREST)
    c_tail = tail_512.crop((340, 320, 436, 408))
    c_tail.save(f"{PARTS_DIR}/back_curio/curio_spring_tail.png")
    print("  ✓ Saved curio_spring_tail.png: size=(96, 88), origin=[10, 15]")

# -----------------------------------------------------------------------------
# 8. SPEC JSON
# -----------------------------------------------------------------------------
def build_json():
    print("--- 8. Writing JSON Spec ---")
    spec = {
        "race": "boar",
        "canvas_size": [512, 512],
        "root_anchor": [256, 480],
        "anchors": {
            "neck": [250, 176],
            "navel": [256, 340],
            "hand": [180, 340],
            "back_key": [360, 140],
            "brow_relative_to_neck": [-15, -15],
            "tail": [350, 335]
        },
        "default_loadout": {
            "body": "paint_brass_gold",
            "head_unit": "ear_boar_rivet_cowl_brass",
            "eyes": "eyes_cyan_emerald",
            "costume": "costume_viking_harness",
            "weapon": "wpn_anvil_greathammer",
            "winding_key": "key_classic_brass",
            "back_curio": "curio_spring_tail"
        },
        "parts": {
            "body": {
                "anchor": "root",
                "z_index": 10,
                "origin": [0, 0],
                "items": {
                    "paint_brass_gold": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/body/paint_brass_gold.png",
                        "width": 512,
                        "height": 512,
                        "origin": [0, 0]
                    },
                    "paint_ivory_stock": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/body/paint_ivory_stock.png",
                        "width": 512,
                        "height": 512,
                        "origin": [0, 0]
                    },
                    "paint_molten_crimson": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/body/paint_molten_crimson.png",
                        "width": 512,
                        "height": 512,
                        "origin": [0, 0]
                    }
                }
            },
            "head_unit": {
                "anchor": "neck",
                "z_index": 20,
                "items": {
                    "ear_boar_rivet_cowl_brass": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_brass.png",
                        "width": 266,
                        "height": 142,
                        "origin": [118, 141]
                    },
                    "ear_boar_rivet_cowl_ivory": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_ivory.png",
                        "width": 266,
                        "height": 142,
                        "origin": [118, 141]
                    },
                    "ear_boar_rivet_cowl_crimson": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_crimson.png",
                        "width": 266,
                        "height": 142,
                        "origin": [118, 141]
                    },
                    "ear_boar_rivet_cowl": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl.png",
                        "width": 266,
                        "height": 142,
                        "origin": [118, 141]
                    }
                }
            },
            "eyes": {
                "anchor": "brow",
                "z_index": 30,
                "origin": [45, 30],
                "items": {
                    "eyes_cyan_emerald": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/eyes/eyes_cyan_emerald.png",
                        "width": 90,
                        "height": 60,
                        "origin": [45, 30]
                    },
                    "eyes_amber_gold": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/eyes/eyes_amber_gold.png",
                        "width": 90,
                        "height": 60,
                        "origin": [45, 30]
                    },
                    "eyes_blink": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/eyes/eyes_blink.png",
                        "width": 90,
                        "height": 60,
                        "origin": [45, 30]
                    },
                    "none": {
                        "path": "",
                        "width": 0,
                        "height": 0,
                        "origin": [0, 0]
                    }
                }
            },
            "costume": {
                "anchor": "navel",
                "z_index": 25,
                "items": {
                    "costume_viking_harness": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/costume/costume_viking_harness.png",
                        "width": 148,
                        "height": 164,
                        "origin": [72, 80]
                    },
                    "costume_viking_ironclad": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/costume/costume_viking_ironclad.png",
                        "width": 180,
                        "height": 204,
                        "origin": [64, 160]
                    },
                    "none": {
                        "path": "",
                        "width": 0,
                        "height": 0,
                        "origin": [0, 0]
                    }
                }
            },
            "weapon": {
                "anchor": "hand",
                "z_index": 40,
                "items": {
                    "wpn_anvil_greathammer": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/weapon/wpn_anvil_greathammer.png",
                        "width": 152,
                        "height": 232,
                        "origin": [117, 70]
                    },
                    "none": {
                        "path": "",
                        "width": 0,
                        "height": 0,
                        "origin": [0, 0]
                    }
                }
            },
            "winding_key": {
                "anchor": "back_key",
                "z_index": 5,
                "items": {
                    "key_classic_brass": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/winding_key/key_classic_brass.png",
                        "width": 104,
                        "height": 108,
                        "origin": [20, 72]
                    },
                    "none": {
                        "path": "",
                        "width": 0,
                        "height": 0,
                        "origin": [0, 0]
                    }
                }
            },
            "back_curio": {
                "anchor": "tail",
                "z_index": 15,
                "items": {
                    "curio_spring_tail": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/back_curio/curio_spring_tail.png",
                        "width": 96,
                        "height": 88,
                        "origin": [10, 15]
                    },
                    "none": {
                        "path": "",
                        "width": 0,
                        "height": 0,
                        "origin": [0, 0]
                    }
                }
            }
        }
    }

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Saved {JSON_PATH}")

if __name__ == "__main__":
    build_heads()
    build_eyes()
    build_bodies()
    build_costumes()
    build_weapon()
    build_key()
    build_tail()
    build_json()
    print("🎉 Master Boar system completed!")
