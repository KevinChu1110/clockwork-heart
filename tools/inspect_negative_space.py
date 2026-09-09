#!/usr/bin/env python3
from typing import cast
from PIL import Image

gold = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png").convert("RGBA")
w, h = gold.size

# Let's inspect the bounding box and context around each of the 3 negative space regions
def inspect_box(x1: int, y1: int, x2: int, y2: int, title: str):
    print(f"=== {title} ({x1}..{x2}, {y1}..{y2}) ===")
    for y in range(y1, y2 + 1):
        row = ""
        for x in range(x1, x2 + 1):
            r, g, b, a = cast(tuple[int, int, int, int], gold.getpixel((x, y)))
            if a == 0:
                row += " "
            elif r > 230 and g > 220 and b > 200:
                row += "X" # off-white negative space
            elif r < 60 and g < 60 and b < 70:
                row += "#" # dark outline
            else:
                row += "." # normal body/armor
        print(f"Y={y:3d} |{row}|")

inspect_box(90, 58, 100, 66, "Winding Key Hole")
inspect_box(38, 85, 55, 116, "Lance and Torso Gap")
inspect_box(62, 102, 74, 116, "Between Legs Gap")
