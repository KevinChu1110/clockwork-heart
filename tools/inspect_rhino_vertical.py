#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
RHINO_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rhino"
comp = Image.open(f"{RHINO_DIR}/proof_paperdoll_rhino_composite.png").convert("RGBA")
arr = np.array(comp)

for y in range(128):
    cnt = np.sum(arr[y, :, 3] > 20)
    if cnt > 0:
        print(f"y={y:3d}: {cnt:3d} pixels")
