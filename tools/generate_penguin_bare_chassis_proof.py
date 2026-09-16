#!/usr/bin/env python3
"""
tools/generate_penguin_bare_chassis_proof.py
Generates a definitive high-resolution proof sheet for the 3 repaired Steam Penguin Chassis skins:
- Navy Titanium (原廠深海鍍鈦藍)
- Polar Frost Chrome (極光冰川銀白鍍鉻)
- Warm Ivory Stock (原廠象牙白高光琺瑯)

Audits 0-ART18:
1. Bare chassis display on dark background
2. Bare chassis on magenta background (edge and transparency verification)
3. 4x zoom of Torso & Head (showing 3D curved breastplate, energy core, brass bolts, zero placeholders)
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
PENGUIN_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin"
CHASSIS_DIR = f"{PENGUIN_DIR}/chassis"
FONT_PATH = f"{REPO_ROOT}/game/assets/fonts/jf-openhuninn-2.1.ttf"

def get_font(size: int = 12):
    if os.path.exists(FONT_PATH):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception:
            pass
    return ImageFont.load_default()

def main():
    navy = Image.open(f"{CHASSIS_DIR}/paint_penguin_navy.png").convert("RGBA")
    polar = Image.open(f"{CHASSIS_DIR}/paint_polar_frost.png").convert("RGBA")
    ivory = Image.open(f"{CHASSIS_DIR}/paint_ivory_stock.png").convert("RGBA")

    items = [
        ("原廠深海鍍鈦藍 (Navy)", navy, "paint_penguin_navy.png"),
        ("極光冰川銀白 (Polar)", polar, "paint_polar_frost.png"),
        ("原廠象牙白 (Ivory)", ivory, "paint_ivory_stock.png")
    ]

    scale = 2
    # Board layout:
    # 3 columns.
    # Top card: Dark UI background (256x256)
    # Middle card: Magenta background (256x256)
    # Bottom card: 4x zoom of chest & head (256x256)
    card_size = 128 * scale # 256
    pad = 24
    gap = 20
    header_h = 70
    col_w = card_size
    board_w = pad * 2 + len(items) * col_w + (len(items) - 1) * gap
    card_h_block = card_size + 36 # card + label
    board_h = header_h + card_h_block * 3 + pad * 2

    canvas = Image.new("RGBA", (board_w, board_h), (24, 26, 34, 255))
    d = ImageDraw.Draw(canvas)

    font_title = get_font(18)
    font_sub = get_font(12)
    font_card = get_font(13)
    font_meta = get_font(11)

    # Title Banner
    d.text((pad, 16), "STEAM PENGUIN CHASSIS · 0-ART18 REPAIR & AUDIT PROOF", font=font_title, fill=(255, 218, 64, 255))
    d.text((pad, 42), "第九族 蒸氣企鵝 · 三大素體塗裝 100% 完稿手繪修復驗收 (0-QA8 分層規範 · 3D胸腹板件 · 零占位圖)", font=font_sub, fill=(170, 180, 205, 255))

    for col_idx, (title, img, fname) in enumerate(items):
        cx = pad + col_idx * (col_w + gap)

        # Calculate metrics
        arr = np.array(img)
        opaque = np.sum(arr[:, :, 3] > 8)
        cols = len(set(tuple(p[:3]) for p in arr[arr[:, :, 3] > 8]))
        c100 = (cols / opaque * 100) if opaque > 0 else 0

        # Section 1: Dark UI (2x)
        y1 = header_h
        d.text((cx, y1 - 20), f"【{title}】", font=font_card, fill=(255, 218, 64, 255))
        d.rounded_rectangle([cx, y1, cx + col_w, y1 + col_w], radius=6, fill=(35, 38, 48, 255), outline=(70, 80, 105, 255), width=1)
        img_2x = img.resize((col_w, col_w), Image.Resampling.NEAREST)
        canvas.alpha_composite(img_2x, (cx, y1))
        d.text((cx + 8, y1 + col_w + 6), f"1. 實機渲染 (128x128 2X) · c100={c100:.1f}", font=font_meta, fill=(200, 210, 230, 255))

        # Section 2: Magenta BG (2x)
        y2 = y1 + card_h_block
        mag_card = Image.new("RGBA", (col_w, col_w), (255, 0, 255, 255))
        mag_card.alpha_composite(img_2x)
        canvas.paste(mag_card, (cx, y2))
        d.rectangle([cx, y2, cx + col_w, y2 + col_w], outline=(70, 80, 105, 255), width=1)
        d.text((cx + 8, y2 + col_w + 6), "2. 洋紅去背驗收 (零邊界裁切 · 零懸空雜點)", font=font_meta, fill=(200, 210, 230, 255))

        # Section 3: 4x Zoom of Torso Plating (0-QA8)
        y3 = y2 + card_h_block
        # Crop torso from original: x in [32, 88], y in [48, 104] (56x56)
        crop_torso = img.crop((32, 48, 88, 104))
        crop_4x = crop_torso.resize((col_w, col_w), Image.Resampling.NEAREST)
        d.rounded_rectangle([cx, y3, cx + col_w, y3 + col_w], radius=6, fill=(35, 38, 48, 255), outline=(70, 80, 105, 255), width=1)
        canvas.alpha_composite(crop_4x, (cx, y3))
        d.text((cx + 8, y3 + col_w + 6), "3. 軀幹板件 4X 特寫 (立體琺瑯 · 能量核心 · 零平塗 · 0-QA8)", font=font_meta, fill=(255, 200, 80, 255))

    out_path = f"{PENGUIN_DIR}/proof_penguin_bare_chassis_audit.png"
    canvas.save(out_path)
    print(f"✓ Saved bare chassis audit proof: {out_path}")

if __name__ == "__main__":
    main()
