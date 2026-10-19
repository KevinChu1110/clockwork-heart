#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"

parts = [
    "body/paint_brass_gold.png",
    "head_unit/ear_boar_rivet_cowl_brass.png",
    "costume/costume_viking_ironclad.png",
    "costume/costume_viking_harness.png",
    "weapon/wpn_anvil_greathammer.png",
    "winding_key/key_classic_brass.png",
    "back_curio/curio_spring_tail.png"
]

for p in parts:
    im = Image.open(f"{PARTS_DIR}/{p}").convert("RGBA")
    arr = np.array(im)
    # 檢查是否有深藍色 (B > R + 30, B > G + 30) 或是橙色 (R > 200, G in 80..150, B < 50)
    orange_mask = (arr[:, :, 0] > 180) & (arr[:, :, 1] > 60) & (arr[:, :, 1] < 150) & (arr[:, :, 2] < 50) & (arr[:, :, 3] > 100)
    blue_mask = (arr[:, :, 2] > arr[:, :, 0] + 40) & (arr[:, :, 2] > arr[:, :, 1] + 20) & (arr[:, :, 3] > 100)
    print(f"{p}: orange={np.sum(orange_mask)}, blue={np.sum(blue_mask)}")
