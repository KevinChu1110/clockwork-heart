#!/usr/bin/env python3
"""
tools/generate_elephant_proofs.py
Generates side-by-side comparison proof images, variants matrix,
magenta composite verification, and verification crop images for Colossus Elephant paperdoll expansion.
- Clean centered 2-line labels with zero overlap
- Crisp 'NEW' badge on top-right of new variant preview cards
- Uses project font Open-Huninn (jf-openhuninn-2.1.ttf)
- Strictly composited from shipped slice assets in z-index order onto magenta
"""

import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
ELEPHANT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/elephant"
PROOFS_DIR = f"{REPO_ROOT}/proofs/wardrobe_elephant"
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
    p = f"{ELEPHANT_DIR}/{slot}/{fn}"
    return Image.open(p).convert("RGBA")

def build_composite(chassis_fn: str, costume_fn: str | None = None) -> Image.Image:
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Z-index ascending order:
    # 1. winding_key (Z: 5)
    comp.alpha_composite(get_slot_layer("winding_key", "key_heavy_cross_wheel.png"))
    # 2. back_curio (Z: 8)
    comp.alpha_composite(get_slot_layer("back_curio", "curio_dual_pressure_gauge.png"))
    # 3. chassis (Z: 10)
    comp.alpha_composite(get_slot_layer("chassis", chassis_fn))
    # 4. head_unit (Z: 20)
    comp.alpha_composite(get_slot_layer("head_unit", "head_colossus_elephant_stock.png"))
    # 5. costume (Z: 25)
    if costume_fn and costume_fn != "none":
        comp.alpha_composite(get_slot_layer("costume", costume_fn))
    # 6. optic_core (Z: 30)
    comp.alpha_composite(get_slot_layer("optic_core", "core_sky_quartz.png"))
    # 7. weapon (Z: 40)
    comp.alpha_composite(get_slot_layer("weapon", "wpn_colossus_cleaver_axe.png"))
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
    c_brass = build_composite("paint_elephant_brass.png", None)
    c_tungsten = build_composite("paint_tungsten_iron.png", None)

    items = [
        (c_brass, "原廠巨輪工坊黃銅原金", "Stock Workshop Brass", False),
        (c_tungsten, "高爐鎢鋼淬火黑 [新]", "Furnace Tungsten Iron", True)
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
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=(140, 150, 170, 255))

    out_p1 = f"{ELEPHANT_DIR}/proof_elephant_chassis_comparison.png"
    out_p2 = f"{PROOFS_DIR}/proof_elephant_chassis_comparison.png"
    canvas.save(out_p1)
    canvas.save(out_p2)
    print(f"  ✓ Saved chassis comparison -> {out_p1}")

