#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/tortoise_idle_x3.png")
arr = np.array(im)

for y in range(112, 128):
    xs = np.where(arr[y, :, 3] > 20)[0]
    print(f"y={y}: count={len(xs)}, xs={xs.min() if len(xs) else 0}..{xs.max() if len(xs) else 0}")
