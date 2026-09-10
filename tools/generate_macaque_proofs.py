#!/usr/bin/env python3
"""
tools/generate_macaque_proofs.py
Generates side-by-side comparison proof images, variants matrix,
magenta composite verification, and verification crop images for Macaque paperdoll expansion.
- Clean centered 2-line labels with zero overlap
- Crisp 'NEW' badge on top-right of new variant preview cards
- Uses project font Open-Huninn (jf-openhuninn-2.1.ttf)
- Strictly composited from shipped slice assets in z-index order onto magenta
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"
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
    p = f"{MACAQUE_DIR}/{slot}/{fn}"
    return Image.open(p).convert("RGBA")

def build_composite(chassis_fn: str, costume_fn: str | None = None) -> Image.Image:
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Z-index ascending order:
    # 1. winding_key (Z: 5)
    comp.alpha_composite(get_slot_layer("winding_key", "key_classic_brass.png"))
    # 2. back_curio (Z: 8)
    comp.alpha_composite(get_slot_layer("back_curio", "curio_spring_tail.png"))
    # 3. chassis (Z: 10)
    comp.alpha_composite(get_slot_layer("chassis", chassis_fn))
    # 4. head_unit (Z: 20)
    comp.alpha_composite(get_slot_layer("head_unit", "ear_macaque_coaxial.png"))
    # 5. costume (Z: 25)
    if costume_fn and costume_fn != "none":
        comp.alpha_composite(get_slot_layer("costume", costume_fn))
    # 6. optic_core (Z: 30)
    comp.alpha_composite(get_slot_layer("optic_core", "core_cyan_emerald.png"))
    # 7. weapon (Z: 40)
    comp.alpha_composite(get_slot_layer("weapon", "wpn_spring_claws.png"))
    return comp

def draw_new_badge(draw: ImageDraw.ImageDraw, x: int, y: int, bg_color: tuple[int, int, int, int], text_color: tuple[int, int, int, int]):
    badge_w, badge_h = 36, 18
    bx = x + 128 - badge_w - 4
    by = y + 4
    draw.rounded_rectangle((bx, by, bx + badge_w, by + badge_h), radius=4, fill=bg_color)
    font_badge = get_font(10)
    tb = draw.textbbox((0, 0), "NEW", font=font_badge)
    tw = tb[2] - tb[0]
    th = tb[3] - tb[1]
    tx = bx + (badge_w - tw) // 2
    ty = by + (badge_h - th) // 2 - 1
    draw.text((tx, ty), "NEW", font=font_badge, fill=text_color)

def generate_chassis_comparison():
    # Chassis variants on Dawn Monk Tunic
    c_ivory = build_composite("paint_ivory_stock.png", "costume_dawn_monk_tunic.png")
    c_bronze = build_composite("paint_bamboo_bronze.png", "costume_dawn_monk_tunic.png")

    pad = 24
    gap = 28
    canvas_w = pad * 2 + 128 * 2 + gap  # 332
    canvas_h = 205
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)
    font_zh = get_font(13)
    font_en = get_font(11)

    items = [
        (c_ivory, "原廠象牙白", "Ivory Stock", False),
        (c_bronze, "天元青古銅 [新]", "Bamboo Bronze", True)
    ]

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (78, 216, 106, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        if is_new:
            draw_new_badge(draw, x, y, (78, 216, 106, 255), (15, 35, 20, 255))

        b_zh = draw.textbbox((0, 0), l_zh, font=font_zh)
        w_zh = b_zh[2] - b_zh[0]
        tx_zh = x + (128 - w_zh) // 2
        ty_zh = y + 128 + 8
        color_zh = (255, 218, 64, 255) if is_new else (225, 230, 240, 255)
        draw.text((tx_zh, ty_zh), l_zh, font=font_zh, fill=color_zh)

        b_en = draw.textbbox((0, 0), l_en, font=font_en)
        w_en = b_en[2] - b_en[0]
        tx_en = x + (128 - w_en) // 2
        ty_en = ty_zh + 18
        color_en = (78, 216, 106, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{MACAQUE_DIR}/proof_macaque_chassis_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved chassis comparison: {out_p}")

def generate_costume_comparison():
    # 3 Costume options on Ivory Stock: Bare, Dawn Monk Tunic, Zen Striker
    c_bare = build_composite("paint_ivory_stock.png", None)
    c_tunic = build_composite("paint_ivory_stock.png", "costume_dawn_monk_tunic.png")
    c_zen = build_composite("paint_ivory_stock.png", "costume_zen_striker.png")

    pad = 20
    gap = 24
    canvas_w = pad * 2 + 128 * 3 + gap * 2  # 472
    canvas_h = 205
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)
    font_zh = get_font(13)
    font_en = get_font(11)

    items = [
        (c_bare, "裸機素體", "Bare Chassis", False),
        (c_tunic, "晨曦行者短褂", "Dawn Monk Tunic", False),
        (c_zen, "天元演武機關甲 [新]", "Zen Striker", True)
    ]

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (255, 160, 16, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        if is_new:
            draw_new_badge(draw, x, y, (255, 160, 16, 255), (40, 20, 0, 255))

        b_zh = draw.textbbox((0, 0), l_zh, font=font_zh)
        w_zh = b_zh[2] - b_zh[0]
        tx_zh = x + (128 - w_zh) // 2
        ty_zh = y + 128 + 8
        color_zh = (255, 218, 64, 255) if is_new else (225, 230, 240, 255)
        draw.text((tx_zh, ty_zh), l_zh, font=font_zh, fill=color_zh)

        b_en = draw.textbbox((0, 0), l_en, font=font_en)
        w_en = b_en[2] - b_en[0]
        tx_en = x + (128 - w_en) // 2
        ty_en = ty_zh + 18
        color_en = (255, 160, 16, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{MACAQUE_DIR}/proof_macaque_costume_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved costume comparison: {out_p}")

def generate_matrix_proof():
    # Matrix: Rows = Costumes, Cols = Chassis
    chassis_list = [
        ("paint_ivory_stock.png", "原廠象牙白"),
        ("paint_bamboo_bronze.png", "天元青古銅 [新]")
    ]
    costume_list = [
        ("costume_dawn_monk_tunic.png", "晨曦行者短褂"),
        ("costume_zen_striker.png", "天元演武機關甲 [新]"),
        (None, "裸機素體")
    ]

    pad = 12
    gap = 12
    cw = pad * 2 + len(chassis_list) * (128 + gap) - gap
    ch = pad * 2 + len(costume_list) * (128 + gap) - gap
    canvas = Image.new("RGBA", (cw, ch), (20, 22, 28, 255))
    draw = ImageDraw.Draw(canvas)

    for row_idx, (cos_fn, cos_label) in enumerate(costume_list):
        for col_idx, (ch_fn, ch_label) in enumerate(chassis_list):
            comp = build_composite(ch_fn, cos_fn)
            x = pad + col_idx * (128 + gap)
            y = pad + row_idx * (128 + gap)
            canvas.paste(comp, (x, y), comp)
            is_new = (cos_fn == "costume_zen_striker.png") or (ch_fn == "paint_bamboo_bronze.png")
            border_col = (78, 216, 106, 255) if is_new else (50, 55, 65, 255)
            draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

    out_p = f"{MACAQUE_DIR}/proof_macaque_variants_matrix.png"
    canvas.save(out_p)
    print(f"✓ Saved mix-and-match matrix: {out_p}")

def generate_magenta_proofs():
    # 1. Zen Striker on Bamboo Bronze (New Costume + New Paint)
    c_new_both = build_composite("paint_bamboo_bronze.png", "costume_zen_striker.png")
    mag1 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag1.alpha_composite(c_new_both)
    out1 = f"{MACAQUE_DIR}/proof_paperdoll_macaque_zen_bronze_magenta.png"
    mag1.save(out1)

    # 2. Zen Striker on Ivory Stock (New Costume + Default Paint)
    c_new_zen = build_composite("paint_ivory_stock.png", "costume_zen_striker.png")
    mag2 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag2.alpha_composite(c_new_zen)
    out2 = f"{MACAQUE_DIR}/proof_paperdoll_macaque_zen_ivory_magenta.png"
    mag2.save(out2)

    # 3. Dawn Monk Tunic on Bamboo Bronze (Default Costume + New Paint)
    c_new_bronze = build_composite("paint_bamboo_bronze.png", "costume_dawn_monk_tunic.png")
    mag3 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag3.alpha_composite(c_new_bronze)
    out3 = f"{MACAQUE_DIR}/proof_paperdoll_macaque_tunic_bronze_magenta.png"
    mag3.save(out3)

    print(f"✓ Saved magenta proofs:\n  • {out1}\n  • {out2}\n  • {out3}")

def generate_verification_crops():
    # Crop 1: Zen Striker cuirass, pauldron rivets, and brass core bezel
    zen_slice = Image.open(f"{MACAQUE_DIR}/costume/costume_zen_striker.png").convert("RGBA")
    # Region around chest/belt/tassets: X[34..80], Y[56..103]
    crop_zen = zen_slice.crop((34, 56, 80, 103))
    crop_zen_large = crop_zen.resize((crop_zen.width * 8, crop_zen.height * 8), Image.Resampling.NEAREST)
    out_zen = f"{MACAQUE_DIR}/verification_crop_zen_striker.png"
    crop_zen_large.save(out_zen)

    # Crop 2: Bamboo Bronze chassis torso/head/limbs plates
    bronze_slice = Image.open(f"{MACAQUE_DIR}/chassis/paint_bamboo_bronze.png").convert("RGBA")
    # Region around torso/joints: X[34..80], Y[50..100]
    crop_bronze = bronze_slice.crop((34, 50, 80, 100))
    crop_bronze_large = crop_bronze.resize((crop_bronze.width * 8, crop_bronze.height * 8), Image.Resampling.NEAREST)
    out_bronze = f"{MACAQUE_DIR}/verification_crop_bamboo_bronze.png"
    crop_bronze_large.save(out_bronze)

    print(f"✓ Saved verification crops:\n  • {out_zen}\n  • {out_bronze}")

if __name__ == "__main__":
    generate_chassis_comparison()
    generate_costume_comparison()
    generate_matrix_proof()
    generate_magenta_proofs()
    generate_verification_crops()
