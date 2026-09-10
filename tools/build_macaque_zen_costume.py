#!/usr/bin/env python3
"""
tools/build_macaque_zen_costume.py
Constructs high-fidelity costume_zen_striker.png for Macaque paperdoll.
- Tailored for Macaque's agile 2.3-head chibi martial artist body (Monk archetype, R09 Bamboo Grove)
- Zero fur / zero leather / zero biological cloth (Rule 5a / 23f-4 / 2i)
- 0a-3: Pure original clockwork toy design, NO Sun Wukong / Journey to the West elements.
- Features:
  1. High collar gorget plate with brass chamfered rim (Y: 56..64)
  2. Stepped dual articulated shoulder pauldrons with brass rivets (X: 34..46, 68..80, Y: 58..74)
  3. Mortise-and-tenon interlocking burnished bronze breastplate with circular brass core bezel ring (X: 41..70, Y: 62..82)
  4. Heavy Zen martial girdle / gear-buckle belt (X: 38..72, Y: 81..88)
  5. Segmented three-tier bronze martial tassets / hip plates (X: 38..72, Y: 88..102)
- Continuous lighting, specular bevels, 3D spherical clockwork rivets, anti-aliased outlines (colors/100px >= 24)
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
    tunic = Image.open(f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic.png").convert("RGBA")
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

    def core_a(x: int, y: int) -> int:
        if 0 <= x < w and 0 <= y < h:
            return cast(tuple[int, int, int, int], core.getpixel((x, y)))[3]
        return 0

    # 1. Gorget Collar Plate (Neck protector): X: 45..69, Y: 56..64
    for y in range(56, 65):
        for x in range(45, 70):
            if ch_a(x, y) > 30:
                dx = abs(x - 56.5) / 11.5
                dy = (y - 56) / 8.0
                n = noise(x, y) * 6.0

                # Deep ancient bronze with subtle cyan undertone (#3A524D ~ #4C6A64)
                base_r = 65.0 - dx * 20.0 + (1.0 - dy) * 25.0 + n
                base_g = 88.0 - dx * 22.0 + (1.0 - dy) * 30.0 + n
                base_b = 82.0 - dx * 20.0 + (1.0 - dy) * 25.0 + n

                # Polished brass rim on top edge (Y=56..57)
                if y == 56 or (y == 57 and dx < 0.6):
                    base_r += 115.0; base_g += 90.0; base_b -= 15.0 # Gold rim (#FFD028)
                elif y == 64:
                    base_r -= 25.0; base_g -= 25.0; base_b -= 20.0 # Shadow groove

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 2. Left Articulated Pauldron (viewer left): X: 34..46, Y: 58..75
    for y in range(58, 76):
        for x in range(34, 47):
            if ch_a(x, y) > 20:
                dist_top = (y - 58) / 17.0
                dist_left = (x - 34) / 12.0
                n = noise(x, y) * 7.0

                # Tier 1 (upper, y <= 66) vs Tier 2 (lower, y >= 67)
                if y <= 66:
                    base_r = 75.0 + (1.0 - dist_top) * 35.0 - dist_left * 15.0 + n
                    base_g = 98.0 + (1.0 - dist_top) * 40.0 - dist_left * 15.0 + n
                    base_b = 92.0 + (1.0 - dist_top) * 35.0 - dist_left * 15.0 + n
                    # Gold top and left bevel
                    if x == 34 or y == 58:
                        base_r += 95.0; base_g += 75.0; base_b -= 10.0
                    elif y == 66:
                        base_r -= 30.0; base_g -= 30.0; base_b -= 25.0 # Divider groove
                else:
                    base_r = 60.0 + (1.0 - dist_top) * 30.0 + n
                    base_g = 80.0 + (1.0 - dist_top) * 35.0 + n
                    base_b = 75.0 + (1.0 - dist_top) * 30.0 + n
                    if y == 67:
                        base_r += 75.0; base_g += 60.0; base_b -= 5.0 # Flange highlight
                    elif y == 75:
                        base_r -= 25.0; base_g -= 25.0; base_b -= 20.0

                # Spherical brass rivet stud at (38, 62) and (38, 71)
                for rx, ry in [(38, 62), (38, 71)]:
                    dr = math.sqrt((x - rx)**2 + (y - ry)**2)
                    if dr <= 1.8:
                        base_r = 235.0 - dr * 45.0 + n
                        base_g = 190.0 - dr * 40.0 + n
                        base_b = 55.0 - dr * 20.0 + n

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 3. Right Articulated Pauldron (viewer right): X: 67..80, Y: 58..75
    for y in range(58, 76):
        for x in range(67, 81):
            if ch_a(x, y) > 20:
                dist_top = (y - 58) / 17.0
                dist_right = (80 - x) / 13.0
                n = noise(x, y) * 7.0

                if y <= 66:
                    base_r = 70.0 + (1.0 - dist_top) * 30.0 + dist_right * 15.0 + n
                    base_g = 92.0 + (1.0 - dist_top) * 35.0 + dist_right * 15.0 + n
                    base_b = 86.0 + (1.0 - dist_top) * 30.0 + dist_right * 15.0 + n
                    if x == 80 or y == 58:
                        base_r += 95.0; base_g += 75.0; base_b -= 10.0
                    elif y == 66:
                        base_r -= 30.0; base_g -= 30.0; base_b -= 25.0
                else:
                    base_r = 55.0 + (1.0 - dist_top) * 25.0 + n
                    base_g = 75.0 + (1.0 - dist_top) * 30.0 + n
                    base_b = 70.0 + (1.0 - dist_top) * 25.0 + n
                    if y == 67:
                        base_r += 75.0; base_g += 60.0; base_b -= 5.0
                    elif y == 75:
                        base_r -= 25.0; base_g -= 25.0; base_b -= 20.0

                # Spherical brass rivet stud at (74, 62) and (74, 71)
                for rx, ry in [(74, 62), (74, 71)]:
                    dr = math.sqrt((x - rx)**2 + (y - ry)**2)
                    if dr <= 1.8:
                        base_r = 235.0 - dr * 45.0 + n
                        base_g = 190.0 - dr * 40.0 + n
                        base_b = 55.0 - dr * 20.0 + n

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 4. Central Mortise-and-Tenon Interlocking Breastplate: X: 41..70, Y: 64..82
    for y in range(64, 83):
        for x in range(41, 71):
            if ch_a(x, y) > 25:
                # Check if this pixel is inside the optic heart gem opening:
                # Core gem is around x=48..56, y=72..77
                dx_core = x - 52.0
                dy_core = y - 74.5
                dist_core = math.sqrt(dx_core * dx_core * 1.0 + dy_core * dy_core * 1.3)

                # Aperture window for the heart gem (leave open for glowing gem underneath)
                if dist_core < 3.2:
                    continue

                n = noise(x, y) * 6.0
                dist_c = abs(x - 55.5) / 14.5
                dist_v = (y - 64) / 18.0

                # Brass Bezel Ring around core aperture (dist_core between 3.2 and 5.2)
                if 3.2 <= dist_core <= 5.2:
                    ring_light = max(0.0, 1.0 - abs(dist_core - 4.2) / 1.0)
                    base_r = 205.0 + ring_light * 45.0 - dy_core * 8.0 + n
                    base_g = 165.0 + ring_light * 40.0 - dy_core * 6.0 + n
                    base_b = 50.0 + ring_light * 20.0 + n
                    pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)
                    continue

                # Main Cuirass Plates:
                # Dual-tone: Left pectoral vs Right pectoral with center seam at x=55
                key_light = max(0.0, (1.0 - dist_c * 0.6) * (1.0 - dist_v * 0.5))
                bounce_light = max(0.0, dist_v * 0.35) * (1.0 - dist_c * 0.4)

                # Rich burnished patinated bronze plates
                base_r = 55.0 + key_light * 55.0 + bounce_light * 25.0 + n
                base_g = 78.0 + key_light * 60.0 + bounce_light * 30.0 + n
                base_b = 75.0 + key_light * 50.0 + bounce_light * 25.0 + n

                # Top plate bevel (y=64..65)
                if y == 64:
                    base_r += 65.0; base_g += 55.0; base_b += 15.0 # Gold trim
                elif y == 65 and dist_c < 0.7:
                    base_r += 30.0; base_g += 25.0; base_b += 10.0

                # Center mortise seam at x=55
                if x == 55 and y < 71:
                    base_r -= 30.0; base_g -= 30.0; base_b -= 25.0
                elif x == 56 and y < 71:
                    base_r += 25.0; base_g += 25.0; base_b += 20.0

                # Horizontal mortise plate divide at y=71 (outside core)
                if y == 71 and abs(x - 52) > 5:
                    base_r -= 28.0; base_g -= 28.0; base_b -= 22.0
                elif y == 72 and abs(x - 52) > 5:
                    base_r += 20.0; base_g += 22.0; base_b += 18.0

                # Lateral gold border trims at x=41, 42 and x=69, 70
                if x in (41, 42, 69, 70):
                    base_r += 55.0; base_g += 45.0; base_b += 0.0

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 5. Zen Martial Girdle / Belt with Clockwork Gear Medallion: X: 38..73, Y: 81..88
    for y in range(81, 89):
        for x in range(38, 74):
            if ch_a(x, y) > 25:
                n = noise(x, y) * 5.0
                dist_mid = abs(x - 55.5) / 17.5

                # Central Round Gear Buckle at (55.5, 84.5)
                dx_b = x - 55.5
                dy_b = y - 84.5
                dist_b = math.sqrt(dx_b * dx_b + dy_b * dy_b)

                if dist_b <= 4.2:
                    # Polished brass clockwork gear medallion
                    b_light = max(0.0, 1.0 - dist_b / 4.2)
                    base_r = 210.0 + b_light * 40.0 - dy_b * 6.0 + n
                    base_g = 170.0 + b_light * 35.0 - dy_b * 5.0 + n
                    base_b = 55.0 + b_light * 20.0 + n
                    if dist_b <= 1.5:
                        # Cyan core gem pip in buckle center (#4ED86A)
                        base_r = 50.0 + n; base_g = 215.0 + n; base_b = 130.0 + n
                    pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)
                    continue

                # Belt Band: Dark lacquered iron with warm brass edges
                base_r = 40.0 + (1.0 - dist_mid) * 20.0 + n
                base_g = 48.0 + (1.0 - dist_mid) * 22.0 + n
                base_b = 52.0 + (1.0 - dist_mid) * 20.0 + n

                # Upper & lower brass piping rims
                if y == 81 or y == 88:
                    base_r += 120.0; base_g += 95.0; base_b += 10.0 # Gold trim
                elif y in (82, 87):
                    base_r += 40.0; base_g += 30.0; base_b += 5.0

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 6. Segmented Three-Tier Bronze Martial Tassets / Hip Plates: X: 39..73, Y: 88..102
    for y in range(88, 103):
        for x in range(39, 74):
            if ch_a(x, y) > 25:
                # Leave groin center slit at y >= 96 for leg movement
                if y >= 98 and abs(x - 55.5) <= 1.5:
                    continue

                n = noise(x, y) * 6.0
                dist_t = (y - 88) / 14.0
                dist_lat = abs(x - 55.5) / 17.5

                # Determine tier: Tier 1 (88..92), Tier 2 (93..97), Tier 3 (98..102)
                tier = (y - 88) // 5
                tier_rel_y = (y - 88) % 5

                base_r = 60.0 + (1.0 - dist_t) * 30.0 + dist_lat * 15.0 + n
                base_g = 82.0 + (1.0 - dist_t) * 35.0 + dist_lat * 15.0 + n
                base_b = 78.0 + (1.0 - dist_t) * 30.0 + dist_lat * 15.0 + n

                # Tier top overlap highlight
                if tier_rel_y == 0:
                    base_r += 50.0; base_g += 45.0; base_b += 10.0
                # Tier bottom edge shadow
                elif tier_rel_y == 4:
                    base_r -= 25.0; base_g -= 25.0; base_b -= 20.0

                # Outer plate edge gold trim
                if x in (39, 40, 72, 73):
                    base_r += 75.0; base_g += 60.0; base_b += 5.0

                # Brass rivet on each tasset plate
                if tier_rel_y == 2 and x in (45, 66):
                    base_r = 230.0 + n; base_g = 185.0 + n; base_b = 50.0 + n

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # Write all pixels to art image
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
