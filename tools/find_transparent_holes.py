#!/usr/bin/env python3
from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png"
im = Image.open(p).convert("RGBA")
arr = np.array(im)

# 檢查胸部中央 (x: 200..260, y: 200..260) 的 alpha
chest_alpha = arr[200:260, 200:260, 3]
print("Min alpha in chest (200..260, 200..260):", np.min(chest_alpha))
print("Mean alpha in chest:", np.mean(chest_alpha))

# 檢查 (x: 180..230, y: 170..210) 鼻下/頸部交接處的 alpha
neck_alpha = arr[170:210, 180:230, 3]
print("Min alpha in neck (170..210, 180..230):", np.min(neck_alpha))
print("Zero alpha pixels in neck:", np.sum(neck_alpha == 0))
