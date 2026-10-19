#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PARTS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar/maple_parts"

for root, dirs, files in os.walk(PARTS_DIR):
    for f in files:
        if f.endswith(".png"):
            p = os.path.join(root, f)
            im = Image.open(p).convert("RGBA")
            arr = np.array(im)
            
            # 純白點
            white_mask = (arr[:, :, 0] > 245) & (arr[:, :, 1] > 245) & (arr[:, :, 2] > 245) & (arr[:, :, 3] > 200)
            cnt = np.sum(white_mask)
            rel = os.path.relpath(p, PARTS_DIR)
            if cnt > 0:
                ys, xs = np.where(white_mask)
                print(f"WHITE IN {rel:35}: count={cnt}, x={xs.min()}..{xs.max()}, y={ys.min()}..{ys.max()}")
            else:
                print(f"OK (0 white): {rel:35}")
