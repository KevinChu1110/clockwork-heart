#!/usr/bin/env python3
from PIL import Image

ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")
w, h = ivory.size

# Let's inspect the exact pixels around the face
# 1. Eye crack: x: 64..72, y: 31..45
print("=== Eye crack region ===")
for y in range(31, 46):
    for x in range(64, 72):
        r, g, b, a = ivory.getpixel((x, y))
        print(f"({x:2d}, {y:2d}): rgba({r:3d}, {g:3d}, {b:3d}, {a:3d})")
