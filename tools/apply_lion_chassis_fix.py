#!/usr/bin/env python3
"""
tools/apply_lion_chassis_fix.py
Removes built-in weapon from Lion chassis (paint_brass_gold, paint_ivory_stock, paint_midnight_navy)
following 0-ART9 and ART_DIRECTION.md 2.2.
Sculpts clean clenched gauntlet fist and clears background negative space bleed.
"""

import os
import colorsys
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
LION_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion"

def build_cleaned_brass_gold() -> Image.Image:
    src_p = f"{LION_DIR}/chassis/paint_brass_gold.png"
    gold = Image.open(src_p).convert("RGBA")
    cleaned = gold.copy()

    # 1. Clear above hand: y=55..72, x=30..43 (spear blade & collar)
    for y in range(55, 73):
        for x in range(30, 44):
            cleaned.putpixel((x, y), (0, 0, 0, 0))

    # 2. Clear hand area to sculpt clean fist: y=72..86, x=30..42
    for y in range(72, 87):
        for x in range(30, 42):
            cleaned.putpixel((x, y), (0, 0, 0, 0))

    # 3. Below hand to base: y=87..116, x=30..44 (spear shaft)
    for y in range(87, 117):
        for x in range(30, 45):
            cleaned.putpixel((x, y), (0, 0, 0, 0))

    # Clear stray floating pixel at y=113, x=44
    cleaned.putpixel((44, 113), (0, 0, 0, 0))

    # 4. Clear white bleed between body and arm (negative space):
    for y in range(85, 116):
        for x in range(39, 56):
            p = cleaned.getpixel((x, y))
            if isinstance(p, tuple) and len(p) == 4 and p[3] > 0 and p[0] > 200 and p[1] > 200 and p[2] > 180:
                cleaned.putpixel((x, y), (0, 0, 0, 0))

    # Clear white bleed between legs (negative space):
    for y in range(103, 115):
        for x in range(64, 73):
            p = cleaned.getpixel((x, y))
            if isinstance(p, tuple) and len(p) == 4 and p[3] > 0 and p[0] > 200 and p[1] > 200 and p[2] > 180:
                cleaned.putpixel((x, y), (0, 0, 0, 0))

    # Clear winding key cutout hole:
    for y in (61, 62):
        for x in (94, 95):
            cleaned.putpixel((x, y), (0, 0, 0, 0))

    # 5. Hand / Fist sculpting (articulated brass/gold clenched gauntlet):
    hand_pixels = {
        73: [(39, (45, 30, 22)), (40, (145, 110, 65)), (41, (175, 135, 80))],
        74: [(37, (45, 30, 22)), (38, (175, 135, 80)), (39, (225, 185, 110)), (40, (205, 165, 95)), (41, (145, 110, 65))],
        75: [(36, (45, 30, 22)), (37, (235, 205, 130)), (38, (255, 225, 150)), (39, (225, 185, 110)), (40, (175, 135, 80)), (41, (120, 85, 55))],
        76: [(36, (45, 30, 22)), (37, (205, 165, 95)), (38, (235, 205, 130)), (39, (195, 155, 90)), (40, (145, 110, 65)), (41, (105, 75, 48))],
        77: [(37, (45, 30, 22)), (38, (125, 85, 50)), (39, (155, 115, 70)), (40, (145, 105, 65)), (41, (115, 80, 50))],
        78: [(36, (45, 30, 22)), (37, (225, 190, 120)), (38, (245, 215, 140)), (39, (205, 165, 95)), (40, (155, 115, 70)), (41, (120, 85, 55))],
        79: [(36, (45, 30, 22)), (37, (205, 165, 95)), (38, (225, 190, 120)), (39, (185, 145, 85)), (40, (145, 105, 65)), (41, (110, 75, 48))],
        80: [(37, (45, 30, 22)), (38, (135, 95, 55)), (39, (165, 125, 75)), (40, (140, 100, 60)), (41, (105, 70, 45))],
        81: [(36, (45, 30, 22)), (37, (205, 165, 95)), (38, (225, 185, 110)), (39, (175, 135, 80)), (40, (135, 95, 55)), (41, (95, 65, 40))],
        82: [(36, (45, 30, 22)), (37, (175, 135, 80)), (38, (195, 155, 90)), (39, (155, 115, 70)), (40, (120, 80, 50)), (41, (85, 55, 35))],
        83: [(37, (45, 30, 22)), (38, (145, 105, 65)), (39, (165, 125, 75)), (40, (125, 85, 50)), (41, (75, 50, 32))],
        84: [(37, (45, 30, 22)), (38, (115, 75, 45)), (39, (135, 95, 60)), (40, (105, 70, 42)), (41, (65, 40, 26))],
        85: [(38, (45, 30, 22)), (39, (45, 30, 22)), (40, (45, 30, 22)), (41, (45, 30, 22))]
    }
    for y, row in hand_pixels.items():
        for x, c in row:
            cleaned.putpixel((x, y), (c[0], c[1], c[2], 255))

    # 6. Symmetrical ground shadow:
    for y in range(117, 126):
        for x in range(0, 48):
            cleaned.putpixel((x, y), (0, 0, 0, 0))

    center_x = 68
    for y in range(117, 126):
        right_xs = []
        for x in range(center_x, 128):
            p = gold.getpixel((x, y))
            if isinstance(p, tuple) and len(p) == 4 and p[3] > 0:
                right_xs.append(x)
        if right_xs:
            max_r = max(right_xs)
            radius = max_r - center_x
            for dx in range(1, radius + 1):
                rx = center_x + dx
                lx = center_x - dx
                if lx < 48:
                    rp = gold.getpixel((rx, y))
                    if isinstance(rp, tuple) and len(rp) == 4:
                        cleaned.putpixel((lx, y), rp)

    return cleaned

