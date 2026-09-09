#!/usr/bin/env python3
"""
tools/build_rabbit_royal_costume.py
Constructs costume_royal_parade.png for Rabbit paperdoll.
- Royal Parade Ceremonial Gala Armor / Uniform (皇家巡遊金屬禮服)
- 100% mechanical toy metal/enamel construction: zero fur, zero leather, zero cloth (Rule 5a / 23f-4)
- High-fidelity continuous shading, specular bevels, 3D gear buttons, and hand-painted gradients
  achieving colors/100px >= 24 (Rule 10a-2)
- Layer independence: 0% identical pixels with chassis (Rule 4c)
- 128x128 RGBA
"""

import math
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
RABBIT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rabbit"

def clamp(v: float, low: float = 0.0, high: float = 255.0) -> int:
    return int(max(low, min(high, round(v))))

def noise(x: int, y: int) -> float:
    return (math.sin(x * 0.92 + y * 0.48) * 0.5 +
            math.cos(x * 0.38 - y * 0.72) * 0.3 +
            math.sin((x + y) * 1.15) * 0.2)

def micro_grain(x: int, y: int) -> float:
    return ((math.sin(x * 12.9898 + y * 78.233) * 43758.5453) % 1.0 - 0.5) * 3.5

def create_rabbit_costume_royal_parade() -> Image.Image:
    w, h = 128, 128
    costume = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    nut = Image.open(f"{RABBIT_DIR}/costume/costume_nutcracker_guard.png").convert("RGBA")
    chassis = Image.open(f"{RABBIT_DIR}/chassis/paint_brass_gold.png").convert("RGBA")

    pixels: dict[tuple[int, int], tuple[int, int, int, int]] = {}

    def nut_a(x: int, y: int) -> int:
        return cast(tuple[int, int, int, int], nut.getpixel((x, y)))[3]

    def ch_a(x: int, y: int) -> int:
        return cast(tuple[int, int, int, int], chassis.getpixel((x, y)))[3]

    # Outline color: deep indigo-navy #1F1A3A
    OUTLINE = (31, 26, 58, 255)

    # -------------------------------------------------------------
    # 1. Pauldrons / Shoulder Epaulets (X: 43..52 left, X: 74..83 right, Y: 74..83)
    # -------------------------------------------------------------
    # Left shoulder (viewer left):
    for y in range(74, 84):
        for x in range(43, 53):
            if nut_a(x, y) > 15 or (ch_a(x, y) > 20 and x <= 50):
                # Tiered brass pauldron plate
                dist_top = (y - 74) / 9.0
                dist_left = (x - 43) / 9.0
                n = noise(x, y) * 6.0 + micro_grain(x, y)
                # Gilded brass with directional light from top-left
                base_r = 235.0 - dist_top * 65.0 - dist_left * 25.0 + n
                base_g = 185.0 - dist_top * 60.0 - dist_left * 20.0 + n
                base_b = 65.0 - dist_top * 30.0 - dist_left * 15.0 + n
                if y == 74 or (y == 75 and x <= 47):
                    # Specular rim
                    base_r += 25; base_g += 30; base_b += 40
                if y >= 82 or x == 43:
                    # Shadow bevel
                    base_r -= 35; base_g -= 35; base_b -= 15
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # Right shoulder (viewer right):
    for y in range(74, 84):
        for x in range(74, 84):
            if nut_a(x, y) > 15 or (ch_a(x, y) > 20 and x >= 76):
                dist_top = (y - 74) / 9.0
                dist_right = (83 - x) / 9.0
                n = noise(x, y) * 6.0 + micro_grain(x, y)
                base_r = 215.0 - dist_top * 65.0 + dist_right * 20.0 + n
                base_g = 165.0 - dist_top * 60.0 + dist_right * 15.0 + n
                base_b = 60.0 - dist_top * 30.0 + dist_right * 10.0 + n
                if y == 74 or (y == 75 and x >= 79):
                    base_r += 20; base_g += 25; base_b += 35
                if y >= 82 or x == 83:
                    base_r -= 35; base_g -= 35; base_b -= 15
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # -------------------------------------------------------------
    # 2. Gorget / High Gilded Collar (Y: 74..78, X: 51..75)
    # -------------------------------------------------------------
    for y in range(74, 79):
        for x in range(51, 76):
            if nut_a(x, y) > 10 or ch_a(x, y) > 25:
                n = noise(x, y) * 5.0 + micro_grain(x, y)
                cx = abs(x - 63) / 12.0
                # Polished golden gorget plate
                base_r = 245.0 - cx * 40.0 - (y - 74) * 12.0 + n
                base_g = 195.0 - cx * 35.0 - (y - 74) * 12.0 + n
                base_b = 75.0 - cx * 20.0 - (y - 74) * 5.0 + n
                if y == 74:
                    # Top highlight
                    base_r += 15; base_g += 25; base_b += 35
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # -------------------------------------------------------------
    # 3. Double-breasted Gala Breastplate (Y: 79..93, X: 48..78)
    # -------------------------------------------------------------
    # Deep royal blue enamel with gilded edge trims and center seam
    for y in range(79, 94):
        for x in range(48, 79):
            if nut_a(x, y) > 10 or ch_a(x, y) > 20:
                n = noise(x, y) * 6.0 + micro_grain(x, y)
                vy = (y - 79) / 14.0
                vx = (x - 48) / 30.0
                cx = abs(x - 63.5)

                # Is this a gold trim or seam?
                is_outer_gold = (x in (48, 49, 77, 78)) or (y in (79, 80))
                is_center_gold = (cx <= 1.2)
                is_sash_chevron = (abs(y - (85 - int(cx * 0.4))) <= 1) and cx <= 8

                if is_outer_gold or is_center_gold or is_sash_chevron:
                    # Gilded filigree & trim
                    base_r = 225.0 - vy * 45.0 - (x - 48) * 0.8 + n
                    base_g = 175.0 - vy * 40.0 - (x - 48) * 0.8 + n
                    base_b = 60.0 - vy * 20.0 + n
                    if is_center_gold:
                        base_r += 15; base_g += 15; base_b += 10
                else:
                    # Royal Blue / Cobalt Enamel Plate
                    # Curvature highlight around x=58..62, y=82..88
                    spec = math.exp(-((x - 59)**2 / 24.0 + (y - 84)**2 / 18.0)) * 65.0
                    base_r = 32.0 + vy * 12.0 - vx * 8.0 + spec * 0.6 + n
                    base_g = 55.0 + vy * 18.0 - vx * 10.0 + spec * 0.8 + n
                    base_b = 105.0 + vy * 25.0 - vx * 12.0 + spec * 1.2 + n
                    # Ambient occlusion near borders
                    if x in (50, 76) or y == 93:
                        base_r -= 12; base_g -= 16; base_b -= 22

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # -------------------------------------------------------------
    # 4. Spherical Gilded Gear Buttons (6 buttons, 2 columns of 3)
    # -------------------------------------------------------------
    button_coords = [
        (54, 82), (54, 86), (54, 90),
        (72, 82), (72, 86), (72, 90)
    ]
    for bx, by in button_coords:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                pos = (bx + dx, by + dy)
                dist = math.sqrt(dx * dx + dy * dy)
                if dist <= 1.4:
                    # 3D sphere highlight: light from top-left (-1, -1)
                    light = (-dx - dy) / 2.0
                    n = micro_grain(pos[0], pos[1])
                    br = 220.0 + light * 45.0 + n
                    bg = 175.0 + light * 40.0 + n
                    bb = 55.0 + light * 25.0 + n
                    if dist <= 0.6:
                        # specular hot-spot
                        br += 30; bg += 35; bb += 45
                    pixels[pos] = (clamp(br), clamp(bg), clamp(bb), 255)

    # -------------------------------------------------------------
    # 5. Royal Belt & Clockwork Buckle (Y: 94..98, X: 48..78)
    # -------------------------------------------------------------
    for y in range(94, 99):
        for x in range(48, 79):
            if nut_a(x, y) > 10 or ch_a(x, y) > 20:
                n = noise(x, y) * 5.0 + micro_grain(x, y)
                cx = abs(x - 63.5)
                # Central Buckle (X: 59..68)
                if cx <= 4.5:
                    dist_b = math.sqrt((cx)**2 + (y - 96)**2)
                    if dist_b <= 4.0:
                        # Octagonal/round clockwork star buckle
                        base_r = 250.0 - dist_b * 15.0 + n
                        base_g = 205.0 - dist_b * 15.0 + n
                        base_b = 85.0 - dist_b * 8.0 + n
                        if dist_b <= 1.5:
                            # Center cyan-tinted core jewel
                            base_r = 50; base_g = 220; base_b = 240
                    else:
                        base_r = 210.0 + n; base_g = 160.0 + n; base_b = 55.0 + n
                else:
                    # Burnished gold metallic belt
                    by = (y - 94) / 4.0
                    base_r = 195.0 - by * 30.0 + n
                    base_g = 150.0 - by * 25.0 + n
                    base_b = 50.0 - by * 15.0 + n
                    if y in (94, 98):
                        base_r -= 30; base_g -= 25; base_b -= 15
                    if y == 95:
                        base_r += 25; base_g += 25; base_b += 20

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # -------------------------------------------------------------
    # 6. Tiered Ceremonial Hip Skirt Plates / Tassets (Y: 99..106, X: 47..79)
    # -------------------------------------------------------------
    for y in range(99, 107):
        for x in range(47, 80):
            if nut_a(x, y) > 10 or ch_a(x, y) > 20:
                n = noise(x, y) * 6.0 + micro_grain(x, y)
                vy = (y - 99) / 7.0
                cx = abs(x - 63.5)

                # Segmented tassets:
                # Left plate X: 47..56, Center plate X: 58..69, Right plate X: 71..79
                is_crease = (x in (57, 70))
                is_border = (y == 106 or x in (47, 79))
                is_gold_edge = (y == 105 or is_border or (cx <= 1.2))

                if is_crease:
                    # Dark articulation seam
                    base_r = 28.0 + n; base_g = 24.0 + n; base_b = 48.0 + n
                elif is_gold_edge:
                    # Gilded bottom trim of coat-tails
                    base_r = 220.0 - vy * 40.0 + n
                    base_g = 170.0 - vy * 35.0 + n
                    base_b = 55.0 - vy * 15.0 + n
                    if y == 105:
                        base_r += 15; base_g += 20; base_b += 25
                else:
                    # Blue enamel tasset plates
                    base_r = 28.0 + vy * 10.0 + n
                    base_g = 48.0 + vy * 15.0 + n
                    base_b = 95.0 + vy * 22.0 + n

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # Corner studs on tassets:
    skirt_rivets = [(49, 104), (55, 104), (72, 104), (77, 104)]
    for rx, ry in skirt_rivets:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if abs(dx) + abs(dy) <= 1:
                    pos = (rx + dx, ry + dy)
                    n = micro_grain(pos[0], pos[1])
                    pixels[pos] = (clamp(240.0 + n), clamp(190.0 + n), clamp(70.0 + n), 255)

    # -------------------------------------------------------------
    # 7. Deep Contour Outlines (#1F1A3A, Rule 16)
    # -------------------------------------------------------------
    raw_coords = set(pixels.keys())
    # Apply pixels to image
    for (x, y), col in pixels.items():
        # Soften border pixels adjacent to transparent
        has_trans_neighbor = any((x + dx, y + dy) not in raw_coords for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)])
        if has_trans_neighbor:
            # Blend slightly with outline color #1F1A3A for smooth mobile antialiasing
            r = int(col[0] * 0.45 + OUTLINE[0] * 0.55)
            g = int(col[1] * 0.45 + OUTLINE[1] * 0.55)
            b = int(col[2] * 0.45 + OUTLINE[2] * 0.55)
            costume.putpixel((x, y), (r, g, b, 255))
        else:
            costume.putpixel((x, y), col)

    out_path = f"{RABBIT_DIR}/costume/costume_royal_parade.png"
    costume.save(out_path)

    # Quality check
    opaque = [
        cast(tuple[int, int, int, int], costume.getpixel((x, y)))[:3]
        for y in range(h)
        for x in range(w)
        if cast(tuple[int, int, int, int], costume.getpixel((x, y)))[3] > 0
    ]
    u_colors = set(opaque)
    ratio = len(u_colors) / (len(opaque) / 100.0) if opaque else 0.0
    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {len(opaque)}")
    print(f"  Unique colors: {len(u_colors)}")
    print(f"  Colors/100px: {ratio:.2f}")

    return costume

if __name__ == "__main__":
    create_rabbit_costume_royal_parade()
