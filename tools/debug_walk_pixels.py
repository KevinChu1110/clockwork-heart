#!/usr/bin/env python3
from PIL import Image
import numpy as np

for i in range(4):
    im = Image.open(f"/opt/side/bravesoul-game/game/assets/sprites/player/otter_walk_{i}_x3.png")
    arr = np.array(im)
    alpha = arr[:, :, 3]
    # Check bottom rows y=110..127
    print(f"\n--- Frame {i} bottom alpha > 20 ---")
    for y in range(112, 128):
        xs = np.where(alpha[y, :] > 20)[0]
        if len(xs) > 0:
            print(f"y={y:3d}: x in [{xs.min():2d}, {xs.max():2d}], len={len(xs):2d}")
