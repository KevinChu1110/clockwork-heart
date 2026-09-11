#!/usr/bin/env python3
"""
tools/generate_bamboo_bronze_pure.py
Pure, continuous, noise-free cyan-bronze baked enamel (天元青古銅烤漆).
Transforms clean ivory chassis into a lustrous, smooth, pristine toy finish.
"""

from typing import cast
from PIL import Image

def build_bamboo_bronze(src_path: str, out_path: str):
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

            # 1. Outline: crisp #1F1A3A
            if lum < 55:
                bronze.putpixel((x, y), (31, 26, 58, a))
            else:
                # Continuous smooth cyan-bronze enamel ramp:
                # f goes from 0.0 (shadow) to 1.0 (specular)
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

    bronze.save(out_path)
    print(f"✓ Saved pure bronze enamel to {out_path}")

if __name__ == "__main__":
    src = "/tmp/clean_master_ivory.png"
    out = "/tmp/test_pure_bronze.png"
    build_bamboo_bronze(src, out)
