#!/usr/bin/env python3
import os
import math
from PIL import Image, ImageChops, ImageDraw

LION_DIR = "game/assets/sprites/player/paperdoll/lion"

def create_lion_paint_midnight_navy():
    gold = Image.open(f"{LION_DIR}/chassis/paint_brass_gold.png").convert("RGBA")
    w, h = gold.size
    navy = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sp = gold.load()
    np = navy.load()

    for y in range(h):
        for x in range(w):
            r, g, b, a = sp[x, y]
            if a == 0:
                continue
            lum = int(0.299 * r + 0.587 * g + 0.114 * b)

            # Ground soft shadow region (Y >= 116)
            if y >= 116:
                # Keep shadow consistent with the other chassis variants
                # Outline/shadow blend: deep navy purple
                np[x, y] = (31, 26, 58, a)
                continue

            if lum < 50:
                # Outline #1F1A3A
                np[x, y] = (31, 26, 58, a)
            elif lum < 85:
                # Ball sockets, gear joints, hinge seams: Antique warm bronze/brass
                f = (lum - 50) / 35.0
                br_r = int(140 + f * 50)
                br_g = int(100 + f * 40)
                br_b = int(45 + f * 35)
                np[x, y] = (br_r, br_g, br_b, a)
            elif lum < 125:
                # Deep midnight navy enamel (shadowed plates and crevices)
                f = (lum - 85) / 40.0
                nr = int(22 + f * 14)
                ng = int(32 + f * 20)
                nb = int(58 + f * 34)
                np[x, y] = (nr, ng, nb, a)
            elif lum < 185:
                # Mid-tone Midnight Navy High-Gloss Enamel
                f = (lum - 125) / 60.0
                nr = int(36 + f * 32)
                ng = int(52 + f * 42)
                nb = int(92 + f * 62)
                np[x, y] = (nr, ng, nb, a)
            else:
                # Polished specular enamel edge reflections & cyan-tinted highlight
                f = max(0.0, min(1.0, (lum - 185) / 70.0))
                nr = int(68 + f * 55)
                ng = int(94 + f * 70)
                nb = int(154 + f * 90)
                np[x, y] = (nr, ng, nb, a)

    out_path = f"{LION_DIR}/chassis/paint_midnight_navy.png"
    navy.save(out_path)
    print(f"✓ Saved {out_path} ({navy.size}, non-trans: {sum(1 for y in range(h) for x in range(w) if np[x, y][3] > 0)})")
    return navy

if __name__ == "__main__":
    create_lion_paint_midnight_navy()
