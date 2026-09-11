#!/usr/bin/env python3
from PIL import Image

mb = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_battle.png").convert("RGBA")

# Belly in macaque_battle: x: 45..70, y: 70..90
for y in range(70, 90):
    for x in range(45, 70):
        r, g, b, a = mb.getpixel((x, y))
        val = (r + g + b) // 3
        if val < 140 and a > 200:
            print(f"Belly speck/scratch in macaque_battle at ({x}, {y}): val={val}")
