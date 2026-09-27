#!/usr/bin/env python3
import numpy as np
from PIL import Image

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/chassis/chassis_otter_abyssal_cyan_default.png"
im = Image.open(p).convert("RGBA")
arr = np.array(im)
alpha = arr[:, :, 3]
ys, xs = np.where(alpha > 20)
print(f"Chassis bounds: y in [{ys.min()}, {ys.max()}], x in [{xs.min()}, {xs.max()}]")

for y in range(70, 126, 4):
    row_xs = np.where(alpha[y, :] > 20)[0]
    if len(row_xs) > 0:
        print(f"y={y:3d}: count={len(row_xs):2d}, x_min={row_xs.min():2d}, x_max={row_xs.max():2d}")

# Check leg split at y=95..120
print("\nChecking leg split around y=105:")
row_105 = np.where(alpha[105, :] > 20)[0]
print("y=105 xs:", row_105)
row_110 = np.where(alpha[110, :] > 20)[0]
print("y=110 xs:", row_110)
row_115 = np.where(alpha[115, :] > 20)[0]
print("y=115 xs:", row_115)
