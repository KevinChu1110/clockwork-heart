#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/head_unit/ear_boar_rivet_cowl_512.png").convert("RGBA")
print("Size:", im.size, "bbox:", im.getbbox())
arr = np.array(im)
print("Non-zero alpha pixels:", np.sum(arr[:, :, 3] > 0))

# Check where alpha > 0
ys, xs = np.where(arr[:, :, 3] > 0)
print(f"Y range: {ys.min()}..{ys.max()}, X range: {xs.min()}..{xs.max()}")