def make_ivory_chassis(base_img: Image.Image) -> Image.Image:
    w, h = base_img.size
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            p = base_img.getpixel((x, y))
            if isinstance(p, tuple) and len(p) == 4:
                r, g, b, a = p
                if a < 10: continue
                lum = int(0.299 * r + 0.587 * g + 0.114 * b)
                if lum < 50:
                    out.putpixel((x, y), (30, 24, 45, a))
                elif lum < 90:
                    out.putpixel((x, y), (int(r*0.7 + 90*0.3), int(g*0.7 + 75*0.3), int(b*0.7 + 60*0.3), a))
                else:
                    f = max(0.0, min(1.0, (lum - 90) / 165.0))
                    out.putpixel((x, y), (int(215 + f*38), int(208 + f*42), int(195 + f*48), a))
    return out

def is_navy_negative_space(x: int, y: int, r: int, g: int, b: int) -> bool:
    if y in (61, 62) and x in (94, 95):
        return True
    if 85 <= y <= 115 and 39 <= x <= 55 and (r > 230 and g > 220 and b > 200):
        return True
    if 103 <= y <= 114 and 64 <= x <= 72 and (r > 230 and g > 220 and b > 200):
        return True
    return False

def make_navy_chassis(gold: Image.Image) -> Image.Image:
    w, h = gold.size
    navy = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    opaque_pixels = []

    for y in range(h):
        for x in range(w):
            p = gold.getpixel((x, y))
            if not (isinstance(p, tuple) and len(p) == 4):
                continue
            r, g, b, a = p
            if a == 0:
                continue
            if is_navy_negative_space(x, y, r, g, b):
                continue

            if y >= 116 and (r < 60 and g < 60 and b < 80):
                navy.putpixel((x, y), (31, 26, 58, a))
                opaque_pixels.append((31, 26, 58))
                continue

            rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
            h_val, s_val, v_val = colorsys.rgb_to_hsv(rf, gf, bf)
            h_offset = (h_val - 0.12) * 0.15

            if v_val < 0.25:
                target_h = 0.68 + h_offset
                target_s = min(0.65, max(0.20, s_val * 0.90 + 0.15))
            elif v_val < 0.75:
                target_h = 0.61 + h_offset
                target_s = min(0.75, max(0.35, s_val * 1.05 + 0.10))
            else:
                target_h = 0.57 + h_offset
                target_s = min(0.55, max(0.25, s_val * 0.85 + 0.05))

            nr, ng, nb = colorsys.hsv_to_rgb(target_h % 1.0, target_s, v_val)
            ir = int(max(0, min(255, round(nr * 255))))
            ig = int(max(0, min(255, round(ng * 255))))
            ib = int(max(0, min(255, round(nb * 255))))

            navy.putpixel((x, y), (ir, ig, ib, a))
            opaque_pixels.append((ir, ig, ib))

    return navy

def calc_semi(im: Image.Image) -> float:
    solid, semi = 0, 0
    for y in range(im.height):
        for x in range(im.width):
            p = im.getpixel((x, y))
            if isinstance(p, tuple) and len(p) == 4:
                a = p[3]
                if a == 255: solid += 1
                elif a > 0: semi += 1
    tot = solid + semi
    return (semi / tot * 100) if tot > 0 else 0.0

def main():
    print("=== APPLYING LION CHASSIS WEAPON REMOVAL (0-ART9) ===")
    gold_clean = build_cleaned_brass_gold()
    ivory_clean = make_ivory_chassis(gold_clean)
    navy_clean = make_navy_chassis(gold_clean)

    p_gold = f"{LION_DIR}/chassis/paint_brass_gold.png"
    p_ivory = f"{LION_DIR}/chassis/paint_ivory_stock.png"
    p_navy = f"{LION_DIR}/chassis/paint_midnight_navy.png"

    gold_clean.save(p_gold)
    ivory_clean.save(p_ivory)
    navy_clean.save(p_navy)

    print(f"✓ Saved {p_gold}")
    print(f"  Semi%: {calc_semi(gold_clean):.2f}%")
    print(f"✓ Saved {p_ivory}")
    print(f"  Semi%: {calc_semi(ivory_clean):.2f}%")
    print(f"✓ Saved {p_navy}")
    print(f"  Semi%: {calc_semi(navy_clean):.2f}%")

if __name__ == "__main__":
    main()
