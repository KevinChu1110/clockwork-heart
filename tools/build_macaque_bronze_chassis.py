#!/usr/bin/env python3
"""
tools/build_macaque_bronze_chassis.py
Constructs paint_bamboo_bronze.png for Macaque paperdoll chassis.
- Source: paint_ivory_stock.png
- Continuous cyan-bronze baked enamel (天元青古銅烤漆).
- Smooth lustrous enamel finish with clean specular highlights.
- Zero noise / dithering / verdigris grunge.
- 128x128 RGBA
"""

import os
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

def create_macaque_paint_bamboo_bronze(src_path: str = "", out_path: str = ""):
    if not src_path:
        src_path = f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png"
    if not out_path:
        out_path = f"{MACAQUE_DIR}/chassis/paint_bamboo_bronze.png"

    ivory = Image.open(src_path).convert("RGBA")
    w, h = ivory.size
    bronze = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    opaque_pixels = []

    for y in range(h):
        for x in range(w):
            r, g, b, a = cast(tuple[int, int, int, int], ivory.getpixel((x, y)))
            if a == 0:
                continue

            # Ground soft shadow at base (Y >= 118)
            if y >= 118 and (r < 75 and g < 75 and b < 85):
                bronze.putpixel((x, y), (r, g, b, a))
                opaque_pixels.append((r, g, b))
                continue

            lum = int(0.299 * r + 0.587 * g + 0.114 * b)

            # 1. Outline: crisp #1F1A3A
            if lum < 55:
                bronze.putpixel((x, y), (31, 26, 58, a))
                opaque_pixels.append((31, 26, 58))
            else:
                # Continuous smooth cyan-bronze enamel ramp:
                f = max(0.0, min(1.0, (lum - 55) / 195.0))
                
                # Smooth curve:
                # Shadow:   ( 58,  86,  78)
                # Midtone:  ( 95, 136, 126)
                # Light:    (155, 195, 185)
                # Specular: (225, 245, 240)
                if f < 0.5:
                    t = f / 0.5
                    cr = int(58 + t * (95 - 58))
                    cg = int(86 + t * (136 - 86))
                    cb = int(78 + t * (126 - 78))
                else:
                    t = (f - 0.5) / 0.5
                    cr = int(95 + t * (225 - 95))
                    cg = int(136 + t * (245 - 136))
                    cb = int(126 + t * (240 - 126))

                bronze.putpixel((x, y), (cr, cg, cb, a))
                opaque_pixels.append((cr, cg, cb))

    bronze.save(out_path)

    u_colors = set(opaque_pixels)
    ratio = len(u_colors) / (len(opaque_pixels) / 100.0) if opaque_pixels else 0.0
    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {len(opaque_pixels)}, unique colors: {len(u_colors)}, ratio: {ratio:.1f}")
    return bronze

if __name__ == "__main__":
    create_macaque_paint_bamboo_bronze()
