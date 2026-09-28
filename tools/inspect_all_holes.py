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
    total_holes = int(np.sum(holes))
    lbl, num = label(holes)
    clusters = []
    for i in range(1, num + 1):
        cys, cxs = np.where(lbl == i)
        clusters.append((len(cxs), (min(cys), max(cys)), (min(cxs), max(cxs))))
    clusters.sort(key=lambda x: x[0], reverse=True)
    print(f"Pose {p:10s}: total={total_holes:4d}, top clusters={clusters[:3]}")
