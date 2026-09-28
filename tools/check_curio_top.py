#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
curio = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rhino/back_curio/curio_rhino_steam_furnace_exhaust.png").convert("RGBA")
arr = np.array(curio)
for y in range(8):
    alpha_cnt = np.sum(arr[y, :, 3] > 0)
    print(f"curio y={y}: {alpha_cnt} non-zero alpha pixels")
