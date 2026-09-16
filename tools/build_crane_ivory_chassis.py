#!/usr/bin/env python3
"""
tools/build_crane_ivory_chassis.py
Constructs paint_ivory_stock.png for Cloud Crane (雲嵐鶴) paperdoll chassis.
- Source: game/assets/sprites/player/paperdoll/crane/chassis/paint_crane_porcelain.png
- Style: 原廠象牙白高光琺瑯塗層 (Ivory Stock Enamel)
- Pure clockwork toy aesthetic: warm ivory enamel body plates (#FDF8EE ~ #D8CCA8),
  rich polished brass joints & bearings (#FFD028 / #FFA010), crisp #1F1A3A outline.
- Retains cloud crane's slender mechanical crane legs and articulated avian talons.
- Conforms to CANON.md (zero fur/flesh, metal clockwork chassis) & review.md 0-ART18.
- 128x128 RGBA
"""

import os
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
CRANE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crane"

def create_crane_paint_ivory_stock(src_path: str = "", out_path: str = "") -> Image.Image:
    if not src_path:
        src_path = f"{CRANE_DIR}/chassis/paint_crane_porcelain.png"
    if not out_path:
        out_path = f"{CRANE_DIR}/chassis/paint_ivory_stock.png"

    porcelain = Image.open(src_path).convert("RGBA")
    w, h = porcelain.size
    ivory = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    opaque_pixels = []

    for y in range(h):
        for x in range(w):
            r, g, b, a = cast(tuple[int, int, int, int], porcelain.getpixel((x, y)))
            if a <= 10:
                continue

            # 1. Ground soft contact shadow at base (Y >= 118)
            if y >= 118 and (r < 75 and g < 75 and b < 85):
                ivory.putpixel((x, y), (r, g, b, a))
                opaque_pixels.append((r, g, b))
                continue

            lum = int(0.299 * r + 0.587 * g + 0.114 * b)

            # 2. Dark outline / seam groove: crisp deep blue-purple #1F1A3A
            if lum < 50:
                ivory.putpixel((x, y), (31, 26, 58, a))
                opaque_pixels.append((31, 26, 58))
                continue

            # 3. Check for brass ball joints & mechanical bearings
            # Shoulders (x: 44..52, y: 55..63 and x: 74..82, y: 57..65)
            # Waist ball joint (x: 58..70, y: 76..84)
            # Knee / leg joints (x: 48..56 or 70..78, y: 88..98)
            # Existing gold / brass parts
            is_joint = False
            if ((44 <= x <= 52 and 55 <= y <= 63) or
                (74 <= x <= 82 and 57 <= y <= 65) or
                (58 <= x <= 70 and 76 <= y <= 84) or
                ((48 <= x <= 56 or 70 <= x <= 78) and 88 <= y <= 98)):
                if (r > 120 and g > 80) or (b > 180 and g > 120 and r < 100 and y >= 88):
                    is_joint = True
            elif (r > 160 and g > 110 and b < 100):
                is_joint = True

            if is_joint:
                # Rich brass gold joint accent (#FFD028 / #FFA010)
                f_j = max(0.0, min(1.0, (lum - 50) / 180.0))
                jr = int(180 + f_j * 75)   # 180..255
                jg = int(120 + f_j * 88)   # 120..208
                jb = int(25 + f_j * 35)    # 25..60
                ivory.putpixel((x, y), (jr, jg, jb, a))
                opaque_pixels.append((jr, jg, jb))
                continue

            # 4. Chest cyan energy core (x: 52..68, y: 58..69)
            if 52 <= x <= 68 and 58 <= y <= 69 and (b > 180 and g > 110 and r < 100):
                # Glowing cyan diamond energy core framed in gold
                ivory.putpixel((x, y), (r, g, b, a))
                opaque_pixels.append((r, g, b))
                continue

            # 5. Primary Body: Warm Ivory Enamel ramp
            # Specular:  (253, 248, 238)  # Pristine ivory glint (#FDF8EE)
            # Light:     (238, 230, 216)  # Warm ivory (#EEE6D8)
            # Midtone:   (218, 206, 186)  # Creamy enamel (#DACEBA)
            # Shadow:    (172, 156, 134)  # Warm shadow (#AC9C86)
            # Deep tone: (132, 118, 98)   # Crease shading (#847662)
            f = max(0.0, min(1.0, (lum - 50) / 195.0))

            if f < 0.35:
                t = f / 0.35
                cr = int(132 + t * (172 - 132))
                cg = int(118 + t * (156 - 118))
                cb = int(98 + t * (134 - 98))
            elif f < 0.70:
                t = (f - 0.35) / 0.35
                cr = int(172 + t * (218 - 172))
                cg = int(156 + t * (206 - 156))
                cb = int(134 + t * (186 - 134))
            elif f < 0.90:
                t = (f - 0.70) / 0.20
                cr = int(218 + t * (238 - 218))
                cg = int(206 + t * (230 - 206))
                cb = int(186 + t * (216 - 186))
            else:
                t = (f - 0.90) / 0.10
                cr = int(238 + t * (253 - 238))
                cg = int(230 + t * (248 - 230))
                cb = int(216 + t * (238 - 216))

            # Subtle specular on top-facing curves
            if lum > 175 and y < 85:
                cr = min(255, cr + 2)
                cg = min(255, cg + 2)

            ivory.putpixel((x, y), (cr, cg, cb, a))
            opaque_pixels.append((cr, cg, cb))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    ivory.save(out_path)
    u_colors = set(opaque_pixels)
    c100 = len(u_colors) / (len(opaque_pixels) / 100.0) if opaque_pixels else 0.0
    print(f"✓ Saved crane ivory chassis: {out_path} (bbox: {ivory.getbbox()})")
    print(f"  Opaque pixels: {len(opaque_pixels)}, unique colors: {len(u_colors)}, c100: {c100:.2f}")
    return ivory

if __name__ == "__main__":
    create_crane_paint_ivory_stock()
