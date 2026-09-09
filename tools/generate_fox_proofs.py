#!/usr/bin/env python3
"""
tools/generate_fox_proofs.py
Generates side-by-side comparison proof images, 3x3 variants matrix,
magenta composite verification, and verification crop images for Fox paperdoll expansion.
- Clean centered 2-line labels with zero overlap (Rule 10a-2 review feedback)
- Crisp 'NEW' badge on top-right of new variant preview cards
- Uses project font Open-Huninn (jf-openhuninn-2.1.ttf)
- Strictly composited from shipped slice assets in z-index order onto magenta (Rule 4c-4 / 19f-3)
"""

import os
from typing import cast
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
FOX_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox"
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
    p = f"{FOX_DIR}/{slot}/{fn}"
    return Image.open(p).convert("RGBA")

def build_composite(chassis_fn: str, costume_fn: str | None = None) -> Image.Image:
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Z-index ascending order:
    # 1. winding_key (Z: 5)
    comp.alpha_composite(get_slot_layer("winding_key", "key_classic_brass.png"))
    # 2. back_curio (Z: 8)
    comp.alpha_composite(get_slot_layer("back_curio", "curio_fox_astral_tail.png"))
    # 3. chassis (Z: 10)
    comp.alpha_composite(get_slot_layer("chassis", chassis_fn))
    # 4. head_unit (Z: 20)
    comp.alpha_composite(get_slot_layer("head_unit", "ear_fox_radar.png"))
    # 5. costume (Z: 25)
    if costume_fn and costume_fn != "none":
        comp.alpha_composite(get_slot_layer("costume", costume_fn))
    # 6. optic_core (Z: 30)
    comp.alpha_composite(get_slot_layer("optic_core", "core_cyan_emerald.png"))
    # 7. weapon (Z: 40)
    comp.alpha_composite(get_slot_layer("weapon", "wpn_astral_staff.png"))
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
    # 3 Chassis variants on Astral Cape costume
    c_orange = build_composite("paint_fox_orange.png", "costume_astral_cape.png")
    c_ivory = build_composite("paint_ivory_stock.png", "costume_astral_cape.png")
    c_emerald = build_composite("paint_emerald_glaze.png", "costume_astral_cape.png")

    pad = 20
    gap = 24
    canvas_w = pad * 2 + 128 * 3 + gap * 2  # 472
    canvas_h = 205
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (24, 26, 32, 255))
    draw = ImageDraw.Draw(canvas)
    font_zh = get_font(13)
    font_en = get_font(11)

    items = [
        (c_orange, "靈狐曜橙", "Fox Orange", False),
        (c_ivory, "原廠象牙白", "Ivory Stock", False),
        (c_emerald, "翡翠螢光 [新]", "Emerald Glaze", True)
    ]

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (78, 216, 106, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        if is_new:
            draw_new_badge(draw, x, y, (78, 216, 106, 255), (15, 35, 20, 255))

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
        color_en = (78, 216, 106, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{FOX_DIR}/proof_fox_chassis_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved chassis comparison: {out_p}")

def generate_costume_comparison():
    # 3 Costume options on Fox Orange: Bare, Astral Cape, Astral Observer
    c_bare = build_composite("paint_fox_orange.png", None)
    c_cape = build_composite("paint_fox_orange.png", "costume_astral_cape.png")
    c_obs = build_composite("paint_fox_orange.png", "costume_astral_observer.png")

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
        (c_cape, "星紋見習斗篷", "Astral Cape", False),
        (c_obs, "星象觀測儀裝 [新]", "Astral Observer", True)
    ]

    for i, (img, l_zh, l_en, is_new) in enumerate(items):
        x = pad + i * (128 + gap)
        y = 16
        canvas.paste(img, (x, y), img)
        border_col = (255, 160, 16, 255) if is_new else (60, 65, 75, 255)
        draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

        if is_new:
            draw_new_badge(draw, x, y, (255, 160, 16, 255), (40, 20, 0, 255))

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
        color_en = (255, 160, 16, 255) if is_new else (140, 148, 165, 255)
        draw.text((tx_en, ty_en), l_en, font=font_en, fill=color_en)

    out_p = f"{FOX_DIR}/proof_fox_costume_comparison.png"
    canvas.save(out_p)
    print(f"✓ Saved costume comparison: {out_p}")

def generate_matrix_proof():
    # 3x3 Matrix: Rows = Costumes, Cols = Chassis
    chassis_list = [
        ("paint_fox_orange.png", "靈狐曜橙"),
        ("paint_ivory_stock.png", "原廠象牙白"),
        ("paint_emerald_glaze.png", "翡翠螢光 [新]")
    ]
    costume_list = [
        ("costume_astral_cape.png", "星紋見習斗篷"),
        ("costume_astral_observer.png", "星象觀測儀裝 [新]"),
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
            is_new = (cos_fn == "costume_astral_observer.png") or (ch_fn == "paint_emerald_glaze.png")
            border_col = (78, 216, 106, 255) if is_new else (50, 55, 65, 255)
            draw.rectangle((x, y, x + 128, y + 128), outline=border_col, width=2 if is_new else 1)

    out_p = f"{FOX_DIR}/proof_fox_variants_matrix.png"
    canvas.save(out_p)
    print(f"✓ Saved 3x3 mix-and-match matrix: {out_p}")

def generate_magenta_proofs():
    # 1. New Astral Observer on Emerald Glaze (New Costume + New Paint)
    c_new_both = build_composite("paint_emerald_glaze.png", "costume_astral_observer.png")
    mag1 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag1.alpha_composite(c_new_both)
    out1 = f"{FOX_DIR}/proof_paperdoll_fox_observer_emerald_magenta.png"
    mag1.save(out1)

    # 2. New Astral Observer on Fox Orange (New Costume + Default Paint)
    c_new_obs = build_composite("paint_fox_orange.png", "costume_astral_observer.png")
    mag2 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag2.alpha_composite(c_new_obs)
    out2 = f"{FOX_DIR}/proof_paperdoll_fox_observer_orange_magenta.png"
    mag2.save(out2)

    # 3. Astral Cape on Emerald Glaze (Default Costume + New Paint)
    c_new_eme = build_composite("paint_emerald_glaze.png", "costume_astral_cape.png")
    mag3 = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag3.alpha_composite(c_new_eme)
    out3 = f"{FOX_DIR}/proof_paperdoll_fox_cape_emerald_magenta.png"
    mag3.save(out3)

    print(f"✓ Saved magenta proofs:\n  • {out1}\n  • {out2}\n  • {out3}")

def generate_verification_crops():
    # Crop 1: Astral Observer astrolabe breastplate, buckles, and pauldrons
    obs_slice = Image.open(f"{FOX_DIR}/costume/costume_astral_observer.png").convert("RGBA")
    # Region around chest/belt/buckle: X[36..86], Y[58..105]
    crop_obs = obs_slice.crop((36, 58, 86, 105))
    crop_obs_large = crop_obs.resize((crop_obs.width * 8, crop_obs.height * 8), Image.Resampling.NEAREST)
    out_obs = f"{FOX_DIR}/verification_crop_astral_observer.png"
    crop_obs_large.save(out_obs)

    # Crop 2: Emerald Glaze chassis chest/head/belly plates
    eme_slice = Image.open(f"{FOX_DIR}/chassis/paint_emerald_glaze.png").convert("RGBA")
    # Region around chest/joints: X[36..86], Y[50..100]
    crop_eme = eme_slice.crop((36, 50, 86, 100))
    crop_eme_large = crop_eme.resize((crop_eme.width * 8, crop_eme.height * 8), Image.Resampling.NEAREST)
    out_eme = f"{FOX_DIR}/verification_crop_emerald_glaze.png"
    crop_eme_large.save(out_eme)

    print(f"✓ Saved verification crops:\n  • {out_obs}\n  • {out_eme}")

if __name__ == "__main__":
    generate_chassis_comparison()
    generate_costume_comparison()
    generate_matrix_proof()
    generate_magenta_proofs()
    generate_verification_crops()
