#!/usr/bin/env python3
from typing import cast
from PIL import Image

gold = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png").convert("RGBA")
w, h = gold.size

off_white = []
for y in range(h):
    for x in range(w):
        r, g, b, a = cast(tuple[int, int, int, int], gold.getpixel((x, y)))
        if a > 0:
            # check if it's the off-white background fill
            # (250, 243, 224) or similar light colors > 230
            if r > 230 and g > 220 and b > 200:
                off_white.append((x, y, (r, g, b)))

print(f"Total off-white pixels: {len(off_white)}")
# Print grouped by Y
lines: dict[int, list[int]] = {}
for x, y, c in off_white:
    lines.setdefault(y, []).append(x)

for y in sorted(lines.keys()):
    xs = lines[y]
    print(f"Y={y:3d}: X={min(xs)}..{max(xs)} (count={len(xs)}): {xs}")
