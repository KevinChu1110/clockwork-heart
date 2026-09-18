#!/usr/bin/env python3
"""
tools/generate_crane_matrix_hd.py
Generates HD (2048x1616) variants matrix for Cloud Crane using original 512x512 slices.
Complies with review.md 19g-16 (>=1200px long edge) and 0-ART9/11/12/17.
"""

import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
CRANE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crane"
FONT_PATH = f"{REPO_ROOT}/game/assets/fonts/jf-openhuninn-2.1.ttf"

def get_font(size: int = 48):
    if os.path.exists(FONT_PATH):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception as e:
            print(f"Warning loading font: {e}")
    return ImageFont.load_default()

def ensure_curio_512():
    curio_512 = f"{CRANE_DIR}/back_curio/curio_origami_crane_512.png"
    if not os.path.exists(curio_512):
        src = f"{CRANE_DIR}/back_curio/curio_origami_crane.png"
        with Image.open(src) as img:
            resized = img.convert("RGBA").resize((512, 512), resample=Image.Resampling.LANCZOS)
            resized.save(curio_512, format="PNG")
            print(f"Generated {curio_512} via LANCZOS")
    return curio_512

def get_layer_512(slot: str, fn_base: str) -> Image.Image:
    # If fn_base is e.g. "paint_crane_porcelain.png", look for "paint_crane_porcelain_512.png"
    name_no_ext, ext = os.path.splitext(fn_base)
    fn_512 = f"{name_no_ext}_512{ext}" if not name_no_ext.endswith("_512") else fn_base
    p = f"{CRANE_DIR}/{slot}/{fn_512}"
    if not os.path.exists(p):
        p_orig = f"{CRANE_DIR}/{slot}/{fn_base}"
        with Image.open(p_orig) as img:
            res = img.convert("RGBA").resize((512, 512), resample=Image.Resampling.LANCZOS)
            res.save(p, format="PNG")
            print(f"Upscaled missing {p} via LANCZOS")
            return res
    return Image.open(p).convert("RGBA")

def build_composite_512(chassis_fn: str, costume_fn: str | None = None) -> Image.Image:
    comp = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    # Z-index ascending order:
    # 1. winding_key (Z: 5)
    comp.alpha_composite(get_layer_512("winding_key", "key_tri_wing_zephyr.png"))
    # 2. back_curio (Z: 8)
    ensure_curio_512()
    comp.alpha_composite(get_layer_512("back_curio", "curio_origami_crane.png"))
    # 3. chassis (Z: 10)
    comp.alpha_composite(get_layer_512("chassis", chassis_fn))
    # 4. head_unit (Z: 20)
    comp.alpha_composite(get_layer_512("head_unit", "head_cloud_crane_stock.png"))
    # 5. costume (Z: 25)
    if costume_fn and costume_fn != "none":
        comp.alpha_composite(get_layer_512("costume", costume_fn))
    # 6. optic_core (Z: 30)
    comp.alpha_composite(get_layer_512("optic_core", "core_vermilion_lens.png"))
    # 7. weapon (Z: 40)
    comp.alpha_composite(get_layer_512("weapon", "wpn_zephyr_wing_bow.png"))
    return comp

def draw_new_badge_512(draw: ImageDraw.ImageDraw, x: int, y: int, bg_color: tuple, text_color: tuple):
    badge_w, badge_h = 144, 72
    bx = x + 512 - badge_w - 16
    by = y + 16
    draw.rounded_rectangle((bx, by, bx + badge_w, by + badge_h), radius=16, fill=bg_color)
    font_badge = get_font(40)
    tb = draw.textbbox((0, 0), "NEW", font=font_badge)
    tw = tb[2] - tb[0]
    th = tb[3] - tb[1]
    tx = bx + (badge_w - tw) // 2
    ty = by + (badge_h - th) // 2 - 4
    draw.text((tx, ty), "NEW", font=font_badge, fill=text_color)

def generate_variants_matrix_hd():
    chassis_list = [
        ("paint_crane_porcelain.png", "原廠冷淬青瓷白", "Porcelain White"),
        ("paint_zephyr_azure.png", "晴空凌雲湛藍 [新]", "Zephyr Azure")
    ]
    costume_list = [
        ("none", "裸像素體", "Bare Chassis"),
        ("costume_zephyr_robe.png", "凌雲羽衣輕鋼道袍", "Zephyr Robe"),
        ("costume_sky_hunter_mail.png", "晴空巡獵機關羽甲", "Sky Hunter Mail")
    ]

    pad = 112
    gap_x = 144
    gap_y = 192
    canvas_w = pad * 2 + 512 * 3 + gap_x * 2  # 224 + 1536 + 288 = 2048
    canvas_h = pad * 2 + 512 * 2 + gap_y + 176  # 224 + 1024 + 192 + 176 = 1616

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (20, 22, 28, 255))
    draw = ImageDraw.Draw(canvas)
    font_title = get_font(60)
    font_zh1 = get_font(48)
    font_zh2 = get_font(44)

    # Title
    t_text = "雲嵐鶴 (Cloud Crane) 紙娃娃雙塗裝 x 雙外裝矩陣"
    tb = draw.textbbox((0, 0), t_text, font=font_title)
    draw.text(((canvas_w - (tb[2] - tb[0])) // 2, 48), t_text, font=font_title, fill=(255, 218, 64, 255))

    for row_idx, (ch_fn, ch_zh, ch_en) in enumerate(chassis_list):
        for col_idx, (cos_fn, cos_zh, cos_en) in enumerate(costume_list):
            comp = build_composite_512(ch_fn, cos_fn)
            x = pad + col_idx * (512 + gap_x)
            y = 176 + row_idx * (512 + gap_y)

            canvas.paste(comp, (x, y), comp)
            is_new = (cos_fn == "costume_sky_hunter_mail.png" or ch_fn == "paint_zephyr_azure.png")
            border_col = (255, 160, 16, 255) if is_new else (55, 60, 70, 255)
            draw.rectangle((x, y, x + 512, y + 512), outline=border_col, width=8 if is_new else 4)

            if is_new:
                draw_new_badge_512(draw, x, y, (255, 160, 16, 255), (40, 20, 0, 255))

            # Two neat lines to avoid any horizontal overlap
            lb1 = draw.textbbox((0, 0), cos_zh, font=font_zh1)
            lw1 = lb1[2] - lb1[0]
            col1 = (255, 218, 64, 255) if is_new else (225, 230, 240, 255)
            draw.text((x + (512 - lw1) // 2, y + 512 + 24), cos_zh, font=font_zh1, fill=col1)

            lb2 = draw.textbbox((0, 0), f"({ch_zh})", font=font_zh2)
            lw2 = lb2[2] - lb2[0]
            col2 = (56, 160, 255, 255) if is_new else (140, 148, 165, 255)
            draw.text((x + (512 - lw2) // 2, y + 512 + 88), f"({ch_zh})", font=font_zh2, fill=col2)

    out_p = f"{CRANE_DIR}/proof_crane_variants_matrix_hd.png"
    canvas.save(out_p)
    print(f"✓ Saved HD variants matrix: {out_p} ({canvas_w}x{canvas_h})")

if __name__ == "__main__":
    generate_variants_matrix_hd()
