#!/usr/bin/env python3
from PIL import Image
import numpy as np

chassis = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/bison/chassis/chassis_bison_rusted_tinplate_default.png")
arr = np.array(chassis)

print("Chassis rows 110..127:")
for y in range(110, 128):
    xs = np.where(arr[y, :, 3] > 10)[0]
    if len(xs) > 0:
        print(f"y={y}: count={len(xs):2d} xs=[{xs.min():2d}..{xs.max():2d}] max_alpha={arr[y, :, 3].max():3d}")
    else:
        print(f"y={y}: count= 0")
