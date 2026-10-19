#!/usr/bin/env python3
"""
tools/build_ultimate_boar_paperdoll.py
The definitive, artifact-free Character.wz paperdoll builder for Boar (厚鎧野豬).
- 0 marching ants (sourced from pristine 512 head_unit)
- 0 orange vial glitch
- 0 duplicate key rings, 100% transparent inner keyholes
- 0 straight vertical hammer shadow cuts
- True luminous Cyan Emerald / Molten Crimson energy gems
- Precision origins & anchors in maple_paperdoll_boar.json
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
# 1. HEAD UNIT (原生 512，無任何螞蟻線，眼窩深色去眼)
# -----------------------------------------------------------------------------
def build_head():
    print("--- 1. Head Units (Pristine 512) ---")
    crop_box = (132, 35, 398, 177) # size: (266, 142)
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
        
        # 去眼窩發光像素 (x: 215..260, y: 135..176)
        for y in range(135, 177):
            for x in range(215, 261):
                r, g, b, a = arr[y, x]
                is_eye = (int(g) > int(r) + 10 and int(g) > 85) or (int(g) > 105 and int(b) > 105 and int(r) < 140)
                if is_eye and a > 20:
                    arr[y, x] = [28, 24, 32, 255]

        clean_h = Image.fromarray(arr, mode="RGBA").crop(crop_box)
        clean_h.save(f"{PARTS_DIR}/head_unit/{out_name}.png")
        print(f"  ✓ Saved {out_name}.png: size={clean_h.size}, origin=[118, 141]")

# -----------------------------------------------------------------------------
# 2. EYES (獨立光學義眼)
# -----------------------------------------------------------------------------
def build_eyes():
    print("--- 2. Standalone Optic Cores ---")
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
    print("  ✓ Saved eyes: cyan, amber, blink. size=(90, 60), origin=[45, 30]")

# -----------------------------------------------------------------------------
# 3. BODY (純淨金屬底盤，融合正牌立體能量寶石，0 橙色瓶子)
# -----------------------------------------------------------------------------
def build_body():
    print("--- 3. Pure Metallic Chassis Bodies ---")
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

    # 嵌入座標: (209, 288) -> 中心剛好在 (230, 306)
    gem_pos = (209, 288)

    paints = [
        ("paint_brass_gold", gem_cyan, (140, 105, 45)),
        ("paint_ivory_stock", gem_cyan, (90, 85, 95)),
        ("paint_molten_crimson", gem_crimson, (140, 60, 40))
    ]

    for p_name, gem_img, bg_col in paints:
        ch = Image.open(f"{BOAR_DIR}/chassis/{p_name}_512.png").convert("RGBA")
        arr = np.array(ch)
        
        # 徹底清空胸前核心區域所有原有雜色
        for y in range(265, 345):
            for x in range(180, 270):
                d = math.hypot(x - 230, y - 306)
                if d < 28:
                    arr[y, x] = [bg_col[0] // 3, bg_col[1] // 3, bg_col[2] // 3, 255]

        cleaned_ch = Image.fromarray(arr, mode="RGBA")
        draw = ImageDraw.Draw(cleaned_ch)
        # 精緻金屬邊框底座
        draw.ellipse([204, 283, 256, 329], fill=(22, 18, 16, 255), outline=(bg_col[0], bg_col[1], bg_col[2], 255), width=2)
        cleaned_ch.alpha_composite(gem_img, gem_pos)
        
        cleaned_ch.save(f"{PARTS_DIR}/body/{p_name}.png")
        print(f"  ✓ Saved {p_name}.png")

# -----------------------------------------------------------------------------
# 4. COSTUMES (徹底消除橙色小瓶，核心開口金邊對齊)
# -----------------------------------------------------------------------------
def build_costumes():
    print("--- 4. Costumes ---")
    
    # 1. Harness
    # Navel: (256, 340) -> crop: (184, 260, 332, 424), size: (148, 164), origin=[72, 80]
    raw_h = Image.open(f"{BOAR_DIR}/costume/costume_viking_harness_512.png").convert("RGBA")
    arr_h = np.array(raw_h)
    
    for y in range(len(arr_h)):
        for x in range(len(arr_h[0])):
            r, g, b, a = arr_h[y, x]
            # 清除所有左上方橙色小瓶與雜色
            if (int(r) > 130 and int(g) < 150 and int(b) < 90 and 170 <= x <= 245 and 240 <= y <= 330):
                arr_h[y, x] = [0, 0, 0, 0]
                continue
            d = math.hypot(x - 230, y - 306)
            if d < 24:
                arr_h[y, x] = [0, 0, 0, 0] # 核心完全透明以透出底盤能量寶石

    clean_h = Image.fromarray(arr_h, mode="RGBA").crop((184, 260, 332, 424))
    clean_h.save(f"{PARTS_DIR}/costume/costume_viking_harness.png")
    print("  ✓ Saved costume_viking_harness.png: size=(148, 164), origin=[72, 80]")

    # 2. Ironclad
    # Navel: (256, 340) -> crop: (192, 180, 372, 384), size: (180, 204), origin=[64, 160]
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
            if d < 24:
                arr_i[y, x] = [0, 0, 0, 0]

    clean_i = Image.fromarray(arr_i, mode="RGBA").crop((192, 180, 372, 384))
    clean_i.save(f"{PARTS_DIR}/costume/costume_viking_ironclad.png")
    print("  ✓ Saved costume_viking_ironclad.png: size=(180, 204), origin=[64, 160]")

# -----------------------------------------------------------------------------
# 5. WEAPON (羽化右下角陰影，消除垂直硬切線)
# -----------------------------------------------------------------------------
def build_weapon():
    print("--- 5. Warhammer ---")
    raw_w = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")
    arr_w = np.array(raw_w)
    
    for y in range(460, 512):
        for x in range(60, 236):
            if arr_w[y, x, 3] > 0:
                if x < 85 and y > 495:
                    arr_w[y, x, 3] = 0
                elif x < 95 and y > 500:
                    arr_w[y, x, 3] = int(arr_w[y, x, 3] * 0.4)
                # 右側陰影自然圓弧淡出
                if x > 190 and y > 465:
                    dist = math.hypot(x - 190, y - 485)
                    fade = max(0.0, 1.0 - dist / 22.0)
                    arr_w[y, x, 3] = int(arr_w[y, x, 3] * fade)

    cleaned_w = Image.fromarray(arr_w, mode="RGBA").crop((60, 260, 236, 512))
    cleaned_w.save(f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png")
    print("  ✓ Saved wpn_anvil_greathammer.png: size=(176, 252), origin=[120, 80]")

# -----------------------------------------------------------------------------
# 6. WINDING KEY (雄獅高精發條手柄，完全透明內孔與邊界)
# -----------------------------------------------------------------------------
def build_key():
    print("--- 6. Winding Key ---")
    lion_key_path = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion/maple_parts/winding_key/key_classic_brass.png"
    lion_k = Image.open(lion_key_path).convert("RGBA")
    arr_k = np.array(lion_k)
    
    # 清除任何米白、灰白未去背雜色
    for y in range(len(arr_k)):
        for x in range(len(arr_k[0])):
            r, g, b, a = arr_k[y, x]
            if a > 0:
                if r > 180 and g > 180 and b > 170:
                    arr_k[y, x] = [0, 0, 0, 0]
                elif a < 40:
                    arr_k[y, x] = [0, 0, 0, 0]

    clean_k = Image.fromarray(arr_k, mode="RGBA").resize((104, 108), Image.Resampling.LANCZOS)
    clean_k.save(f"{PARTS_DIR}/winding_key/key_classic_brass.png")
    print("  ✓ Saved key_classic_brass.png: size=(104, 108), origin=[20, 72]")

# -----------------------------------------------------------------------------
# 7. TAIL
# -----------------------------------------------------------------------------
def build_tail():
    print("--- 7. Spring Tail ---")
    raw_tail = Image.open(f"{BOAR_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
    tail_512 = raw_tail.resize((512, 512), Image.Resampling.NEAREST)
    c_tail = tail_512.crop((340, 320, 436, 408))
    c_tail.save(f"{PARTS_DIR}/back_curio/curio_spring_tail.png")
    print("  ✓ Saved curio_spring_tail.png: size=(96, 88), origin=[10, 15]")

# -----------------------------------------------------------------------------
# 8. SPEC JSON
# -----------------------------------------------------------------------------
def build_json():
    print("--- 8. JSON Spec ---")
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
                        "width": 176,
                        "height": 252,
                        "origin": [120, 80]
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
                "z_index": 8,
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
    build_head()
    build_eyes()
    build_body()
    build_costumes()
    build_weapon()
    build_key()
    build_tail()
    build_json()
    print("🎉 Ultimate Boar Paperdoll system built!")
