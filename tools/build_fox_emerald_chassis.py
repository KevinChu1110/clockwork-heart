#!/usr/bin/env python3
"""
tools/build_fox_emerald_chassis.py
Constructs paint_emerald_glaze.png for Fox paperdoll chassis.
- Source: paint_fox_orange.png
- High-fidelity continuous HSV recoloring:
  Transforms the entire chassis into R03 Emerald Woods luminescent porcelain glaze
  (翡翠螢光釉面), featuring:
  1. Rich polished emerald green porcelain enamel plates with radiant specular highlights
  2. Pale celadon / luminous jade accent plates on muzzle and inner plates
  3. Antique warm brass-gold joint gears, hinges, and rivets
  4. Deep indigo-pine shadow contours and mechanical panel grooves
- Clears trapped beige background bleed (380px) at the base to transparent (Rule 10a-2)
- Preserves micro-variations from original artwork achieving thousands of unique colors (colors/100px >= 24)
- 128x128 RGBA
"""

import os
import colorsys
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
FOX_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox"

def is_negative_space(x: int, y: int, r: int, g: int, b: int) -> bool:
    # Trapped beige background bleed at the base:
    # In paint_fox_orange, Y >= 115 has background bleed with (r > 150 and g > 130 and b > 100)
    # Outside the feet and staff base:
    if y >= 115 and (r > 150 and g > 130 and b > 100):
        return True
    return False

def create_fox_paint_emerald_glaze():
    orange_path = f"{FOX_DIR}/chassis/paint_fox_orange.png"
    orange = Image.open(orange_path).convert("RGBA")
    w, h = orange.size
    emerald = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    opaque_pixels = []

    for y in range(h):
        for x in range(w):
            r, g, b, a = cast(tuple[int, int, int, int], orange.getpixel((x, y)))
            if a == 0:
                continue
            if is_negative_space(x, y, r, g, b):
                continue

            # Ground soft shadow at base (Y >= 122 and very dark/neutral)
            if y >= 122 and (r < 65 and g < 65 and b < 80):
                emerald.putpixel((x, y), (20, 36, 30, a))
                opaque_pixels.append((20, 36, 30))
                continue

            rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
            h_val, s_val, v_val = colorsys.rgb_to_hsv(rf, gf, bf)

            # Preserve micro-variations from original artwork:
            h_offset = (h_val - 0.10) * 0.15

            # 1. Deep mechanical grooves and outlines
            if v_val < 0.22:
                target_h = 0.46 + h_offset
                target_s = min(0.65, max(0.30, s_val * 0.95 + 0.15))
                target_v = v_val

            # 2. Warm brass/gold hinges, screws, rivets (yellow-gold hues, distinct from body)
            elif 0.10 <= h_val <= 0.16 and s_val > 0.55 and v_val > 0.45 and (r > 1.25 * g and g > 1.35 * b):
                target_h = 0.125 + h_offset
                target_s = min(0.90, max(0.55, s_val * 1.05))
                target_v = v_val

            # 3. Secondary plates (muzzle, inner ear, belly) with pale celadon jade glaze
            elif s_val < 0.26 and v_val > 0.45:
                target_h = 0.41 + h_offset
                target_s = min(0.42, max(0.18, s_val * 1.1 + 0.14))
                target_v = min(1.0, v_val * 1.08)

            # 4. Main body chassis plates -> Radiant Emerald Porcelain Glaze
            elif v_val >= 0.72:
                # Polished specular highlights: cyan-emerald luminous sheen (#6DF0B0 ~ #98F8CA)
                target_h = 0.445 + h_offset
                target_s = min(0.70, max(0.35, s_val * 1.1 + 0.15))
                target_v = min(1.0, v_val * 1.12)
            else:
                # Rich, vibrant emerald glaze (#24A864 ~ #1A844E)
                target_h = 0.418 + h_offset
                target_s = min(0.88, max(0.50, s_val * 1.30 + 0.25))
                target_v = min(1.0, v_val * 1.05)

            nr, ng, nb = colorsys.hsv_to_rgb(target_h % 1.0, target_s, target_v)
            ir = int(max(0, min(255, round(nr * 255))))
            ig = int(max(0, min(255, round(ng * 255))))
            ib = int(max(0, min(255, round(nb * 255))))

            emerald.putpixel((x, y), (ir, ig, ib, a))
            opaque_pixels.append((ir, ig, ib))

    out_path = f"{FOX_DIR}/chassis/paint_emerald_glaze.png"
    emerald.save(out_path)

    u_colors = set(opaque_pixels)
    ratio = len(u_colors) / (len(opaque_pixels) / 100.0) if opaque_pixels else 0.0
    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {len(opaque_pixels)}")
    print(f"  Unique colors: {len(u_colors)}")
    print(f"  Colors/100px: {ratio:.2f}")

    return emerald

if __name__ == "__main__":
    create_fox_paint_emerald_glaze()
