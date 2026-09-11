#!/usr/bin/env python3
from PIL import Image

mb = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_battle.png").convert("RGBA")
print("macaque_battle size:", mb.size)

# Forehead hairline crack on macaque_battle: x: 60..72, y: 28..42
for y in range(28, 43):
    for x in range(60, 72):
        r, g, b, a = mb.getpixel((x, y))
        val = (r + g + b) // 3
        if val < 130 and a > 200:
            print(f"Crack in macaque_battle at ({x}, {y}): val={val}")
