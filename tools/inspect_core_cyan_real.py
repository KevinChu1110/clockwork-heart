#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

c = Image.open(f"{BOAR_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")
# 裁出有效 bbox
bbox = c.getbbox()
print("core_cyan_emerald_512 bbox:", bbox)
crop = c.crop(bbox)
crop.save("/tmp/core_cyan_emerald_crop.png")

arr = np.array(crop)
# 找主要顏色
colors, counts = np.unique(arr.reshape(-1, 4), axis=0, return_counts=True)
# 按數量排序
idx = np.argsort(-counts)
for i in range(min(15, len(colors))):
    col = colors[idx[i]]
    cnt = counts[idx[i]]
    if col[3] > 0:
        print(f"Color: {col}, Count: {cnt}")
