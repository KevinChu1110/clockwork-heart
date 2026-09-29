#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/hippo"
chassis = Image.open(f"{PD_DIR}/chassis/chassis_hippo_thick_cast_brass_default.png").convert("RGBA")
arr = np.array(chassis)

print("Chassis bbox:", chassis.getbbox())
for y in range(40, 128, 5):
    row_px = np.sum(arr[y, :, 3] > 10)
    xs = np.where(arr[y, :, 3] > 10)[0]
    min_x = xs.min() if len(xs) > 0 else 0
    max_x = xs.max() if len(xs) > 0 else 0
    print(f"y={y:3d}: count={row_px:2d}, x_span=[{min_x:2d}, {max_x:2d}]")
