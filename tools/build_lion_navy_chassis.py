#!/usr/bin/env python3
"""
tools/build_lion_navy_chassis.py
Constructs paint_midnight_navy.png for Lion paperdoll chassis.
- Source: paint_brass_gold.png
- High-fidelity continuous HSV recoloring: preserves V (luminance) and micro-variations,
  achieving thousands of unique colors (colors/100px >= 24).
- Clears negative space background bleed (Rule 10a-2):
  1. Lance and torso gap
  2. Between legs gap
  3. Inside winding key hole
"""

import os
import colorsys
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
LION_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion"

def is_negative_space(x: int, y: int, r: int, g: int, b: int) -> bool:
    # 1. Winding key hole cutout
    if y in (61, 62) and x in (94, 95):
        return True
    # 2. Gap between lance and torso
    if 85 <= y <= 115 and 39 <= x <= 55 and (r > 230 and g > 220 and b > 200):
        return True
    # 3. Gap between legs
    if 103 <= y <= 114 and 64 <= x <= 72 and (r > 230 and g > 220 and b > 200):
        return True
    return False

def create_lion_paint_midnight_navy():
    gold_path = f"{LION_DIR}/chassis/paint_brass_gold.png"
    gold = Image.open(gold_path).convert("RGBA")
    w, h = gold.size
    navy = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    opaque_pixels = []

    for y in range(h):
        for x in range(w):
            r, g, b, a = cast(tuple[int, int, int, int], gold.getpixel((x, y)))
            if a == 0:
                continue
            if is_negative_space(x, y, r, g, b):
                # Clean negative space to transparent
                continue

            # Ground soft shadow at base (Y >= 116)
            if y >= 116 and (r < 60 and g < 60 and b < 80):
                navy.putpixel((x, y), (31, 26, 58, a))
                opaque_pixels.append((31, 26, 58))
                continue

            rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
            h_val, s_val, v_val = colorsys.rgb_to_hsv(rf, gf, bf)

            # Continuous mapping to Midnight Navy:
            # Preserve micro-variations from original artwork:
            h_offset = (h_val - 0.12) * 0.15

            if v_val < 0.25:
                # Deep shadows & outlines: indigo-navy (#1F1A3A)
                target_h = 0.68 + h_offset
                target_s = min(0.65, max(0.20, s_val * 0.90 + 0.15))
            elif v_val < 0.75:
                # Mid-tone Midnight Navy High-Gloss Enamel
                target_h = 0.61 + h_offset
                target_s = min(0.75, max(0.35, s_val * 1.05 + 0.10))
            else:
                # Polished specular highlight (cyan-tinted sheen)
                target_h = 0.57 + h_offset
                target_s = min(0.55, max(0.25, s_val * 0.85 + 0.05))

            nr, ng, nb = colorsys.hsv_to_rgb(target_h % 1.0, target_s, v_val)
            ir = int(max(0, min(255, round(nr * 255))))
            ig = int(max(0, min(255, round(ng * 255))))
            ib = int(max(0, min(255, round(nb * 255))))

            navy.putpixel((x, y), (ir, ig, ib, a))
            opaque_pixels.append((ir, ig, ib))

    out_path = f"{LION_DIR}/chassis/paint_midnight_navy.png"
    navy.save(out_path)

    u_colors = set(opaque_pixels)
    ratio = len(u_colors) / (len(opaque_pixels) / 100.0) if opaque_pixels else 0.0
    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {len(opaque_pixels)}")
    print(f"  Unique colors: {len(u_colors)}")
    print(f"  Colors/100px: {ratio:.2f}")

    return navy

if __name__ == "__main__":
    create_lion_paint_midnight_navy()
