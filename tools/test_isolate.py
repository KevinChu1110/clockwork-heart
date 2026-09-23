#!/usr/bin/env python3
import numpy as np
from PIL import Image

im = Image.open("/tmp/tortoise_main_view.png").convert("RGBA")
arr = np.array(im, dtype=np.float32)
r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

# Magenta background: r is high, g is low, b is high
# Compute distance from pure magenta (255, 0, 255)
dist = np.sqrt((255 - r)**2 + (0 - g)**2 + (255 - b)**2)
# Anti-aliased smooth alpha
alpha = np.clip((dist - 15.0) / 25.0, 0.0, 1.0) * 255.0

# In addition, crop out anything x > 820 (secondary view artifact if any)
alpha[:, 820:] = 0

arr[:, :, 3] = alpha
res = Image.fromarray(arr.astype(np.uint8))
bbox = res.getbbox()
print("Extracted character bbox:", bbox)
cropped = res.crop(bbox)
cropped.save("/tmp/tortoise_isolated_perfect.png")
print("Saved /tmp/tortoise_isolated_perfect.png, size:", cropped.size)
