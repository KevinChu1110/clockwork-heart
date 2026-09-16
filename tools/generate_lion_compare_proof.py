#!/usr/bin/env python3
"""
tools/generate_lion_compare_proof.py
Generates proof_paperdoll_lion_compare.png for Lion paperdoll assembly verification.
Modeled after tools/generate_penguin_compare_proof.py.
"""

import os
from PIL import Image, ImageDraw, ImageFont

root = "/opt/side/bravesoul-game"
pd_dir = f"{root}/game/assets/sprites/player/paperdoll/lion"
comp_path = f"{pd_dir}/proof_paperdoll_lion_composite.png"
out_path = f"{pd_dir}/proof_paperdoll_lion_compare.png"

comp_img = Image.open(comp_path).convert("RGBA")
scale = 2
comp_2x = comp_img.resize((comp_img.width * scale, comp_img.height * scale), Image.Resampling.NEAREST)

W, H = 640, 380
canvas = Image.new("RGBA", (W, H), (28, 24, 40, 255))
draw = ImageDraw.Draw(canvas)

font_path = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
if not os.path.exists(font_path):
    font_path = f"{root}/game/assets/fonts/jf-openhuninn-2.1.ttf"

font = ImageFont.truetype(font_path, 14)
font_title = ImageFont.truetype(font_path, 16)

# Title banner
title_text = "LION KNIGHT · PAPERDOLL ASSEMBLY & MAGENTA PROOF"
sub_text = "第三族 獅族騎士 · 紙娃娃 7 槽裝配與洋紅底板去背驗收 (0-ART9 單持驗證)"
draw.text((30, 16), title_text, font=font_title, fill=(255, 215, 64, 255))
draw.text((30, 40), sub_text, font=font, fill=(180, 170, 200, 255))

# Card 1: Composite (Left)
card1_box = [30, 68, 305, 360]
draw.rounded_rectangle(card1_box, radius=8, fill=(42, 36, 56, 255), outline=(90, 75, 110, 255), width=2)
draw.text((45, 78), "1. 裝配成品 (COMPOSITE)", font=font, fill=(255, 215, 64, 255))
spr1_x = card1_box[0] + (card1_box[2] - card1_box[0] - comp_2x.width) // 2
spr1_y = card1_box[1] + 32
canvas.alpha_composite(comp_2x, (spr1_x, spr1_y))

# Card 2: Magenta Proof (Right)
card2_box = [335, 68, 610, 360]
draw.rounded_rectangle(card2_box, radius=8, fill=(42, 36, 56, 255), outline=(90, 75, 110, 255), width=2)
draw.text((350, 78), "2. 洋紅驗收 (MAGENTA PROOF)", font=font, fill=(255, 215, 64, 255))

mag_sub = Image.new("RGBA", (256, 256), (255, 0, 255, 255))
mag_sub.alpha_composite(comp_2x)
spr2_x = card2_box[0] + (card2_box[2] - card2_box[0] - 256) // 2
spr2_y = card2_box[1] + 32
canvas.alpha_composite(mag_sub, (spr2_x, spr2_y))
draw.rectangle([spr2_x, spr2_y, spr2_x + 256, spr2_y + 256], outline=(255, 215, 64, 200), width=1)

canvas.save(out_path)
print(f"Successfully generated: {out_path}")
