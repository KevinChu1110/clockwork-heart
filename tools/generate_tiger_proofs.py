#!/usr/bin/env python3
"""
tools/generate_tiger_proofs.py
Generates side-by-side comparison proof images, variants matrix,
magenta composite verification, and verification crop images for Tiger paperdoll expansion.
- Clean centered 2-line labels with zero overlap
- Crisp 'NEW' badge on top-right of new variant preview cards
- Uses project font Open-Huninn (jf-openhuninn-2.1.ttf)
- Strictly composited from shipped slice assets in z-index order onto magenta
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
TIGER_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tiger"
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
    p = f"{TIGER_DIR}/{slot}/{fn}"
    return Image.open(p).convert("RGBA")

def build_composite(chassis_fn: str, costume_fn: str | None = None) -> Image.Image:
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Z-index ascending order:
    # 1. winding_key (Z: 5)
    comp.alpha_composite(get_slot_layer("winding_key", "key_turbine_flame.png"))
    # 2. back_curio (Z: 8)
    comp.alpha_composite(get_slot_layer("back_curio", "curio_exhaust_tiger_tail.png"))
    # 3. chassis (Z: 10)
    comp.alpha_composite(get_slot_layer("chassis", chassis_fn))
    # 4. head_unit (Z: 20)
    comp.alpha_composite(get_slot_layer("head_unit", "head_ember_tiger_stock.png"))
    # 5. costume (Z: 25)
    if costume_fn and costume_fn != "none":
        comp.alpha_composite(get_slot_layer("costume", costume_fn))
    # 6. optic_core (Z: 30)
    comp.alpha_composite(get_slot_layer("optic_core", "core_molten_amber.png"))
    # 7. weapon (Z: 40)
    comp.alpha_composite(get_slot_layer("weapon", "wpn_twin_ember_sabers.png"))
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
    # Chassis variants on Ember Tunic
    c_orange = build_composite("paint_ember_orange.png", "costume_ember_tunic.png")
    c_volcano = build_composite("paint_volcano_black.png", "costume_ember_tunic.png")
    c_ivory = build_composite("paint_ivory_stock.png", "costume_ember_tunic.png")

    pad = 20
    gap = 24
    canvas_w = pad * 2 + 128 * 3 + gap * 2
    canvas_h = 205
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)
    font_zh = get_font(13)
    font_en = get_font(11)

    items = [
        (c_orange, "原廠餘燼橙紅", "Ember Orange", False),
        (c_volcano, "鍛爐淬火曜黑 [新]", "Volcano Black", True),
        (c_ivory, "原廠象牙白", "Ivory Stock", False)
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

    out_p = f"{TIGER_DIR}/proof_tiger_chassis_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved chassis comparison: {out_p}")

def generate_costume_comparison():
    # 3 Costume options on Ember Orange: Bare, Ember Tunic, Ash Ninja Garb
    c_bare = build_composite("paint_ember_orange.png", None)
    c_tunic = build_composite("paint_ember_orange.png", "costume_ember_tunic.png")
    c_ninja = build_composite("paint_ember_orange.png", "costume_ash_ninja_garb.png")

    pad = 20
    gap = 24
    canvas_w = pad * 2 + 128 * 3 + gap * 2
    canvas_h = 205
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)
    font_zh = get_font(13)
    font_en = get_font(11)

    items = [
        (c_bare, "裸機素體", "Bare Chassis", False),
        (c_tunic, "餘燼工匠淬火戰褂", "Ember Quenched Tunic", False),
        (c_ninja, "灰燼夜行機關裝 [新]", "Ash Ninja Garb", True)
    ]

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (140, 80, 255, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        if is_new:
            draw_new_badge(draw, x, y, (140, 80, 255, 255), (255, 255, 255, 255))

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
        color_en = (180, 140, 255, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{TIGER_DIR}/proof_tiger_costume_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved costume comparison: {out_p}")

def generate_matrix_proof():
    # Matrix: Rows = Costumes, Cols = Chassis
    chassis_list = [
        ("paint_ember_orange.png", "原廠餘燼橙紅"),
        ("paint_volcano_black.png", "鍛爐淬火曜黑 [新]"),
        ("paint_ivory_stock.png", "原廠象牙白")
    ]
    costume_list = [
        ("costume_ember_tunic.png", "餘燼工匠淬火戰褂"),
        ("costume_ash_ninja_garb.png", "灰燼夜行機關裝 [新]"),
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
            is_new = (cos_fn == "costume_ash_ninja_garb.png") or (ch_fn == "paint_volcano_black.png")
            border_col = (255, 160, 16, 255) if is_new else (50, 55, 65, 255)
            draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

    out_p = f"{TIGER_DIR}/proof_tiger_variants_matrix.png"
    canvas.save(out_p)
    print(f"✓ Saved mix-and-match matrix: {out_p}")

def generate_magenta_proofs():
    # 1. Ash Ninja Garb on Volcano Black (New Costume + New Paint)
    c_new_both = build_composite("paint_volcano_black.png", "costume_ash_ninja_garb.png")
    mag1 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag1.alpha_composite(c_new_both)
    out1 = f"{TIGER_DIR}/proof_paperdoll_tiger_ninja_black_magenta.png"
    mag1.save(out1)

    # 2. Ash Ninja Garb on Ember Orange (New Costume + Stock Orange)
    c_ninja_orange = build_composite("paint_ember_orange.png", "costume_ash_ninja_garb.png")
    mag2 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag2.alpha_composite(c_ninja_orange)
    out2 = f"{TIGER_DIR}/proof_paperdoll_tiger_ninja_orange_magenta.png"
    mag2.save(out2)

    # 3. Ember Tunic on Volcano Black (Stock Costume + New Paint)
    c_tunic_black = build_composite("paint_volcano_black.png", "costume_ember_tunic.png")
    mag3 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag3.alpha_composite(c_tunic_black)
    out3 = f"{TIGER_DIR}/proof_paperdoll_tiger_tunic_black_magenta.png"
    mag3.save(out3)

    print(f"✓ Saved magenta proofs:\n  • {out1}\n  • {out2}\n  • {out3}")

def generate_verification_crops():
    # Crop 1: Ash Ninja Garb cuirass, pauldron rivets, and brass core bezel
    ninja_slice = Image.open(f"{TIGER_DIR}/costume/costume_ash_ninja_garb.png").convert("RGBA")
    # Region around chest and belt: X[36..90], Y[56..96]
    crop_ninja = ninja_slice.crop((36, 56, 90, 96))
    crop_ninja_large = crop_ninja.resize((crop_ninja.width * 8, crop_ninja.height * 8), Image.Resampling.NEAREST)
    out_ninja = f"{TIGER_DIR}/verification_crop_ash_ninja_garb.png"
    crop_ninja_large.save(out_ninja)

    # Crop 2: Volcano Black chassis torso/limbs plates and joints
    volcano_slice = Image.open(f"{TIGER_DIR}/chassis/paint_volcano_black.png").convert("RGBA")
    # Region around torso/joints: X[34..94], Y[50..105]
    crop_volcano = volcano_slice.crop((34, 50, 94, 105))
    crop_volcano_large = crop_volcano.resize((crop_volcano.width * 8, crop_volcano.height * 8), Image.Resampling.NEAREST)
    out_volcano = f"{TIGER_DIR}/verification_crop_volcano_black.png"
    crop_volcano_large.save(out_volcano)

    print(f"✓ Saved verification crops:\n  • {out_ninja}\n  • {out_volcano}")

if __name__ == "__main__":
    generate_chassis_comparison()
    generate_costume_comparison()
    generate_matrix_proof()
    generate_magenta_proofs()
    generate_verification_crops()
