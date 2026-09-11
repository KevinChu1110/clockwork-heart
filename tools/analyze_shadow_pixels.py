#!/usr/bin/env python3
import os
from PIL import Image

def analyze(path):
    im = Image.open(path).convert('RGBA')
    w, h = im.size
    y_start = int(h * 0.85)
    print(f"=== {path} (size {w}x{h}, y_start {y_start}) ===")
    dark_semi = []
    opaque_dark = 0
    for y in range(y_start, h):
        row_dark_semi = 0
        for x in range(w):
            px = im.getpixel((x, y))
            if isinstance(px, tuple) and len(px) >= 4:
                r, g, b, a = px[0], px[1], px[2], px[3]
                if a > 200:
                    lum = 0.299 * r + 0.587 * g + 0.114 * b
                    if lum < 110:
                        opaque_dark += 1
                elif 10 <= a <= 200:
                    lum = 0.299 * r + 0.587 * g + 0.114 * b
                    if lum < 110:
                        row_dark_semi += 1
        if row_dark_semi > 0:
            dark_semi.append((y, row_dark_semi))
    print(f"  opaque_dark: {opaque_dark}")
    print(f"  dark_semi rows: {len(dark_semi)}, total dark_semi: {sum(r[1] for r in dark_semi)}")
    for y, cnt in dark_semi[-10:]:
        print(f"    y={y}: {cnt} px")

for p in [
    '/opt/side/bravesoul-game/game/assets/sprites/player/poses/boar/attack.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/poses/boar/idle.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/attack.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/idle.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/proof_paperdoll_fox_composite.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_paperdoll_boar_composite.png',
]:
    if os.path.exists(p):
        analyze(p)
