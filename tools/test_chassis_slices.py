#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/gecko"

ch = Image.open(f"{PD_DIR}/chassis/chassis_gecko_brass_patina_default.png").convert("RGBA")
arr = np.array(ch)
print("Chassis bbox:", ch.getbbox())

for y in range(70, 120, 5):
    cnt = np.sum(arr[y, :, 3] > 20)
    xs = np.where(arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f"y={y:3d}: count={cnt:2d}, x in [{xs.min()}..{xs.max()}]")
