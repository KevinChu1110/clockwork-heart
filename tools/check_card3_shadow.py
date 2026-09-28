#!/usr/bin/env python3
from PIL import Image
import numpy as np

c3 = Image.open("proofs/official_assets_kite/proof_03_walk_cycle.png")
# Check pixels at the bottom of card 0 (px=35..305, py=110..380)
# img is 256x256 inside [35+7, 110+7] = [42, 117]
# 128x128 scaled by 2, so y=118..127 in 128 corresponds to py = 117 + 118*2 = 353..371
arr = np.array(c3)
for frame_idx in range(4):
    px = 42 + frame_idx * 285
    # shadow is at py = 353..371, x in px..px+256
    shadow_crop = arr[353:371, px:px+256, :3]
    # how many dark pixels (not white 255,255,255)
    dark_px = np.sum(np.all(shadow_crop < 240, axis=2))
    print(f"Card 3 Frame {frame_idx} enlarged shadow dark pixel count: {dark_px}")
