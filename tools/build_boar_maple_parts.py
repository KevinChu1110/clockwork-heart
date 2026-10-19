#!/usr/bin/env python3
"""
tools/build_boar_maple_parts.py
Builds Character.wz style tight slices and origins for Boar (厚鎧野豬).
Conforms to review.md 0-ART50 / 0-ART51 / 0-ART18 standards:
1. Pure metallic chassis without placeholder solid blocks; eyes not baked in head.
2. Tight slices with precise origin coordinates.
3. Clean boundaries without stray noise, dark clipping lines, or artifacts.
4. Generates maple_paperdoll_boar.json table.
"""

import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
SRC_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
OUT_DIR = f"{SRC_DIR}/maple_parts"
JSON_PATH = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_boar.json"

def ensure_dirs():
    for sub in ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]:
        os.makedirs(f"{OUT_DIR}/{sub}", exist_ok=True)

def build_body_slices():
    print("--- 1. Building Body Slices ---")
    core_cyan = Image.open(f"{SRC_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")
    core_crimson = Image.open(f"{SRC_DIR}/optic_core/core_molten_crimson_512.png").convert("RGBA")

    paints = [
        ("paint_brass_gold", core_cyan),
        ("paint_ivory_stock", core_cyan),
        ("paint_molten_crimson", core_crimson)
    ]

    for paint_name, core_img in paints:
        chassis_path = f"{SRC_DIR}/chassis/{paint_name}_512.png"
        chassis = Image.open(chassis_path).convert("RGBA")
        
        # Composite chassis with chest core
        body = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        body.alpha_composite(chassis)
        body.alpha_composite(core_img)

        out_path = f"{OUT_DIR}/body/{paint_name}.png"
        body.save(out_path)
        print(f"  ✓ {out_path}: {body.size}, bbox={body.getbbox()}")

def build_head_unit_slices():
    print("--- 2. Building Head Unit Slices (Eyes unbaked) ---")
    # Head bbox in 512: (132, 35, 398, 177) -> width: 266, height: 142
    # Neck anchor in 512: (250, 176) -> Origin: (250 - 132, 176 - 35) = (118, 141)
    crop_box = (132, 35, 398, 177)
    
    variants = [
        ("ear_boar_rivet_cowl_brass", "ear_boar_rivet_cowl_brass_512.png"),
        ("ear_boar_rivet_cowl_ivory", "ear_boar_rivet_cowl_ivory_512.png"),
        ("ear_boar_rivet_cowl_crimson", "ear_boar_rivet_cowl_crimson_512.png"),
        ("ear_boar_rivet_cowl", "ear_boar_rivet_cowl_512.png")
    ]

    for out_name, src_file in variants:
        src_path = f"{SRC_DIR}/head_unit/{src_file}"
        im = Image.open(src_path).convert("RGBA")
        
        # 移除眼窩內部的發光眼球像素，替換為深色金屬眼窩底面，確保眼睛不畫死在頭部上 (0-ART51)
        arr = np.array(im)
        # Eye region in 512: X: 221..255, Y: 142..174
        for y in range(142, 175):
            for x in range(221, 256):
                # 判斷是否為青藍/發光眼球像素
                r, g, b, a = arr[y, x]
                if a > 50 and (g > 115 and (g > r + 15 or (g > 130 and b > 130))):
                    # 替換為眼窩金屬暗陰影色 (28, 24, 38, 255) 帶漸層
                    depth_factor = 1.0 - (float(y - 142) / 33.0) * 0.3
                    base_r = int(24 * depth_factor)
                    base_g = int(20 * depth_factor)
                    base_b = int(32 * depth_factor)
                    arr[y, x] = [base_r, base_g, base_b, 255]

        cleaned_im = Image.fromarray(arr, mode="RGBA")
        cropped = cleaned_im.crop(crop_box)
        out_path = f"{OUT_DIR}/head_unit/{out_name}.png"
        cropped.save(out_path)
        print(f"  ✓ {out_path}: {cropped.size}, origin=[118, 141], bbox={cropped.getbbox()}")

