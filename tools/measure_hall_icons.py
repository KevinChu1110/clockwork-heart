#!/usr/bin/env python3
"""
tools/measure_hall_icons.py
Measure color richness, outline pixels (#1F1A3A), and transparency for hall icons.
"""
import numpy as np
from PIL import Image

TARGETS = [
    "icon_hall_forge.png",
    "icon_hall_gem.png",
    "icon_hall_arena.png",
    "icon_hall_quest.png"
]

OUTLINE_RGB = np.array([31, 26, 58])

print("=== HALL ICONS METRICS ===")
for name in TARGETS:
    path = f"/opt/side/bravesoul-game/game/assets/icons/hud/{name}"
    im = Image.open(path)
    arr = np.array(im)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    
    opaque_mask = alpha > 128
    opaque_pixels = arr[opaque_mask]
    
    # Unique colors
    # Pack RGB into single uint32 for fast unique counting
    packed = (opaque_pixels[:, 0].astype(np.uint32) << 16) | \
             (opaque_pixels[:, 1].astype(np.uint32) << 8) | \
             (opaque_pixels[:, 2].astype(np.uint32))
    unique_colors = len(np.unique(packed))
    total_opaque = len(opaque_pixels)
    colors_per_100px = (unique_colors / total_opaque) * 100.0
    
    # Count outline pixels (#1F1A3A) with slight color distance <= 15
    color_diff = np.abs(rgb[opaque_mask] - OUTLINE_RGB)
    outline_matches = np.all(color_diff <= 15, axis=1).sum()
    
    trans_count = (alpha == 0).sum()
    trans_ratio = trans_count / alpha.size
    
    print(f"{name}:")
    print(f"  Size: {im.size}, Mode: {im.mode}")
    print(f"  Opaque pixels: {total_opaque}, Transparent: {trans_count} ({trans_ratio*100:.1f}%)")
    print(f"  Unique colors: {unique_colors} ({colors_per_100px:.1f} colours per 100px, threshold > 10)")
    print(f"  Outline (#1F1A3A) pixels: {outline_matches}")
