#!/usr/bin/env python3
from typing import cast
from PIL import Image
from collections import Counter

nut = Image.open("game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard.png").convert("RGBA")
w, h = nut.size

colors = []
for y in range(h):
    for x in range(w):
        p = cast(tuple[int, int, int, int], nut.getpixel((x, y)))
        if p[3] > 0:
            colors.append((p[0], p[1], p[2]))

print(f"Total opaque pixels: {len(colors)}")
c = Counter(colors)
print("Top 20 colors:")
for col, cnt in c.most_common(20):
    print(f"  {col}: {cnt}")
