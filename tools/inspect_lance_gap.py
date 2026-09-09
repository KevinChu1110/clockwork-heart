#!/usr/bin/env python3
from typing import cast
from PIL import Image

gold = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png").convert("RGBA")
lance = Image.open("game/assets/sprites/player/paperdoll/lion/weapon/wpn_knight_lance.png").convert("RGBA")

# Let's inspect rows 85 to 118 from X=20 to X=60
for y in range(85, 118):
    row = ""
    for x in range(20, 60):
        gp = cast(tuple[int, int, int, int], gold.getpixel((x, y)))
        lp = cast(tuple[int, int, int, int], lance.getpixel((x, y)))
        if gp[3] > 0 and lp[3] > 0:
            row += "B" # both
        elif gp[3] > 0:
            if gp[0] > 230 and gp[1] > 220 and gp[2] > 200:
                row += "X" # off-white in gold
            else:
                row += "G" # gold
        elif lp[3] > 0:
            row += "L" # lance
        else:
            row += "." # neither
    print(f"Y={y:3d} |{row}|")
