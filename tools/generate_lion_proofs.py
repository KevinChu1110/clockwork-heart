#!/usr/bin/env python3
"""
tools/generate_lion_proofs.py
Generates side-by-side comparison proof images, magenta composite verification,
and verification crop images for Lion paperdoll expansion.
"""

import os
from PIL import Image, ImageDraw, ImageChops

LION_DIR = "game/assets/sprites/player/paperdoll/lion"
BG_MAGENTA = (255, 0, 255, 255)

def get_slot_layer(slot, fn):
    p = f"{LION_DIR}/{slot}/{fn}"
    return Image.open(p).convert("RGBA")

def build_composite(chassis_fn, costume_fn=None):
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    comp.alpha_composite(get_slot_layer("winding_key", "key_classic_brass.png"))
    comp.alpha_composite(get_slot_layer("back_curio", "curio_lion_fan_tail.png"))
    comp.alpha_composite(get_slot_layer("chassis", chassis_fn))
    comp.alpha_composite(get_slot_layer("head_unit", "ear_lion_gilded_mane.png"))
    if costume_fn and costume_fn != "none":
        comp.alpha_composite(get_slot_layer("costume", costume_fn))
    comp.alpha_composite(get_slot_layer("optic_core", "core_amber_sun.png"))
    comp.alpha_composite(get_slot_layer("weapon", "wpn_knight_lance.png"))
    return comp

def generate_chassis_comparison():
    # 3 Chassis variants: Brass Gold, Ivory Stock, Midnight Navy
    c_gold = build_composite("paint_brass_gold.png", "costume_nutcracker_guard.png")
    c_ivory = build_composite("paint_ivory_stock.png", "costume_nutcracker_guard.png")
    c_navy = build_composite("paint_midnight_navy.png", "costume_nutcracker_guard.png")

    canvas_w = 128 * 3 + 40
    canvas_h = 168
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)

    items = [
        (c_gold, "1. 黃銅原金 (Brass Gold)"),
        (c_ivory, "2. 原廠象牙白 (Ivory Stock)"),
        (c_navy, "3. 午夜深藍 (Midnight Navy - NEW)")
    ]

    for i, (img, label) in enumerate(items):
        x = 10 + i * (128 + 10)
        canvas.paste(img, (x, 10), img)
        draw.rectangle((x, 10, x + 128, 138), outline=(60, 65, 75, 255), width=1)

    out_p = f"{LION_DIR}/proof_lion_chassis_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved chassis comparison: {out_p}")

def generate_costume_comparison():
    # 3 Costume options on Brass Gold: Bare, Nutcracker Guard, Steam Artisan
    c_bare = build_composite("paint_brass_gold.png", None)
    c_nut = build_composite("paint_brass_gold.png", "costume_nutcracker_guard.png")
    c_art = build_composite("paint_brass_gold.png", "costume_steam_artisan.png")

    canvas_w = 128 * 3 + 40
    canvas_h = 168
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)

    items = [
        (c_bare, "1. 裸機素體 (Bare)"),
        (c_nut, "2. 胡桃鉗近衛軍裝 (Nutcracker)"),
        (c_art, "3. 蒸氣工匠吊帶裝 (Steam Artisan - NEW)")
    ]

    for i, (img, label) in enumerate(items):
        x = 10 + i * (128 + 10)
        canvas.paste(img, (x, 10), img)
        draw.rectangle((x, 10, x + 128, 138), outline=(60, 65, 75, 255), width=1)

    out_p = f"{LION_DIR}/proof_lion_costume_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved costume comparison: {out_p}")

def generate_matrix_proof():
    # 3x3 Matrix: Rows = Costumes (Nutcracker, Steam Artisan, Bare), Cols = Chassis (Brass Gold, Ivory Stock, Midnight Navy)
    chassis_list = [
        ("paint_brass_gold.png", "黃銅原金"),
        ("paint_ivory_stock.png", "原廠象牙白"),
        ("paint_midnight_navy.png", "午夜深藍 [新]")
    ]
    costume_list = [
        ("costume_nutcracker_guard.png", "胡桃鉗近衛"),
        ("costume_steam_artisan.png", "蒸氣工匠 [新]"),
        (None, "裸機素體")
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
            # Highlight new variants with cyan border, others with subtle gray
            is_new = (cos_fn == "costume_steam_artisan.png") or (ch_fn == "paint_midnight_navy.png")
            border_col = (56, 160, 255, 255) if is_new else (50, 55, 65, 255)
            draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=1)

    out_p = f"{LION_DIR}/proof_lion_variants_matrix.png"
    canvas.save(out_p)
    print(f"✓ Saved 3x3 mix-and-match matrix: {out_p}")

def generate_magenta_proofs():
    # 1. New Steam Artisan on Midnight Navy (New Costume + New Paint)
    c_new_both = build_composite("paint_midnight_navy.png", "costume_steam_artisan.png")
    mag1 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag1.alpha_composite(c_new_both)
    out1 = f"{LION_DIR}/proof_paperdoll_lion_artisan_navy_magenta.png"
    mag1.save(out1)

    # 2. New Steam Artisan on Brass Gold (New Costume + Default Paint)
    c_new_art = build_composite("paint_brass_gold.png", "costume_steam_artisan.png")
    mag2 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag2.alpha_composite(c_new_art)
    out2 = f"{LION_DIR}/proof_paperdoll_lion_artisan_gold_magenta.png"
    mag2.save(out2)

    # 3. Nutcracker on Midnight Navy (Default Costume + New Paint)
    c_new_navy = build_composite("paint_midnight_navy.png", "costume_nutcracker_guard.png")
    mag3 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag3.alpha_composite(c_new_navy)
    out3 = f"{LION_DIR}/proof_paperdoll_lion_nutcracker_navy_magenta.png"
    mag3.save(out3)

    print(f"✓ Saved magenta proofs:\n  • {out1}\n  • {out2}\n  • {out3}")

def generate_verification_crops():
    # Crop 1: Steam Artisan suspenders & wrought iron bib
    art_slice = Image.open(f"{LION_DIR}/costume/costume_steam_artisan.png").convert("RGBA")
    # Region around chest/suspenders: X[40..85], Y[65..105]
    crop_art = art_slice.crop((40, 65, 86, 105))
    crop_art_large = crop_art.resize((crop_art.width * 8, crop_art.height * 8), Image.Resampling.NEAREST)
    out_art = f"{LION_DIR}/verification_crop_steam_artisan.png"
    crop_art_large.save(out_art)

    # Crop 2: Midnight Navy chassis plating & bronze joints
    navy_slice = Image.open(f"{LION_DIR}/chassis/paint_midnight_navy.png").convert("RGBA")
    # Region around chest/joints: X[45..85], Y[55..95]
    crop_navy = navy_slice.crop((45, 55, 86, 95))
    crop_navy_large = crop_navy.resize((crop_navy.width * 8, crop_navy.height * 8), Image.Resampling.NEAREST)
    out_navy = f"{LION_DIR}/verification_crop_midnight_navy.png"
    crop_navy_large.save(out_navy)

    print(f"✓ Saved verification crops:\n  • {out_art}\n  • {out_navy}")

if __name__ == "__main__":
    generate_chassis_comparison()
    generate_costume_comparison()
    generate_matrix_proof()
    generate_magenta_proofs()
    generate_verification_crops()
