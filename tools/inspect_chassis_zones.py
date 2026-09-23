#!/usr/bin/env python3
from PIL import Image
import numpy as np

chassis = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise/chassis/paint_tortoise_jade.png").convert("RGBA")
arr = np.array(chassis)

# Check vertical zones
for y in range(45, 123, 5):
    row_x = np.where(arr[y, :, 3] > 20)[0]
    if len(row_x) > 0:
        print(f"y={y:3d}: x min={row_x.min():2d}, max={row_x.max():2d}, count={len(row_x):2d}")
