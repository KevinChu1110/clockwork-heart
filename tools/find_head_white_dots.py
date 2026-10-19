#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"

head = Image.open(f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl_brass.png").convert("RGBA")
arr = np.array(head)

# 搜尋純白/亮灰色像素：R > 230, G > 230, B > 230
white_mask = (arr[:, :, 0] > 220) & (arr[:, :, 1] > 220) & (arr[:, :, 2] > 220) & (arr[:, :, 3] > 50)
ys, xs = np.where(white_mask)
print(f"White pixels in head_unit: count={len(ys)}")
for i in range(min(15, len(ys))):
    print(f"  White pixel at ({xs[i]}, {ys[i]}): {arr[ys[i], xs[i]]}")
