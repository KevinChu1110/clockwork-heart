#!/usr/bin/env python3
from typing import cast
from PIL import Image
from collections import Counter

art = Image.open("game/assets/sprites/player/paperdoll/rabbit/costume/costume_steam_artisan.png").convert("RGBA")
w, h = art.size

colors = []
for y in range(h):
    for x in range(w):
        p = cast(tuple[int, int, int, int], art.getpixel((x, y)))
        if p[3] > 0:
            colors.append((p[0], p[1], p[2]))

print(f"Total opaque pixels: {len(colors)}")
c = Counter(colors)
print("Top 20 colors in rabbit costume_steam_artisan:")
for col, cnt in c.most_common(20):
    print(f"  {col}: {cnt}")
