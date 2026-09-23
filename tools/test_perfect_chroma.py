#!/usr/bin/env python3
import numpy as np
from PIL import Image

im = Image.open("/tmp/tortoise_main_view.png").convert("RGB")
arr = np.array(im)
r = arr[:, :, 0].astype(int)
g = arr[:, :, 1].astype(int)
b = arr[:, :, 2].astype(int)

# Exact chroma key
is_magenta_bg = (r > 200) & (b > 200) & (g < 70)
# Edge anti-aliasing: transition pixels
is_edge = (r > 180) & (b > 180) & (g < 100) & (~is_magenta_bg)

rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
rgba[:, :, :3] = arr
rgba[:, :, 3] = 255
rgba[is_magenta_bg, 3] = 0
rgba[is_edge, 3] = 128

# Crop x > 820
rgba[:, 820:, 3] = 0

clean = Image.fromarray(rgba)
bbox = clean.getbbox()
print("Cleaned bbox:", bbox)
cropped = clean.crop(bbox)
cropped.save("/tmp/perfect_isolated.png")

# Magenta test
mag = Image.new("RGBA", cropped.size, (255, 0, 255, 255))
mag.alpha_composite(cropped)
mag.save("/tmp/perfect_isolated_magenta.png")
print("Saved /tmp/perfect_isolated_magenta.png")
