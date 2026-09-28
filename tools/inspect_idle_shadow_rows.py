#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/bison/idle.png")
arr = np.array(im)
for y in range(114, 124):
    xs = np.where(arr[y, :, 3] > 20)[0]
    print(f"y={y}: count={len(xs):2d} min_x={xs.min():2d} max_x={xs.max():2d}")
