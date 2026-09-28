#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/party/raven_idle.png").convert("RGBA")
px = im.load()
assert px is not None

print("ASCII map of raven_idle.png ground shadow (y=116..123, x=35..95):")
for y in range(116, 124):
    line = f"{y:3d} "
    for x in range(35, 95):
        p = px[x, y]
        if p[3] > 20:
            line += "#"
        else:
            line += "."
    print(line)
