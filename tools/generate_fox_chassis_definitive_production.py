#!/usr/bin/env python3
"""
tools/generate_fox_chassis_definitive_production.py
Generates official 128x128 and 512x512 pure bare chassis for Fox:
1. paint_fox_orange (靈狐曜橙): Vibrant warm orange + cream enamel plates.
2. paint_ivory_stock (白瓷原色): Elegant ivory white high-gloss porcelain plates.
3. paint_emerald_glaze (翡翠螢光釉面): Luminescent emerald glaze plates + pale jade accents.
All variants feature:
- 100% zero cloth / zero coat / zero lining / zero buttons.
- Fully intact automaton joints, brass winding key, tail, limbs, cyan heart core.
- Perfectly aligned central torso axis and safe margin around feet.
- Both 128x128 and 512x512 PNGs.
"""

import os
import math
import colorsys
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
CHASSIS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/chassis"
BASE_IMG_PATH = "/opt/side/bravesoul-game/tools/fox_base_pure.png"

def make_orange_variant(base_rgba: Image.Image) -> Image.Image:
    arr = np.array(base_rgba)
    h, w, _ = arr.shape
    for y in range(h):
        for x in range(w):
            r, g, b, a = arr[y, x]
            if a < 20:
                continue
            if g > 130 and b > 140 and r < 120:
                continue
            if r > 160 and g > 110 and b < 65 and (r > 1.25 * g and g > 1.35 * b):
                continue
            if r < 50 and g < 50 and b < 50:
                continue
            if r < 75 and g < 60 and b < 55:
                continue
                
            rf, gf, bf = r/255.0, g/255.0, b/255.0
            h_val, s_val, v_val = colorsys.rgb_to_hsv(rf, gf, bf)
            
            if 0.04 <= h_val <= 0.16 and s_val > 0.35:
                target_h = 0.08
                target_s = min(0.95, s_val * 1.15)
                target_v = v_val
                nr, ng, nb = colorsys.hsv_to_rgb(target_h, target_s, target_v)
                arr[y, x] = [int(nr*255), int(ng*255), int(nb*255), a]
            elif s_val < 0.25 and v_val > 0.70:
                if x < 130 or x > 310 or y > 420:
                    target_h = 0.08
                    target_s = 0.65
                    target_v = min(1.0, v_val * 1.05)
                    nr, ng, nb = colorsys.hsv_to_rgb(target_h, target_s, target_v)
                    arr[y, x] = [int(nr*255), int(ng*255), int(nb*255), a]

    return Image.fromarray(arr)

def make_ivory_variant(base_rgba: Image.Image) -> Image.Image:
    arr = np.array(base_rgba)
    h, w, _ = arr.shape
    for y in range(h):
        for x in range(w):
            r, g, b, a = arr[y, x]
            if a < 20:
                continue
            if g > 130 and b > 140 and r < 120:
                continue
            if r > 160 and g > 110 and b < 65 and (r > 1.25 * g and g > 1.35 * b):
                continue
            if r < 50 and g < 50 and b < 50:
                continue
            if r < 75 and g < 60 and b < 55:
                continue
                
            rf, gf, bf = r/255.0, g/255.0, b/255.0
            h_val, s_val, v_val = colorsys.rgb_to_hsv(rf, gf, bf)
            
            if 0.04 <= h_val <= 0.18 and s_val > 0.25:
                target_h = 0.12
                target_s = 0.10
                target_v = min(1.0, v_val * 1.08)
                nr, ng, nb = colorsys.hsv_to_rgb(target_h, target_s, target_v)
                arr[y, x] = [int(nr*255), int(ng*255), int(nb*255), a]

    return Image.fromarray(arr)

def make_emerald_variant(base_rgba: Image.Image) -> Image.Image:
    arr = np.array(base_rgba)
    h, w, _ = arr.shape
    for y in range(h):
        for x in range(w):
            r, g, b, a = arr[y, x]
            if a < 20:
                continue
            if g > 130 and b > 140 and r < 120:
                arr[y, x] = [0, 240, 180, a]
                continue
            if r > 160 and g > 110 and b < 65 and (r > 1.25 * g and g > 1.35 * b):
                continue
            if r < 50 and g < 50 and b < 50:
                continue
            if r < 75 and g < 60 and b < 55:
                continue
                
            rf, gf, bf = r/255.0, g/255.0, b/255.0
            h_val, s_val, v_val = colorsys.rgb_to_hsv(rf, gf, bf)
            
            if 0.04 <= h_val <= 0.18 and s_val > 0.25:
                target_h = 0.42
                target_s = min(0.85, s_val * 1.2)
                target_v = v_val
                nr, ng, nb = colorsys.hsv_to_rgb(target_h, target_s, target_v)
                arr[y, x] = [int(nr*255), int(ng*255), int(nb*255), a]
            elif s_val < 0.25 and v_val > 0.65:
                target_h = 0.43
                target_s = 0.28
                target_v = min(1.0, v_val * 1.05)
                nr, ng, nb = colorsys.hsv_to_rgb(target_h, target_s, target_v)
                arr[y, x] = [int(nr*255), int(ng*255), int(nb*255), a]

    return Image.fromarray(arr)

def produce_all():
    os.makedirs(CHASSIS_DIR, exist_ok=True)
    base_raw = Image.open(BASE_IMG_PATH).convert("RGBA")
    
    arr_base = np.array(base_raw)
    cy, cx = np.where((arr_base[:, :, 0] < 120) & (arr_base[:, :, 1] > 140) & (arr_base[:, :, 2] > 140))
    core_cx = float(cx.mean()) # ~157
    core_cy = float(cy.mean()) # ~367

    variants = [
        ("paint_fox_orange", make_orange_variant(base_raw)),
        ("paint_ivory_stock", make_ivory_variant(base_raw)),
        ("paint_emerald_glaze", make_emerald_variant(base_raw)),
    ]
    
    # Scale down slightly so feet have safe bottom margin (height ~450px)
    scale_512 = 0.74
    bw, bh = base_raw.size
    target_w_512 = int(round(bw * scale_512))
    target_h_512 = int(round(bh * scale_512))
    
    # Position: core at X=256, Y=315 -> feet around Y=485 (safe 27px margin)
    offset_x_512 = int(round(256 - core_cx * scale_512))
    offset_y_512 = int(round(315 - core_cy * scale_512))
    
    scale_128 = scale_512 / 4.0
    target_w_128 = int(round(bw * scale_128))
    target_h_128 = int(round(bh * scale_128))
    offset_x_128 = int(round(64 - core_cx * scale_128))
    offset_y_128 = int(round(79 - core_cy * scale_128))
    
    for name, full_img in variants:
        # 128x128
        scaled_128 = full_img.resize((target_w_128, target_h_128), resample=Image.Resampling.LANCZOS)
        c128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        c128.paste(scaled_128, (offset_x_128, offset_y_128), scaled_128)
        p128 = f"{CHASSIS_DIR}/{name}.png"
        c128.save(p128, format="PNG")
        print(f"✓ Saved {name}.png (128x128)")
        
        # 512x512
        scaled_512 = full_img.resize((target_w_512, target_h_512), resample=Image.Resampling.LANCZOS)
        c512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        c512.paste(scaled_512, (offset_x_512, offset_y_512), scaled_512)
        p512 = f"{CHASSIS_DIR}/{name}_512.png"
        c512.save(p512, format="PNG")
        print(f"✓ Saved {name}_512.png (512x512)")

if __name__ == "__main__":
    produce_all()
