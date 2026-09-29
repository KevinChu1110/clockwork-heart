#!/usr/bin/env python3
from PIL import Image
import numpy as np

chassis_im = Image.open("game/assets/sprites/player/paperdoll/takin/chassis/chassis_takin_bronze_cast_default.png").convert("RGBA")
arr = np.array(chassis_im)
for y in range(100, 128):
    row_xs = np.where(arr[y, :, 3] > 50)[0]
    if len(row_xs) > 0:
        print(f"chassis y={y:3d}: x in [{min(row_xs):3d}..{max(row_xs):3d}], count={len(row_xs):2d}")
