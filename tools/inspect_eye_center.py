#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/tmp/authentic_eye_in_512.png")
arr = np.array(im)
# Find the glowing cyan pixels
cyan = (arr[:, :, 1] > 120) & (arr[:, :, 2] > 120) & (arr[:, :, 0] < 140)
ys, xs = np.where(cyan)
print(f"Cyan eyeball center in (90, 60) sprite: ({int(np.mean(xs))}, {int(np.mean(ys))})")
print(f"Eyeball span: X: {xs.min()}..{xs.max()}, Y: {ys.min()}..{ys.max()}")
