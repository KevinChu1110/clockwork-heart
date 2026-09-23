#!/usr/bin/env python3
from PIL import Image
import numpy as np

comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise/proof_paperdoll_tortoise_composite.png").convert("RGBA")
arr = np.array(comp)

for y in range(112, 128):
    xs = np.where(arr[y, :, 3] > 20)[0]
    count = len(xs)
    print(f"y={y:3d}: count={count:2d} xs=[{xs.min() if count else 0}..{xs.max() if count else 0}]")
