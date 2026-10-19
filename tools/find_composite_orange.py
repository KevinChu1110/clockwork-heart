#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/tmp/boar_proof_harness.png").convert("RGBA")
arr = np.array(im)

# 搜尋所有帶有橙紅色的像素：R > 180, G in [50..160], B < 80
mask = (arr[:, :, 0] > 180) & (arr[:, :, 1] > 50) & (arr[:, :, 1] < 160) & (arr[:, :, 2] < 80) & (arr[:, :, 3] > 50)
ys, xs = np.where(mask)
print(f"Total orange/red pixels in composite: {len(ys)}")
if len(ys) > 0:
    for i in range(min(10, len(ys))):
        print(f"  Pixel at ({xs[i]}, {ys[i]}): {arr[ys[i], xs[i]]}")
    print(f"Bbox of orange pixels: X={xs.min()}..{xs.max()}, Y={ys.min()}..{ys.max()}")
