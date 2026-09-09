#!/usr/bin/env python3
"""
tools/generate_rabbit_proofs.py
Generates side-by-side comparison proof images, magenta composite verification,
and verification crop images for Rabbit paperdoll expansion.
- Clean centered 2-line labels with zero overlap (Rule 10a-2 review feedback)
- Uses project font Open-Huninn (jf-openhuninn-2.1.ttf)
- Strictly composited from shipped slice assets in ascending z-index order onto magenta (Rule 4c-4 / 19f-3)
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
RABBIT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rabbit"
FONT_PATH = f"{REPO_ROOT}/game/assets/fonts/jf-openhuninn-2.1.ttf"
BG_MAGENTA = (255, 0, 255, 255)

def get_font(size: int = 12):
    if os.path.exists(FONT_PATH):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception:
            pass
    return ImageFont.load_default()

def get_slot_layer(slot: str, fn: str) -> Image.Image:
    p = f"{RABBIT_DIR}/{slot}/{fn}"
    return Image.open(p).convert("RGBA")

def build_composite(chassis_fn: str, costume_fn: str | None = None) -> Image.Image:
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Z-index ascending order:
    # 1. winding_key (Z: 5)
    comp.alpha_composite(get_slot_layer("winding_key", "key_classic_brass.png"))
    # 2. back_curio (Z: 8)
    comp.alpha_composite(get_slot_layer("back_curio", "curio_clockwork_pigeon.png"))
    # 3. chassis (Z: 10)
    comp.alpha_composite(get_slot_layer("chassis", chassis_fn))
    # 4. head_unit (Z: 20)
    comp.alpha_composite(get_slot_layer("head_unit", "ear_rabbit_straight.png"))
    # 5. costume (Z: 25)
    if costume_fn and costume_fn != "none":
        comp.alpha_composite(get_slot_layer("costume", costume_fn))
    # 6. optic_core (Z: 30)
    comp.alpha_composite(get_slot_layer("optic_core", "core_cyan_emerald.png"))
    # 7. weapon (Z: 40)
    comp.alpha_composite(get_slot_layer("weapon", "wpn_dawn_blade.png"))
    return comp

def generate_chassis_comparison():
    # 3 Chassis variants on Royal Parade costume
    c_ivory = build_composite("paint_ivory_stock.png", "costume_royal_parade.png")
    c_gold = build_composite("paint_brass_gold.png", "costume_royal_parade.png")
    c_navy = build_composite("paint_midnight_navy.png", "costume_royal_parade.png")

    pad = 20
    gap = 24
    canvas_w = pad * 2 + 128 * 3 + gap * 2  # 472
    canvas_h = 205
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)
    font_zh = get_font(13)
    font_en = get_font(11)

    items = [
        (c_ivory, "原廠象牙白", "Ivory Stock", False),
        (c_gold, "黃銅原金", "Brass Gold", False),
        (c_navy, "午夜深藍 [新]", "Midnight Navy", True),
    ]

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (56, 160, 255, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        # Centered Chinese label
        b_zh = draw.textbbox((0, 0), l_zh, font=font_zh)
        w_zh = b_zh[2] - b_zh[0]
        tx_zh = x + (128 - w_zh) // 2
        ty_zh = y + 128 + 8
        color_zh = (255, 218, 64, 255) if is_new else (225, 230, 240, 255)
        draw.text((tx_zh, ty_zh), l_zh, font=font_zh, fill=color_zh)

        # Centered English label
        b_en = draw.textbbox((0, 0), l_en, font=font_en)
        w_en = b_en[2] - b_en[0]
        tx_en = x + (128 - w_en) // 2
        ty_en = ty_zh + 18
        color_en = (56, 160, 255, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{RABBIT_DIR}/proof_rabbit_chassis_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved chassis comparison: {out_p}")

def generate_costume_comparison():
    # 4 Costume options on Ivory Stock: Bare, Nutcracker Guard, Steam Artisan, Royal Parade
    c_bare = build_composite("paint_ivory_stock.png", None)
    c_nut = build_composite("paint_ivory_stock.png", "costume_nutcracker_guard.png")
    c_art = build_composite("paint_ivory_stock.png", "costume_steam_artisan.png")
    c_roy = build_composite("paint_ivory_stock.png", "costume_royal_parade.png")

    pad = 20
    gap = 20
    canvas_w = pad * 2 + 128 * 4 + gap * 3  # 612
    canvas_h = 205
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)
    font_zh = get_font(13)
    font_en = get_font(11)

    items = [
        (c_bare, "裸機素體", "Bare Chassis", False),
        (c_nut, "胡桃鉗近衛", "Nutcracker", False),
        (c_art, "蒸氣工匠", "Steam Artisan", False),
        (c_roy, "皇家巡遊 [新]", "Royal Parade", True),
    ]

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (56, 160, 255, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        # Centered Chinese label
        b_zh = draw.textbbox((0, 0), l_zh, font=font_zh)
        w_zh = b_zh[2] - b_zh[0]
        tx_zh = x + (128 - w_zh) // 2
        ty_zh = y + 128 + 8
        color_zh = (255, 218, 64, 255) if is_new else (225, 230, 240, 255)
        draw.text((tx_zh, ty_zh), l_zh, font=font_zh, fill=color_zh)

        # Centered English label
        b_en = draw.textbbox((0, 0), l_en, font=font_en)
        w_en = b_en[2] - b_en[0]
        tx_en = x + (128 - w_en) // 2
        ty_en = ty_zh + 18
        color_en = (56, 160, 255, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{RABBIT_DIR}/proof_rabbit_costume_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved costume comparison: {out_p}")

def generate_matrix_proof():
    # 4x3 Matrix: Rows = Costumes, Cols = Chassis
    chassis_list = [
        ("paint_ivory_stock.png", "原廠象牙白"),
        ("paint_brass_gold.png", "黃銅原金"),
        ("paint_midnight_navy.png", "午夜深藍 [新]"),
    ]
    costume_list = [
        ("costume_nutcracker_guard.png", "胡桃鉗近衛"),
        ("costume_steam_artisan.png", "蒸氣工匠"),
        ("costume_royal_parade.png", "皇家巡遊 [新]"),
        (None, "裸機素體"),
    ]

    cw = 10 + len(chassis_list) * (128 + 10)
    ch = 10 + len(costume_list) * (128 + 10)
    canvas = Image.new("RGBA", (cw, ch), (20, 22, 28, 255))
    draw = ImageDraw.Draw(canvas)

    for row_idx, (cos_fn, cos_label) in enumerate(costume_list):
        for col_idx, (ch_fn, ch_label) in enumerate(chassis_list):
            comp = build_composite(ch_fn, cos_fn)
            x = 10 + col_idx * (128 + 10)
            y = 10 + row_idx * (128 + 10)
            canvas.paste(comp, (x, y), comp)
            is_new = (cos_fn == "costume_royal_parade.png") or (ch_fn == "paint_midnight_navy.png")
            border_col = (255, 218, 64, 255) if (cos_fn == "costume_royal_parade.png" and ch_fn == "paint_midnight_navy.png") else ((56, 160, 255, 255) if is_new else (50, 55, 65, 255))
            draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

    out_p = f"{RABBIT_DIR}/proof_rabbit_variants_matrix.png"
    canvas.save(out_p)
    print(f"✓ Saved 4x3 mix-and-match matrix: {out_p}")

def generate_magenta_proofs():
    # 1. New Royal Parade on Midnight Navy (New Costume + New Paint)
    c_new_both = build_composite("paint_midnight_navy.png", "costume_royal_parade.png")
    mag1 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag1.alpha_composite(c_new_both)
    out1 = f"{RABBIT_DIR}/proof_paperdoll_rabbit_royal_navy_magenta.png"
    mag1.save(out1)

    # 2. New Royal Parade on Ivory Stock (New Costume + Default Paint)
    c_new_roy = build_composite("paint_ivory_stock.png", "costume_royal_parade.png")
    mag2 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag2.alpha_composite(c_new_roy)
    out2 = f"{RABBIT_DIR}/proof_paperdoll_rabbit_royal_ivory_magenta.png"
    mag2.save(out2)

    # 3. Nutcracker on Midnight Navy (Default Costume + New Paint)
    c_new_navy = build_composite("paint_midnight_navy.png", "costume_nutcracker_guard.png")
    mag3 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag3.alpha_composite(c_new_navy)
    out3 = f"{RABBIT_DIR}/proof_paperdoll_rabbit_nutcracker_navy_magenta.png"
    mag3.save(out3)

    print(f"✓ Saved magenta proofs:\n  • {out1}\n  • {out2}\n  • {out3}")

def generate_verification_crops():
    # Crop 1: Royal Parade ceremonial gorget, double-breasted gala breastplate & gear buttons
    roy_slice = Image.open(f"{RABBIT_DIR}/costume/costume_royal_parade.png").convert("RGBA")
    crop_roy = roy_slice.crop((44, 74, 84, 107))
    crop_roy_large = crop_roy.resize((crop_roy.width * 8, crop_roy.height * 8), Image.Resampling.NEAREST)
    out_roy = f"{RABBIT_DIR}/verification_crop_royal_parade.png"
    crop_roy_large.save(out_roy)

    # Crop 2: Midnight Navy chassis plating & ball joints
    navy_slice = Image.open(f"{RABBIT_DIR}/chassis/paint_midnight_navy.png").convert("RGBA")
    crop_navy = navy_slice.crop((42, 55, 88, 105))
    crop_navy_large = crop_navy.resize((crop_navy.width * 8, crop_navy.height * 8), Image.Resampling.NEAREST)
    out_navy = f"{RABBIT_DIR}/verification_crop_midnight_navy.png"
    crop_navy_large.save(out_navy)

    print(f"✓ Saved verification crops:\n  • {out_roy}\n  • {out_navy}")

if __name__ == "__main__":
    generate_chassis_comparison()
    generate_costume_comparison()
    generate_matrix_proof()
    generate_magenta_proofs()
    generate_verification_crops()
