#!/usr/bin/env python3
from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png"
im = Image.open(p).convert("RGBA")
arr = np.array(im)

# 搜尋純白像素：R > 250, G > 250, B > 250, A > 200
pure_white = (arr[:, :, 0] > 250) & (arr[:, :, 1] > 250) & (arr[:, :, 2] > 250) & (arr[:, :, 3] > 200)
ys, xs = np.where(pure_white)
print(f"Pure white pixels in composite: {len(ys)}")
if len(ys) > 0:
    print(f"X: {xs.min()}..{xs.max()}, Y: {ys.min()}..{ys.max()}")
