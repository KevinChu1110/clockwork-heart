#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

comp = Image.open(f"{BOAR_DIR}/proof_paperdoll_boar_composite.png").convert("RGBA")
# 裁出 (50, 35, 70, 50)
eye_128 = comp.crop((50, 35, 70, 50))
print("Eye region in 128 composite:")
arr = np.array(eye_128)
for y in range(arr.shape[0]):
    row = ""
    for x in range(arr.shape[1]):
        px = arr[y, x]
        if px[3] > 0:
            if px[1] > 150 and px[2] > 150: # cyan
                row += "C"
            elif px[0] > 150 and px[1] > 150: # yellow/white
                row += "Y"
            else:
                row += "#"
        else:
            row += "."
    print(f"{35+y:2d}: {row}")