def build_eyes_slices():
    print("--- 3. Building Eyes Slices ---")
    # Brow anchor in 512: (235, 161)
    # Eye canvas: 90 x 60 centered around (235, 161)
    # Origin: (45, 30)
    w_eye, h_eye = 90, 60
    cx_canvas, cy_canvas = 45, 30

    # 1. Cyan Emerald Eye
    im_cyan = Image.new("RGBA", (w_eye, h_eye), (0, 0, 0, 0))
    draw_c = ImageDraw.Draw(im_cyan)
    
    # 從原 512 head 截取發光眼球像素並放置在 center (45, 30)
    head_brass = Image.open(f"{SRC_DIR}/head_unit/ear_boar_rivet_cowl_brass_512.png").convert("RGBA")
    h_arr = np.array(head_brass)
    
    # 提取 (221, 142, 255, 174) 內的眼球像素
    for y in range(142, 175):
        for x in range(221, 256):
            r, g, b, a = h_arr[y, x]
            if a > 50 and (g > 115 and (g > r + 10 or (g > 130 and b > 130))):
                dx = x - 235
                dy = y - 161
                tx = cx_canvas + dx
                ty = cy_canvas + dy
                if 0 <= tx < w_eye and 0 <= ty < h_eye:
                    im_cyan.putpixel((tx, ty), (r, g, b, a))

    out_cyan = f"{OUT_DIR}/eyes/eyes_cyan_emerald.png"
    im_cyan.save(out_cyan)
    print(f"  ✓ {out_cyan}: {im_cyan.size}, origin=[45, 30], bbox={im_cyan.getbbox()}")

    # 2. Amber Gold / Molten Crimson Eye
    im_amber = Image.new("RGBA", (w_eye, h_eye), (0, 0, 0, 0))
    for y in range(h_eye):
        for x in range(w_eye):
            r, g, b, a = im_cyan.getpixel((x, y))
            if a > 0:
                # 轉為赤焰琥珀金
                lum = (int(r) + int(g) + int(b)) / 3.0
                ar = min(255, int(lum * 1.3 + 40))
                ag = min(255, int(lum * 0.75 + 10))
                ab = min(255, int(lum * 0.2))
                im_amber.putpixel((x, y), (ar, ag, ab, a))

    out_amber = f"{OUT_DIR}/eyes/eyes_amber_gold.png"
    im_amber.save(out_amber)
    print(f"  ✓ {out_amber}: {im_amber.size}, origin=[45, 30], bbox={im_amber.getbbox()}")

    # 3. Eyes Blink (金屬眼瞼閉合線)
    im_blink = Image.new("RGBA", (w_eye, h_eye), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(im_blink)
    # 閉合眼瞼弧線：center ~ (45, 30), span 32..58
    col_shadow = (25, 20, 32, 255)
    col_rim = (245, 205, 55, 255) # 黃銅高光
    draw_b.arc([30, 24, 60, 38], start=10, end=170, fill=col_shadow, width=4)
    draw_b.line([(31, 31), (59, 31)], fill=col_shadow, width=3)
    draw_b.line([(33, 30), (57, 30)], fill=col_rim, width=1)

    out_blink = f"{OUT_DIR}/eyes/eyes_blink.png"
    im_blink.save(out_blink)
    print(f"  ✓ {out_blink}: {im_blink.size}, origin=[45, 30], bbox={im_blink.getbbox()}")

def build_costume_slices():
    print("--- 4. Building Costume Slices ---")
    # Navel anchor in 512: (256, 340)
    # Crop box for Ironclad: (180, 170, 382, 396) -> size (202, 226), origin=[256-180, 340-170] = [76, 170]
    # Crop box for Harness: (180, 256, 336, 426) -> size (156, 170), origin=[256-180, 340-256] = [76, 84]
    
    # 1. Ironclad
    crop_iron = (180, 170, 382, 396)
    im_iron = Image.open(f"{SRC_DIR}/costume/costume_viking_ironclad_512.png").convert("RGBA")
    c_iron = im_iron.crop(crop_iron)
    out_iron = f"{OUT_DIR}/costume/costume_viking_ironclad.png"
    c_iron.save(out_iron)
    print(f"  ✓ {out_iron}: {c_iron.size}, origin=[76, 170], bbox={c_iron.getbbox()}")

    # 2. Harness
    crop_harn = (180, 256, 336, 426)
    im_harn = Image.open(f"{SRC_DIR}/costume/costume_viking_harness_512.png").convert("RGBA")
    c_harn = im_harn.crop(crop_harn)
    out_harn = f"{OUT_DIR}/costume/costume_viking_harness.png"
    c_harn.save(out_harn)
    print(f"  ✓ {out_harn}: {c_harn.size}, origin=[76, 84], bbox={c_harn.getbbox()}")

def build_weapon_slices():
    print("--- 5. Building Weapon Slices ---")
    # Hand anchor in 512: (180, 340)
    # Weapon bbox in 512: (63, 270, 233, 509) -> size (170, 239)
    # Origin: (180 - 63, 340 - 270) = (117, 70)
    crop_box = (63, 270, 233, 509)
    im_w = Image.open(f"{SRC_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")
    c_w = im_w.crop(crop_box)
    out_w = f"{OUT_DIR}/weapon/wpn_anvil_greathammer.png"
    c_w.save(out_w)
    print(f"  ✓ {out_w}: {c_w.size}, origin=[117, 70], bbox={c_w.getbbox()}")

def build_winding_key_slices():
    print("--- 6. Building Winding Key Slices ---")
    # Back key anchor in 512: (360, 140)
    # 從 verification_crop_key.png 或高精切片建立專屬雙環黃銅發條鑰匙
    # 尺寸設為 110x120
    # 在 512 畫布中 key 位於 (340, 68, 444, 176)
    # 裁切 box: (335, 60, 445, 175) -> size (110, 115)
    # Origin: (360 - 335, 140 - 60) = (25, 80)
    
    # 載入 vk
    vk = Image.open(f"{SRC_DIR}/verification_crop_key.png").convert("RGBA")
    # vk 尺寸 (1288, 1334)，等比縮放到 (110, 115)
    vk_crop = vk.crop((0, 46, 1242, 1334))
    vk_resized = vk_crop.resize((110, 115), Image.Resampling.LANCZOS)
    
    out_k = f"{OUT_DIR}/winding_key/key_classic_brass.png"
    vk_resized.save(out_k)
    print(f"  ✓ {out_k}: {vk_resized.size}, origin=[25, 80], bbox={vk_resized.getbbox()}")

def build_back_curio_slices():
    print("--- 7. Building Back Curio Slices ---")
    # Tail anchor in 512: (350, 335)
    # curio_spring_tail.png 尺寸 128x128，在 512 放大 4 倍
    tail_128 = Image.open(f"{SRC_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
    tail_512 = tail_128.resize((512, 512), Image.Resampling.NEAREST)
    # Tail bbox in 512 is (340, 320, 436, 408) -> size (96, 88)
    crop_box = (340, 320, 436, 408)
    c_tail = tail_512.crop(crop_box)
    # Origin: (350 - 340, 335 - 320) = (10, 15)
    out_tail = f"{OUT_DIR}/back_curio/curio_spring_tail.png"
    c_tail.save(out_tail)
    print(f"  ✓ {out_tail}: {c_tail.size}, origin=[10, 15], bbox={c_tail.getbbox()}")

def generate_json_spec():
    print("--- 8. Generating maple_paperdoll_boar.json ---")
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
            "costume": "costume_viking_ironclad",
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
                    "costume_viking_ironclad": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/costume/costume_viking_ironclad.png",
                        "width": 202,
                        "height": 226,
                        "origin": [76, 170]
                    },
                    "costume_viking_harness": {
                        "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/costume/costume_viking_harness.png",
                        "width": 156,
                        "height": 170,
                        "origin": [76, 84]
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
                        "width": 170,
                        "height": 239,
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
                        "width": 110,
                        "height": 115,
                        "origin": [25, 80]
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
    ensure_dirs()
    build_body_slices()
    build_head_unit_slices()
    build_eyes_slices()
    build_costume_slices()
    build_weapon_slices()
    build_winding_key_slices()
    build_back_curio_slices()
    generate_json_spec()
    print("🎉 All Boar MapleStory-style slices and spec built successfully!")
