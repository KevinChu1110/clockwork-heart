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

            # Ground soft shadow at base (Y >= 117)
            if y >= 117 and (r < 75 and g < 75 and b < 85):
                volcano.putpixel((x, y), (r, g, b, a))
                opaque_pixels.append((r, g, b))
                continue

            lum = int(0.299 * r + 0.587 * g + 0.114 * b)

            # Dark outline: crisp deep blue-purple #1F1A3A
            if lum < 50:
                volcano.putpixel((x, y), (31, 26, 58, a))
                opaque_pixels.append((31, 26, 58))
                continue

            # Mechanical brass ball joints ONLY at true articulated pivots:
            is_joint = False
            if ((36 <= x <= 43 and 68 <= y <= 76) or
                (86 <= x <= 91 and 78 <= y <= 82)):
                if r > 130 and g > 60:
                    is_joint = True

            if is_joint:
                f_j = max(0.0, min(1.0, (lum - 50) / 180.0))
                jr = int(140 + f_j * 115) # 140..255
                jg = int(90 + f_j * 105)  # 90..195
                jb = int(25 + f_j * 40)   # 25..65
                volcano.putpixel((x, y), (jr, jg, jb, a))
                opaque_pixels.append((jr, jg, jb))
            else:
                # Enhanced Volcano Black baked enamel ramp with crisp metallic specular definition:
                # Shadow:   ( 24,  22,  34)  # Deep obsidian crease
                # Midtone:  ( 52,  46,  70)  # Dark titanium steel
                # Light:    ( 95,  88, 122)  # Curved surface highlight
                # Specular: (185, 178, 215)  # Polished mirror reflection
                f = max(0.0, min(1.0, (lum - 50) / 200.0))

                if f < 0.40:
                    t = f / 0.40
                    cr = int(24 + t * (52 - 24))
                    cg = int(22 + t * (46 - 22))
                    cb = int(34 + t * (70 - 34))
                elif f < 0.75:
                    t = (f - 0.40) / 0.35
                    cr = int(52 + t * (95 - 52))
                    cg = int(46 + t * (88 - 46))
                    cb = int(70 + t * (122 - 70))
                else:
                    t = (f - 0.75) / 0.25
                    cr = int(95 + t * (185 - 95))
                    cg = int(88 + t * (178 - 88))
                    cb = int(122 + t * (215 - 122))

                if lum > 175 and (x > 82 or y < 65):
                    cr = min(255, cr + 35)
                    cg = min(255, cg + 22)

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
