#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/tmp/python_composite_direct.png").convert("RGBA")
arr = np.array(im)

for y in range(300, 500):
    for x in range(180, 240):
        if arr[y, x, 3] < 100:
            print(f"Hole at ({x}, {y})")
            break
