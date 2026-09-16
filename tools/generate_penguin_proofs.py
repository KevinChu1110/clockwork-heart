#!/usr/bin/env python3
"""
tools/generate_penguin_proofs.py
Generates side-by-side comparison proof images, variants matrix,
magenta composite verification, and verification crop images for The Steam Penguin paperdoll expansion.
- Clean centered 2-line labels with zero overlap
- Crisp 'NEW' badge on top-right of new variant preview cards
- Uses project font Open-Huninn (jf-openhuninn-2.1.ttf)
- Strictly composited from shipped slice assets in z-index order onto magenta
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
PENGUIN_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin"
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
    p = f"{PENGUIN_DIR}/{slot}/{fn}"
    return Image.open(p).convert("RGBA")

def build_composite(chassis_fn: str, costume_fn: str | None = None) -> Image.Image:
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Z-index ascending order:
    # 1. winding_key (Z: 5)
    comp.alpha_composite(get_slot_layer("winding_key", "key_twin_ring_helm.png"))
    # 2. back_curio (Z: 8)
    comp.alpha_composite(get_slot_layer("back_curio", "curio_mini_steam_boiler.png"))
    # 3. chassis (Z: 10)
    comp.alpha_composite(get_slot_layer("chassis", chassis_fn))
    # 4. head_unit (Z: 20)
    comp.alpha_composite(get_slot_layer("head_unit", "head_steam_penguin_stock.png"))
    # 5. costume (Z: 25)
    if costume_fn and costume_fn != "none":
        comp.alpha_composite(get_slot_layer("costume", costume_fn))
    # 6. optic_core (Z: 30)
    comp.alpha_composite(get_slot_layer("optic_core", "core_cyan_quartz.png"))
    # 7. weapon (Z: 40)
    comp.alpha_composite(get_slot_layer("weapon", "wpn_twin_harpoon_gun.png"))
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
    c_navy = build_composite("paint_penguin_navy.png", None)
    c_polar = build_composite("paint_polar_frost.png", None)
    c_ivory = build_composite("paint_ivory_stock.png", None)

    items = [
        (c_navy, "原廠深海鍍鈦藍", "Deepsea Navy Titanium", False),
        (c_polar, "極光冰川銀白 [新]", "Polar Frost Chrome", True),
        (c_ivory, "原廠象牙白", "Ivory Stock", False)
    ]

    pad = 20
    gap = 24
    canvas_w = pad * 2 + 128 * len(items) + gap * (len(items) - 1)
    canvas_h = 205
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)
    font_zh = get_font(13)
    font_en = get_font(11)

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (56, 160, 255, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        if is_new:
            draw_new_badge(draw, x, y, (56, 160, 255, 255), (10, 30, 60, 255))

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
        color_en = (100, 200, 255, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{PENGUIN_DIR}/proof_penguin_chassis_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved chassis comparison: {out_p}")

def generate_costume_comparison():
    c_bare = build_composite("paint_penguin_navy.png", None)
    c_nav = build_composite("paint_penguin_navy.png", "costume_navigator_harness.png")
    c_abyssal = build_composite("paint_penguin_navy.png", "costume_abyssal_diver_cuirass.png")

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
        (c_nav, "深海導航員大衣", "Navigator Harness", False),
        (c_abyssal, "淵海深潛耐壓機關鎧 [新]", "Abyssal Diver Cuirass", True)
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
        color_en = (255, 180, 50, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{PENGUIN_DIR}/proof_penguin_costume_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved costume comparison: {out_p}")

def generate_matrix_proof():
    chassis_list = [
        ("paint_penguin_navy.png", "原廠深海鍍鈦藍"),
        ("paint_polar_frost.png", "極光冰川銀白 [新]")
    ]
    costume_list = [
        ("costume_navigator_harness.png", "深海導航員大衣"),
        ("costume_abyssal_diver_cuirass.png", "淵海深潛耐壓機關鎧 [新]"),
        (None, "裸機素體")
    ]

    pad = 14
    gap = 14
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
            is_new = (cos_fn == "costume_abyssal_diver_cuirass.png") or (ch_fn == "paint_polar_frost.png")
            border_col = (255, 160, 16, 255) if is_new else (50, 55, 65, 255)
            draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

    out_p = f"{PENGUIN_DIR}/proof_penguin_variants_matrix.png"
    canvas.save(out_p)
    print(f"✓ Saved mix-and-match matrix: {out_p}")

def generate_magenta_proofs():
    # 1. Abyssal Diver Cuirass on Polar Frost (New Costume + New Paint)
    c_new_both = build_composite("paint_polar_frost.png", "costume_abyssal_diver_cuirass.png")
    mag1 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag1.alpha_composite(c_new_both)
    out1 = f"{PENGUIN_DIR}/proof_paperdoll_penguin_abyssal_polar_magenta.png"
    mag1.save(out1)

    # 2. Abyssal Diver Cuirass on Navy Titanium (New Costume + Stock Navy)
    c_aby_navy = build_composite("paint_penguin_navy.png", "costume_abyssal_diver_cuirass.png")
    mag2 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag2.alpha_composite(c_aby_navy)
    out2 = f"{PENGUIN_DIR}/proof_paperdoll_penguin_abyssal_magenta.png"
    mag2.save(out2)

    # 3. Navigator Harness on Polar Frost (Stock Costume + New Paint)
    c_nav_polar = build_composite("paint_polar_frost.png", "costume_navigator_harness.png")
    mag3 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag3.alpha_composite(c_nav_polar)
    out3 = f"{PENGUIN_DIR}/proof_paperdoll_penguin_polar_magenta.png"
    mag3.save(out3)

    print(f"✓ Saved magenta proofs:\n  • {out1}\n  • {out2}\n  • {out3}")

def generate_verification_crops():
    # Crop 1: Abyssal Diver Cuirass, pauldron rivets, and brass core bezel
    aby_slice = Image.open(f"{PENGUIN_DIR}/costume/costume_abyssal_diver_cuirass.png").convert("RGBA")
    # Region around chest and shoulders: X[32..90], Y[48..96]
    crop_aby = aby_slice.crop((32, 48, 90, 96))
    crop_aby_large = crop_aby.resize((crop_aby.width * 8, crop_aby.height * 8), Image.Resampling.NEAREST)
    out_aby = f"{PENGUIN_DIR}/verification_crop_abyssal_cuirass.png"
    crop_aby_large.save(out_aby)

    # Crop 2: Polar Frost chassis flipper joints and feet
    polar_slice = Image.open(f"{PENGUIN_DIR}/chassis/paint_polar_frost.png").convert("RGBA")
    # Region around flippers, torso, and feet: X[20..90], Y[48..122]
    crop_polar = polar_slice.crop((20, 48, 90, 122))
    crop_polar_large = crop_polar.resize((crop_polar.width * 8, crop_polar.height * 8), Image.Resampling.NEAREST)
    out_polar = f"{PENGUIN_DIR}/verification_crop_polar_frost.png"
    crop_polar_large.save(out_polar)

    print(f"✓ Saved verification crops:\n  • {out_aby}\n  • {out_polar}")

def main():
    print("=== GENERATING THE STEAM PENGUIN PAPERDOLL EXPANSION PROOFS ===")
    generate_chassis_comparison()
    generate_costume_comparison()
    generate_matrix_proof()
    generate_magenta_proofs()
    generate_verification_crops()
    print("=== ALL STEAM PENGUIN PROOFS GENERATED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
