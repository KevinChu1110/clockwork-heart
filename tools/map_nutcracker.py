#!/usr/bin/env python3
from typing import cast
from PIL import Image

nut = Image.open("game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard.png").convert("RGBA")
chassis = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png").convert("RGBA")

w, h = nut.size

# Print ASCII map of nutcracker guard on lion
for y in range(60, 110, 2):
    row = ""
    for x in range(35, 90):
        np = cast(tuple[int, int, int, int], nut.getpixel((x, y)))
        cp = cast(tuple[int, int, int, int], chassis.getpixel((x, y)))
        if np[3] > 20:
            # what color is np?
            r, g, b = np[0], np[1], np[2]
            if r > 150 and g < 60 and b < 60:
                row += "R" # red uniform
            elif r > 150 and g > 130 and b < 80:
                row += "G" # gold / brass buttons/epaulets
            elif r < 60 and g < 60 and b < 70:
                row += "#" # dark outline
            else:
                row += "c" # other costume
        elif cp[3] > 20:
            row += "." # chassis bare body
        else:
            row += " " # transparent
    print(f"Y={y:3d} |{row}|")
