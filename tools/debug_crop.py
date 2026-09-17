#!/usr/bin/env python3
import os
import sys
import numpy as np
from PIL import Image

im = Image.open('screenshots/crop_stage_rabbit.png')
arr = np.array(im)
h, w, _ = arr.shape
print(f"Crop size: {w}x{h}")
dup_bg_cols = 0
dup_char_cols = 0
for x in range(w - 1):
    if np.array_equal(arr[:, x], arr[:, x + 1]):
        # check if it is background (e.g. mostly white #ffffff or solid pedestal)
        is_bg = np.all(arr[:200, x, :3] == [255, 255, 255])
        if is_bg:
            dup_bg_cols += 1
        else:
            dup_char_cols += 1

print(f"Duplicate background columns (solid white panel): {dup_bg_cols}/{w-1} ({dup_bg_cols/(w-1):.2%})")
print(f"Duplicate character columns: {dup_char_cols}/{w-1} ({dup_char_cols/(w-1):.2%})")
