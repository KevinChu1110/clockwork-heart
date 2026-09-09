#!/usr/bin/env python3
from typing import cast
from PIL import Image

gold = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png").convert("RGBA")

def inspect_box(x1: int, y1: int, x2: int, y2: int, title: str):
    print(f"=== {title} ({x1}..{x2}, {y1}..{y2}) ===")
    for y in range(y1, y2 + 1):
        row = ""
        for x in range(x1, x2 + 1):
            r, g, b, a = cast(tuple[int, int, int, int], gold.getpixel((x, y)))
            if a == 0:
                row += " "
            elif r > 230 and g > 220 and b > 200:
                row += "X" # off-white
            elif r < 60 and g < 60 and b < 70:
                row += "#" # dark outline
            else:
                row += "." # normal
        print(f"Y={y:3d} |{row}|")

inspect_box(54, 48, 62, 54, "Y=49..52, X=56..59 (Face / Forehead?)")
inspect_box(65, 71, 75, 76, "Y=72..74 (Chest / Core?)")
inspect_box(75, 78, 88, 85, "Y=78..84 (Arm / Side?)")
