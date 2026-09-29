#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
chassis = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/takin/chassis/chassis_takin_bronze_cast_default.png").convert("RGBA")
arr = np.array(chassis)

print("Chassis bbox:", chassis.getbbox())
for y in range(80, 124, 2):
    xs = np.where(arr[y, :, 3] > 30)[0]
    if len(xs) > 0:
        print(f"y={y:3d}: x in [{min(xs):2d}..{max(xs):2d}], count={len(xs):2d}, xs={xs}")
