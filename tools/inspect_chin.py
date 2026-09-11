#!/usr/bin/env python3
from PIL import Image

ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")

print("=== Chin region (x: 46..55, y: 47..53) ===")
for y in range(47, 54):
    for x in range(46, 56):
        r, g, b, a = ivory.getpixel((x, y))
        print(f"({x:2d}, {y:2d}): rgba({r:3d}, {g:3d}, {b:3d}, {a:3d})")
