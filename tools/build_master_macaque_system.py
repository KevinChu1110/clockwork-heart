#!/usr/bin/env python3
"""
tools/build_master_macaque_system.py
Creates the definitive Character.wz paperdoll assets and JSON table for Macaque (靈爪猴).
- Sourced directly from pristine 512 raw assets.
- Pure shaded metal eye sockets, independent optic cores (cyan emerald, amber gold, blink).
- Zero fur / zero biological material / pure clockwork toy aesthetics.
- Compact sprite slices with mathematically precise origins.
- Outputs game/data/tables/maple_paperdoll_macaque.json.
"""

import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"
PARTS_DIR = f"{MACAQUE_DIR}/maple_parts"
JSON_PATH = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_macaque.json"

for sub in ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]:
    os.makedirs(f"{PARTS_DIR}/{sub}", exist_ok=True)

# -----------------------------------------------------------------------------
# 1. HEAD UNIT: 緊湊切片 (108, 51, 355, 263) -> size=(247, 212)
# Neck: (232, 260) -> Origin: (232 - 108, 260 - 51) = (124, 209)
# -----------------------------------------------------------------------------
def build_heads():
    print("--- 1. Building Pristine Head Units ---")
    crop_box = (108, 51, 355, 263) # (247, 212)

    variants = [
        ("ear_macaque_coaxial", "ear_macaque_coaxial_512.png"),
        ("ear_macaque_coaxial_bronze", "ear_macaque_coaxial_bronze_512.png"),
        ("ear_macaque_coaxial_ivory", "ear_macaque_coaxial_ivory_512.png")
    ]

    for out_name, src_file in variants:
        p = f"{MACAQUE_DIR}/head_unit/{src_file}"
        im = Image.open(p).convert("RGBA")
        cropped = im.crop(crop_box)
        out_p = f"{PARTS_DIR}/head_unit/{out_name}.png"
        cropped.save(out_p)
        print(f"  ✓ Saved {out_name}.png: size={cropped.size}, origin=[124, 209]")

# -----------------------------------------------------------------------------
# 2. STANDALONE EYES: 獨立光學義眼 (天青祖母綠、琥珀金陽、機械眨眼)
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
    print("  ✓ Saved eyes (cyan_emerald, amber_gold, blink)")

# -----------------------------------------------------------------------------
# 3. PURE METALLIC BODIES: 3 款塗裝 (象牙白、天元青古銅、金光禪武)
# -----------------------------------------------------------------------------
def build_bodies():
    print("--- 3. Building Pure Bodies ---")
    ivory_path = f"{MACAQUE_DIR}/chassis/paint_ivory_stock_512.png"
    bronze_path = f"{MACAQUE_DIR}/chassis/paint_bamboo_bronze_512.png"

    im_ivory = Image.open(ivory_path).convert("RGBA")
    im_bronze = Image.open(bronze_path).convert("RGBA")

    # 1. 象牙白
    im_ivory.save(f"{PARTS_DIR}/body/paint_ivory_stock.png")

    # 2. 天元青古銅
    im_bronze.save(f"{PARTS_DIR}/body/paint_bamboo_bronze.png")

    # 3. 金光禪武塗裝 (paint_zen_gold)
    w, h = im_ivory.size
    im_gold = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            r, g, b, a = im_ivory.getpixel((x, y))
            if a == 0:
                continue
            lum = int(0.299 * r + 0.587 * g + 0.114 * b)
            if lum < 55:
                # 深藍紫描邊 #1F1A3A
                im_gold.putpixel((x, y), (31, 26, 58, a))
            else:
                f = max(0.0, min(1.0, (lum - 55) / 195.0))
                # 多巴胺金黃 #FFD028 漸層
                if f < 0.5:
                    t = f / 0.5
                    cr = int(140 + t * (210 - 140))
                    cg = int(95 + t * (160 - 95))
                    cb = int(25 + t * (40 - 25))
                else:
                    t = (f - 0.5) / 0.5
                    cr = int(210 + t * (255 - 210))
                    cg = int(160 + t * (225 - 160))
                    cb = int(40 + t * (90 - 40))
                im_gold.putpixel((x, y), (cr, cg, cb, a))

    im_gold.save(f"{PARTS_DIR}/body/paint_zen_gold.png")
    print("  ✓ Saved bodies: paint_ivory_stock, paint_bamboo_bronze, paint_zen_gold")

