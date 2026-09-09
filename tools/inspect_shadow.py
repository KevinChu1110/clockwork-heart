#!/usr/bin/env python3
from typing import cast
from PIL import Image

gold = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png").convert("RGBA")

for y in range(112, 127):
    row = ""
    for x in range(30, 105):
        p = cast(tuple[int, int, int, int], gold.getpixel((x, y)))
        if p[3] == 0:
            row += " "
        elif p[0] > 230 and p[1] > 220 and p[2] > 200:
            row += "X"
        elif p[0] < 50 and p[1] < 45 and p[2] < 65:
            row += "_" # soft shadow / outline
        else:
            row += "#" # feet
    print(f"Y={y:3d} |{row}|")
