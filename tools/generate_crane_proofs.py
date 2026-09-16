#!/usr/bin/env python3
"""
tools/generate_crane_proofs.py
Generates side-by-side comparison proof images, variants matrix,
magenta composite verification, and verification crop images for Cloud Crane paperdoll expansion.
- Clean centered 2-line labels with zero overlap
- Crisp 'NEW' badge on top-right of new variant preview cards
- Uses project font Open-Huninn (jf-openhuninn-2.1.ttf)
- Strictly composited from shipped slice assets in z-index order onto magenta
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
CRANE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crane"
COMMON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll"
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
    p = f"{CRANE_DIR}/{slot}/{fn}"
    if not os.path.exists(p):
        # Fallback to universal/other races if needed
        p_alt = f"{COMMON_DIR}/{slot}/{fn}"
        if os.path.exists(p_alt):
            return Image.open(p_alt).convert("RGBA")
        p_rabbit = f"{COMMON_DIR}/rabbit/{slot}/{fn}"
        if os.path.exists(p_rabbit):
            return Image.open(p_rabbit).convert("RGBA")
    return Image.open(p).convert("RGBA")

def build_composite(chassis_fn: str, costume_fn: str | None = None) -> Image.Image:
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Z-index ascending order:
    # 1. winding_key (Z: 5)
    comp.alpha_composite(get_slot_layer("winding_key", "key_tri_wing_zephyr.png"))
    # 2. back_curio (Z: 8)
    comp.alpha_composite(get_slot_layer("back_curio", "curio_origami_crane.png"))
    # 3. chassis (Z: 10)
    comp.alpha_composite(get_slot_layer("chassis", chassis_fn))
    # 4. head_unit (Z: 20)
    comp.alpha_composite(get_slot_layer("head_unit", "head_cloud_crane_stock.png"))
    # 5. costume (Z: 25)
    if costume_fn and costume_fn != "none":
        comp.alpha_composite(get_slot_layer("costume", costume_fn))
    # 6. optic_core (Z: 30)
    comp.alpha_composite(get_slot_layer("optic_core", "core_vermilion_lens.png"))
    # 7. weapon (Z: 40)
    comp.alpha_composite(get_slot_layer("weapon", "wpn_zephyr_wing_bow.png"))
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
    c_porcelain = build_composite("paint_crane_porcelain.png", "costume_zephyr_robe.png")
    c_azure = build_composite("paint_zephyr_azure.png", "costume_zephyr_robe.png")
    c_ivory = build_composite("paint_ivory_stock.png", "costume_zephyr_robe.png")

    pad = 20
    gap = 24
    canvas_w = pad * 2 + 128 * 3 + gap * 2
    canvas_h = 205
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)
    font_zh = get_font(13)
    font_en = get_font(11)

    items = [
        (c_porcelain, "原廠冷淬青瓷白", "Porcelain White", False),
        (c_azure, "晴空凌雲湛藍 [新]", "Zephyr Azure", True),
        (c_ivory, "原廠象牙白", "Ivory Stock", False)
    ]

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (56, 160, 255, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        if is_new:
            draw_new_badge(draw, x, y, (56, 160, 255, 255), (255, 255, 255, 255))

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
        color_en = (100, 180, 255, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{CRANE_DIR}/proof_crane_chassis_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved chassis comparison: {out_p}")

def generate_costume_comparison():
    c_bare = build_composite("paint_crane_porcelain.png", None)
    c_robe = build_composite("paint_crane_porcelain.png", "costume_zephyr_robe.png")
    c_hunter = build_composite("paint_crane_porcelain.png", "costume_sky_hunter_mail.png")

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
        (c_robe, "凌雲羽衣輕鋼道袍", "Zephyr Wind Robe", False),
        (c_hunter, "晴空巡獵機關羽甲 [新]", "Sky Hunter Mail", True)
    ]

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (255, 208, 40, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        if is_new:
            draw_new_badge(draw, x, y, (255, 208, 40, 255), (40, 25, 0, 255))

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
        color_en = (255, 208, 40, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{CRANE_DIR}/proof_crane_costume_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved costume comparison: {out_p}")

def generate_variants_matrix():
    # 2 chassis x 3 costumes
    chassis_list = [
        ("paint_crane_porcelain.png", "原廠青瓷白", "Porcelain"),
        ("paint_zephyr_azure.png", "晴空凌雲湛藍", "Zephyr Azure")
    ]
    costume_list = [
        (None, "裸機素體", "Bare Chassis"),
        ("costume_zephyr_robe.png", "凌雲羽衣輕鋼道袍", "Zephyr Robe"),
        ("costume_sky_hunter_mail.png", "晴空巡獵機關羽甲", "Sky Hunter Mail")
    ]

    pad = 28
    gap_x = 36
    gap_y = 48
    canvas_w = pad * 2 + 128 * 3 + gap_x * 2
    canvas_h = pad * 2 + 128 * 2 + gap_y + 44
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (20, 22, 28, 255))
    draw = ImageDraw.Draw(canvas)
    font_title = get_font(15)
    font_zh1 = get_font(12)
    font_zh2 = get_font(11)

    # Title
    t_text = "雲嵐鶴 (Cloud Crane) 紙娃娃雙塗裝 x 雙外裝矩陣"
    tb = draw.textbbox((0, 0), t_text, font=font_title)
    draw.text(((canvas_w - (tb[2] - tb[0])) // 2, 12), t_text, font=font_title, fill=(255, 218, 64, 255))

    for row_idx, (ch_fn, ch_zh, ch_en) in enumerate(chassis_list):
        for col_idx, (cos_fn, cos_zh, cos_en) in enumerate(costume_list):
            comp = build_composite(ch_fn, cos_fn)
            x = pad + col_idx * (128 + gap_x)
            y = 44 + row_idx * (128 + gap_y)

            canvas.paste(comp, (x, y), comp)
            is_new = (cos_fn == "costume_sky_hunter_mail.png" or ch_fn == "paint_zephyr_azure.png")
            border_col = (255, 160, 16, 255) if is_new else (55, 60, 70, 255)
            draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

            if is_new:
                draw_new_badge(draw, x, y, (255, 160, 16, 255), (40, 20, 0, 255))

            # Two neat lines to avoid any horizontal overlap
            lb1 = draw.textbbox((0, 0), cos_zh, font=font_zh1)
            lw1 = lb1[2] - lb1[0]
            col1 = (255, 218, 64, 255) if is_new else (225, 230, 240, 255)
            draw.text((x + (128 - lw1) // 2, y + 128 + 6), cos_zh, font=font_zh1, fill=col1)

            lb2 = draw.textbbox((0, 0), f"({ch_zh})", font=font_zh2)
            lw2 = lb2[2] - lb2[0]
            col2 = (56, 160, 255, 255) if is_new else (140, 148, 165, 255)
            draw.text((x + (128 - lw2) // 2, y + 128 + 22), f"({ch_zh})", font=font_zh2, fill=col2)

    out_p = f"{CRANE_DIR}/proof_crane_variants_matrix.png"
    canvas.save(out_p)
    print(f"✓ Saved variants matrix: {out_p}")

def generate_magenta_proofs():
    # 1. Porcelain + Sky Hunter on magenta
    comp_sky_hunter = build_composite("paint_crane_porcelain.png", "costume_sky_hunter_mail.png")
    m1 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    m1.alpha_composite(comp_sky_hunter)
    out1 = f"{CRANE_DIR}/proof_paperdoll_crane_sky_hunter_magenta.png"
    m1.save(out1)
    print(f"✓ Saved sky hunter magenta proof: {out1}")

    # 2. Azure + Zephyr Robe on magenta
    comp_azure_robe = build_composite("paint_zephyr_azure.png", "costume_zephyr_robe.png")
    m2 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    m2.alpha_composite(comp_azure_robe)
    out2 = f"{CRANE_DIR}/proof_paperdoll_crane_azure_magenta.png"
    m2.save(out2)
    print(f"✓ Saved azure robe magenta proof: {out2}")

    # 3. Azure + Sky Hunter on magenta
    comp_azure_hunter = build_composite("paint_zephyr_azure.png", "costume_sky_hunter_mail.png")
    m3 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    m3.alpha_composite(comp_azure_hunter)
    out3 = f"{CRANE_DIR}/proof_paperdoll_crane_hunter_azure_magenta.png"
    m3.save(out3)
    print(f"✓ Saved azure hunter magenta proof: {out3}")

def generate_crops():
    # Verification crop of costume
    cos_img = Image.open(f"{CRANE_DIR}/costume/costume_sky_hunter_mail.png").convert("RGBA")
    bbox_cos = cos_img.getbbox() or (38, 52, 87, 95)
    crop_cos = cos_img.crop((max(0, bbox_cos[0] - 4), max(0, bbox_cos[1] - 4),
                             min(128, bbox_cos[2] + 4), min(128, bbox_cos[3] + 4)))
    crop_cos_p = f"{CRANE_DIR}/verification_crop_sky_hunter_mail.png"
    crop_cos.save(crop_cos_p)
    print(f"✓ Saved costume verification crop: {crop_cos_p}")

    # Verification crop of azure chassis
    ch_img = Image.open(f"{CRANE_DIR}/chassis/paint_zephyr_azure.png").convert("RGBA")
    bbox_ch = ch_img.getbbox() or (34, 54, 92, 128)
    crop_ch = ch_img.crop((max(0, bbox_ch[0] - 2), max(0, bbox_ch[1] - 2),
                           min(128, bbox_ch[2] + 2), min(128, bbox_ch[3] + 2)))
    crop_ch_p = f"{CRANE_DIR}/verification_crop_zephyr_azure.png"
    crop_ch.save(crop_ch_p)
    print(f"✓ Saved azure chassis verification crop: {crop_ch_p}")

if __name__ == "__main__":
    generate_chassis_comparison()
    generate_costume_comparison()
    generate_variants_matrix()
    generate_magenta_proofs()
    generate_crops()
