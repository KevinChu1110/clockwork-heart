#!/usr/bin/env python3
import os
from PIL import Image

paths = [
    '/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/attack.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/idle.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/poses/boar/attack.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/poses/boar/idle.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/poses/lion/attack.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/poses/lion/idle.png',
]

for p in paths:
    if os.path.exists(p):
        im = Image.open(p).convert('RGBA')
        w, h = im.size
        y_start = int(h * 0.85)
        count = 0
        for y in range(y_start, h):
            for x in range(w):
                pixel = im.getpixel((x, y))
                if isinstance(pixel, tuple) and len(pixel) >= 4:
                    r, g, b, a = pixel[0], pixel[1], pixel[2], pixel[3]
                    if 10 <= a <= 200:
                        lum = 0.299 * r + 0.587 * g + 0.114 * b
                        if lum < 110.0:
                            count += 1
        print(f'{p.split("/")[-2]}/{os.path.basename(p)}: {count} px')
