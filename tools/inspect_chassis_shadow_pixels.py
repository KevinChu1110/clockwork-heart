#!/usr/bin/env python3
from PIL import Image
import numpy as np

ch = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/chassis/chassis_otter_abyssal_cyan_default.png")
arr = np.array(ch)
for y in range(114, 126):
    xs = np.where(arr[y, :, 3] > 20)[0]
    for x in xs:
        r, g, b, a = arr[y, x]
        # print first few of each row
        if x in [xs[0], xs[len(xs)//2], xs[-1]]:
            print(f"y={y}, x={x}: rgba=({r}, {g}, {b}, {a})")
