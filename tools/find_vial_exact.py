#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PARTS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar/maple_parts"

for slot in ["costume/costume_viking_harness.png", "body/paint_brass_gold.png", "weapon/wpn_anvil_greathammer.png"]:
    p = f"{PARTS_DIR}/{slot}"
    im = Image.open(p).convert("RGBA")
    arr = np.array(im)
    # 找橙色像素：R > 200, G in [50..180], B < 50
    mask = (arr[:, :, 0] > 180) & (arr[:, :, 1] > 60) & (arr[:, :, 1] < 180) & (arr[:, :, 2] < 50) & (arr[:, :, 3] > 50)
    ys, xs = np.where(mask)
    if len(ys) > 0:
        print(f"FOUND IN {slot}: count={len(ys)}")
        print(f"  Y range: {ys.min()}..{ys.max()}, X range: {xs.min()}..{xs.max()}")
        print(f"  Center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")
