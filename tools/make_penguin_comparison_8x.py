#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
FONT_PATH = f"{REPO_ROOT}/game/assets/fonts/jf-openhuninn-2.1.ttf"

def get_font(size: int = 16):
    if os.path.exists(FONT_PATH):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception:
            pass
    return ImageFont.load_default()

rabbit_p = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rabbit/chassis/paint_midnight_navy.png"
bear_p = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear/chassis/paint_bear_amber.png"
pen_navy_p = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin/chassis/paint_penguin_navy.png"
pen_polar_p = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin/chassis/paint_polar_frost.png"
pen_ivory_p = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin/chassis/paint_ivory_stock.png"

items = [
    ("兔族 (Rabbit Navy)", rabbit_p, (38, 52, 86, 94)),
    ("熊族 (Bear Amber)", bear_p, (42, 52, 86, 94)),
    ("企鵝 (Penguin Navy)", pen_navy_p, (38, 52, 86, 94)),
    ("企鵝 (Penguin Polar)", pen_polar_p, (38, 52, 86, 94)),
    ("企鵝 (Penguin Ivory)", pen_ivory_p, (38, 52, 86, 94)),
]

scale = 6
crop_w = 48
crop_h = 42
box_w = crop_w * scale
box_h = crop_h * scale
pad = 20
gap = 16
header_h = 50

total_w = pad * 2 + len(items) * box_w + (len(items) - 1) * gap
total_h = header_h + box_h + 40 + pad * 2

canvas = Image.new("RGBA", (total_w, total_h), (24, 26, 34, 255))
d = ImageDraw.Draw(canvas)
font_title = get_font(20)
font_lbl = get_font(15)

d.text((pad, pad), "Chassis Torso 6x Zoom Comparison (Rabbit vs Bear vs Penguin)", font=font_title, fill=(255, 215, 64, 255))

for i, (label, path, (x0, y0, x1, y1)) in enumerate(items):
    x = pad + i * (box_w + gap)
    y = header_h + pad

    im = Image.open(path).convert("RGBA")
    # crop region
    crop = im.crop((x0, y0, x1, y1))
    # resize 6x NEAREST
    scaled = crop.resize((box_w, box_h), Image.Resampling.NEAREST)

    # background card
    bg = Image.new("RGBA", (box_w, box_h), (40, 42, 54, 255))
    bg.alpha_composite(scaled)
    canvas.alpha_composite(bg, (x, y))

    d.rectangle([x, y, x + box_w, y + box_h], outline=(100, 110, 130, 255), width=2)
    d.text((x + 10, y + box_h + 8), label, font=font_lbl, fill=(240, 240, 250, 255))

out_p = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin/proof_penguin_chassis_zoom_comparison.png"
canvas.save(out_p)
print(f"✓ Saved 6x comparison to {out_p}")
