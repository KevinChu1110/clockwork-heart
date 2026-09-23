#!/usr/bin/env python3
from PIL import Image
import numpy as np

chassis_512 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise/chassis/paint_tortoise_jade_512.png").convert("RGBA")
arr = np.array(chassis_512)

for y in range(300, 480, 20):
    xs = np.where(arr[y, :, 3] > 10)[0]
    print(f"y={y}: count={len(xs)}, xs={xs.min() if len(xs) else 0}..{xs.max() if len(xs) else 0}")
