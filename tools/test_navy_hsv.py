#!/usr/bin/env python3
from typing import cast
import colorsys
from PIL import Image

gold = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png").convert("RGBA")
w, h = gold.size

# Check negative space coordinates
# 1. Winding key hole: X=94..95, Y=61..62
# 2. Lance gap: Y=85..115, X=39..55 (where it was off-white background fill)
# 3. Between legs: Y=103..114, X=64..72 (where it was off-white background fill)

def is_negative_space(x: int, y: int, r: int, g: int, b: int) -> bool:
    if y in (61, 62) and x in (94, 95):
        return True
    if 85 <= y <= 115 and 39 <= x <= 55 and (r > 230 and g > 220 and b > 200):
        return True
    if 103 <= y <= 114 and 64 <= x <= 72 and (r > 230 and g > 220 and b > 200):
        return True
    return False

# Test continuous HSV mapping
navy_pixels = []
new_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

for y in range(h):
    for x in range(w):
        r, g, b, a = cast(tuple[int, int, int, int], gold.getpixel((x, y)))
        if a == 0:
            continue
        if is_negative_space(x, y, r, g, b):
            continue
        
        # Soft ground shadow at bottom (y >= 116)
        if y >= 116 and (r < 60 and g < 60 and b < 80):
            new_img.putpixel((x, y), (31, 26, 58, a))
            navy_pixels.append((31, 26, 58))
            continue
            
        rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
        h_val, s_val, v_val = colorsys.rgb_to_hsv(rf, gf, bf)
        
        # Midnight navy: Deep saturated dark blue with cyan specular highlights
        # Target H: around 0.61 (220 deg - midnight blue)
        # For highlights (high V), shift slightly toward cyan (H ~ 0.56..0.58)
        # For shadows (low V), shift toward deep indigo/purple (#1F1A3A, H ~ 0.68..0.70)
        # Preserve V!
        
        # Smooth hue variation based on V and input H:
        # V ranges from ~0.1 to ~1.0
        # If dark (outline/crevice, v_val < 0.3): target indigo-navy H ~ 0.68
        # If mid (v_val 0.3..0.75): target midnight navy H ~ 0.60..0.62
        # If highlight (v_val > 0.75): target polished cyan-navy highlight H ~ 0.56..0.58
        
        # Continuous H function of v_val:
        if v_val < 0.3:
            t = v_val / 0.3
            new_h = 0.68 - t * 0.07 # 0.68 -> 0.61
            new_s = max(0.2, min(0.65, s_val * 0.9 + 0.15))
        elif v_val < 0.75:
            t = (v_val - 0.3) / 0.45
            new_h = 0.61 - t * 0.04 # 0.61 -> 0.57
            new_s = max(0.35, min(0.75, s_val * 1.0 + 0.1))
        else:
            t = min(1.0, (v_val - 0.75) / 0.25)
            new_h = 0.57 - t * 0.02 # 0.57 -> 0.55
            new_s = max(0.25, min(0.60, s_val * 0.85 + 0.05))
            
        # Subtle preservation of original subtle color nuances:
        # add tiny fraction of (h_val - 0.12) to new_h so micro-variations are preserved
        new_h = (new_h + (h_val - 0.12) * 0.05) % 1.0
        new_v = v_val
        
        nr, ng, nb = colorsys.hsv_to_rgb(new_h, new_s, new_v)
        ir, ig, ib = int(round(nr * 255)), int(round(ng * 255)), int(round(nb * 255))
        new_img.putpixel((x, y), (ir, ig, ib, a))
        navy_pixels.append((ir, ig, ib))

opaque_cnt = len(navy_pixels)
unique_cnt = len(set(navy_pixels))
ratio = unique_cnt / (opaque_cnt / 100.0)
print(f"Opaque pixels: {opaque_cnt}")
print(f"Unique colors: {unique_cnt}")
print(f"Colors/100px: {ratio:.2f}")