# -----------------------------------------------------------------------------
# 4. COSTUMES: 晨曦僧袍與禪拳戰裝
# -----------------------------------------------------------------------------
def build_costumes():
    print("--- 4. Building Compact Costumes ---")
    # 1. 晨曦僧袍
    # Tunic bbox = (183, 262, 334, 426) -> size=(151, 164)
    # Navel: (256, 345) -> Origin: (256 - 183, 345 - 262) = (73, 83)
    tunic_raw = Image.open(f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic_512.png").convert("RGBA")
    tunic_crop = tunic_raw.crop((183, 262, 334, 426))
    tunic_crop.save(f"{PARTS_DIR}/costume/costume_dawn_monk_tunic.png")
    print(f"  ✓ Saved costume_dawn_monk_tunic.png: size={tunic_crop.size}, origin=[73, 83]")

    # 2. 禪拳戰裝
    # Zen bbox = (135, 227, 285, 345) -> size=(150, 118)
    # Navel: (256, 345) -> Origin: (256 - 135, 345 - 227) = (121, 118)
    zen_raw = Image.open(f"{MACAQUE_DIR}/costume/costume_zen_striker_512.png").convert("RGBA")
    zen_crop = zen_raw.crop((135, 227, 285, 345))
    zen_crop.save(f"{PARTS_DIR}/costume/costume_zen_striker.png")
    print(f"  ✓ Saved costume_zen_striker.png: size={zen_crop.size}, origin=[121, 118]")

# -----------------------------------------------------------------------------
# 5. WEAPON: 彈簧金屬爪 (wpn_spring_claws)
# -----------------------------------------------------------------------------
def build_weapon():
    print("--- 5. Building Compact Weapon Claws ---")
    # Claws bbox = (63, 271, 341, 417) -> size=(278, 146)
    # Hand: (200, 340) -> Origin: (200 - 63, 340 - 271) = (137, 69)
    claws_raw = Image.open(f"{MACAQUE_DIR}/weapon/wpn_spring_claws_512.png").convert("RGBA")
    claws_crop = claws_raw.crop((63, 271, 341, 417))
    claws_crop.save(f"{PARTS_DIR}/weapon/wpn_spring_claws.png")
    print(f"  ✓ Saved wpn_spring_claws.png: size={claws_crop.size}, origin=[137, 69]")

# -----------------------------------------------------------------------------
# 6. WINDING KEY: 經典黃銅發條鑰匙 (key_classic_brass)
# -----------------------------------------------------------------------------
def build_key():
    print("--- 6. Building Pristine Winding Key ---")
    # 使用野豬經過考驗的無暗暈經典黃銅鑰匙
    boar_key_path = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar/maple_parts/winding_key/key_classic_brass.png"
    im_key = Image.open(boar_key_path).convert("RGBA")
    im_key.save(f"{PARTS_DIR}/winding_key/key_classic_brass.png")
    print(f"  ✓ Saved key_classic_brass.png: size={im_key.size}, origin=[18, 80]")

# -----------------------------------------------------------------------------
# 7. BACK CURIO: 靈爪長彈簧猴尾 (curio_spring_tail)
# -----------------------------------------------------------------------------
def build_tail():
    print("--- 7. Building Spring Tail ---")
    w, h = 76, 192
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # 頂部接合金屬基座軸承 (10, 104) 附近
    d.ellipse([4, 100, 22, 116], fill=(130, 95, 30, 255), outline=(31, 26, 58, 255), width=3)
    d.ellipse([7, 103, 19, 113], fill=(255, 208, 40, 255))

    # 彈簧環曲線
    rings = [
        (12, 92, 28, 20),
        (18, 76, 32, 22),
        (26, 58, 36, 24),
        (35, 40, 36, 24),
        (42, 22, 32, 22),
        (46, 6, 28, 20),
        (42, 0, 24, 18),
        (34, 12, 22, 18),
        (28, 28, 24, 20),
        (26, 48, 26, 22),
        (30, 68, 28, 22),
        (36, 88, 30, 24),
        (44, 108, 30, 24),
        (50, 128, 26, 22),
        (52, 146, 22, 20),
        (48, 162, 18, 18),
    ]

    for rx, ry, rw, rh in rings:
        d.ellipse([rx, ry, rx + rw, ry + rh], outline=(31, 26, 58, 255), width=4)
        d.ellipse([rx + 2, ry + 2, rx + rw - 2, ry + rh - 2], fill=(200, 150, 30, 255))
        d.ellipse([rx + 4, ry + 4, rx + rw - 4, ry + rh - 4], fill=(255, 225, 120, 255))
        d.ellipse([rx + 7, ry + 7, rx + rw - 7, ry + rh - 7], fill=(0, 0, 0, 0))

    # 末端小金屬發條小銅珠
    d.ellipse([42, 172, 56, 186], fill=(255, 208, 40, 255), outline=(31, 26, 58, 255), width=3)
    d.ellipse([45, 175, 49, 179], fill=(255, 255, 255, 255))

    out_p = f"{PARTS_DIR}/back_curio/curio_spring_tail.png"
    im.save(out_p)
    print(f"  ✓ Saved curio_spring_tail.png: size={im.size}, origin=[10, 108]")

# -----------------------------------------------------------------------------
# 8. JSON TABLE: game/data/tables/maple_paperdoll_macaque.json
# -----------------------------------------------------------------------------
def build_json():
    print("--- 8. Generating maple_paperdoll_macaque.json ---")
    spec = {
        "race": "macaque",
        "canvas_size": [512, 512],
        "root_anchor": [256, 480],
        "anchors": {
            "neck": [232, 260],
            "navel": [256, 345],
            "hand": [200, 340],
            "back_key": [330, 240],
            "brow_relative_to_neck": [-2, -120],
            "tail": [350, 280]
        },
        "default_loadout": {
            "body": "paint_ivory_stock",
            "head_unit": "ear_macaque_coaxial",
            "eyes": "eyes_cyan_emerald",
            "costume": "costume_dawn_monk_tunic",
            "weapon": "wpn_spring_claws",
            "winding_key": "key_classic_brass",
            "back_curio": "curio_spring_tail"
        },
        "parts": {
            "body": {
                "anchor": "root",
                "z_index": 10,
                "origin": [0, 0],
                "items": {
                    "paint_ivory_stock": {
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/body/paint_ivory_stock.png",
                        "width": 512,
                        "height": 512,
                        "origin": [0, 0]
                    },
                    "paint_bamboo_bronze": {
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/body/paint_bamboo_bronze.png",
                        "width": 512,
                        "height": 512,
                        "origin": [0, 0]
                    },
                    "paint_zen_gold": {
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/body/paint_zen_gold.png",
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
                    "ear_macaque_coaxial": {
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/head_unit/ear_macaque_coaxial.png",
                        "width": 247,
                        "height": 212,
                        "origin": [124, 209]
                    },
                    "ear_macaque_coaxial_bronze": {
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/head_unit/ear_macaque_coaxial_bronze.png",
                        "width": 247,
                        "height": 212,
                        "origin": [124, 209]
                    },
                    "ear_macaque_coaxial_ivory": {
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/head_unit/ear_macaque_coaxial_ivory.png",
                        "width": 247,
                        "height": 212,
                        "origin": [124, 209]
                    }
                }
            },
            "eyes": {
                "anchor": "brow",
                "z_index": 30,
                "origin": [45, 30],
                "items": {
                    "eyes_cyan_emerald": {
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/eyes/eyes_cyan_emerald.png",
                        "width": 90,
                        "height": 60,
                        "origin": [45, 30]
                    },
                    "eyes_amber_gold": {
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/eyes/eyes_amber_gold.png",
                        "width": 90,
                        "height": 60,
                        "origin": [45, 30]
                    },
                    "eyes_blink": {
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/eyes/eyes_blink.png",
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
                    "costume_dawn_monk_tunic": {
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/costume/costume_dawn_monk_tunic.png",
                        "width": 151,
                        "height": 164,
                        "origin": [73, 83]
                    },
                    "costume_zen_striker": {
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/costume/costume_zen_striker.png",
                        "width": 150,
                        "height": 118,
                        "origin": [121, 118]
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
                    "wpn_spring_claws": {
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/weapon/wpn_spring_claws.png",
                        "width": 278,
                        "height": 146,
                        "origin": [137, 69]
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
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/winding_key/key_classic_brass.png",
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
                        "path": "res://assets/sprites/player/paperdoll/macaque/maple_parts/back_curio/curio_spring_tail.png",
                        "width": 76,
                        "height": 192,
                        "origin": [10, 108]
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
    print("🎉 Master Macaque System successfully built!")
