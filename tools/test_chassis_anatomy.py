#!/usr/bin/env python3
from PIL import Image
import numpy as np

chassis = Image.open("game/assets/sprites/player/paperdoll/swan/chassis/chassis_swan_silver_enamel_default.png").convert("RGBA")
arr = np.array(chassis)

print("Chassis alpha > 20 bbox:")
ys, xs = np.where(arr[:, :, 3] > 20)
print(f"y: min={ys.min()}, max={ys.max()}")
print(f"x: min={xs.min()}, max={xs.max()}")

for y in range(85, 120, 3):
    row_xs = np.where(arr[y, :, 3] > 20)[0]
    if len(row_xs) > 0:
        print(f"y={y:3d}: x min={row_xs.min():2d}, max={row_xs.max():2d}, count={len(row_xs):2d}")
