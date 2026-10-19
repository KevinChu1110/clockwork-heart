#!/usr/bin/env python3
import os
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PARTS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar/maple_parts"

for f in os.listdir(f"{PARTS_DIR}/head_unit"):
    if f.endswith(".png"):
        p = f"{PARTS_DIR}/head_unit/{f}"
        im = Image.open(p).convert("RGBA")
        arr = np.array(im)
        
        # 尋找亮白螞蟻線像素
        white_mask = (arr[:, :, 0] > 200) & (arr[:, :, 1] > 200) & (arr[:, :, 2] > 200) & (arr[:, :, 3] > 50)
        ys, xs = np.where(white_mask)
        print(f"{f}: found {len(ys)} marching ants pixels")
        
        # 替換為相鄰的金屬色（或者如果是邊緣外部，直接轉透明）
        for x, y in zip(xs, ys):
            # 檢查四周是否有透明
            neighbors = []
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < arr.shape[0] and 0 <= nx < arr.shape[1]:
                        if not white_mask[ny, nx]:
                            neighbors.append(arr[ny, nx])
            
            # 如果周圍大部分是透明，直接透明
            alphas = [n[3] for n in neighbors]
            if len(alphas) > 0 and (sum(alphas) / len(alphas) < 100):
                arr[y, x] = [0, 0, 0, 0]
            else:
                # 替換為深藍金屬色 (42, 55, 78, 255)
                arr[y, x] = [42, 55, 78, 255]

        cleaned = Image.fromarray(arr, mode="RGBA")
        cleaned.save(p)
        print(f"  ✓ Cleaned {f}")
