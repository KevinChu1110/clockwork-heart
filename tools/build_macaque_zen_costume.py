#!/usr/bin/env python3
"""
tools/build_macaque_zen_costume.py
Constructs high-fidelity costume_zen_striker.png for Macaque paperdoll.
- Tailored for Macaque's agile 2.3-head chibi martial artist body (Monk archetype, R09 Bamboo Grove)
- Zero fur / zero leather / zero biological cloth (Rule 5a / 23f-4 / 2i)
- 0a-3: Pure original clockwork toy design, NO Sun Wukong / Journey to the West elements.
- Features:
  1. Low-profile mortise-and-tenon gorget collar plate with brass chamfered rim (Y >= 59, dipping in center to leave jaw/mouth 100% visible)
  2. Stepped dual articulated shoulder pauldrons with brass rivets (X: 36..46, 60..68, Y: 60..75)
  3. Mortise-and-tenon interlocking burnished bronze breastplate with circular brass core bezel ring (X: 41..68, Y: 64..80)
  4. Compact Zen martial girdle / gear-buckle belt (X: 41..68, Y: 81..83, stops cleanly at Y=83 to match monk tunic)
- Complies strictly with review.md Rule 4c-9 and 4c-9-1:
  - Collar top edge Y >= 59 (matches or lower than dawn monk tunic)
  - Altered bare chassis dark line pixels <= 255 (does not invade face/mouth/jaw)
- Continuous lighting, specular bevels, 3D spherical clockwork rivets, anti-aliased outlines (colors/100px in 24..96)
- Layer independence: 0 identical pixels with chassis (Rule 4c)
- 128x128 RGBA
"""

import math
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

