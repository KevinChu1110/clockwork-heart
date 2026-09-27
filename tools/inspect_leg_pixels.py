#!/usr/bin/env python3
from PIL import Image
import numpy as np

ch = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/chassis/chassis_otter_abyssal_cyan_default.png")
arr = np.array(ch)
for y in range(108, 116):
    for x in range(68, 78):
        r, g, b, a = arr[y, x]
        if a > 0:
            print(f"y={y}, x={x}: rgba=({r}, {g}, {b}, {a})")
