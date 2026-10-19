#!/usr/bin/env python3
from PIL import Image
import numpy as np

head512 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/head_unit/ear_boar_rivet_cowl_brass_512.png").convert("RGBA")
arr = np.array(head512)

# 搜尋純白點 (R>240, G>240, B>240)
white_mask = (arr[:, :, 0] > 240) & (arr[:, :, 1] > 240) & (arr[:, :, 2] > 240) & (arr[:, :, 3] > 100)
print("White pixels in head 512 raw:", np.sum(white_mask))
