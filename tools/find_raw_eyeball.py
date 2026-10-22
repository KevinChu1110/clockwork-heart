#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/tmp/raw_eye_crop.png")
arr = np.array(im)
h, w, _ = arr.shape
print("raw_eye_crop size:", w, h)

# In raw_eye_crop, look for the brightest cyan/white pixels:
# Specular highlight is very bright (R>220, G>230, B>230)
highlight = (arr[:, :, 0] > 200) & (arr[:, :, 1] > 220) & (arr[:, :, 2] > 220)
ys_hi, xs_hi = np.where(highlight)
if len(ys_hi) > 0:
    print(f"Highlight center: ({int(np.mean(xs_hi))}, {int(np.mean(ys_hi))})")
    print(f"Highlight range: X: {xs_hi.min()}..{xs_hi.max()}, Y: {ys_hi.min()}..{ys_hi.max()}")

# Cyan glow:
cyan = (arr[:, :, 1] > 160) & (arr[:, :, 2] > 180) & (arr[:, :, 0] < 120)
ys_c, xs_c = np.where(cyan)
if len(ys_c) > 0:
    print(f"Cyan glow center: ({int(np.mean(xs_c))}, {int(np.mean(ys_c))})")
    print(f"Cyan glow range: X: {xs_c.min()}..{xs_c.max()}, Y: {ys_c.min()}..{ys_c.max()}")
