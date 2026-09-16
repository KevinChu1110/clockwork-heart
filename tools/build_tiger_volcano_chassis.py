#!/usr/bin/env python3
"""
tools/build_tiger_volcano_chassis.py
Constructs paint_volcano_black.png for Tiger paperdoll chassis.
- Source: game/assets/sprites/player/paperdoll/tiger/chassis/paint_ember_orange.png
- Style: 鍛爐淬火曜黑烤漆 (Volcano Black Baked Enamel)
- Pure clockwork toy aesthetic: polished obsidian enamel with brass ball-joint accents.
- Zero rust, zero dirt, crisp #1F1A3A outlines, smooth specular highlights.
- 128x128 RGBA
"""

from typing import cast
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
TIGER_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tiger"

def create_tiger_paint_volcano_black(src_path: str = "", out_path: str = ""):
    if not src_path:
        src_path = f"{TIGER_DIR}/chassis/paint_ember_orange.png"
    if not out_path:
        out_path = f"{TIGER_DIR}/chassis/paint_volcano_black.png"

    orange = Image.open(src_path).convert("RGBA")
    w, h = orange.size
    volcano = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    opaque_pixels = []

    for y in range(h):
        for x in range(w):
            r, g, b, a = cast(tuple[int, int, int, int], orange.getpixel((x, y)))
            if a <= 10:
                continue

            # Ground soft shadow at base (Y >= 118)
            if y >= 118 and (r < 75 and g < 75 and b < 85):
                volcano.putpixel((x, y), (r, g, b, a))
                opaque_pixels.append((r, g, b))
                continue

            lum = int(0.299 * r + 0.587 * g + 0.114 * b)

            # 1. Dark outline: crisp deep blue-purple #1F1A3A
            if lum < 50:
                volcano.putpixel((x, y), (31, 26, 58, a))
                opaque_pixels.append((31, 26, 58))
                continue

            # Check if this pixel is part of a brass ball joint / mechanical bearing
            # (Elbows/wrists/knees/ankles where warm gold highlights reside)
            is_joint = False
            # Ball joint areas on tiger mannequin:
            # Left wrist: x in [36..43], y in [68..76]
            # Right wrist: x in [84..92], y in [76..84]
            # Knees: x in [48..56] or [70..78], y in [92..102]
            # Ankles/Boots: y in [108..116]
            if ((36 <= x <= 43 and 68 <= y <= 76) or
                (84 <= x <= 92 and 76 <= y <= 84) or
                ((49 <= x <= 55 or 71 <= x <= 77) and 93 <= y <= 101)):
                if r > 120 and g > 50:
                    is_joint = True

            if is_joint:
                # Rich brass gold joint accent
                f_j = max(0.0, min(1.0, (lum - 50) / 180.0))
                jr = int(140 + f_j * 115) # 140..255
                jg = int(90 + f_j * 105)  # 90..195
                jb = int(25 + f_j * 40)   # 25..65
                volcano.putpixel((x, y), (jr, jg, jb, a))
                opaque_pixels.append((jr, jg, jb))
            else:
                # Volcano Black baked enamel ramp:
                # Shadow:   ( 24,  22,  34)  # Deep obsidian
                # Midtone:  ( 42,  38,  56)  # Dark titanium steel
                # Light:    ( 72,  65,  92)  # High gloss reflection
                # Specular: (160, 150, 185)  # Polished enamel edge
                f = max(0.0, min(1.0, (lum - 50) / 200.0))

                if f < 0.55:
                    t = f / 0.55
                    cr = int(24 + t * (42 - 24))
                    cg = int(22 + t * (38 - 22))
                    cb = int(34 + t * (56 - 34))
                elif f < 0.85:
                    t = (f - 0.55) / 0.30
                    cr = int(42 + t * (72 - 42))
                    cg = int(38 + t * (65 - 38))
                    cb = int(56 + t * (92 - 56))
                else:
                    t = (f - 0.85) / 0.15
                    cr = int(72 + t * (160 - 72))
                    cg = int(65 + t * (150 - 65))
                    cb = int(92 + t * (185 - 92))

                # Subtle volcanic ember edge on rightmost/topmost specular highlights
                if lum > 170 and (x > 82 or y < 65):
                    # Slight warm gold sheen on high specular
                    cr = min(255, cr + 30)
                    cg = min(255, cg + 20)

                volcano.putpixel((x, y), (cr, cg, cb, a))
                opaque_pixels.append((cr, cg, cb))

    volcano.save(out_path)
    u_colors = set(opaque_pixels)
    ratio = len(u_colors) / (len(opaque_pixels) / 100.0) if opaque_pixels else 0.0
    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {len(opaque_pixels)}, unique colors: {len(u_colors)}, ratio: {ratio:.1f}")
    return volcano

if __name__ == "__main__":
    create_tiger_paint_volcano_black()
