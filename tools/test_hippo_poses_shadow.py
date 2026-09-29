#!/usr/bin/env python3
import os
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/hippo"

poses = ["idle", "attack", "telegraph", "hit", "skill", "recover"]
for p in poses:
    im = Image.open(f"{POSES_DIR}/{p}.png").convert("RGBA")
    arr = np.array(im)
    sh = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"Pose {p:10s} shadow (118..127): {sh}")
