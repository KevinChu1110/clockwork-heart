#!/usr/bin/env python3
"""
tools/build_tiger_ivory_chassis.py
Constructs true paint_ivory_stock.png for Tiger paperdoll chassis.
- Source: game/assets/sprites/player/paperdoll/tiger/chassis/paint_ember_orange.png
- Style: 原廠象牙白高光琺瑯塗層 (Ivory Stock Enamel)
- Creamy ivory body plates (#F0EBE0 ~ #C8C0B0), polished brass joints (#E5B842), #1F1A3A outline.
- 128x128 RGBA
"""

from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
TIGER_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tiger"

def create_tiger_paint_ivory_stock(src_path: str = "", out_path: str = ""):
    if not src_path:
        src_path = f"{TIGER_DIR}/chassis/paint_ember_orange.png"
    if not out_path:
        out_path = f"{TIGER_DIR}/chassis/paint_ivory_stock.png"

    orange = Image.open(src_path).convert("RGBA")
    w, h = orange.size
    ivory = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    opaque_pixels = []

    for y in range(h):
        for x in range(w):
            r, g, b, a = cast(tuple[int, int, int, int], orange.getpixel((x, y)))
            if a <= 10:
                continue

            # Ground soft shadow at base (Y >= 118)
            if y >= 118 and (r < 75 and g < 75 and b < 85):
                ivory.putpixel((x, y), (r, g, b, a))
                opaque_pixels.append((r, g, b))
                continue

            lum = int(0.299 * r + 0.587 * g + 0.114 * b)

            # Dark outline: crisp deep blue-purple #1F1A3A
            if lum < 50:
                ivory.putpixel((x, y), (31, 26, 58, a))
                opaque_pixels.append((31, 26, 58))
                continue

            # Joint check
            is_joint = False
            if ((36 <= x <= 43 and 68 <= y <= 76) or
                (84 <= x <= 92 and 76 <= y <= 84) or
                ((49 <= x <= 55 or 71 <= x <= 77) and 93 <= y <= 101)):
                if r > 120 and g > 50:
                    is_joint = True

            if is_joint:
                # Rich brass gold joint accent
                f_j = max(0.0, min(1.0, (lum - 50) / 180.0))
                jr = int(140 + f_j * 115)
                jg = int(95 + f_j * 100)
                jb = int(25 + f_j * 40)
                ivory.putpixel((x, y), (jr, jg, jb, a))
                opaque_pixels.append((jr, jg, jb))
            else:
                # Creamy ivory enamel ramp:
                # Shadow:   (130, 120, 110)
                # Midtone:  (185, 178, 168)
                # Light:    (230, 225, 215)
                # Specular: (252, 250, 245)
                f = max(0.0, min(1.0, (lum - 50) / 200.0))
                if f < 0.5:
                    t = f / 0.5
                    cr = int(130 + t * (185 - 130))
                    cg = int(120 + t * (178 - 120))
                    cb = int(110 + t * (168 - 110))
                elif f < 0.85:
                    t = (f - 0.5) / 0.35
                    cr = int(185 + t * (230 - 185))
                    cg = int(178 + t * (225 - 178))
                    cb = int(168 + t * (215 - 168))
                else:
                    t = (f - 0.85) / 0.15
                    cr = int(230 + t * (252 - 230))
                    cg = int(225 + t * (250 - 225))
                    cb = int(215 + t * (245 - 215))

                ivory.putpixel((x, y), (cr, cg, cb, a))
                opaque_pixels.append((cr, cg, cb))

    ivory.save(out_path)
    u_colors = set(opaque_pixels)
    ratio = len(u_colors) / (len(opaque_pixels) / 100.0) if opaque_pixels else 0.0
    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {len(opaque_pixels)}, unique colors: {len(u_colors)}, ratio: {ratio:.1f}")
    return ivory

if __name__ == "__main__":
    create_tiger_paint_ivory_stock()
