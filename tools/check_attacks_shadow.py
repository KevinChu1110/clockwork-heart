#!/usr/bin/env python3
import os
from PIL import Image

def count_dark_semi(path):
    if not os.path.exists(path):
        return -1
    im = Image.open(path).convert('RGBA')
    w, h = im.size
    y_start = int(h * 0.85)
    cnt = 0
    for y in range(y_start, h):
        for x in range(w):
            px = im.getpixel((x, y))
            if isinstance(px, tuple) and len(px) >= 4:
                r, g, b, a = px[0], px[1], px[2], px[3]
                if 10 <= a <= 200:
                    lum = 0.299 * r + 0.587 * g + 0.114 * b
                    if lum < 110:
                        cnt += 1
    return cnt

for r in ['rabbit', 'lion', 'fox', 'boar', 'macaque']:
    if r == 'rabbit':
        p = '/opt/side/bravesoul-game/game/assets/sprites/player/poses/attack.png'
    else:
        p = f'/opt/side/bravesoul-game/game/assets/sprites/player/poses/{r}/attack.png'
    print(f'{r} attack: {count_dark_semi(p)} px')
