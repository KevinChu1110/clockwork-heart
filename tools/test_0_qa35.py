#!/usr/bin/env python3
import os
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"

idle512 = Image.open(f"{PLAYER_DIR}/poses/gecko/idle_512.png").convert("RGBA")

for i in range(4):
    wf512 = Image.open(f"{PLAYER_DIR}/gecko_walk_{i}_512.png").convert("RGBA")
    diff = ImageChops.difference(idle512, wf512)
    arr = np.array(diff)
    diff_mask = np.any(arr > 0, axis=2)

    head_diff = np.sum(diff_mask[:160, :])
    torso_diff = np.sum(diff_mask[160:350, :])
    leg_diff = np.sum(diff_mask[350:, :])

    print(f"Walk frame {i} diff vs idle_512: head={head_diff} (target >1500), torso={torso_diff} (target >1500), legs={leg_diff} (target >1500)")
