#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

head = Image.open(f"{BOAR_DIR}/head_unit/ear_boar_rivet_cowl_brass_512.png").convert("RGBA")
arr = np.array(head)

# 搜尋發亮青藍色 (Cyan) 或是特定特徵的像素
# 在 vision analyze 中：
# "眼睛呈翠綠色（翡翠綠）瞳孔，發出微弱光芒，眼神朝向右前方"
# "機械發光眼，散發出高亮度的亮青藍色（Cyan/霓虹水藍）光芒"
# 讓我們找出高亮度青藍色像素 (R < 100, G > 150, B > 150)
cyan_mask = (arr[:, :, 0] < 120) & (arr[:, :, 1] > 140) & (arr[:, :, 2] > 140) & (arr[:, :, 3] > 100)
cy_ys, cy_xs = np.where(cyan_mask)
print(f"Cyan eye pixels in head: count={len(cy_ys)}")
if len(cy_ys) > 0:
    print(f"Eye Y range: {cy_ys.min()} .. {cy_ys.max()}, X range: {cy_xs.min()} .. {cy_xs.max()}")
    print(f"Eye center: X={np.mean(cy_xs):.1f}, Y={np.mean(cy_ys):.1f}")
