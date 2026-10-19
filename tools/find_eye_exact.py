#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

head = Image.open(f"{BOAR_DIR}/head_unit/ear_boar_rivet_cowl_brass_512.png").convert("RGBA")
arr = np.array(head)

# 在 (210, 140, 260, 180) 區域內找綠色/青綠色像素
sub = arr[140:180, 210:260]
# 條件：G > 120, G > R + 20, B > 80, A > 100
green_mask = (sub[:, :, 1] > 120) & (sub[:, :, 1] > sub[:, :, 0] + 15) & (sub[:, :, 3] > 100)
ys, xs = np.where(green_mask)
print("Green/Cyan pixels count:", len(ys))
if len(ys) > 0:
    abs_ys = ys + 140
    abs_xs = xs + 210
    print(f"Eye in 512: X={abs_xs.min()}..{abs_xs.max()}, Y={abs_ys.min()}..{abs_ys.max()}")
    print(f"Eye center in 512: X={np.mean(abs_xs):.1f}, Y={np.mean(abs_ys):.1f}")
