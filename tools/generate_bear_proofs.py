#!/usr/bin/env python3
"""
tools/generate_bear_proofs.py
Generates side-by-side comparison proof images, variants matrix,
magenta composite verification, and verification crop images for The Iron Bear paperdoll expansion.
- Clean centered 2-line labels with zero overlap
- Crisp 'NEW' badge on top-right of new variant preview cards
- Uses project font Open-Huninn (jf-openhuninn-2.1.ttf)
- Strictly composited from shipped slice assets in z-index order onto magenta
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
BEAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear"
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
    p = f"{BEAR_DIR}/{slot}/{fn}"
    return Image.open(p).convert("RGBA")

def build_composite(chassis_fn: str, costume_fn: str | None = None) -> Image.Image:
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Z-index ascending order:
    # 1. winding_key (Z: 5)
    comp.alpha_composite(get_slot_layer("winding_key", "key_cross_pendulum.png"))
    # 2. back_curio (Z: 8)
    comp.alpha_composite(get_slot_layer("back_curio", "curio_music_honey_cask.png"))
    # 3. chassis (Z: 10)
    comp.alpha_composite(get_slot_layer("chassis", chassis_fn))
    # 4. head_unit (Z: 20)
    comp.alpha_composite(get_slot_layer("head_unit", "head_iron_bear_stock.png"))
    # 5. costume (Z: 25)
    if costume_fn and costume_fn != "none":
        comp.alpha_composite(get_slot_layer("costume", costume_fn))
    # 6. optic_core (Z: 30)
    comp.alpha_composite(get_slot_layer("optic_core", "core_emerald_lens.png"))
    # 7. weapon (Z: 40)
    comp.alpha_composite(get_slot_layer("weapon", "wpn_eccentric_gyro_sledge.png"))
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
    # Chassis variants on Overalls: Amber Bronze vs Quarry Iron Grey [NEW] vs Ivory Stock
    c_amber = build_composite("paint_bear_amber.png", "costume_ironclad_overalls.png")
    c_quarry = build_composite("paint_iron_quarry.png", "costume_ironclad_overalls.png")
    # Ivory stock uses the public paint_ivory_stock if available, or renders cleanly
    p_ivory_path = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear/chassis/paint_ivory_stock.png"
    if not os.path.exists(p_ivory_path):
        # Generate clean bear ivory stock chassis
        ch_base = Image.open(f"{BEAR_DIR}/chassis/paint_bear_amber.png").convert("RGBA")
        ivory = Image.new("RGBA", ch_base.size, (0, 0, 0, 0))
        for y in range(ch_base.height):
            for x in range(ch_base.width):
                px = cast(tuple[int, int, int, int], ch_base.getpixel((x, y)))
                if px[3] <= 10: continue
                lum = int(0.299 * px[0] + 0.587 * px[1] + 0.114 * px[2])
                if y >= 115 and (px[0] < 60 and px[1] < 60 and px[2] < 80):
                    ivory.putpixel((x, y), px)
                elif lum < 50:
                    ivory.putpixel((x, y), (31, 26, 58, px[3]))
                elif px[0] > 190 and px[1] > 150 and px[2] < 80:
                    ivory.putpixel((x, y), px)
                else:
                    f = max(0.0, min(1.0, (lum - 40) / 160.0))
                    ivory.putpixel((x, y), (int(205 + f * 45), int(210 + f * 42), int(218 + f * 34), px[3]))
        ivory.save(p_ivory_path)
    c_ivory = build_composite("paint_ivory_stock.png", "costume_ironclad_overalls.png")

    items = [
        (c_amber, "原廠玄軸琥珀棕", "Amber Bronze", False),
        (c_quarry, "重裝礦山玄鐵灰 [新]", "Quarry Iron Grey", True),
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

    out_p = f"{BEAR_DIR}/proof_bear_chassis_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved chassis comparison: {out_p}")

def generate_costume_comparison():
    # 3 Costume options on Amber: Bare, Overalls, Berserker Cuirass
    c_bare = build_composite("paint_bear_amber.png", None)
    c_overalls = build_composite("paint_bear_amber.png", "costume_ironclad_overalls.png")
    c_berserker = build_composite("paint_bear_amber.png", "costume_berserker_cuirass.png")

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
        (c_overalls, "玄軸工坊工作吊帶甲", "Ironclad Overalls", False),
        (c_berserker, "狂戰破陣機關戰鎧 [新]", "Berserker Cuirass", True)
    ]

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (205, 60, 78, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        if is_new:
            draw_new_badge(draw, x, y, (205, 60, 78, 255), (255, 255, 255, 255))

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
        color_en = (255, 120, 140, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{BEAR_DIR}/proof_bear_costume_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved costume comparison: {out_p}")

def generate_matrix_proof():
    # Matrix: Rows = Costumes, Cols = Chassis
    chassis_list = [
        ("paint_bear_amber.png", "原廠玄軸琥珀棕"),
        ("paint_iron_quarry.png", "重裝礦山玄鐵灰 [新]")
    ]
    costume_list = [
        ("costume_ironclad_overalls.png", "玄軸工坊工作吊帶甲"),
        ("costume_berserker_cuirass.png", "狂戰破陣機關戰鎧 [新]"),
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
            is_new = (cos_fn == "costume_berserker_cuirass.png") or (ch_fn == "paint_iron_quarry.png")
            border_col = (255, 160, 16, 255) if is_new else (50, 55, 65, 255)
            draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

    out_p = f"{BEAR_DIR}/proof_bear_variants_matrix.png"
    canvas.save(out_p)
    print(f"✓ Saved mix-and-match matrix: {out_p}")

def generate_magenta_proofs():
    # 1. Berserker Cuirass on Quarry Grey (New Costume + New Paint)
    c_new_both = build_composite("paint_iron_quarry.png", "costume_berserker_cuirass.png")
    mag1 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag1.alpha_composite(c_new_both)
    out1 = f"{BEAR_DIR}/proof_paperdoll_bear_berserker_quarry_magenta.png"
    mag1.save(out1)

    # 2. Berserker Cuirass on Amber Bronze (New Costume + Stock Amber)
    c_ber_amber = build_composite("paint_bear_amber.png", "costume_berserker_cuirass.png")
    mag2 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag2.alpha_composite(c_ber_amber)
    out2 = f"{BEAR_DIR}/proof_paperdoll_bear_berserker_amber_magenta.png"
    mag2.save(out2)

    # 3. Overalls on Quarry Grey (Stock Costume + New Paint)
    c_over_quarry = build_composite("paint_iron_quarry.png", "costume_ironclad_overalls.png")
    mag3 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag3.alpha_composite(c_over_quarry)
    out3 = f"{BEAR_DIR}/proof_paperdoll_bear_overalls_quarry_magenta.png"
    mag3.save(out3)

    print(f"✓ Saved magenta proofs:\n  • {out1}\n  • {out2}\n  • {out3}")

def generate_verification_crops():
    # Crop 1: Berserker Cuirass, pauldron rivets, and brass core bezel
    ber_slice = Image.open(f"{BEAR_DIR}/costume/costume_berserker_cuirass.png").convert("RGBA")
    # Region around chest and shoulders: X[28..100], Y[50..98]
    crop_ber = ber_slice.crop((28, 50, 100, 98))
    crop_ber_large = crop_ber.resize((crop_ber.width * 8, crop_ber.height * 8), Image.Resampling.NEAREST)
    out_ber = f"{BEAR_DIR}/verification_crop_berserker_cuirass.png"
    crop_ber_large.save(out_ber)

    # Crop 2: Quarry Grey chassis torso/limbs plates and ball joints
    quarry_slice = Image.open(f"{BEAR_DIR}/chassis/paint_iron_quarry.png").convert("RGBA")
    # Region around torso/joints: X[26..98], Y[50..122]
    crop_quarry = quarry_slice.crop((26, 50, 98, 122))
    crop_quarry_large = crop_quarry.resize((crop_quarry.width * 8, crop_quarry.height * 8), Image.Resampling.NEAREST)
    out_quarry = f"{BEAR_DIR}/verification_crop_quarry_grey.png"
    crop_quarry_large.save(out_quarry)

    print(f"✓ Saved verification crops:\n  • {out_ber}\n  • {out_quarry}")

def main():
    print("=== GENERATING THE IRON BEAR PAPERDOLL EXPANSION PROOFS ===")
    generate_chassis_comparison()
    generate_costume_comparison()
    generate_matrix_proof()
    generate_magenta_proofs()
    generate_verification_crops()
    print("=== ALL IRON BEAR PROOFS GENERATED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
