#!/usr/bin/env python3
"""
tools/clean_boar_floating_noise.py
1. Cleans floating noise pixels and selection dashed-line artifacts around head_unit and winding_key.
2. Enhances the chest energy core with seamless metallic bezel and natural lighting transition.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"

def clean_floating_pixels(im: Image.Image, min_size: int = 24) -> Image.Image:
    arr = np.array(im)
    alpha = arr[:, :, 3] > 10
    labeled, num_features = label(alpha)
    
    cleaned_arr = arr.copy()
    for i in range(1, num_features + 1):
        size = np.sum(labeled == i)
        if size < min_size:
            cleaned_arr[labeled == i] = [0, 0, 0, 0]
            
    return Image.fromarray(cleaned_arr, mode="RGBA")

# 1. 清理 4 款 head_unit 周圍的浮動雜點與選取虛線
print("--- 1. Cleaning Head Units Noise ---")
for f in os.listdir(f"{PARTS_DIR}/head_unit"):
    if f.endswith(".png"):
        p = f"{PARTS_DIR}/head_unit/{f}"
        im = Image.open(p).convert("RGBA")
        cleaned = clean_floating_pixels(im, min_size=32)
        cleaned.save(p)
        print(f"  ✓ Cleaned {f}")

# 2. 清理 winding_key 周圍的雜點
print("--- 2. Cleaning Winding Key Noise ---")
key_p = f"{PARTS_DIR}/winding_key/key_classic_brass.png"
key_im = Image.open(key_p).convert("RGBA")
cleaned_key = clean_floating_pixels(key_im, min_size=40)
cleaned_key.save(key_p)
print("  ✓ Cleaned key_classic_brass.png")

# 3. 完美重繪胸腹核心 (無生硬圓形補丁，具備立體金屬鑲邊與環境光)
print("--- 3. Refining Seamless Core in Bodies ---")
for p_name in ["paint_brass_gold", "paint_ivory_stock", "paint_molten_crimson"]:
    body_p = f"{PARTS_DIR}/body/{p_name}.png"
    body = Image.open(body_p).convert("RGBA")
    
    draw = ImageDraw.Draw(body)
    cx, cy = 230, 306
    is_crimson = (p_name == "paint_molten_crimson")
    
    col_bezel = (185, 140, 45, 255) if not is_crimson else (175, 75, 35, 255)
    col_shadow = (25, 20, 18, 255)
    
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=col_shadow, width=3)
    draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=col_bezel, width=2)
    for rad, deg in [(23, 0), (23, 90), (23, 180), (23, 270)]:
        rx = cx + int(rad * math.cos(math.radians(deg)))
        ry = cy + int(rad * math.sin(math.radians(deg)))
        draw.ellipse([rx-3, ry-3, rx+3, ry+3], fill=(245, 205, 55, 255), outline=col_shadow, width=1)
        
    body.save(body_p)
    print(f"  ✓ Refined core bezel for {p_name}")

print("🎉 Noise cleaning and core refinement complete!")
