#!/usr/bin/env python3
from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player"
idle = Image.open(f"{p}/party/raven_idle.png")
arr = np.array(idle)
for y in range(110, 128):
    count = int(np.sum(arr[y, :, 3] > 20))
    xs = [x for x in range(128) if arr[y, x, 3] > 20]
    x_range = f"{min(xs)}..{max(xs)}" if xs else "none"
    print(f"y={y}: count={count:2d}, x_range={x_range}")
