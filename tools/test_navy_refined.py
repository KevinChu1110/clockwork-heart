#!/usr/bin/env python3
from typing import cast
import colorsys
from PIL import Image

gold = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png").convert("RGBA")
w, h = gold.size

pixels = []
new_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

def is_neg_space(x: int, y: int, r: int, g: int, b: int) -> bool:
    # Winding key hole
    if y in (61, 62) and x in (94, 95):
        return True
    # Lance and torso gap
    if 85 <= y <= 115 and 39 <= x <= 55 and (r > 230 and g > 220 and b > 200):
        return True
    # Between legs gap
    if 103 <= y <= 114 and 64 <= x <= 72 and (r > 230 and g > 220 and b > 200):
        return True
    return False

for y in range(h):
    for x in range(w):
        r, g, b, a = cast(tuple[int, int, int, int], gold.getpixel((x, y)))
        if a == 0:
            continue
        if is_neg_space(x, y, r, g, b):
            continue
        if y >= 116 and (r < 60 and g < 60 and b < 80):
            # Ground soft shadow
            new_img.putpixel((x, y), (31, 26, 58, a))
            pixels.append((31, 26, 58))
            continue

        rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
        h_val, s_val, v_val = colorsys.rgb_to_hsv(rf, gf, bf)

        # Shift hue to Midnight Navy (around 220 deg / 0.611)
        # Preserve relative hue variations:
        h_offset = (h_val - 0.12) * 0.15
        
        if v_val < 0.25:
            # Deep shadow / outline: indigo navy #1F1A3A direction
            target_h = 0.68 + h_offset
            target_s = min(0.65, max(0.20, s_val * 0.9 + 0.15))
        elif v_val < 0.75:
            # Body midnight navy enamel
            target_h = 0.61 + h_offset
            target_s = min(0.75, max(0.35, s_val * 1.05 + 0.10))
        else:
            # Polished specular highlight (cyan-tinted sheen)
            target_h = 0.57 + h_offset
            target_s = min(0.55, max(0.25, s_val * 0.85 + 0.05))

        nr, ng, nb = colorsys.hsv_to_rgb(target_h % 1.0, target_s, v_val)
        ir, ig, ib = int(round(nr * 255)), int(round(ng * 255)), int(round(nb * 255))
        new_img.putpixel((x, y), (ir, ig, ib, a))
        pixels.append((ir, ig, ib))

opaque_cnt = len(pixels)
unique_cnt = len(set(pixels))
ratio = unique_cnt / (opaque_cnt / 100.0)
print(f"Navy Test:")
print(f"  Opaque: {opaque_cnt}")
print(f"  Unique colors: {unique_cnt}")
print(f"  Colors/100px: {ratio:.2f}")
