#!/usr/bin/env python3
"""
tools/build_macaque_bronze_chassis.py
Constructs paint_bamboo_bronze.png for Macaque paperdoll chassis.
- Source: paint_ivory_stock.png
- High-fidelity continuous HSV recoloring: transforms chassis into R09 Bamboo Grove patinated ancient cyan-bronze (天元青古銅烤漆).
- Deep patinated antique bronze / cyan-bronze enamel with warm brass hinges, rivets, and joints.
- Preserves micro-variations from original artwork (colors/100px >= 24).
- 128x128 RGBA
"""

import os
import math
import colorsys
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

def noise(x: int, y: int) -> float:
    return (math.sin(x * 0.85 + y * 0.45) * 0.5 + 
            math.cos(x * 0.35 - y * 0.75) * 0.3 + 
            math.sin((x + y) * 1.2) * 0.2)

def create_macaque_paint_bamboo_bronze():
    ivory_path = f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png"
    ivory = Image.open(ivory_path).convert("RGBA")
    w, h = ivory.size
    bronze = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    opaque_pixels = []

    for y in range(h):
        for x in range(w):
            r, g, b, a = cast(tuple[int, int, int, int], ivory.getpixel((x, y)))
            if a == 0:
                continue

            # Ground soft shadow at base (Y >= 118, neutral dark/shadow)
            if y >= 118 and (r < 75 and g < 75 and b < 85):
                bronze.putpixel((x, y), (r, g, b, a))
                opaque_pixels.append((r, g, b))
                continue

            rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
            h_val, s_val, v_val = colorsys.rgb_to_hsv(rf, gf, bf)

            # Micro-variations
            h_offset = (h_val - 0.10) * 0.20
            n = noise(x, y) * 0.015

            # 1. Deep mechanical grooves and outlines (v_val < 0.25)
            if v_val < 0.25:
                # Deep ink-slate / dark bronze charcoal
                target_h = 0.45 + h_offset + n
                target_s = min(0.55, max(0.20, s_val * 0.90 + 0.15))
                target_v = v_val * 0.95

            # 2. Brass/gold joints, hinges, screws (yellowish tones in original)
            elif (0.08 <= h_val <= 0.18 and s_val > 0.40) or (r > 1.2 * b and g > 1.15 * b and s_val > 0.35):
                # Vibrant polished brass gold (#FFD028 ~ #E5A93C)
                target_h = 0.125 + h_offset * 0.5 + n
                target_s = min(0.92, max(0.60, s_val * 1.10 + 0.10))
                target_v = min(1.0, v_val * 1.05)

            # 3. Muzzle, cheek plate, inner ear accents (lighter, lower saturation)
            elif s_val < 0.22 and v_val > 0.50 and y < 58:
                # Champagne bronze / pale bronze glaze (#8FA69D ~ #A8BDB5)
                target_h = 0.40 + h_offset + n
                target_s = min(0.35, max(0.16, s_val * 1.05 + 0.12))
                target_v = min(1.0, v_val * 1.06)

            # 4. Main body chassis plates -> Patinated Ancient Cyan-Bronze Enamel (青古銅)
            elif v_val >= 0.75:
                # Specular bevels & highlights: lustrous antique bronze sheen with slight cyan tint (#76A69D ~ #90BFB6)
                target_h = 0.435 + h_offset + n
                target_s = min(0.55, max(0.25, s_val * 1.05 + 0.18))
                target_v = min(1.0, v_val * 1.10)
            else:
                # Rich patinated ancient cyan-bronze (#3E635C ~ #2E4E48 ~ #527B73)
                target_h = 0.440 + h_offset + n
                target_s = min(0.78, max(0.38, s_val * 1.25 + 0.22))
                target_v = min(1.0, v_val * 1.04)

            nr, ng, nb = colorsys.hsv_to_rgb(target_h % 1.0, max(0.0, min(1.0, target_s)), max(0.0, min(1.0, target_v)))
            ir = int(max(0, min(255, round(nr * 255))))
            ig = int(max(0, min(255, round(ng * 255))))
            ib = int(max(0, min(255, round(nb * 255))))

            bronze.putpixel((x, y), (ir, ig, ib, a))
            opaque_pixels.append((ir, ig, ib))

    out_path = f"{MACAQUE_DIR}/chassis/paint_bamboo_bronze.png"
    bronze.save(out_path)

    u_colors = set(opaque_pixels)
    ratio = len(u_colors) / (len(opaque_pixels) / 100.0) if opaque_pixels else 0.0
    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {len(opaque_pixels)}")
    print(f"  Unique colors: {len(u_colors)}")
    print(f"  Colors/100px: {ratio:.2f}")

    return bronze

if __name__ == "__main__":
    create_macaque_paint_bamboo_bronze()