def generate_costume_comparison():
    c_overalls = build_composite("paint_elephant_brass.png", "costume_cog_workshop_overalls.png")
    c_bastion = build_composite("paint_elephant_brass.png", "costume_colossus_bastion_plate.png")

    items = [
        (c_overalls, "巨輪工坊厚鋼工裝", "Workshop Overalls", False),
        (c_bastion, "鋼岳要塞重裝戰鎧 [新]", "Colossus Bastion Plate", True)
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
        border_col = (255, 180, 40, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        if is_new:
            draw_new_badge(draw, x, y, (255, 180, 40, 255), (60, 35, 0, 255))

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
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=(140, 150, 170, 255))

    out_p1 = f"{ELEPHANT_DIR}/proof_elephant_costume_comparison.png"
    out_p2 = f"{PROOFS_DIR}/proof_elephant_costume_comparison.png"
    canvas.save(out_p1)
    canvas.save(out_p2)
    print(f"  ✓ Saved costume comparison -> {out_p1}")

def generate_magenta_verification():
    """Generates pure composite on magenta to visually verify zero fringe, zero clipping, perfect alignment."""
    c_new = build_composite("paint_tungsten_iron.png", "costume_colossus_bastion_plate.png")
    mag_canvas = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag_canvas.alpha_composite(c_new)

    out_p1 = f"{ELEPHANT_DIR}/proof_elephant_magenta_verification.png"
    out_p2 = f"{PROOFS_DIR}/proof_elephant_magenta_verification.png"
    mag_canvas.save(out_p1)
    mag_canvas.save(out_p2)
    print(f"  ✓ Saved magenta composite verification -> {out_p1}")

def generate_variants_matrix():
    """Generates 2x2 Matrix showing all combinations of paints and costumes."""
    combinations = [
        ("paint_elephant_brass.png", "costume_cog_workshop_overalls.png", "黃銅原金 ＋ 厚鋼工裝", "Brass + Overalls"),
        ("paint_elephant_brass.png", "costume_colossus_bastion_plate.png", "黃銅原金 ＋ 要塞戰鎧 [新裝]", "Brass + Bastion Plate"),
        ("paint_tungsten_iron.png", "costume_cog_workshop_overalls.png", "鎢鋼黑 ＋ 厚鋼工裝 [新塗]", "Tungsten + Overalls"),
        ("paint_tungsten_iron.png", "costume_colossus_bastion_plate.png", "鎢鋼黑 ＋ 要塞戰鎧 [雙新]", "Tungsten + Bastion Plate")
    ]

    pad = 20
    gap_x = 24
    gap_y = 20
    col_w = 128
    cell_h = 175
    canvas_w = pad * 2 + col_w * 2 + gap_x
    canvas_h = pad * 2 + cell_h * 2 + gap_y

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (20, 22, 28, 255))
    draw = ImageDraw.Draw(canvas)
    font_zh = get_font(12)
    font_en = get_font(10)

    for idx, (ch_fn, cos_fn, l_zh, l_en) in enumerate(combinations):
        col = idx % 2
        row = idx // 2
        x = pad + col * (col_w + gap_x)
        y = pad + row * (cell_h + gap_y)

        comp = build_composite(ch_fn, cos_fn)
        canvas.paste(comp, (x, y), comp)

        is_new = "[新" in l_zh or "[雙新]" in l_zh
        border_col = (255, 180, 40, 255) if "[雙新]" in l_zh else ((56, 160, 255, 255) if is_new else (50, 55, 65, 255))
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        if is_new:
            badge_text = "DOUBLE NEW" if "[雙新]" in l_zh else "NEW"
            badge_w = 68 if "[雙新]" in l_zh else 36
            badge_h = 16
            bx = x + 128 - badge_w - 4
            by = y + 4
            bg_col = (255, 180, 40, 255) if "[雙新]" in l_zh else (56, 160, 255, 255)
            txt_col = (60, 35, 0, 255) if "[雙新]" in l_zh else (10, 30, 60, 255)
            draw.rounded_rectangle((bx, by, bx + badge_w, by + badge_h), radius=3, fill=bg_col)
            font_badge = get_font(9)
            tb = draw.textbbox((0, 0), badge_text, font=font_badge)
            tw = tb[2] - tb[0]
            th = tb[3] - tb[1]
            draw.text((bx + (badge_w - tw) // 2, by + (badge_h - th) // 2 - 1), badge_text, font=font_badge, fill=txt_col)

        b_zh = draw.textbbox((0, 0), l_zh, font=font_zh)
        w_zh = b_zh[2] - b_zh[0]
        tx_zh = x + (128 - w_zh) // 2
        ty_zh = y + 128 + 6
        color_zh = (255, 218, 64, 255) if is_new else (220, 225, 235, 255)
        draw.text((tx_zh, ty_zh), l_zh, font=font_zh, fill=color_zh)

        b_en = draw.textbbox((0, 0), l_en, font=font_en)
        w_en = b_en[2] - b_en[0]
        tx_en = x + (128 - w_en) // 2
        ty_en = ty_zh + 16
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=(135, 145, 165, 255))

    out_p1 = f"{ELEPHANT_DIR}/proof_elephant_variants_matrix.png"
    out_p2 = f"{PROOFS_DIR}/proof_elephant_variants_matrix.png"
    canvas.save(out_p1)
    canvas.save(out_p2)
    print(f"  ✓ Saved variants matrix -> {out_p1}")

def main():
    print("=== GENERATING COLOSSUS ELEPHANT EXPANSION PROOF IMAGES ===")
    os.makedirs(PROOFS_DIR, exist_ok=True)
    generate_chassis_comparison()
    generate_costume_comparison()
    generate_magenta_verification()
    generate_variants_matrix()
    print("=== ALL PROOFS GENERATED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
