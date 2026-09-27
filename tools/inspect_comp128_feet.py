#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/proof_paperdoll_otter_composite.png")
arr = np.array(im)
alpha = arr[:, :, 3]

for y in range(112, 128):
    xs = np.where(alpha[y, :] > 20)[0]
    if len(xs) > 0:
        # Check colors
        rgb = arr[y, xs, :3]
        mean_rgb = np.mean(rgb, axis=0).astype(int)
        print(f"y={y:3d}: x in [{xs.min():2d}, {xs.max():2d}], len={len(xs):2d}, mean_rgb={mean_rgb}")
