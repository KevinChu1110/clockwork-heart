#!/usr/bin/env python3
from PIL import Image
import numpy as np

m = Image.open("/tmp/masterpiece_hero_512.png").convert("RGBA")
arr = np.array(m)

# 沿著戰錘木柄 (y: 280..380)，往右看木柄延伸到哪裡
print("Checking shaft end in masterpiece_hero_512.png:")
for y in range(300, 360, 5):
    xs = np.where(arr[y, :, 3] > 100)[0]
    print(f"y={y}: min_x={xs.min()}, max_x={xs.max()}")
