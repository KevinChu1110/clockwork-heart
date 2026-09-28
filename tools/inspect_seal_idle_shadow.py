#!/usr/bin/env python3
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
im = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/seal_idle.png").convert("RGBA")
print("Bbox:", im.getbbox())
arr = np.array(im)
shadow_counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print(f"Shadow counts (118..127): {shadow_counts}")
for y in range(118, 128):
    xs = np.where(arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f"  y={y}: min_x={xs[0]}, max_x={xs[-1]}, count={len(xs)}")
