#!/usr/bin/env python3
import numpy as np
from PIL import Image

im = Image.open("/tmp/tortoise_main_view.png").convert("RGB")
arr = np.array(im)
# Sample corners
print("Corners:", arr[10, 10], arr[10, 500], arr[700, 10], arr[700, 500])

# Background condition:
r = arr[:, :, 0].astype(int)
g = arr[:, :, 1].astype(int)
b = arr[:, :, 2].astype(int)

# In magenta background, G is very low, R and B are high
is_bg = (g < 60) & (r > 160) & (b > 160)
print(f"Total background pixels: {np.sum(is_bg)} / {arr.shape[0]*arr.shape[1]}")

# Check any non-bg pixel with g < 80
fg = ~is_bg
f_r, f_g, f_b = r[fg], g[fg], b[fg]
print("Foreground min RGB:", np.min(f_r), np.min(f_g), np.min(f_b))
