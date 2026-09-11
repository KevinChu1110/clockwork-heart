#!/usr/bin/env python3
from PIL import Image

for race in ['lion']:
    im = Image.open(f'/opt/side/bravesoul-game/game/assets/sprites/player/poses/{race}/attack.png').convert('RGBA')
    w, h = im.size
    print(f"=== {race} attack ===")
    for y in range(108, 128):
        xs = []
        for x in range(w):
            px = im.getpixel((x, y))
            if isinstance(px, tuple) and len(px) >= 4:
                r, g, b, a = px[0], px[1], px[2], px[3]
                if 10 <= a <= 200:
                    lum = 0.299 * r + 0.587 * g + 0.114 * b
                    if lum < 110:
                        xs.append(x)
        if xs:
            print(f"  y={y:3d}: count={len(xs):2d}, x=[{min(xs)}..{max(xs)}]")
