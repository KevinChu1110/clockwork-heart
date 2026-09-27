#!/usr/bin/env python3
from PIL import Image
import numpy as np

f0 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/otter_walk_0_x3.png")
f1 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/otter_walk_1_x3.png")

a0 = np.array(f0)
a1 = np.array(f1)

# Check rows 110 to 127
for y in range(110, 128):
    diff = np.where(np.any(a0[y] != a1[y], axis=1))[0]
    if len(diff) > 0:
        print(f"y={y}: diff at xs {diff}")
        print(f"  f0 alpha: {a0[y, diff, 3]}")
        print(f"  f1 alpha: {a1[y, diff, 3]}")
