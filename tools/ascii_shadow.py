#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/party/kite_idle.png").convert("RGBA")
px = im.load()
assert px is not None

print("ASCII map of kite_idle.png ground shadow (y=116..123, x=40..115):")
for y in range(116, 124):
    line = f"{y:3d} "
    for x in range(40, 116):
        p = px[x, y]
        if p[3] > 20:
            if p[0] > 70 or p[1] > 70 or p[2] > 90:
                line += "$"  # bright
            else:
                line += "#"  # dark shadow
        else:
            line += "."
    print(line)
