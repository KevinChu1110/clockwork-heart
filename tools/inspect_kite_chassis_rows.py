#!/usr/bin/env python3
from PIL import Image
import numpy as np

chassis = Image.open("game/assets/sprites/player/paperdoll/kite/chassis/chassis_kite_copper_obsidian_default.png").convert("RGBA")
arr = np.array(chassis)
for y in range(45, 120, 5):
    row = arr[y, :, 3]
    nonzero = np.where(row > 20)[0]
    if len(nonzero) > 0:
        print(f"y={y:3d}: x in [{nonzero[0]:2d} .. {nonzero[-1]:2d}], count={len(nonzero):2d}")
