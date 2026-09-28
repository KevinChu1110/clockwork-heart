#!/usr/bin/env python3
from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes, label

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/courser"
comp = Image.open(f"{BASE_DIR}/proof_paperdoll_courser_composite.png").convert("RGBA")
arr = np.array(comp)
alpha = arr[:, :, 3]

filled = binary_fill_holes(alpha > 10)
holes = filled & (alpha <= 10)
total_holes = int(np.sum(holes))
lbl, num = label(holes)
print("Baseline composite total internal holes:", total_holes, "num clusters:", num)
for i in range(1, num + 1):
    cys, cxs = np.where(lbl == i)
    print(f"Cluster {i}: size={len(cxs)}, y_range={min(cys)}..{max(cys)}, x_range={min(cxs)}..{max(cxs)}")
