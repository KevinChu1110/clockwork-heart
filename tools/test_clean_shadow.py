#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

shadow = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
shd = ImageDraw.Draw(shadow)
shd.ellipse([30, 113, 98, 123], fill=(31, 26, 58, 110))
shd.ellipse([42, 115, 86, 121], fill=(31, 26, 58, 160))
shadow = shadow.filter(ImageFilter.GaussianBlur(0.8))

arr = np.array(shadow)
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Smooth ellipse shadow counts (118..127):", counts)
for y in range(118, 128):
    xs = np.where(arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f"y={y}: count={len(xs)} min_x={xs.min()} max_x={xs.max()}")
    else:
        print(f"y={y}: count=0")
