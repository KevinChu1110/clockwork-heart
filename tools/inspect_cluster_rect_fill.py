#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes, label

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/courser"
POSES = ['idle', 'attack', 'hit', 'recover', 'skill', 'telegraph']

for p in POSES:
    im = Image.open(f"{POSES_DIR}/{p}.png").convert("RGBA")
    arr = np.array(im)
    alpha = arr[:, :, 3]
    filled = binary_fill_holes(alpha > 10)
    holes = filled & (alpha <= 10)
    lbl, num = label(holes)
    print(f"\nPose {p:10s}:")
    for i in range(1, num + 1):
        cys, cxs = np.where(lbl == i)
        cnt = len(cxs)
        if cnt > 10:
            h = max(cys) - min(cys) + 1
            w = max(cxs) - min(cxs) + 1
            rect_fill = cnt / (w * h)
            print(f"  Cluster {i}: size={cnt}px, bbox=({min(cxs)}, {min(cys)}, {max(cxs)}, {max(cys)}), w={w}, h={h}, rect_fill={rect_fill:.3f}")
