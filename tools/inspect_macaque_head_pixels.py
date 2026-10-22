#!/usr/bin/env python3
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

im_ch = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock_512.png").convert("RGBA")
im_head = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_512.png").convert("RGBA")

# 檢查 head 和 chassis 在 (150..350, 80..220) 區間的像素
print("Checking face region (x: 180..320, y: 100..220)")

for y in range(120, 200, 10):
    for x in range(200, 300, 15):
        p_ch = im_ch.getpixel((x, y))
        p_hd = im_head.getpixel((x, y))
        if p_ch[3] > 0 or p_hd[3] > 0:
            print(f"({x}, {y}): ch_a={p_ch[3]}, hd_a={p_hd[3]}")