def create_macaque_costume_zen_striker():
    w, h = 128, 128
    art = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    chassis = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png").convert("RGBA")
    core = Image.open(f"{MACAQUE_DIR}/optic_core/core_cyan_emerald.png").convert("RGBA")

    pixels: dict[tuple[int, int], tuple[int, int, int, int]] = {}

    def clamp(v: float, low: float = 0.0, high: float = 255.0) -> int:
        return int(max(low, min(high, round(v))))

    def noise(x: int, y: int) -> float:
        return (math.sin(x * 0.85 + y * 0.45) * 0.5 + 
                math.cos(x * 0.35 - y * 0.75) * 0.3 + 
                math.sin((x + y) * 1.2) * 0.2)

    def ch_a(x: int, y: int) -> int:
        if 0 <= x < w and 0 <= y < h:
            return cast(tuple[int, int, int, int], chassis.getpixel((x, y)))[3]
        return 0

    # 1. Gorget Collar Plate (Low collar, following neck curve, y >= 59)
    # Center (x: 48..64) dips to y >= 61 so chin/jaw is completely open!
    # Sides (x: 42..47 and 65..68) start at y=59
    for y in range(59, 66):
        for x in range(42, 69):
            if ch_a(x, y) > 30:
                dx_center = abs(x - 56.0)
                # In center (x: 48..64, dx_center < 8), top y must be >= 61
                if dx_center < 7.0 and y < 61:
                    continue
                if dx_center < 9.0 and y < 60:
                    continue

                dx = abs(x - 56.0) / 13.0
                dy = (y - 59) / 7.0
                n = noise(x, y) * 6.0

                # Deep ancient bronze with cyan undertone (#3A524D ~ #4C6A64)
                base_r = 65.0 - dx * 20.0 + (1.0 - dy) * 25.0 + n
                base_g = 88.0 - dx * 22.0 + (1.0 - dy) * 30.0 + n
                base_b = 82.0 - dx * 20.0 + (1.0 - dy) * 25.0 + n

                # Polished brass rim along top edge
                is_top = (y == 59 and dx_center >= 9.0) or (y == 60 and 7.0 <= dx_center < 9.0) or (y == 61 and dx_center < 7.0)
                if is_top:
                    base_r += 115.0; base_g += 90.0; base_b -= 15.0 # Gold rim (#FFD028)
                elif y == 65:
                    base_r -= 25.0; base_g -= 25.0; base_b -= 20.0 # Shadow groove

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 2. Left Pauldron: X: 36..46, Y: 60..75
    for y in range(60, 76):
        for x in range(36, 47):
            if ch_a(x, y) > 20:
                dist_top = (y - 60) / 15.0
                dist_left = (x - 36) / 11.0
                n = noise(x, y) * 7.0

                if y <= 67:
                    base_r = 75.0 + (1.0 - dist_top) * 35.0 - dist_left * 15.0 + n
                    base_g = 98.0 + (1.0 - dist_top) * 40.0 - dist_left * 15.0 + n
                    base_b = 92.0 + (1.0 - dist_top) * 35.0 - dist_left * 15.0 + n
                    if x == 36 or y == 60:
                        base_r += 95.0; base_g += 75.0; base_b -= 10.0
                    elif y == 67:
                        base_r -= 30.0; base_g -= 30.0; base_b -= 25.0
                else:
                    base_r = 60.0 + (1.0 - dist_top) * 30.0 + n
                    base_g = 80.0 + (1.0 - dist_top) * 35.0 + n
                    base_b = 75.0 + (1.0 - dist_top) * 30.0 + n
                    if y == 68:
                        base_r += 75.0; base_g += 60.0; base_b -= 5.0
                    elif y == 75:
                        base_r -= 25.0; base_g -= 25.0; base_b -= 20.0

                # Rivet at (39, 63) and (39, 72)
                for rx, ry in [(39, 63), (39, 72)]:
                    dr = math.sqrt((x - rx)**2 + (y - ry)**2)
                    if dr <= 1.7:
                        base_r = 235.0 - dr * 45.0 + n
                        base_g = 190.0 - dr * 40.0 + n
                        base_b = 55.0 - dr * 20.0 + n

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 3. Right Pauldron: X: 64..68, Y: 60..75 (kept strictly within x <= 68)
    for y in range(60, 76):
        for x in range(64, 69):
            if ch_a(x, y) > 20:
                dist_top = (y - 60) / 15.0
                dist_right = (68 - x) / 5.0
                n = noise(x, y) * 7.0

                if y <= 67:
                    base_r = 70.0 + (1.0 - dist_top) * 30.0 + dist_right * 15.0 + n
                    base_g = 92.0 + (1.0 - dist_top) * 35.0 + dist_right * 15.0 + n
                    base_b = 86.0 + (1.0 - dist_top) * 30.0 + dist_right * 15.0 + n
                    if x == 68 or y == 60:
                        base_r += 95.0; base_g += 75.0; base_b -= 10.0
                    elif y == 67:
                        base_r -= 30.0; base_g -= 30.0; base_b -= 25.0
                else:
                    base_r = 55.0 + (1.0 - dist_top) * 25.0 + n
                    base_g = 75.0 + (1.0 - dist_top) * 30.0 + n
                    base_b = 70.0 + (1.0 - dist_top) * 25.0 + n
                    if y == 68:
                        base_r += 75.0; base_g += 60.0; base_b -= 5.0
                    elif y == 75:
                        base_r -= 25.0; base_g -= 25.0; base_b -= 20.0

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 4. Central Mortise-and-Tenon Interlocking Breastplate: X: 41..68, Y: 64..80
    for y in range(64, 81):
        for x in range(41, 69):
            if ch_a(x, y) > 25:
                dx_core = x - 52.0
                dy_core = y - 74.5
                dist_core = math.sqrt(dx_core * dx_core * 1.0 + dy_core * dy_core * 1.3)

                # Open aperture for optic heart gem underneath
                if dist_core < 3.2:
                    continue

                n = noise(x, y) * 6.0
                dist_c = abs(x - 55.5) / 13.5
                dist_v = (y - 64) / 16.0

                # Brass Bezel Ring around core aperture
                if 3.2 <= dist_core <= 5.2:
                    ring_light = max(0.0, 1.0 - abs(dist_core - 4.2) / 1.0)
                    base_r = 205.0 + ring_light * 45.0 - dy_core * 8.0 + n
                    base_g = 165.0 + ring_light * 40.0 - dy_core * 6.0 + n
                    base_b = 50.0 + ring_light * 20.0 + n
                    pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)
                    continue

                key_light = max(0.0, (1.0 - dist_c * 0.6) * (1.0 - dist_v * 0.5))
                bounce_light = max(0.0, dist_v * 0.35) * (1.0 - dist_c * 0.4)

                base_r = 55.0 + key_light * 55.0 + bounce_light * 25.0 + n
                base_g = 78.0 + key_light * 60.0 + bounce_light * 30.0 + n
                base_b = 75.0 + key_light * 50.0 + bounce_light * 25.0 + n

                if y == 64:
                    base_r += 65.0; base_g += 55.0; base_b += 15.0
                elif y == 65 and dist_c < 0.7:
                    base_r += 30.0; base_g += 25.0; base_b += 10.0

                if x == 55 and y < 71:
                    base_r -= 30.0; base_g -= 30.0; base_b -= 25.0
                elif x == 56 and y < 71:
                    base_r += 25.0; base_g += 25.0; base_b += 20.0

                if y == 71 and abs(x - 52) > 5:
                    base_r -= 28.0; base_g -= 28.0; base_b -= 22.0
                elif y == 72 and abs(x - 52) > 5:
                    base_r += 20.0; base_g += 22.0; base_b += 18.0

                if x in (41, 42, 67, 68):
                    base_r += 55.0; base_g += 45.0; base_b += 0.0

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 5. Zen Martial Girdle / Belt with Clockwork Gear Medallion: X: 41..68, Y: 81..83 (stops at y=83)
    for y in range(81, 84):
        for x in range(41, 69):
            if ch_a(x, y) > 25:
                n = noise(x, y) * 5.0
                dist_mid = abs(x - 55.5) / 13.5

                dx_b = x - 55.5
                dy_b = y - 82.0
                dist_b = math.sqrt(dx_b * dx_b + dy_b * dy_b)

                if dist_b <= 3.2:
                    b_light = max(0.0, 1.0 - dist_b / 3.2)
                    base_r = 210.0 + b_light * 40.0 - dy_b * 6.0 + n
                    base_g = 170.0 + b_light * 35.0 - dy_b * 5.0 + n
                    base_b = 55.0 + b_light * 20.0 + n
                    if dist_b <= 1.2:
                        base_r = 50.0 + n; base_g = 215.0 + n; base_b = 130.0 + n
                    pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)
                    continue

                base_r = 40.0 + (1.0 - dist_mid) * 20.0 + n
                base_g = 48.0 + (1.0 - dist_mid) * 22.0 + n
                base_b = 52.0 + (1.0 - dist_mid) * 20.0 + n

                if y == 81 or y == 83:
                    base_r += 120.0; base_g += 95.0; base_b += 10.0
                elif y == 82:
                    base_r += 40.0; base_g += 30.0; base_b += 5.0

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    for (x, y), col in pixels.items():
        art.putpixel((x, y), col)

    out_path = f"{MACAQUE_DIR}/costume/costume_zen_striker.png"
    art.save(out_path)

    opaque = [c for c in pixels.values()]
    u_colors = set(opaque)
    ratio = len(u_colors) / (len(opaque) / 100.0) if opaque else 0.0
    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {len(opaque)}")
    print(f"  Unique colors: {len(u_colors)}")
    print(f"  Colors/100px: {ratio:.2f}")

    return art

if __name__ == "__main__":
    create_macaque_costume_zen_striker()
