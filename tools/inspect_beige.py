#!/usr/bin/env python3
import numpy as np
from PIL import Image

im = Image.open("/tmp/test_chassis_crafted_magenta.png").convert("RGBA")
arr = np.array(im)
# Find pixels where magenta is not present, i.e. not (255, 0, 255)
mask = ~((arr[:, :, 0] == 255) & (arr[:, :, 1] == 0) & (arr[:, :, 2] == 255))

for y in range(95, 128, 2):
    row_pixels = arr[y, mask[y, :]]
    if len(row_pixels) > 0:
        # Check colors
        r = row_pixels[:, 0]
        g = row_pixels[:, 1]
        b = row_pixels[:, 2]
        # Are there yellowish pixels (r>180, g>160, b>130)?
        beige = (r > 160) & (g > 140) & (b > 110) & (np.abs(r - g) < 30)
        beige_count = np.sum(beige)
        xs = np.where(mask[y, :])[0]
        print(f"y={y}: total pixels={len(row_pixels)}, beige pixels={beige_count}, x_range=[{np.min(xs)}, {np.max(xs)}]")
        if beige_count > 0:
            print(f"   sample beige RGB: {row_pixels[beige][0]}")
