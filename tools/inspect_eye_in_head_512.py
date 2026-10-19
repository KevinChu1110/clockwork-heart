#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

head = Image.open(f"{BOAR_DIR}/head_unit/ear_boar_rivet_cowl_brass_512.png").convert("RGBA")
crop = head.crop((220, 150, 250, 180))
print("Head 512 crop (220, 150, 250, 180):")
arr = np.array(crop)
for y in range(0, arr.shape[0], 2):
    row = ""
    for x in range(0, arr.shape[1], 2):
        px = arr[y, x]
        if px[3] > 20:
            if px[1] > 140 and px[2] > 140:
                row += "C"
            elif px[0] > 140 and px[1] > 140:
                row += "Y"
            else:
                row += "#"
        else:
            row += "."
    print(f"{150+y:3d}: {row}")
