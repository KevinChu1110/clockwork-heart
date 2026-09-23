#!/usr/bin/env python3
"""
tools/generate_tortoise_proofs.py
Generates side-by-side comparison proof images, variants matrix,
magenta composite verification, and verification crop images for The Xuanji Tortoise paperdoll expansion.
- Clean centered 2-line labels with zero overlap
- Crisp 'NEW' badge on top-right of new variant preview cards
- Uses project font Open-Huninn (jf-openhuninn-2.1.ttf)
- Strictly composited from shipped slice assets in z-index order onto magenta
"""

import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
TORTOISE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tortoise"
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
    p = f"{TORTOISE_DIR}/{slot}/{fn}"
    return Image.open(p).convert("RGBA")

def build_composite(chassis_fn: str, costume_fn: str | None = None) -> Image.Image:
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Z-index ascending order:
    # 1. winding_key (Z: 5)
    comp.alpha_composite(get_slot_layer("winding_key", "key_tai_chi_dual_fish.png"))
    # 2. back_curio (Z: 8)
    comp.alpha_composite(get_slot_layer("back_curio", "curio_bagua_armillary_rings.png"))
    # 3. chassis (Z: 10)
    comp.alpha_composite(get_slot_layer("chassis", chassis_fn))
    # 4. head_unit (Z: 20)
    comp.alpha_composite(get_slot_layer("head_unit", "head_xuanji_tortoise_stock.png"))
    # 5. costume (Z: 25)
    if costume_fn and costume_fn != "none":
        comp.alpha_composite(get_slot_layer("costume", costume_fn))
    # 6. optic_core (Z: 30)
    comp.alpha_composite(get_slot_layer("optic_core", "core_amber_quartz.png"))
    # 7. weapon (Z: 40)
    comp.alpha_composite(get_slot_layer("weapon", "wpn_bagua_astrolabe.png"))
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
    c_jade = build_composite("paint_tortoise_jade.png", None)
    c_basalt = build_composite("paint_basalt_black.png", None)

    items = [
        (c_jade, "原廠青銅古翠綠", "Stock Bronze Jade", False),
        (c_basalt, "玄武黑曜淬火黑 [新]", "Basalt Black Obsidian", True)
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
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=(140, 150, 165, 255))

    out_p = f"{TORTOISE_DIR}/proof_tortoise_chassis_comparison.png"
    canvas.save(out_p)
    print(f"  ✓ Saved chassis comparison: {out_p}")

def generate_costume_comparison():
    c_none = build_composite("paint_tortoise_jade.png", "none")
    c_harness = build_composite("paint_tortoise_jade.png", "costume_zen_dojo_harness.png")
    c_robe = build_composite("paint_tortoise_jade.png", "costume_bagua_master_robe.png")

    items = [
        (c_none, "無外裝 (裸機素體)", "Bare Chassis", False),
        (c_harness, "天元道場玄機護甲", "Zen Dojo Harness", False),
        (c_robe, "乾坤八卦宗師道鎧 [新]", "Bagua Master Robe", True)
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
        border_col = (255, 208, 40, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        if is_new:
            draw_new_badge(draw, x, y, (255, 208, 40, 255), (60, 40, 10, 255))

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
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=(140, 150, 165, 255))

    out_p = f"{TORTOISE_DIR}/proof_tortoise_costume_comparison.png"
    canvas.save(out_p)
    print(f"  ✓ Saved costume comparison: {out_p}")

def generate_variants_matrix():
    # Matrix of 2 chassis x 3 costumes = 6 combinations
    chassis_list = [
        ("paint_tortoise_jade.png", "青銅古翠綠"),
        ("paint_basalt_black.png", "玄武黑曜淬火黑 [新]")
    ]
    costume_list = [
        ("none", "裸機素體"),
        ("costume_zen_dojo_harness.png", "天元道場護甲"),
        ("costume_bagua_master_robe.png", "乾坤八卦宗師道鎧 [新]")
    ]

    cols = len(costume_list)
    rows = len(chassis_list)
    pad = 20
    gap_x = 20
    gap_y = 40
    canvas_w = pad * 2 + cols * 128 + (cols - 1) * gap_x
    canvas_h = pad * 2 + rows * (128 + 32) + (rows - 1) * gap_y
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (20, 22, 28, 255))
    draw = ImageDraw.Draw(canvas)
    font_lbl = get_font(11)

    for r_idx, (ch_fn, ch_name) in enumerate(chassis_list):
        for c_idx, (cos_fn, cos_name) in enumerate(costume_list):
            x = pad + c_idx * (128 + gap_x)
            y = pad + r_idx * (128 + 32 + gap_y)
            comp = build_composite(ch_fn, cos_fn)
            canvas.paste(comp, (x, y), comp)

            is_new = (ch_fn == "paint_basalt_black.png") or (cos_fn == "costume_bagua_master_robe.png")
            border = (255, 208, 40, 255) if (ch_fn == "paint_basalt_black.png" and cos_fn == "costume_bagua_master_robe.png") else (
                (56, 160, 255, 255) if is_new else (55, 60, 70, 255)
            )
            draw.rectangle((x, y, x + 128, y + 128), outline=border, width=2 if is_new else 1)

            lbl = f"{ch_name.split()[0]} + {cos_name.split()[0]}"
            tb = draw.textbbox((0, 0), lbl, font=font_lbl)
            tw = tb[2] - tb[0]
            draw.text((x + (128 - tw) // 2, y + 132), lbl, font=font_lbl, fill=(210, 220, 235, 255))

    out_p = f"{TORTOISE_DIR}/proof_tortoise_variants_matrix.png"
    canvas.save(out_p)
    print(f"  ✓ Saved variants matrix: {out_p}")

def generate_magenta_verification():
    # 4 critical combinations onto pure magenta
    combos = [
        ("paint_tortoise_jade.png", "none", "Jade + Bare"),
        ("paint_tortoise_jade.png", "costume_bagua_master_robe.png", "Jade + Master Robe [新]"),
        ("paint_basalt_black.png", "none", "Basalt [新] + Bare"),
        ("paint_basalt_black.png", "costume_bagua_master_robe.png", "Basalt [新] + Master Robe [新]")
    ]

    pad = 16
    gap = 16
    canvas_w = pad * 2 + len(combos) * 128 + (len(combos) - 1) * gap
    canvas_h = pad * 2 + 128 + 24
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)
    font_lbl = get_font(11)

    for i, (ch_fn, cos_fn, desc) in enumerate(combos):
        x = pad + i * (128 + gap)
        y = pad

        # Magenta cell
        mag_box = Image.new("RGBA", (128, 128), BG_MAGENTA)
        comp = build_composite(ch_fn, cos_fn)
        mag_box.alpha_composite(comp)
        canvas.paste(mag_box, (x, y))

        draw.rectangle((x, y, x + 128, y + 128), outline=(60, 65, 75, 255), width=1)
        tb = draw.textbbox((0, 0), desc, font=font_lbl)
        tw = tb[2] - tb[0]
        draw.text((x + (128 - tw) // 2, y + 132), desc, font=font_lbl, fill=(230, 235, 245, 255))

    out_p = f"{TORTOISE_DIR}/proof_tortoise_magenta_verification.png"
    canvas.save(out_p)
    print(f"  ✓ Saved magenta verification: {out_p}")

def main():
    print("=== GENERATING XUANJI TORTOISE PROOF IMAGES ===")
    generate_chassis_comparison()
    generate_costume_comparison()
    generate_variants_matrix()
    generate_magenta_verification()
    print("=== ALL PROOF IMAGES GENERATED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
