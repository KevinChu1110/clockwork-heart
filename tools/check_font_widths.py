#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
FONT_PATH = f"{REPO_ROOT}/game/assets/fonts/jf-openhuninn-2.1.ttf"

font_12 = ImageFont.truetype(FONT_PATH, 12)
font_11 = ImageFont.truetype(FONT_PATH, 11)

labels_chassis = [
    ("黃銅原金", "Brass Gold"),
    ("原廠象牙白", "Ivory Stock"),
    ("午夜深藍 [新]", "Midnight Navy"),
]

labels_costume = [
    ("裸機素體", "Bare Chassis"),
    ("胡桃鉗近衛", "Nutcracker"),
    ("蒸氣工匠 [新]", "Steam Artisan"),
]

im = Image.new("RGBA", (100, 100))
draw = ImageDraw.Draw(im)

for group in [labels_chassis, labels_costume]:
    for l1, l2 in group:
        b1 = draw.textbbox((0, 0), l1, font=font_12)
        b2 = draw.textbbox((0, 0), l2, font=font_11)
        w1 = b1[2] - b1[0]
        w2 = b2[2] - b2[0]
        print(f"'{l1}' width: {w1}, '{l2}' width: {w2}")
