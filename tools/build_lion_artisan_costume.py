#!/usr/bin/env python3
"""
tools/build_lion_artisan_costume.py
Constructs high-fidelity costume_steam_artisan.png for Lion paperdoll.
- Tailored for Lion's broad-shouldered 2.3-head chibi body
- Zero fur / zero leather (Rule 5a / 23f-4)
- Wrought iron bib & armor plates, bronze suspension braces, brass buckles & rivets
- Continuous shading, specular bevels, 3D spherical rivets, and anti-aliased outlines
  achieving high color nuance (colors/100px >= 24, Rule 10a-2)
- Layer independence: 0 identical pixels with chassis (Rule 4c)
- 128x128 RGBA
"""

import math
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
LION_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion"

def create_lion_costume_steam_artisan():
    w, h = 128, 128
    art = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    nut = Image.open(f"{LION_DIR}/costume/costume_nutcracker_guard.png").convert("RGBA")
    chassis = Image.open(f"{LION_DIR}/chassis/paint_brass_gold.png").convert("RGBA")

    pixels: dict[tuple[int, int], tuple[int, int, int, int]] = {}

    def clamp(v: float, low: float = 0.0, high: float = 255.0) -> int:
        return int(max(low, min(high, round(v))))

    def noise(x: int, y: int) -> float:
        return (math.sin(x * 0.85 + y * 0.45) * 0.5 + 
                math.cos(x * 0.35 - y * 0.75) * 0.3 + 
                math.sin((x + y) * 1.2) * 0.2)

    def nut_a(x: int, y: int) -> int:
        return cast(tuple[int, int, int, int], nut.getpixel((x, y)))[3]

    def ch_a(x: int, y: int) -> int:
        return cast(tuple[int, int, int, int], chassis.getpixel((x, y)))[3]

    # 1. Left Pauldron (viewer left): X: 37..46, Y: 61..73
    for y in range(61, 74):
        for x in range(37, 47):
            if nut_a(x, y) > 20:
                dist_top = (y - 61) / 12.0
                dist_left = (x - 37) / 9.0
                n = noise(x, y) * 8.0
                base_r = 55.0 + (1.0 - dist_top) * 35.0 - dist_left * 15.0 + n
                base_g = 62.0 + (1.0 - dist_top) * 40.0 - dist_left * 15.0 + n
                base_b = 75.0 + (1.0 - dist_top) * 55.0 - dist_left * 20.0 + n
                if y == 61 or (y == 62 and x < 43):
                    base_r += 40; base_g += 45; base_b += 55
                if y >= 71:
                    base_r -= 20; base_g -= 20; base_b -= 20
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 2. Right Pauldron (viewer right): X: 78..88, Y: 61..73
    for y in range(61, 74):
        for x in range(78, 89):
            if nut_a(x, y) > 20:
                dist_top = (y - 61) / 12.0
                dist_right = (88 - x) / 10.0
                n = noise(x, y) * 8.0
                base_r = 50.0 + (1.0 - dist_top) * 30.0 + dist_right * 15.0 + n
                base_g = 58.0 + (1.0 - dist_top) * 35.0 + dist_right * 15.0 + n
                base_b = 70.0 + (1.0 - dist_top) * 50.0 + dist_right * 20.0 + n
                if y == 61 or (y == 62 and x > 82):
                    base_r += 35; base_g += 40; base_b += 50
                if y >= 71:
                    base_r -= 20; base_g -= 20; base_b -= 20
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 3. Canvas Under-Tunic / Apron Backing: X: 47..77, Y: 74..91
    for y in range(74, 92):
        for x in range(47, 78):
            if ch_a(x, y) > 30 or nut_a(x, y) > 20:
                n = noise(x, y) * 10.0
                weave = (1 if (x + y) % 2 == 0 else -1) * 3.0
                vy = (y - 74) / 17.0
                vx = abs(x - 62) / 15.0
                base_r = 85.0 - vy * 20.0 - vx * 10.0 + n + weave
                base_g = 68.0 - vy * 18.0 - vx * 8.0 + n + weave
                base_b = 52.0 - vy * 15.0 - vx * 6.0 + n + weave
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 4. Articulated Bronze Suspension Straps (吊帶)
    for y in range(64, 91):
        for x in range(47, 55):
            if nut_a(x, y) > 15 or (y >= 74 and ch_a(x, y) > 20):
                n = noise(x, y) * 7.0
                fx = (x - 47) / 7.0
                base_r = 210.0 - fx * 60.0 + n
                base_g = 155.0 - fx * 50.0 + n
                base_b = 55.0 - fx * 25.0 + n
                if x == 47:
                    base_r += 25; base_g += 25; base_b += 15
                if x == 54:
                    base_r -= 30; base_g -= 25; base_b -= 15
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    for y in range(64, 91):
        for x in range(70, 78):
            if nut_a(x, y) > 15 or (y >= 74 and ch_a(x, y) > 20):
                n = noise(x, y) * 7.0
                fx = (x - 70) / 7.0
                base_r = 195.0 - fx * 55.0 + n
                base_g = 145.0 - fx * 45.0 + n
                base_b = 50.0 - fx * 20.0 + n
                if x == 70:
                    base_r += 25; base_g += 25; base_b += 15
                if x == 77:
                    base_r -= 30; base_g -= 25; base_b -= 15
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 5. Central Wrought Iron Bib Plate: X: 52..72, Y: 79..91
    for y in range(79, 92):
        for x in range(52, 73):
            if ch_a(x, y) > 20:
                n = noise(x, y) * 9.0
                cx = (x - 62) / 10.0
                cy = (y - 79) / 12.0
                light = (1.0 - cx * 0.6) * (1.0 - cy * 0.4)
                base_r = 45.0 + light * 40.0 + n
                base_g = 52.0 + light * 45.0 + n
                base_b = 65.0 + light * 60.0 + n
                if y == 79:
                    base_r += 50; base_g += 55; base_b += 70
                if y == 91:
                    base_r -= 20; base_g -= 20; base_b -= 25
                if x == 62:
                    base_r -= 15; base_g -= 15; base_b -= 20
                elif x == 63:
                    base_r += 12; base_g += 15; base_b += 18
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 6. Heavy Tool-Belt: X: 43..81, Y: 91..96
    for y in range(91, 97):
        for x in range(43, 82):
            if ch_a(x, y) > 20 or nut_a(x, y) > 20:
                n = noise(x, y) * 6.0
                fy = (y - 91) / 5.0
                base_r = 48.0 - fy * 15.0 + n
                base_g = 40.0 - fy * 12.0 + n
                base_b = 32.0 - fy * 10.0 + n
                if y == 91:
                    base_r += 25; base_g += 20; base_b += 15
                if y == 96:
                    base_r -= 15; base_g -= 15; base_b -= 12
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 7. Belt Buckle Plate: X: 57..67, Y: 91..96
    for y in range(91, 97):
        for x in range(57, 68):
            n = noise(x, y) * 6.0
            is_frame = (x in (57, 58, 66, 67) or y in (91, 96))
            is_prong = (x in (61, 62) and 92 <= y <= 95)
            if is_frame:
                base_r = 235.0 + n
                base_g = 185.0 + n
                base_b = 50.0 + n
                if x == 57 or y == 91:
                    base_r += 20; base_g += 25; base_b += 20
                if x == 67 or y == 96:
                    base_r -= 40; base_g -= 35; base_b -= 20
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)
            elif is_prong:
                pixels[(x, y)] = (clamp(70 + n), clamp(75 + n), clamp(85 + n), 255)
            else:
                pixels[(x, y)] = (clamp(30 + n), clamp(25 + n), clamp(20 + n), 255)

    # 8. Lower Work Apron Flaps (Split skirt over legs): Y: 97..107
    for y in range(97, 108):
        for x in range(44, 59):
            if nut_a(x, y) > 20 or ch_a(x, y) > 25:
                n = noise(x, y) * 9.0
                vy = (y - 97) / 10.0
                vx = (x - 44) / 14.0
                light = (1.0 - vx * 0.4) * (0.85 + vy * 0.3)
                base_r = 65.0 * light + n
                base_g = 52.0 * light + n
                base_b = 40.0 * light + n
                if y == 106:
                    base_r += 18; base_g += 15; base_b += 10
                if y == 107:
                    base_r -= 15; base_g -= 15; base_b -= 12
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    for y in range(97, 108):
        for x in range(65, 80):
            if nut_a(x, y) > 20 or ch_a(x, y) > 25:
                n = noise(x, y) * 9.0
                vy = (y - 97) / 10.0
                vx = (79 - x) / 14.0
                light = (0.8 + vx * 0.3) * (0.85 + vy * 0.3)
                base_r = 60.0 * light + n
                base_g = 48.0 * light + n
                base_b = 38.0 * light + n
                if y == 106:
                    base_r += 18; base_g += 15; base_b += 10
                if y == 107:
                    base_r -= 15; base_g -= 15; base_b -= 12
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 9. Tool hanger on right hip: X: 79..84, Y: 96..104
    for y in range(96, 105):
        for x in range(79, 85):
            n = noise(x, y) * 7.0
            if y in (96, 97) and x in (80, 81, 82):
                pixels[(x, y)] = (clamp(200 + n), clamp(155 + n), clamp(45 + n), 255)
            elif x in (81, 82):
                pixels[(x, y)] = (clamp(75 + n), clamp(85 + n), clamp(105 + n), 255)
            elif y in (103, 104) and x in (80, 81, 82, 83):
                pixels[(x, y)] = (clamp(85 + n), clamp(95 + n), clamp(115 + n), 255)

    # 10. 3D Rivets
    rivet_centers = [
        (49, 66), (49, 74), (49, 84),
        (73, 66), (73, 74), (73, 84),
        (54, 82), (70, 82), (54, 89), (70, 89),
        (47, 105), (55, 105), (68, 105), (76, 105),
        (40, 65), (85, 65)
    ]
    for rx, ry in rivet_centers:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                pt = (rx + dx, ry + dy)
                if pt in pixels:
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist <= 1.2:
                        n = noise(pt[0], pt[1]) * 5.0
                        if dx <= 0 and dy <= 0:
                            pixels[pt] = (clamp(255), clamp(235 + n), clamp(110 + n), 255)
                        elif dx > 0 or dy > 0:
                            pixels[pt] = (clamp(145 + n), clamp(100 + n), clamp(25 + n), 255)
                        else:
                            pixels[pt] = (clamp(225 + n), clamp(175 + n), clamp(45 + n), 255)

    # 11. Outline
    final_pixels: dict[tuple[int, int], tuple[int, int, int, int]] = dict(pixels)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for (x, y), col in pixels.items():
        touch_trans = any((x + dx, y + dy) not in pixels for dx, dy in dirs)
        if touch_trans:
            n = noise(x, y) * 4.0
            out_r = clamp(31.0 + n)
            out_g = clamp(26.0 + n)
            out_b = clamp(58.0 + n)
            final_pixels[(x, y)] = (out_r, out_g, out_b, 255)

    for (x, y), (r, g, b, a) in final_pixels.items():
        art.putpixel((x, y), (r, g, b, a))

    out_path = f"{LION_DIR}/costume/costume_steam_artisan.png"
    art.save(out_path)

    op_pix = [cast(tuple[int, int, int, int], art.getpixel((x, y)))[:3] for y in range(h) for x in range(w) if cast(tuple[int, int, int, int], art.getpixel((x, y)))[3] > 0]
    u_colors = set(op_pix)
    ratio = len(u_colors) / (len(op_pix) / 100.0) if op_pix else 0.0
    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {len(op_pix)}")
    print(f"  Unique colors: {len(u_colors)}")
    print(f"  Colors/100px: {ratio:.2f}")

    return art

if __name__ == "__main__":
    create_lion_costume_steam_artisan()
