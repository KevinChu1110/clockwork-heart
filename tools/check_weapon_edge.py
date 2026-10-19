#!/usr/bin/env python3
from PIL import Image
import numpy as np

w = Image.open("/tmp/zoom_layer_weapon.png").convert("RGBA")
arr = np.array(w)

# 檢查 x=88, 89, 90 的邊緣像素
for y in range(50, 120):
    for x in range(85, 92):
        if x < arr.shape[1] and arr[y, x, 3] > 0:
            print(f"weapon pixel at x={x}, y={y}: RGBA={[int(c) for c in arr[y, x]]}")
            break
