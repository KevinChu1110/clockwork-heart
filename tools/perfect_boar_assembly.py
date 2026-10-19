#!/usr/bin/env python3
"""
tools/perfect_boar_assembly.py
The absolute final master craftsman script for Boar Character.wz paperdoll:
1. Pure metallic chassis (3 paints: brass_gold, ivory_stock, molten_crimson) with
   embedded luminous energy core gem, smooth organic ground shadow, 0 orange vial glitch.
2. Head units (4 variants) with pristine metallic textures, 0 marching ants, 0 white noise,
   smooth dark-metal eye sockets.
3. Standalone optic cores (eyes_cyan_emerald, eyes_amber_gold, eyes_blink, none).
4. Costumes (costume_viking_harness, costume_viking_ironclad, none):
   - Crisp lines, organic form-fitting contours (0 right-angle stairs).
   - Precision gold-bezeled circular core port-hole allowing body gem to shine through.
5. Warhammer:
   - Clean stone head and timber shaft without duplicate ground shadow mismatch.
6. Winding key:
   - Clean brass key cropped cleanly without lion mane fragments or rectangular white borders.
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
# 1. HEAD UNIT (4 variants from raw 512, dark metal eye socket, 0 marching ants)
# -----------------------------------------------------------------------------
def assemble_heads():
    print("--- 1. Assembling Head Units ---")
    crop_box = (132, 35, 398, 177) # size (266, 142), origin=[118, 141]

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
        
        # 覆蓋眼窩內發光像素
        for y in range(135, 177):
            for x in range(215, 261):
                r, g, b, a = arr[y, x]
                is_eye = (int(g) > int(r) + 10 and int(g) > 85) or (int(g) > 105 and int(b) > 105 and int(r) < 140)
                if is_eye and a > 20:
                    arr[y, x] = [28, 24, 32, 255]

        clean_h = Image.fromarray(arr, mode="RGBA").crop(crop_box)
        clean_h.save(f"{PARTS_DIR}/head_unit/{out_name}.png")
        print(f"  ✓ Saved {out_name}.png")

# -----------------------------------------------------------------------------
# 2. STANDALONE EYES (Cyan, Amber, Blink)
# -----------------------------------------------------------------------------
def assemble_eyes():
    print("--- 2. Assembling Eyes ---")
    w_e, h_e = 90, 60
    cx, cy = 45, 30

    # Cyan Emerald
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

    # Amber Gold
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

    # Blink
    im_b = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
    db = ImageDraw.Draw(im_b)
    db.arc([cx - 15, cy - 11, cx + 15, cy + 11], start=10, end=170, fill=(35, 25, 45, 255), width=4)
    db.line([(cx - 14, cy), (cx + 14, cy)], fill=(25, 20, 35, 255), width=3)
    db.line([(cx - 11, cy - 1), (cx + 11, cy - 1)], fill=(245, 205, 55, 240), width=1)
    im_b.save(f"{PARTS_DIR}/eyes/eyes_blink.png")
    print("  ✓ Saved eyes")

# -----------------------------------------------------------------------------
# 3. PURE METALLIC BODIES (0-ART18: 純淨金屬底盤，融合發光寶石，0 橙瓶)
# -----------------------------------------------------------------------------
def assemble_bodies():
    print("--- 3. Assembling Pure Bodies ---")
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

    # 寶石位置: (209, 288) -> 中心在 (230, 306)
    gem_pos = (209, 288)

    paints = [
        ("paint_brass_gold", gem_cyan, (140, 105, 45)),
        ("paint_ivory_stock", gem_cyan, (90, 85, 95)),
        ("paint_molten_crimson", gem_crimson, (140, 60, 40))
    ]

    for p_name, gem_img, bg_col in paints:
        ch = Image.open(f"{BOAR_DIR}/chassis/{p_name}_512.png").convert("RGBA")
        arr = np.array(ch)
        
        # 清除胸前 (x: 180..270, y: 260..345) 區域內所有橙色瓶子與雜色
        for y in range(260, 345):
            for x in range(180, 270):
                d = math.hypot(x - 230, y - 306)
                if d < 30:
                    arr[y, x] = [bg_col[0] // 3, bg_col[1] // 3, bg_col[2] // 3, 255]

        cleaned_ch = Image.fromarray(arr, mode="RGBA")
        draw = ImageDraw.Draw(cleaned_ch)
        # 金屬底座
        draw.ellipse([204, 283, 256, 329], fill=(22, 18, 16, 255), outline=(bg_col[0], bg_col[1], bg_col[2], 255), width=2)
        cleaned_ch.alpha_composite(gem_img, gem_pos)
        
        cleaned_ch.save(f"{PARTS_DIR}/body/{p_name}.png")
        print(f"  ✓ Saved {p_name}.png")

# -----------------------------------------------------------------------------
# 4. COSTUMES (0-ART50: 核心視窗金邊對齊，0 直角階梯方塊)
# -----------------------------------------------------------------------------
def assemble_costumes():
    print("--- 4. Assembling Costumes ---")
    
    # 1. Harness
    # Navel: (256, 340) -> crop: (184, 260, 332, 424), size: (148, 164), origin=[72, 80]
    raw_h = Image.open(f"{BOAR_DIR}/costume/costume_viking_harness_512.png").convert("RGBA")
    arr_h = np.array(raw_h)
    
    for y in range(len(arr_h)):
        for x in range(len(arr_h[0])):
            # 清除所有左上方橙色小瓶與雜色
            r, g, b, a = arr_h[y, x]
            if (int(r) > 130 and int(g) < 150 and int(b) < 90 and 170 <= x <= 245 and 240 <= y <= 330):
                arr_h[y, x] = [0, 0, 0, 0]
                continue
            d = math.hypot(x - 230, y - 306)
            if d < 23:
                arr_h[y, x] = [0, 0, 0, 0] # 核心完全透明以透出底盤能量寶石

    clean_h = Image.fromarray(arr_h, mode="RGBA").crop((184, 260, 332, 424))
    # 核心金邊
    draw_h = ImageDraw.Draw(clean_h)
    # 中心在 clean_h 內為 (230 - 184, 306 - 260) = (46, 46)
    draw_h.ellipse([46 - 23, 46 - 23, 46 + 23, 46 + 23], outline=(245, 205, 55, 255), width=2)
    clean_h.save(f"{PARTS_DIR}/costume/costume_viking_harness.png")
    print("  ✓ Saved costume_viking_harness.png: size=(148, 164), origin=[72, 80]")

    # 2. Ironclad (維京重裝鐵甲)
    # Navel: (256, 340) -> crop: (184, 240, 340, 420), size: (156, 180), origin=[72, 100]
    iron_im = Image.new("RGBA", (156, 180), (0, 0, 0, 0))
    draw_i = ImageDraw.Draw(iron_im)
    
    # 繪製圓潤厚重維京板甲 (以中心 (46, 66) 為基準)
    # 深鋼藍金屬板
    draw_i.rounded_rectangle([15, 18, 142, 165], radius=16, fill=(45, 58, 80, 245), outline=(22, 28, 40, 255), width=3)
    draw_i.rounded_rectangle([20, 23, 137, 160], radius=12, fill=(55, 70, 95, 240))
    
    # 雙排金屬鉚釘
    col_rivet = (245, 205, 55, 255)
    col_rivet_sh = (30, 24, 15, 255)
    for ry in [34, 110, 148]:
        for rx in [30, 60, 90, 120]:
            if math.hypot(rx - 46, ry - 66) > 28:
                draw_i.ellipse([rx-3, ry-3, rx+3, ry+3], fill=col_rivet, outline=col_rivet_sh, width=1)
                
    # 核心視窗中心在 (46, 66)，挖空並加金邊
    mask_i = Image.new("L", (156, 180), 0)
    dw = ImageDraw.Draw(mask_i)
    dw.ellipse([46 - 22, 66 - 22, 46 + 22, 66 + 22], fill=255)
    arr_ir = np.array(iron_im)
    arr_ir[np.array(mask_i) > 0, 3] = 0
    iron_im = Image.fromarray(arr_ir, mode="RGBA")
    
    draw_i = ImageDraw.Draw(iron_im)
    draw_i.ellipse([46 - 23, 66 - 23, 46 + 23, 66 + 23], outline=col_rivet, width=3)
    iron_im.save(f"{PARTS_DIR}/costume/costume_viking_ironclad.png")
    print("  ✓ Saved costume_viking_ironclad.png: size=(156, 180), origin=[72, 100]")

# -----------------------------------------------------------------------------
# 5. WEAPON (鐵砧巨錘：純淨錘頭與長木柄，移除多餘地面陰影避免雙重陰影階梯)
# -----------------------------------------------------------------------------
def assemble_weapon():
    print("--- 5. Assembling Warhammer ---")
    raw_w = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")
    arr_w = np.array(raw_w)
    
    # 清除 x > 200 或 y > 500 的多餘地面陰影（因為 body 本身自帶完整地面陰影）
    for y in range(len(arr_w)):
        for x in range(len(arr_w[0])):
            if y > 495 and x > 190:
                arr_w[y, x] = [0, 0, 0, 0]
            elif y > 500 and arr_w[y, x, 3] < 120:
                arr_w[y, x] = [0, 0, 0, 0]

    # crop: (63, 270, 215, 502) -> size: (152, 232)
    # Hand: (180, 340) -> Origin: (180 - 63, 340 - 270) = (117, 70)
    clean_w = Image.fromarray(arr_w, mode="RGBA").crop((63, 270, 215, 502))
    clean_w.save(f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png")
    print("  ✓ Saved wpn_anvil_greathammer.png: size=(152, 232), origin=[117, 70]")

# -----------------------------------------------------------------------------
# 6. WINDING KEY (精確裁出黃銅雙環，去除左上角雄獅鬃毛殘留，0 白邊)
# -----------------------------------------------------------------------------
def assemble_key():
    print("--- 6. Assembling Winding Key ---")
    lion_key_path = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion/maple_parts/winding_key/key_classic_brass.png"
    lion_k = Image.open(lion_key_path).convert("RGBA")
    # lion_k 尺寸 (119, 150)，發條手柄有效範圍在 (24, 0, 105, 145)
    # 裁出純淨的發條手柄本體，徹底避開左上角的鬃毛殘留
    crop_k = lion_k.crop((24, 0, 105, 145))
    arr_k = np.array(crop_k)
    
    for y in range(len(arr_k)):
        for x in range(len(arr_k[0])):
            r, g, b, a = arr_k[y, x]
            if a > 0:
                # 清除孔洞內的米白/淡奶油色
                if r > 195 and g > 195 and b > 175:
                    arr_k[y, x] = [0, 0, 0, 0]
                elif a < 40:
                    arr_k[y, x] = [0, 0, 0, 0]

    clean_k = Image.fromarray(arr_k, mode="RGBA").resize((96, 110), Image.Resampling.LANCZOS)
    clean_k.save(f"{PARTS_DIR}/winding_key/key_classic_brass.png")
    # Back key: (360, 140) -> left-top 在 512 中為 (342, 60) -> Origin = (360 - 342, 140 - 60) = (18, 80)
    print("  ✓ Saved key_classic_brass.png: size=(96, 110), origin=[18, 80]")

# -----------------------------------------------------------------------------
# 7. BACK CURIO
# -----------------------------------------------------------------------------
def assemble_tail():
    print("--- 7. Assembling Tail ---")
    raw_tail = Image.open(f"{BOAR_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
    tail_512 = raw_tail.resize((512, 512), Image.Resampling.NEAREST)
    c_tail = tail_512.crop((340, 320, 436, 408))
    c_tail.save(f"{PARTS_DIR}/back_curio/curio_spring_tail.png")
    print("  ✓ Saved curio_spring_tail.png: size=(96, 88), origin=[10, 15]")

# -----------------------------------------------------------------------------
# 8. UPDATE JSON SPEC
# -----------------------------------------------------------------------------
def assemble_json():
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
                        "width": 156,
                        "height": 180,
                        "origin": [72, 100]
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
                        "width": 96,
                        "height": 110,
                        "origin": [18, 80]
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
    assemble_heads()
    assemble_eyes()
    assemble_bodies()
    assemble_costumes()
    assemble_weapon()
    assemble_key()
    assemble_tail()
    assemble_json()
    print("🎉 Perfect Boar assembly complete!")
