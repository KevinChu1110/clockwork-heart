#!/usr/bin/env python3
from PIL import Image
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/courser"
comp = Image.open(f"{BASE_DIR}/proof_paperdoll_courser_composite.png").convert("RGBA")
arr = np.array(comp)

for y in range(112, 128):
    xs = np.where(arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f"y={y:3d}: count={len(xs):2d}, x_min={xs[0]:2d}, x_max={xs[-1]:2d}, alpha_mean={np.mean(arr[y, xs, 3]):.1f}")
    else:
        print(f"y={y:3d}: count= 0")
