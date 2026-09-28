#!/usr/bin/env python3
from PIL import Image
import numpy as np

idle = Image.open("game/assets/sprites/player/poses/kite/idle.png").convert("RGBA")
arr = np.array(idle)
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("poses/kite/idle.png shadow counts:", counts)
