#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/takin"
wpn_im = Image.open(f"{BASE_DIR}/weapon/weapon_takin_zen_bamboo_cleaving_axe.png").convert("RGBA")
arr = np.array(wpn_im)

# Look at rows of weapon
for y in range(15, 110, 10):
    row_xs = np.where(arr[y, :, 3] > 50)[0]
    if len(row_xs) > 0:
        print(f"y={y:3d}: x in [{min(row_xs):3d}..{max(row_xs):3d}], width={len(row_xs):2d}")
