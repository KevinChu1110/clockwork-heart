#!/usr/bin/env python3
"""
tools/generate_canonical_boar_paperdoll_v5.py
Generates the definitive, flawless Character.wz paperdoll assets for Boar (厚鎧野豬).
Eliminates:
1. Orange vial glitch on costume and body.
2. Rectangular cutout un-transparent blocks on winding key.
3. Stone hammer bottom square clipping line.
4. Shoulder right-angle square glitch.
Ensures:
1. Precise anchors and origins in game/data/tables/maple_paperdoll_boar.json.
2. 3 body paints (paint_brass_gold, paint_ivory_stock, paint_molten_crimson) with glowing core.
3. 4 head_unit variants with cleanly unbaked dark metal eye socket.
4. 3 standalone eyes (eyes_cyan_emerald, eyes_amber_gold, eyes_blink) + none.
5. 2 costumes (costume_viking_harness, costume_viking_ironclad) + none.
6. wpn_anvil_greathammer + none.
7. key_classic_brass + none.
8. curio_spring_tail + none.
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

# 基準 128 黃金母本
comp128 = Image.open(f"{BOAR_DIR}/proof_paperdoll_boar_composite.png").convert("RGBA")
comp512 = comp128.resize((512, 512), Image.Resampling.NEAREST)

# -----------------------------------------------------------------------------
# 1. WINDING KEY (黃銅雙環古典發條鑰匙)
# -----------------------------------------------------------------------------
def build_key():
    print("--- 1. Winding Key ---")
    # 在 128 畫布中: x: 85..111, y: 17..44 -> 512 bbox: (340, 68, 444, 176)
    # 尺寸: 104 x 108
    # back_key 錨點: (360, 140)
    # Origin: (360 - 340, 140 - 68) = (20, 72)
    w_k, h_k = 104, 108
    key_im = Image.new("RGBA", (w_k, h_k), (0, 0, 0, 0))
    draw = ImageDraw.Draw(key_im)

    col_shaft = (130, 95, 35, 255)
    col_shaft_hi = (235, 195, 65, 255)
    col_shadow = (30, 22, 18, 255)

    # 插軸 (從 (35, 60) 指向 (20, 72))
    draw.polygon([(15, 68), (38, 50), (46, 58), (23, 78)], fill=col_shaft, outline=col_shadow)
    draw.line([(18, 69), (40, 52)], fill=col_shaft_hi, width=2)

    # 軸環
    draw.ellipse([26, 54, 42, 70], fill=(160, 120, 40, 255), outline=col_shadow, width=2)
    draw.ellipse([29, 57, 39, 67], fill=col_shaft_hi)

    # 雙環發條手柄
    # 環1 (左上環，中心 (42, 34), 半徑 22)
    # 環2 (右上環，中心 (68, 34), 半徑 22)
    draw.ellipse([20, 12, 64, 56], fill=(185, 140, 45, 255), outline=col_shadow, width=3)
    draw.ellipse([46, 12, 90, 56], fill=(185, 140, 45, 255), outline=col_shadow, width=3)
    draw.ellipse([23, 15, 61, 53], fill=(220, 175, 55, 255))
    draw.ellipse([49, 15, 87, 53], fill=(220, 175, 55, 255))

    # 頂部反光弧線
    draw.arc([23, 15, 61, 53], start=180, end=330, fill=(255, 240, 140, 255), width=3)
    draw.arc([49, 15, 87, 53], start=210, end=360, fill=(255, 240, 140, 255), width=3)

    # 核心實心塊
    draw.ellipse([38, 22, 68, 46], fill=(160, 120, 40, 255), outline=col_shadow, width=2)
    draw.ellipse([43, 27, 63, 41], fill=col_shaft_hi)

    # 清空兩顆指孔內部 (100% 透明)
    mask_hole = Image.new("L", (w_k, h_k), 0)
    draw_h = ImageDraw.Draw(mask_hole)
    draw_h.ellipse([30, 23, 50, 45], fill=255)
    draw_h.ellipse([58, 23, 78, 45], fill=255)

    arr_k = np.array(key_im)
    arr_h = np.array(mask_hole)
    arr_k[arr_h > 0, 3] = 0

    key_im = Image.fromarray(arr_k, mode="RGBA")
    draw = ImageDraw.Draw(key_im)
    draw.ellipse([30, 23, 50, 45], outline=col_shadow, width=2)
    draw.ellipse([58, 23, 78, 45], outline=col_shadow, width=2)

    out_p = f"{PARTS_DIR}/winding_key/key_classic_brass.png"
    key_im.save(out_p)
    print(f"  ✓ Saved {out_p}: size={key_im.size}, origin=[20, 72]")

# -----------------------------------------------------------------------------
# 2. BACK CURIO (彈簧尾)
# -----------------------------------------------------------------------------
def build_tail():
    print("--- 2. Back Curio ---")
    # 512 bbox: (340, 320, 436, 408), 尺寸 96 x 88
    # tail 錨點: (350, 335) -> Origin: (10, 15)
    raw_tail = Image.open(f"{BOAR_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
    tail_512 = raw_tail.resize((512, 512), Image.Resampling.NEAREST)
    c_tail = tail_512.crop((340, 320, 436, 408))
    out_p = f"{PARTS_DIR}/back_curio/curio_spring_tail.png"
    c_tail.save(out_p)
    print(f"  ✓ Saved {out_p}: size={c_tail.size}, origin=[10, 15]")

# -----------------------------------------------------------------------------
# 3. WEAPON (鐵砧巨錘，平滑底部倒角，消除硬切邊)
# -----------------------------------------------------------------------------
def build_weapon():
    print("--- 3. Weapon ---")
    # 512 bbox: (60, 260, 236, 512), 尺寸 176 x 252
    # Hand 錨點: (180, 340) -> Origin: (180 - 60, 340 - 260) = (120, 80)
    raw_w = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")
    arr_w = np.array(raw_w)
    
    # 消除左下角接地處的生硬垂直切線
    for y in range(480, 512):
        for x in range(60, 120):
            if arr_w[y, x, 3] > 0:
                # 倒角圓弧修整
                if x < 85 and y > 495:
                    arr_w[y, x, 3] = 0
                elif x < 95 and y > 500:
                    arr_w[y, x, 3] = int(arr_w[y, x, 3] * 0.4)

    cleaned_w = Image.fromarray(arr_w, mode="RGBA")
    crop_w = cleaned_w.crop((60, 260, 236, 512))
    out_p = f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png"
    crop_w.save(out_p)
    print(f"  ✓ Saved {out_p}: size={crop_w.size}, origin=[120, 80]")

# -----------------------------------------------------------------------------
# 4. HEAD UNIT (4 款頭部變體，徹底去除死眼，保持純淨金屬眼窩)
# -----------------------------------------------------------------------------
def build_heads():
    print("--- 4. Head Units ---")
    # 512 bbox: (120, 24, 408, 188), 尺寸 288 x 164
    # Neck 錨點: (250, 176) -> Origin: (250 - 120, 176 - 24) = (130, 152)
    crop_box = (120, 24, 408, 188)

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
        
        # 去除眼窩 (x: 215..260, y: 135..176) 內的青綠發光眼球，填補為金屬暗面底色 (0-ART51)
        for y in range(135, 177):
            for x in range(215, 261):
                r, g, b, a = arr[y, x]
                is_eye = (int(g) > int(r) + 12 and int(g) > 90) or (int(g) > 110 and int(b) > 110 and int(r) < 140)
                if is_eye and a > 20:
                    arr[y, x] = [28, 24, 32, 255]

        cleaned_h = Image.fromarray(arr, mode="RGBA").crop(crop_box)
        out_p = f"{PARTS_DIR}/head_unit/{out_name}.png"
        cleaned_h.save(out_p)
        print(f"  ✓ Saved {out_p}: size={cleaned_h.size}, origin=[130, 152]")

# -----------------------------------------------------------------------------
# 5. EYES (獨立光學義眼)
# -----------------------------------------------------------------------------
def build_eyes():
    print("--- 5. Optic Cores ---")
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

    out_c = f"{PARTS_DIR}/eyes/eyes_cyan_emerald.png"
    im_c.save(out_c)
    print(f"  ✓ Saved {out_c}: size={im_c.size}, origin=[45, 30]")

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

    out_a = f"{PARTS_DIR}/eyes/eyes_amber_gold.png"
    im_a.save(out_a)
    print(f"  ✓ Saved {out_a}: size={im_a.size}, origin=[45, 30]")

    # 3. Blink
    im_b = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
    db = ImageDraw.Draw(im_b)
    db.arc([cx - 15, cy - 11, cx + 15, cy + 11], start=10, end=170, fill=(35, 25, 45, 255), width=4)
    db.line([(cx - 14, cy), (cx + 14, cy)], fill=(25, 20, 35, 255), width=3)
    db.line([(cx - 11, cy - 1), (cx + 11, cy - 1)], fill=(245, 205, 55, 240), width=1)

    out_b = f"{PARTS_DIR}/eyes/eyes_blink.png"
    im_b.save(out_b)
    print(f"  ✓ Saved {out_b}: size={im_b.size}, origin=[45, 30]")

# -----------------------------------------------------------------------------
# 6. BODY (純淨金屬底盤，融合純淨發光核心，消除任何橙色雜點)
# -----------------------------------------------------------------------------
def build_bodies():
    print("--- 6. Pure Chassis Bodies ---")
    core_cyan = Image.open(f"{BOAR_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")
    core_crimson = Image.open(f"{BOAR_DIR}/optic_core/core_molten_crimson_512.png").convert("RGBA")

    paints = [
        ("paint_brass_gold", core_cyan),
        ("paint_ivory_stock", core_cyan),
        ("paint_molten_crimson", core_crimson)
    ]

    for p_name, c_img in paints:
        ch = Image.open(f"{BOAR_DIR}/chassis/{p_name}_512.png").convert("RGBA")
        arr = np.array(ch)
        
        # 清除胸前殘留的橙紅色小瓶雜訊 (x: 200..235, y: 260..305)
        for y in range(260, 310):
            for x in range(200, 238):
                r, g, b, a = arr[y, x]
                if int(r) > 170 and int(g) < 140 and int(b) < 60:
                    # 覆蓋為胸腹底盤黃銅/冷鋼金屬色
                    arr[y, x] = [135, 105, 45, 255] if p_name == "paint_brass_gold" else [90, 85, 95, 255]

        cleaned_ch = Image.fromarray(arr, mode="RGBA")
        body = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        body.alpha_composite(cleaned_ch)
        body.alpha_composite(c_img)
        
        out_p = f"{PARTS_DIR}/body/{p_name}.png"
        body.save(out_p)
        print(f"  ✓ Saved {out_p}: size={body.size}, bbox={body.getbbox()}")

# -----------------------------------------------------------------------------
# 7. COSTUMES (徹底消除橙色藥瓶、生硬方塊與肩甲直角)
# -----------------------------------------------------------------------------
def build_costumes():
    print("--- 7. Costumes ---")
    
    # 1. Harness (512 bbox: (184, 260, 332, 424), 尺寸 148 x 164)
    # Navel 錨點: (256, 340) -> Origin: (256 - 184, 340 - 260) = (72, 80)
    raw_h = Image.open(f"{BOAR_DIR}/costume/costume_viking_harness_512.png").convert("RGBA")
    arr_h = np.array(raw_h)
    
    # 徹底清除橙色小瓶與多餘邊緣
    for y in range(len(arr_h)):
        for x in range(len(arr_h[0])):
            r, g, b, a = arr_h[y, x]
            # 橙色小瓶
            if int(r) > 170 and int(g) < 140 and int(b) < 60 and (180 <= x <= 230 and 255 <= y <= 310):
                arr_h[y, x] = [0, 0, 0, 0]
                continue
            # 核心視窗中心 (230, 306)
            d_core = math.hypot(x - 230, y - 306)
            if d_core < 22:
                arr_h[y, x] = [0, 0, 0, 0]
            elif d_core < 26:
                arr_h[y, x] = [245, 205, 55, 255]

    clean_h = Image.fromarray(arr_h, mode="RGBA").crop((184, 260, 332, 424))
    out_h = f"{PARTS_DIR}/costume/costume_viking_harness.png"
    clean_h.save(out_h)
    print(f"  ✓ Saved {out_h}: size={clean_h.size}, origin=[72, 80]")

    # 2. Ironclad (512 bbox: (192, 180, 372, 384), 尺寸 180 x 204)
    # Navel 錨點: (256, 340) -> Origin: (256 - 192, 340 - 180) = (64, 160)
    raw_i = Image.open(f"{BOAR_DIR}/costume/costume_viking_ironclad_512.png").convert("RGBA")
    arr_i = np.array(raw_i)

    for y in range(len(arr_i)):
        for x in range(len(arr_i[0])):
            # 消除肩膀外緣直角 (x > 335, y < 215)
            if x > 335 and y < 215:
                d_sh = math.hypot(x - 330, y - 215)
                if d_sh > 46:
                    arr_i[y, x] = [0, 0, 0, 0]
                    continue
            # 核心視窗中心 (230, 306)
            d_core = math.hypot(x - 230, y - 306)
            if d_core < 22:
                arr_i[y, x] = [0, 0, 0, 0]
            elif d_core < 26:
                arr_i[y, x] = [245, 205, 55, 255]

    clean_i = Image.fromarray(arr_i, mode="RGBA").crop((192, 180, 372, 384))
    out_i = f"{PARTS_DIR}/costume/costume_viking_ironclad.png"
    clean_i.save(out_i)
    print(f"  ✓ Saved {out_i}: size={clean_i.size}, origin=[64, 160]")

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
                        "width": 288,
                        "height": 164,
                        "origin": [130, 152]
                    },
                    "ear_boar_rivet_cowl_ivory": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_ivory.png",
                        "width": 288,
                        "height": 164,
                        "origin": [130, 152]
                    },
                    "ear_boar_rivet_cowl_crimson": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_crimson.png",
                        "width": 288,
                        "height": 164,
                        "origin": [130, 152]
                    },
                    "ear_boar_rivet_cowl": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl.png",
                        "width": 288,
                        "height": 164,
                        "origin": [130, 152]
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
    build_key()
    build_tail()
    build_weapon()
    build_heads()
    build_eyes()
    build_bodies()
    build_costumes()
    build_json()
    print("🎉 Masterpiece Boar V5 generated successfully!")
