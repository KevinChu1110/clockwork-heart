#!/usr/bin/env python3
import numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes, label

im = Image.open("game/assets/sprites/player/poses/lemur/attack.png").convert("RGBA")
arr = np.array(im)
alpha = arr[:, :, 3]
filled = binary_fill_holes(alpha > 10)
holes = filled & (alpha <= 10)
total_holes = int(np.sum(holes))

lbl, num = label(holes)
print(f"Total holes: {total_holes}, number of hole components: {num}")
for i in range(1, num + 1):
    cys, cxs = np.where(lbl == i)
    cnt = len(cxs)
    h = max(cys) - min(cys) + 1
    w = max(cxs) - min(cxs) + 1
    rect_fill = cnt / (w * h)
    print(f"Hole {i:2d}: count={cnt:4d} px, bbox=({min(cxs)}, {min(cys)}, {max(cxs)}, {max(cys)}), size={w}x{h}, rect_fill={rect_fill:.2f}")
