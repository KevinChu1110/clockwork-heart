#!/usr/bin/env python3
import os
import sys
import numpy as np
from PIL import Image

for race in ["rabbit", "fox", "crane", "lion"]:
    p = f"proofs/creation_stage_512/proof_creation_stage_{race}_512.png"
    im = Image.open(p).convert("RGBA")
    # Character body is around x: 250..370, y: 360..560
    box = (250, 360, 370, 560)
    crop = im.crop(box)
    arr = np.array(crop)
    h, w, _ = arr.shape
    
    dup_cols = 0
    for x in range(w - 1):
        if np.array_equal(arr[:, x, :3], arr[:, x + 1, :3]):
            dup_cols += 1
    dup_col_ratio = dup_cols / (w - 1)
    
    rgb_arr = arr[:, :, :3].reshape(-1, 3)
    unique_colors = len(np.unique(rgb_arr, axis=0))
    print(f"[{race}] Body crop ({box}): {w}x{h} | dup_cols: {dup_cols}/{w-1} ({dup_col_ratio:.2%}) | unique_colors: {unique_colors}")
