#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/party/kite_idle.png")
px = im.load()
assert px is not None

for y in range(118, 128):
    row_pixels = []
    for x in range(128):
        p = px[x, y]
        if p[3] > 20:
            row_pixels.append((x, p))
    print(f"y={y}: count={len(row_pixels)} min_x={row_pixels[0][0] if row_pixels else None} max_x={row_pixels[-1][0] if row_pixels else None}")
    for x, p in row_pixels:
        if p[0] > 100 or p[1] > 100:
            print(f"   non-shadow pixel at x={x}, y={y}: {p}")
