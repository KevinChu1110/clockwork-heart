#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/web/media/hero/char_boar.png")
arr = np.array(im)
h, w, _ = arr.shape
print(f"Size: {w}x{h}")

# Sample top-left corner
print("Top-left (0,0):", arr[0, 0])
# Sample top-right corner
print("Top-right (0, w-1):", arr[0, w-1])
# Sample middle-top
print("Middle-top (0, w//2):", arr[0, w//2])
# Sample near the halo (say y=200, x=150 and x=750)
print("(200, 150):", arr[200, 150])
print("(200, 750):", arr[200, 750])

# What are the colors across row 100?
print("Row 100 min/max RGB:", np.min(arr[100, :, :], axis=0), np.max(arr[100, :, :], axis=0))
