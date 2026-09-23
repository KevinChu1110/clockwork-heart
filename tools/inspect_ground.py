#!/usr/bin/env python3
import numpy as np
from PIL import Image

im = Image.open("/tmp/xuanji_tortoise_concept.png").convert("RGB")
arr = np.array(im)
# Inspect bottom area around character feet: y in [650, 750], x in [400, 800]
crop = arr[650:750, 400:800]
print("Shape:", crop.shape)

# Find unique colors near bottom border y=740..748
bottom_samples = arr[730:748, 400:800]
print("Average RGB at ground base:", np.mean(bottom_samples, axis=(0, 1)))

# Let's inspect rows from 680 to 748
for y in range(680, 748, 10):
    row = arr[y, 500:700]
    print(f"Row {y} mean RGB: {np.mean(row, axis=0)}, min RGB: {np.min(row, axis=0)}")
