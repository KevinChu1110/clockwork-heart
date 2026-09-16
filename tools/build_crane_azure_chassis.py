#!/usr/bin/env python3
"""
tools/build_crane_azure_chassis.py
Constructs paint_zephyr_azure.png for Cloud Crane (雲嵐鶴) paperdoll chassis.
- Source: game/assets/sprites/player/paperdoll/crane/chassis/paint_crane_porcelain.png
- Style: 晴空凌雲湛藍烤漆 (Zephyr Azure Baked Enamel)
- Pure clockwork toy aesthetic: vibrant sky/cobalt blue enamel with bright brass ball-joint accents.
- Preserves soft ground shadow, crisp #1F1A3A outline, smooth specular reflections.
- Conforms to CANON.md (zero fur/flesh, metal clockwork chassis) & dopamine bright palette.
- 128x128 RGBA
"""

import os
from typing import cast
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
CRANE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crane"

def create_crane_paint_zephyr_azure(src_path: str = "", out_path: str = "") -> Image.Image:
    if not src_path:
        src_path = f"{CRANE_DIR}/chassis/paint_crane_porcelain.png"
    if not out_path:
        out_path = f"{CRANE_DIR}/chassis/paint_zephyr_azure.png"

    porcelain = Image.open(src_path).convert("RGBA")
    w, h = porcelain.size
    azure = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    for y in range(h):
        for x in range(w):
            r, g, b, a = cast(tuple[int, int, int, int], porcelain.getpixel((x, y)))
            if a <= 10:
                continue

            # 1. Ground soft contact shadow at base (Y >= 118)
            if y >= 118 and (r < 75 and g < 75 and b < 85):
                azure.putpixel((x, y), (r, g, b, a))
                continue

            lum = int(0.299 * r + 0.587 * g + 0.114 * b)

            # 2. Dark outline / seam groove: crisp deep blue-purple #1F1A3A
            if lum < 50:
                azure.putpixel((x, y), (31, 26, 58, a))
                continue

            # 3. Check for brass ball joints & mechanical bearings
            # Shoulders (x: 44..52, y: 55..63 and x: 74..82, y: 57..65)
            # Waist ball joint (x: 58..70, y: 76..84)
            # Knee / leg joints (x: 48..56 or 70..78, y: 88..98)
            is_joint = False
            if ((44 <= x <= 52 and 55 <= y <= 63) or
                (74 <= x <= 82 and 57 <= y <= 65) or
                (58 <= x <= 70 and 76 <= y <= 84) or
                ((48 <= x <= 56 or 70 <= x <= 78) and 88 <= y <= 98)):
                if r > 120 and g > 80:
                    is_joint = True

            if is_joint:
                # Rich brass gold joint accent (#FFD028 / #FFA010)
                f_j = max(0.0, min(1.0, (lum - 50) / 180.0))
                jr = int(180 + f_j * 75)   # 180..255
                jg = int(120 + f_j * 88)   # 120..208
                jb = int(25 + f_j * 35)    # 25..60
                azure.putpixel((x, y), (jr, jg, jb, a))
                continue

            # 4. Azure Blue baked enamel ramp:
            # Shadow:   ( 18,  52, 130)   # Deep cobalt shadow (#123482)
            # Midtone:  ( 41, 121, 255)   # Radiant azure (#2979FF)
            # Highlight:( 94, 180, 255)   # Bright sky blue (#5EB4FF)
            # Specular: (210, 235, 255)   # Gleaming enamel white-blue (#D2EBFF)
            f = max(0.0, min(1.0, (lum - 50) / 200.0))

            if f < 0.45:
                t = f / 0.45
                cr = int(16 + t * (41 - 16))
                cg = int(48 + t * (121 - 48))
                cb = int(120 + t * (255 - 120))
            elif f < 0.80:
                t = (f - 0.45) / 0.35
                cr = int(41 + t * (94 - 41))
                cg = int(121 + t * (180 - 121))
                cb = int(255 + t * (255 - 255))
            else:
                t = (f - 0.80) / 0.20
                cr = int(94 + t * (220 - 94))
                cg = int(180 + t * (240 - 180))
                cb = int(255 + t * (255 - 255))

            # Subtle extra specular on top-facing curves
            if lum > 175 and y < 85:
                cr = min(255, cr + 25)
                cg = min(255, cg + 15)

            azure.putpixel((x, y), (cr, cg, cb, a))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    azure.save(out_path)
    print(f"✓ Saved crane azure chassis: {out_path} (bbox: {azure.getbbox()})")
    return azure

if __name__ == "__main__":
    create_crane_paint_zephyr_azure()
