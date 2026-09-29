#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/manta_idle.png").convert("RGBA")
arr = np.array(img)
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Party idle shadow (118..127):", counts)

poses_idle = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/manta/idle.png").convert("RGBA")
arr_p = np.array(poses_idle)
counts_p = [int(np.sum(arr_p[y, :, 3] > 20)) for y in range(118, 128)]
print("Poses idle shadow (118..127):", counts_p)

comp_bbox = poses_idle.getbbox()
print("Poses idle bbox:", comp_bbox)

idle_512 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/manta/idle_512.png").convert("RGBA")
print("Poses idle_512 size:", idle_512.size, "bbox:", idle_512.getbbox())
