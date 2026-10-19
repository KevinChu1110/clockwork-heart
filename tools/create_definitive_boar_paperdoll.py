#!/usr/bin/env python3
"""
tools/create_definitive_boar_paperdoll.py
Constructs the definitive, pristine Character.wz paperdoll suite for Boar:
1. Each part is a standalone, fully painted, layer-compositable sprite with 0 holes.
2. Body is a complete pure metallic chassis with authentic glowing energy gem (0-ART18).
3. Head is a complete helmet/tusk unit with shaded dark metal sockets (0-ART51).
4. Eyes are standalone jewel optic cores with Specular highlights and blink lids.
5. Costumes are standalone form-fitting armor layers with core port-holes.
6. Weapon is a standalone warhammer anchored to hand.
7. Winding key is a standalone brass key anchored to back_key.
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
# 1. STANDALONE EYES (90 x 60, origin=[45, 30])
# -----------------------------------------------------------------------------
w_e, h_e = 90, 60
cx, cy = 45, 30

# Cyan Emerald Eye
eye_cyan = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
dc = ImageDraw.Draw(eye_cyan)
dc.ellipse([cx - 15, cy - 14, cx + 15, cy + 14], fill=(20, 18, 25, 255), outline=(130, 105, 50, 255), width=2)
dc.ellipse([cx - 13, cy - 12, cx + 13, cy + 12], fill=(12, 85, 95, 255))
dc.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(25, 175, 185, 255))
dc.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(55, 240, 230, 255))
dc.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(10, 38, 42, 255))
dc.ellipse([cx + 2, cy - 5, cx + 6, cy - 1], fill=(255, 255, 255, 255))
dc.ellipse([cx - 4, cy + 1, cx - 2, cy + 3], fill=(210, 255, 255, 220))
eye_cyan.save(f"{PARTS_DIR}/eyes/eyes_cyan_emerald.png")

# Amber Gold Eye
eye_amber = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
da = ImageDraw.Draw(eye_amber)
da.ellipse([cx - 15, cy - 14, cx + 15, cy + 14], fill=(26, 15, 10, 255), outline=(165, 90, 25, 255), width=2)
da.ellipse([cx - 13, cy - 12, cx + 13, cy + 12], fill=(125, 40, 10, 255))
da.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(220, 110, 18, 255))
da.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(255, 190, 40, 255))
da.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(48, 18, 8, 255))
da.ellipse([cx + 2, cy - 5, cx + 6, cy - 1], fill=(255, 255, 255, 255))
da.ellipse([cx - 4, cy + 1, cx - 2, cy + 3], fill=(255, 230, 170, 220))
eye_amber.save(f"{PARTS_DIR}/eyes/eyes_amber_gold.png")

# Blink Lid
eye_blink = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
db = ImageDraw.Draw(eye_blink)
db.arc([cx - 15, cy - 11, cx + 15, cy + 11], start=10, end=170, fill=(35, 25, 45, 255), width=4)
db.line([(cx - 14, cy), (cx + 14, cy)], fill=(25, 20, 35, 255), width=3)
db.line([(cx - 11, cy - 1), (cx + 11, cy - 1)], fill=(245, 205, 55, 240), width=1)
eye_blink.save(f"{PARTS_DIR}/eyes/eyes_blink.png")
print("✓ Eyes created")

# -----------------------------------------------------------------------------
# 2. STANDALONE HEAD UNITS (4 variants, from raw 512, unbaked eyes)
# -----------------------------------------------------------------------------
crop_box = (132, 35, 398, 177) # size (266, 142), origin=[118, 141]
h_origin = [118, 141]

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
    
    # 覆蓋眼窩內發光像素，填補為深色金屬暗面
    for y in range(145, 173):
        for x in range(226, 253):
            r, g, b, a = arr[y, x]
            if (int(g) > int(r) + 15 and int(g) > 90) or (int(g) > 115 and int(b) > 115 and int(r) < 135):
                arr[y, x] = [28, 24, 34, 255]

    clean_h = Image.fromarray(arr, mode="RGBA").crop(crop_box)
    clean_h.save(f"{PARTS_DIR}/head_unit/{out_name}.png")
print("✓ Heads created")

# -----------------------------------------------------------------------------
# 3. STANDALONE WINDING KEY (雄獅高精發條鑰匙，去背完全透明)
# -----------------------------------------------------------------------------
lion_key_path = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion/maple_parts/winding_key/key_classic_brass.png"
lion_k = Image.open(lion_key_path).convert("RGBA")
# 雄獅發條鑰匙有效主體在 (24, 0, 105, 145)
crop_k = lion_k.crop((24, 0, 105, 145))
arr_k = np.array(crop_k)

for y in range(len(arr_k)):
    for x in range(len(arr_k[0])):
        r, g, b, a = arr_k[y, x]
        if a > 0:
            if r > 195 and g > 195 and b > 175:
                arr_k[y, x] = [0, 0, 0, 0]
            elif a < 40:
                arr_k[y, x] = [0, 0, 0, 0]

key_512 = Image.fromarray(arr_k, mode="RGBA").resize((96, 110), Image.Resampling.LANCZOS)
key_512.save(f"{PARTS_DIR}/winding_key/key_classic_brass.png")
k_origin = [18, 80]
print("✓ Winding key created")

# -----------------------------------------------------------------------------
# 4. STANDALONE TAIL (彈簧尾)
# -----------------------------------------------------------------------------
raw_tail = Image.open(f"{BOAR_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
tail_512 = raw_tail.resize((512, 512), Image.Resampling.NEAREST).crop((340, 320, 436, 408))
tail_512.save(f"{PARTS_DIR}/back_curio/curio_spring_tail.png")
tail_origin = [10, 15]
print("✓ Tail created")

# -----------------------------------------------------------------------------
# 5. STANDALONE WEAPON (鐵砧巨錘：純淨錘頭與握柄，消除右側陰影垂直硬切)
# -----------------------------------------------------------------------------
raw_w = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")
arr_w = np.array(raw_w)
for y in range(len(arr_w)):
    for x in range(len(arr_w[0])):
        if y > 495 and x > 185:
            arr_w[y, x] = [0, 0, 0, 0]
        elif y > 500 and arr_w[y, x, 3] < 120:
            arr_w[y, x] = [0, 0, 0, 0]

weapon_512 = Image.fromarray(arr_w, mode="RGBA").crop((63, 270, 215, 502))
weapon_512.save(f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png")
w_origin = [117, 70]
print("✓ Weapon created")

# -----------------------------------------------------------------------------
# 6. PURE METALLIC BODIES (0-ART18: 純淨金屬身軀，嵌有立體能量寶石，100% 0 洞口)
# -----------------------------------------------------------------------------
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

gem_pos = (209, 288)

paints = [
    ("paint_brass_gold", gem_cyan, (140, 105, 45)),
    ("paint_ivory_stock", gem_cyan, (90, 85, 95)),
    ("paint_molten_crimson", gem_crimson, (140, 60, 40))
]

for p_name, gem_img, bg_col in paints:
    ch = Image.open(f"{BOAR_DIR}/chassis/{p_name}_512.png").convert("RGBA")
    arr = np.array(ch)
    
    # 清理胸前核心區域
    for y in range(265, 345):
        for x in range(180, 270):
            d = math.hypot(x - 230, y - 306)
            if d < 28:
                arr[y, x] = [bg_col[0] // 3, bg_col[1] // 3, bg_col[2] // 3, 255]

    cleaned_ch = Image.fromarray(arr, mode="RGBA")
    draw = ImageDraw.Draw(cleaned_ch)
    draw.ellipse([204, 282, 256, 330], fill=(20, 18, 16, 255), outline=bg_col, width=2)
    cleaned_ch.alpha_composite(gem_img, gem_pos)
    
    cleaned_ch.save(f"{PARTS_DIR}/body/{p_name}.png")
print("✓ Bodies created")

# -----------------------------------------------------------------------------
# 7. STANDALONE COSTUMES (Harness & Ironclad: 核心處留空露出底盤寶石)
# -----------------------------------------------------------------------------
# Harness
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

cos_harness = Image.fromarray(arr_h, mode="RGBA").crop((184, 260, 332, 424))
cos_harness.save(f"{PARTS_DIR}/costume/costume_viking_harness.png")

# Ironclad
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

cos_iron = Image.fromarray(arr_i, mode="RGBA").crop((192, 180, 372, 384))
cos_iron.save(f"{PARTS_DIR}/costume/costume_viking_ironclad.png")
print("✓ Costumes created")

# -----------------------------------------------------------------------------
# 8. SPEC JSON
# -----------------------------------------------------------------------------
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
                    "origin": h_origin
                },
                "ear_boar_rivet_cowl_ivory": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_ivory.png",
                    "width": 266,
                    "height": 142,
                    "origin": h_origin
                },
                "ear_boar_rivet_cowl_crimson": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_crimson.png",
                    "width": 266,
                    "height": 142,
                    "origin": h_origin
                },
                "ear_boar_rivet_cowl": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl.png",
                    "width": 266,
                    "height": 142,
                    "origin": h_origin
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
                    "width": cos_harness.width,
                    "height": cos_harness.height,
                    "origin": [72, 80]
                },
                "costume_viking_ironclad": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/costume/costume_viking_ironclad.png",
                    "width": cos_iron.width,
                    "height": cos_iron.height,
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
                    "width": weapon_512.width,
                    "height": weapon_512.height,
                    "origin": w_origin
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
                    "width": key_512.width,
                    "height": key_512.height,
                    "origin": k_origin
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
            "z_index": 8,
            "items": {
                "curio_spring_tail": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/back_curio/curio_spring_tail.png",
                    "width": tail_512.width,
                    "height": tail_512.height,
                    "origin": tail_origin
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
print("✓ Saved JSON spec")
