#!/usr/bin/env python3
"""
tools/build_rabbit_navy_chassis.py
Constructs paint_midnight_navy.png for Rabbit paperdoll chassis.
- Source: paint_brass_gold.png (Rabbit)
- High-fidelity continuous HSV recoloring: preserves V (luminance) micro-variations while
  mapping to deep, rich Midnight Navy enamel (aligned with Lion midnight navy standard).
- Gunmetal / deep indigo joints (#1F1A3A), deep navy body plating, and polished specular bevel highlights.
- Zero flood-fill holes inside character body (Rule 4c-1).
"""

import os
import math
import colorsys
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
RABBIT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rabbit"

def micro_grain(x: int, y: int) -> float:
    # Subtle deterministic hand-painted surface micro-grain
    return ((math.sin(x * 12.9898 + y * 78.233) * 43758.5453) % 1.0 - 0.5) * 3.0

def create_rabbit_paint_midnight_navy() -> Image.Image:
    gold_path = f"{RABBIT_DIR}/chassis/paint_brass_gold.png"
    gold = Image.open(gold_path).convert("RGBA")
    w, h = gold.size
    navy = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    opaque_pixels = []

    for y in range(h):
        for x in range(w):
            r, g, b, a = cast(tuple[int, int, int, int], gold.getpixel((x, y)))
            if a == 0:
                continue

            # Ground soft shadow at base (Y >= 118)
            if y >= 118 and (r < 60 and g < 60 and b < 80):
                navy.putpixel((x, y), (31, 26, 58, a))
                opaque_pixels.append((31, 26, 58))
                continue

            rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
            h_val, s_val, v_val = colorsys.rgb_to_hsv(rf, gf, bf)

            # Continuous mapping to Midnight Navy:
            # Preserve micro-variations from original artwork:
            h_var = (h_val - 0.12) * 0.35
            s_var = (s_val - 0.60) * 0.20

            # Target Hue: 0.64 (indigo/navy) in shadows down to 0.57 (cyan-sheen) in specular highlights
            target_h = 0.64 - 0.08 * (v_val ** 0.85) + h_var

            # Target Saturation: rich enamel saturation
            target_s = max(0.35, min(0.92, 0.60 + 0.28 * math.sin(v_val * math.pi * 0.85) + s_var))

            # Target Value (luminance):
            # Rich, deep Midnight Navy enamel
            if v_val < 0.40:
                target_v = 0.09 + (v_val / 0.40) * 0.12
                target_s = min(0.60, target_s * 0.75)
            elif v_val < 0.92:
                norm = (v_val - 0.40) / 0.52
                target_v = 0.20 + norm * 0.24  # 0.20 .. 0.44
                target_s = min(0.92, target_s * 1.10)
            else:
                norm = (v_val - 0.92) / 0.08
                target_v = 0.44 + norm * 0.40  # 0.44 .. 0.84
                target_s = max(0.25, target_s * 0.65)

            nr, ng, nb = colorsys.hsv_to_rgb(target_h % 1.0, target_s, target_v)
            grain = micro_grain(x, y)
            ir = max(0, min(255, int(round(nr * 255 + grain))))
            ig = max(0, min(255, int(round(ng * 255 + grain * 0.85))))
            ib = max(0, min(255, int(round(nb * 255 + grain * 1.15))))

            navy.putpixel((x, y), (ir, ig, ib, a))
            opaque_pixels.append((ir, ig, ib))

    out_path = f"{RABBIT_DIR}/chassis/paint_midnight_navy.png"
    navy.save(out_path)

    u_colors = set(opaque_pixels)
    ratio = len(u_colors) / (len(opaque_pixels) / 100.0) if opaque_pixels else 0.0
    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {len(opaque_pixels)}")
    print(f"  Unique colors: {len(u_colors)}")
    print(f"  Colors/100px: {ratio:.2f}")

    return navy

if __name__ == "__main__":
    create_rabbit_paint_midnight_navy()
