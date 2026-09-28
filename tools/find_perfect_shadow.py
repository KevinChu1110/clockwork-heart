#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

shadow = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
shd = ImageDraw.Draw(shadow)
# center around (64, 115), rx=34, ry=6
shd.ellipse([64 - 34, 115 - 6, 64 + 34, 115 + 6], fill=(31, 26, 58, 120))
shd.ellipse([64 - 24, 115 - 4, 64 + 24, 115 + 4], fill=(31, 26, 58, 150))
shadow = shadow.filter(ImageFilter.GaussianBlur(0.7))

arr = np.array(shadow)
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Perfect shadow counts (118..127):", counts)
for y in range(118, 128):
    xs = np.where(arr[y, :, 3] > 10)[0]
    if len(xs) > 0:
        print(f"y={y}: count_gt_10={len(xs):2d} min_x={xs.min():2d} max_x={xs.max():2d} max_alpha={arr[y, :, 3].max():2d}")
    else:
        print(f"y={y}: count_gt_10= 0")
