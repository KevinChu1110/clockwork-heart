#!/usr/bin/env python3
from PIL import Image
import numpy as np

k = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/winding_key/key_classic_brass.png").convert("RGBA")
arr = np.array(k)

# 搜尋任何 alpha > 0 且在右上角 (x > 60, y < 40) 的非金黃色像素
for y in range(40):
    for x in range(60, len(arr[0])):
        r, g, b, a = arr[y, x]
        if a > 0:
            if not (r > g and g > b and b < 100): # 不是黃銅金屬色
                print(f"Artifact in key at ({x}, {y}): RGBA={[int(c) for c in arr[y, x]]}")
