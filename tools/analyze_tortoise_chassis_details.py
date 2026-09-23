#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

chassis = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise/chassis/paint_tortoise_jade.png").convert("RGBA")
arr = np.array(chassis)

print("Chassis bbox:", chassis.getbbox())

# Let's inspect rows from 85 to 122
for y in range(85, 122, 3):
    row = arr[y]
    xs = np.where(row[:, 3] > 10)[0]
    if len(xs) > 0:
        # Check colors
        rgbs = row[xs, :3]
        print(f"y={y:3d}: x=[{xs.min():2d}..{xs.max():2d}] (count={len(xs):2d}) sample_rgb={rgbs[0]}..{rgbs[-1]}")
