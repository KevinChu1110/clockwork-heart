#!/usr/bin/env python3
from PIL import Image
import numpy as np

chassis_128 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/sailfish/chassis/chassis_sailfish_abyssal_titanium_default.png")
arr = np.array(chassis_128)
print("Chassis bbox:", chassis_128.getbbox())

for y in range(45, 124, 5):
    xs = np.where(arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f"y={y:3d}: x range [{xs[0]:2d} .. {xs[-1]:2d}], count={len(xs):2d}")
