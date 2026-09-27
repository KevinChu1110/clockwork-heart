#!/usr/bin/env python3
from PIL import Image
import numpy as np

f0 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/otter_walk_0_x3.png")
f1 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/otter_walk_1_x3.png")

a0 = np.array(f0)
a1 = np.array(f1)

# Look at rows 110 to 118 where alpha is between 1 and 250
print("--- Frame 1 semi-transparent pixels at y=110..118 ---")
for y in range(110, 118):
    semi = np.where((a1[y, :, 3] > 0) & (a1[y, :, 3] < 255))[0]
    for x in semi:
        r, g, b, a = a1[y, x]
        if r > 100 or g > 100 or b > 100:
            print(f"y={y}, x={x}: rgba=({r}, {g}, {b}, {a})")
