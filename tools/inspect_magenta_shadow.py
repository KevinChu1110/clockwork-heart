#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/proof_bison_combat_poses_magenta.png")
arr = np.array(im)

for idx, name in enumerate(["idle", "telegraph", "attack", "recover", "skill", "hit"]):
    sub = arr[:, idx * 128:(idx + 1) * 128]
    print(f"\n--- {name} (x=[{idx*128}..{(idx+1)*128}]) ---")
    for y in range(118, 128):
        # find non-magenta pixels: magenta is (255, 0, 255)
        diff_mag = (sub[y, :, 0] != 255) | (sub[y, :, 1] != 0) | (sub[y, :, 2] != 255)
        xs = np.where(diff_mag)[0]
        if len(xs) > 0:
            print(f"y={y}: count={len(xs):2d} min_x={xs[0]:2d} max_x={xs[-1]:2d}")
        else:
            print(f"y={y}: count= 0")
