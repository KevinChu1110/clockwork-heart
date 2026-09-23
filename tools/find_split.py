#!/usr/bin/env python3
import numpy as np
from PIL import Image

im = Image.open("/tmp/xuanji_tortoise_magenta_raw.png").convert("RGB")
w, h = im.size
print(f"Image size: {w}x{h}")

arr = np.array(im)
r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

# Magenta key: r > 200, g < 60, b > 200
is_magenta = (r > 200) & (g < 60) & (b > 200)
non_magenta = ~is_magenta

# Column density of non-magenta pixels
col_counts = np.sum(non_magenta, axis=0)

# Find columns where character exists
xs = np.where(col_counts > 10)[0]
print(f"Foreground columns: {np.min(xs)} to {np.max(xs)}")

# Let's inspect column counts to find the gap between main character (left) and secondary view (right)
for x in range(w // 3, 2 * w // 3, 20):
    print(f"Col {x}: {col_counts[x]} pixels")

# Save a preview of the left half
left_crop = im.crop((0, 0, w // 2 + 50, h))
left_crop.save("/tmp/tortoise_main_view.png")
print("Saved /tmp/tortoise_main_view.png")
