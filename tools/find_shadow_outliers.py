#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/kite"
POSES = ['idle', 'attack', 'hit', 'recover', 'skill', 'telegraph']

# Baseline shadow mask (y in 118..127)
shadow_im = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/kite_idle.png").convert("RGBA")
sh_arr = np.array(shadow_im)
shadow_mask = np.zeros((128, 128), dtype=bool)
for y in range(118, 128):
    for x in range(128):
        if sh_arr[y, x, 3] > 20:
            shadow_mask[y, x] = True

for p in POSES:
    im = Image.open(os.path.join(POSES_DIR, f"{p}.png")).convert("RGBA")
    arr = np.array(im)
    outliers = []
    for y in range(110, 128):
        for x in range(128):
            a = arr[y, x, 3]
            if a > 0:
                if y >= 118 and not shadow_mask[y, x]:
                    outliers.append((x, y, arr[y, x]))
                elif y < 118 and (x < 35 or x > 95):
                    # Check if body/weapon touches bottom right/left near baseline
                    outliers.append((x, y, arr[y, x]))
    print(f"{p:10s}: outliers count={len(outliers)}")
    if outliers:
        xs = [o[0] for o in outliers]
        ys = [o[1] for o in outliers]
        print(f"   x range=({min(xs)}..{max(xs)}), y range=({min(ys)}..{max(ys)})")
        for x, y, col in outliers[:5]:
            print(f"      sample ({x}, {y}): rgba={tuple(col)}")
