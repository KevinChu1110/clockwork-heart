#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/tmp/python_composite_direct.png").convert("RGBA")
arr = np.array(im)

hammer_region = arr[300:500, 180:240, 3]
print("Min alpha in hammer region (180..240, 300..500):", np.min(hammer_region))
print("Count of alpha < 100 in hammer region:", np.sum(hammer_region < 100))

# 檢查單片眼鏡右下方 (x: 235..250, y: 155..170) 的 Alpha
eye_region = arr[155:170, 235:250, 3]
print("Min alpha in eye region (235..250, 155..170):", np.min(eye_region))
print("Count of alpha < 100 in eye region:", np.sum(eye_region < 100))
