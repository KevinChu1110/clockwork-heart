#!/usr/bin/env python3
from typing import cast
from PIL import Image

art = Image.open("game/assets/sprites/player/paperdoll/rabbit/costume/costume_steam_artisan.png").convert("RGBA")
w, h = art.size

print("Rabbit steam artisan rows (75..110):")
for y in range(75, 111):
    row = ""
    for x in range(45, 85):
        p = cast(tuple[int, int, int, int], art.getpixel((x, y)))
        if p[3] == 0:
            row += " "
        elif p[:3] == (0, 0, 0) or p[0] < 40 and p[1] < 40 and p[2] < 40:
            row += "#"
        elif p[0] > 100 and p[1] > 80 and p[2] < 60:
            row += "*" # brass / rivet
        elif p[0] > 80 and p[1] < 40 and p[2] < 40:
            row += "R" # dark red / bronze
        elif p[0] == p[1] == p[2]:
            row += "=" # iron grey
        else:
            row += "." # canvas / apron
    print(f"Y={y:3d} |{row}|")
