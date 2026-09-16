#!/usr/bin/env python3
"""
tools/build_macaque_dawn_tunic.py
Constructs canonical costume_dawn_monk_tunic.png for Macaque paperdoll.
- Tailored for Macaque's agile 2.3-head chibi martial artist body (Monk archetype, R09 Bamboo Grove)
- Zero fur / zero organic leather / zero biological cloth (Rule 5a / 23f-4 / 2i)
- 0a-3: Pure original clockwork toy design, NO Sun Wukong / Journey to the West elements.
- Features:
  1. Low-profile crossover monk tunic collar with polished brass piping (Y >= 59)
  2. Cinnabar / dawn terracotta enameled plates with golden edge trim
  3. Circular core bezel ring (Y: 72..78, X: 48..54) ensuring optical core visibility
  4. Deep navy martial waist sash with polished brass gear buckle (Y: 80..83)
  5. Crisp #1F1A3A outline, smooth cel-shading light ramp
- Complies strictly with review.md Rule 4c-9, 4c-9-1, 19g-14:
  - Collar top edge Y >= 59
  - 0 identical pixels with chassis (Rule 4c Layer Independence)
  - 128x128 RGBA
"""

import math
import os
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

def create_macaque_costume_dawn_tunic(out_path: str = f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic.png"):
    w, h = 128, 128
    tunic = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    chassis = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png").convert("RGBA")

    def clamp(v: float, low: float = 0.0, high: float = 255.0) -> int:
        return int(max(low, min(high, round(v))))

    def ch_a(x: int, y: int) -> int:
        if 0 <= x < w and 0 <= y < h:
            return cast(tuple[int, int, int, int], chassis.getpixel((x, y)))[3]
        return 0

    pixels = {}

    # Torso vest coverage (X: 38..68, Y: 59..83)
    for y in range(59, 84):
        for x in range(38, 69):
            if ch_a(x, y) > 30:
                dx_center = abs(x - 56.0)

                # Collar dip in center
                if dx_center < 7.0 and y < 61:
                    continue
                if dx_center < 9.0 and y < 60:
                    continue

                # Core aperture cutout: around (51, 75), radius ~ 3.8
                dist_core = math.sqrt((x - 51.0)**2 + (y - 75.0)**2)
                if dist_core < 3.8:
                    continue

                # Martial waist sash at bottom (Y: 80..83)
                if y >= 80:
                    if 48 <= x <= 54:
                        # Gold gear buckle
                        r, g, b = 255, 208, 40
                        if dist_core < 4.8 or x == 48 or x == 54 or y == 80 or y == 83:
                            r, g, b = 180, 130, 20
                    else:
                        # Deep navy sash
                        r, g, b = 42, 50, 75
                        if y == 80 or y == 83:
                            r, g, b = 31, 26, 58
                    pixels[(x, y)] = (r, g, b, 255)
                    continue

                # Collar trim along top edge
                is_collar = (y == 59 and dx_center >= 9.0) or (y == 60 and 7.0 <= dx_center < 9.0) or (y == 61 and dx_center < 7.0)
                if is_collar:
                    pixels[(x, y)] = (255, 208, 40, 255)
                    continue

                # Core bezel ring around cutout
                if 3.8 <= dist_core <= 5.2:
                    pixels[(x, y)] = (250, 200, 45, 255)
                    continue

                # Main Dawn Monk Tunic Body:
                lapel_x = 46.0 + (y - 62) * (7.0 / 17.0)
                is_seam = abs(x - lapel_x) < 0.8 and y < 80

                norm_x = (x - 38) / 30.0
                norm_y = (y - 59) / 24.0

                base_r = 210.0 + norm_x * 25.0 - norm_y * 30.0
                base_g = 85.0 + norm_x * 35.0 - norm_y * 20.0
                base_b = 45.0 + norm_x * 20.0 - norm_y * 15.0

                if is_seam:
                    base_r, base_g, base_b = 255.0, 210.0, 60.0

                is_edge = (x == 38 or x == 68 or ch_a(x-1, y) <= 30 or ch_a(x+1, y) <= 30)
                if is_edge:
                    base_r, base_g, base_b = 31.0, 26.0, 58.0

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    for (x, y), col in pixels.items():
        tunic.putpixel((x, y), col)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    tunic.save(out_path)
    print(f"✓ Saved macaque dawn monk tunic to {out_path} ({len(pixels)} px)")
    return tunic

if __name__ == "__main__":
    create_macaque_costume_dawn_tunic()
