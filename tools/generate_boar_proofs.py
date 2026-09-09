#!/usr/bin/env python3
"""
tools/generate_boar_proofs.py
Generates side-by-side comparison proof images, magenta composite verification,
and verification crop images for Boar paperdoll expansion.
- Clean centered 2-line labels with zero overlap (Rule 10a-2 review feedback)
- Uses project font Open-Huninn (jf-openhuninn-2.1.ttf)
- Strictly composited from shipped slice assets in z-index order onto magenta (Rule 19f-3 / 4c-4)
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
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
    p = f"{BOAR_DIR}/{slot}/{fn}"
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
    comp.alpha_composite(get_slot_layer("head_unit", "ear_boar_rivet_cowl.png"))
    # 5. costume (Z: 25)
    if costume_fn and costume_fn != "none":
        comp.alpha_composite(get_slot_layer("costume", costume_fn))
    # 6. optic_core (Z: 30)
    comp.alpha_composite(get_slot_layer("optic_core", "core_cyan_emerald.png"))
    # 7. weapon (Z: 40)
    comp.alpha_composite(get_slot_layer("weapon", "wpn_anvil_greathammer.png"))
    return comp

def generate_chassis_comparison():
    # 3 Chassis variants on Viking Harness costume
    c_gold = build_composite("paint_brass_gold.png", "costume_viking_harness.png")
    c_ivory = build_composite("paint_ivory_stock.png", "costume_viking_harness.png")
    c_crimson = build_composite("paint_molten_crimson.png", "costume_viking_harness.png")

    pad = 20
    gap = 24
    canvas_w = pad * 2 + 128 * 3 + gap * 2 # 472
    canvas_h = 205
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)
    font_zh = get_font(13)
    font_en = get_font(11)

    items = [
        (c_gold, "黃銅原金", "Brass Gold", False),
        (c_ivory, "原廠象牙白", "Ivory Stock", False),
        (c_crimson, "赤焰熔爐 [新]", "Molten Crimson", True)
    ]

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (255, 69, 0, 255) if is_new else (60, 65, 75, 255)
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
        color_en = (255, 69, 0, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{BOAR_DIR}/proof_boar_chassis_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved chassis comparison: {out_p}")

def generate_costume_comparison():
    # 3 Costume options on Brass Gold: Bare, Viking Harness, Viking Ironclad
    c_bare = build_composite("paint_brass_gold.png", None)
    c_har = build_composite("paint_brass_gold.png", "costume_viking_harness.png")
    c_iron = build_composite("paint_brass_gold.png", "costume_viking_ironclad.png")

    pad = 20
    gap = 24
    canvas_w = pad * 2 + 128 * 3 + gap * 2 # 472
    canvas_h = 205
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)
    font_zh = get_font(13)
    font_en = get_font(11)

    items = [
        (c_bare, "裸機素體", "Bare Chassis", False),
        (c_har, "鍛爐鐵束帶", "Viking Harness", False),
        (c_iron, "維京重裝鐵甲 [新]", "Viking Ironclad", True)
    ]

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (255, 69, 0, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

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
        color_en = (255, 69, 0, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{BOAR_DIR}/proof_boar_costume_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved costume comparison: {out_p}")

def generate_variants_matrix():
    # 3 Chassis x 3 Costume matrix = 9 cells
    chassis_list = [
        ("paint_brass_gold.png", "黃銅原金 (Brass Gold)"),
        ("paint_ivory_stock.png", "象牙白 (Ivory Stock)"),
        ("paint_molten_crimson.png", "赤焰熔爐 (Molten Crimson)")
    ]
    costume_list = [
        (None, "裸機素體 (Bare)"),
        ("costume_viking_harness.png", "鍛爐鐵束帶 (Harness)"),
        ("costume_viking_ironclad.png", "維京重裝 (Ironclad)")
    ]

    pad = 24
    header_top = 40
    header_left = 185
    cell_size = 128
    gap = 20

    grid_w = header_left + 3 * cell_size + 2 * gap + pad
    grid_h = header_top + 3 * cell_size + 2 * gap + pad
    canvas = Image.new("RGBA", (grid_w, grid_h), (20, 22, 28, 255))
    draw = ImageDraw.Draw(canvas)
    font = get_font(12)

    # Draw column headers (Costumes)
    for col_idx, (_, c_label) in enumerate(costume_list):
        cx = header_left + col_idx * (cell_size + gap)
        bbox = draw.textbbox((0, 0), c_label, font=font)
        tw = bbox[2] - bbox[0]
        tx = cx + (cell_size - tw) // 2
        draw.text((tx, 14), c_label, font=font, fill=(240, 242, 248, 255))

    # Draw row headers (Chassis) and composite cells
    for row_idx, (ch_fn, ch_label) in enumerate(chassis_list):
        cy = header_top + row_idx * (cell_size + gap)
        # Row label
        draw.text((pad, cy + 54), ch_label, font=font, fill=(200, 208, 225, 255))

        for col_idx, (cos_fn, _) in enumerate(costume_list):
            cx = header_left + col_idx * (cell_size + gap)
            comp = build_composite(ch_fn, cos_fn)
            canvas.paste(comp, (cx, cy), comp)
            # Highlight border for new variant combos
            is_new = (ch_fn == "paint_molten_crimson.png" or cos_fn == "costume_viking_ironclad.png")
            b_col = (255, 69, 0, 255) if is_new else (50, 54, 66, 255)
            draw.rectangle((cx, cy, cx + cell_size, cy + cell_size), outline=b_col, width=2 if is_new else 1)

    out_p = f"{BOAR_DIR}/proof_boar_variants_matrix.png"
    canvas.save(out_p)
    print(f"✓ Saved 3x3 variants matrix: {out_p}")

def generate_magenta_verifications():
    combos = [
        ("proof_paperdoll_boar_ironclad_crimson_magenta.png", "paint_molten_crimson.png", "costume_viking_ironclad.png"),
        ("proof_paperdoll_boar_ironclad_gold_magenta.png", "paint_brass_gold.png", "costume_viking_ironclad.png"),
        ("proof_paperdoll_boar_harness_crimson_magenta.png", "paint_molten_crimson.png", "costume_viking_harness.png"),
    ]

    for out_fn, ch_fn, cos_fn in combos:
        comp = build_composite(ch_fn, cos_fn)
        mag = Image.new("RGBA", (128, 128), BG_MAGENTA)
        mag.alpha_composite(comp)
        p = f"{BOAR_DIR}/{out_fn}"
        mag.save(p)
        print(f"✓ Saved magenta verification: {p}")

def generate_verification_crops():
    # High-resolution crops for vision model inspections
    ch_img = Image.open(f"{BOAR_DIR}/chassis/paint_molten_crimson.png").convert("RGBA")
    cos_img = Image.open(f"{BOAR_DIR}/costume/costume_viking_ironclad.png").convert("RGBA")

    # Crop chassis torso / leg area (35, 60, 95, 120) and scale 4x
    crop_ch = ch_img.crop((35, 60, 95, 120)).resize((240, 240), Image.Resampling.NEAREST)
    p_ch = f"{BOAR_DIR}/verification_crop_molten_crimson.png"
    crop_ch.save(p_ch)
    print(f"✓ Saved verification crop: {p_ch}")

    # Crop costume pauldron & breastplate (48, 45, 93, 96) and scale 4x
    crop_cos = cos_img.crop((48, 45, 93, 96)).resize((180, 204), Image.Resampling.NEAREST)
    p_cos = f"{BOAR_DIR}/verification_crop_viking_ironclad.png"
    crop_cos.save(p_cos)
    print(f"✓ Saved verification crop: {p_cos}")

if __name__ == "__main__":
    generate_chassis_comparison()
    generate_costume_comparison()
    generate_variants_matrix()
    generate_magenta_verifications()
    generate_verification_crops()
