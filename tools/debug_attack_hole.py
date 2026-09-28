#!/usr/bin/env python3
import numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes, label

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/kite/attack.png")
arr = np.array(im)
alpha = arr[:, :, 3]
bin_solid = alpha > 30
filled = binary_fill_holes(bin_solid)
holes = filled & (~bin_solid)
labeled, num_features = label(holes)

print("Number of hole features:", num_features)
for f_idx in range(1, num_features + 1):
    h_coords = np.argwhere(labeled == f_idx)
    min_y, min_x = np.min(h_coords, axis=0)
    max_y, max_x = np.max(h_coords, axis=0)
    rect_area = (max_y - min_y + 1) * (max_x - min_x + 1)
    fill_ratio = len(h_coords) / float(rect_area)
    print(f"Hole {f_idx}: len={len(h_coords)}, bbox=({min_x}, {min_y}, {max_x}, {max_y}), area={rect_area}, fill_ratio={fill_ratio:.3f}")
