#!/usr/bin/env python3
"""
tools/audit_head_quality.py
Measures quality metrics for paperdoll head_unit assets:
1. Unique color count (色階數, alpha > 0)
2. Flat area ratio (平坦區佔比, gradient < 1.0 among opaque pixels)
3. File size (bytes)
4. Dominant color & color distance to chassis paint
"""

import os
import sys
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"

def measure_image_quality(path):
    if not os.path.exists(path):
        return None
    
    file_size = os.path.getsize(path)
    im = Image.open(path).convert("RGBA")
    arr = np.array(im)
    
    alpha = arr[:, :, 3]
    opaque_pixels = arr[alpha > 0]
    unique_colors = len(np.unique(opaque_pixels, axis=0))
    
    # Calculate gradient on RGB for pixels with alpha > 50
    mask_eval = alpha > 50
    if np.sum(mask_eval) == 0:
        flat_ratio = 0.0
    else:
        rgb = arr[:, :, :3].astype(float)
        gx = np.abs(np.diff(rgb, axis=1, prepend=rgb[:, :1, :]))
        gy = np.abs(np.diff(rgb, axis=0, prepend=rgb[:1, :, :]))
        grad = np.max(gx + gy, axis=2)
        flat_pixels = (grad < 1.0) & mask_eval
        flat_ratio = float(np.sum(flat_pixels)) / float(np.sum(mask_eval))
        
    return {
        "path": path,
        "size": file_size,
        "unique_colors": unique_colors,
        "flat_ratio": flat_ratio,
        "dimensions": im.size
    }

def get_dominant_color(path, is_chassis=False):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im)
    opaque = arr[arr[:, :, 3] > 200][:, :3]
    if is_chassis:
        filtered = opaque[np.max(opaque, axis=1) > 70]
    else:
        filtered = opaque[~((opaque[:, 0] < 50) & (opaque[:, 1] < 50) & (opaque[:, 2] < 50))]
    colors, counts = np.unique(filtered, axis=0, return_counts=True)
    top_color = tuple(int(x) for x in colors[np.argmax(counts)])
    return top_color

def color_distance(c1, c2):
    return float(np.linalg.norm(np.array(c1) - np.array(c2)))

def inspect_all():
    print("================================================================================")
    print("【資產品質稽核】熊族與企鵝族 head_unit 512 規格指標")
    print("================================================================================")
    print(f"{'族系/變體':20s} | {'檔案大小':10s} | {'色階數':8s} | {'平坦區比例':12s} | {'合格判定'}")
    print("-" * 75)
    
    targets = [
        ("Bear Stock (原圖)", f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear/head_unit/head_iron_bear_stock_512.png"),
        ("Bear Amber", f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear/head_unit/head_iron_bear_amber_512.png"),
        ("Bear Quarry", f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear/head_unit/head_iron_bear_quarry_512.png"),
        ("Bear Ivory", f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear/head_unit/head_iron_bear_ivory_512.png"),
        ("Penguin Navy", f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_stock_512.png"),
        ("Penguin Ivory", f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_ivory_512.png"),
        ("Penguin Polar", f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_polar_512.png"),
    ]
    
    for label, p in targets:
        if not os.path.exists(p):
            print(f"{label:20s} | MISSING")
            continue
        q = measure_image_quality(p)
        is_pass = (q["unique_colors"] >= 10000) and (q["flat_ratio"] < 0.10)
        status = "✅ PASS" if is_pass else "❌ FAIL"
        print(f"{label:20s} | {q['size']:7d} B | {q['unique_colors']:6d} | {q['flat_ratio']*100:6.2f}%      | {status}")
    print("-" * 75)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "all":
        target = sys.argv[1]
        res = measure_image_quality(target)
        if res:
            print(f"File: {res['path']}")
            print(f"Dimensions: {res['dimensions']}")
            print(f"Size: {res['size']} bytes")
            print(f"Unique colors (色階): {res['unique_colors']}")
            print(f"Flat ratio (平坦區): {res['flat_ratio']:.4f} ({res['flat_ratio']*100:.2f}%)")
        else:
            print("File not found.")
    else:
        inspect_all()
