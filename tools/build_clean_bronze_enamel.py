#!/usr/bin/env python3
"""
tools/build_clean_bronze_enamel.py
Constructs paint_bamboo_bronze.png using the canonical clean enamel mapping:
- Contrast ratio matches Rabbit's paint_brass_gold standard
- Shadow never drops into muddy black/verdigris
- Smooth, continuous cel-shading enamel tone ramp
- Polished brass hinges and screws
- Crisp #1F1A3A outlines
"""

import colorsys
from typing import cast
from PIL import Image

def make_clean_bronze_enamel(src_path: str, out_path: str):
    ivory = Image.open(src_path).convert("RGBA")
    w, h = ivory.size
    bronze = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    for y in range(h):
        for x in range(w):
            r, g, b, a = cast(tuple[int, int, int, int], ivory.getpixel((x, y)))
            if a == 0:
                continue

            # Ground soft shadow at base (Y >= 118)
            if y >= 118 and (r < 75 and g < 75 and b < 85):
                bronze.putpixel((x, y), (r, g, b, a))
                continue

            lum = int(0.299 * r + 0.587 * g + 0.114 * b)

            # 1. Structural outline: only true outer boundary / deep mechanical lines
            if lum < 55:
                bronze.putpixel((x, y), (31, 26, 58, a)) # Crisp #1F1A3A outline

            # 2. Polished brass joints / screws (if original pixel is yellowish or gold joint)
            elif (r > 1.15 * b and g > 1.1 * b and (r - b) > 25):
                # Smooth brass ramp (like Rabbit paint_brass_gold)
                f = max(0.0, min(1.0, (lum - 70) / 185.0))
                br = int(195 + f * 55)
                bg = int(145 + f * 60)
                bb = int(45 + f * 50)
                bronze.putpixel((x, y), (br, bg, bb, a))

            # 3. Cyan-Bronze Baked Enamel (青古銅烤漆):
            # Smooth continuous ramp from deep bronze-cyan shadow to brilliant specular highlight:
            # Shadow (lum=55):  rgb( 95, 130, 122) -> clean warm-cool bronze enamel
            # Midtone (lum=160): rgb(138, 175, 166)
            # Highlight (lum=240): rgb(190, 222, 214)
            # Specular (lum=255): rgb(225, 245, 239)
            else:
                f = max(0.0, min(1.0, (lum - 55) / 200.0))
                # Smooth curve
                cr = int(95 + f * 125)
                cg = int(130 + f * 110)
                cb = int(122 + f * 112)
                bronze.putpixel((x, y), (cr, cg, cb, a))

    bronze.save(out_path)
    print(f"✓ Saved clean bronze enamel to {out_path}")

if __name__ == "__main__":
    src = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png"
    out = "/tmp/test_clean_bronze_enamel.png"
    make_clean_bronze_enamel(src, out)
