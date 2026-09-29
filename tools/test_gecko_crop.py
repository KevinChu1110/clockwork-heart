#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
comp512 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/gecko/idle_512.png").convert("RGBA")
arr = np.array(comp512)

# Check waist / upper body
print("comp512 bbox:", comp512.getbbox())
for y in range(200, 420, 30):
    ys, xs = np.where((arr[y, :, 3] > 20)[:, None])
    # check width
    xs = np.where(arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f"y={y}: x in [{xs.min()}..{xs.max()}] (width={xs.max()-xs.min()})")
