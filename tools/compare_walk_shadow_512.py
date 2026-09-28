#!/usr/bin/env python3
from PIL import Image
import numpy as np

for race in ["seal", "kite"]:
    for i in range(4):
        im = Image.open(f"game/assets/sprites/player/{race}_walk_{i}_512.png").convert("RGBA")
        arr = np.array(im)
        counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118*4, 128*4, 4)]
        print(f"{race} walk {i} 512 shadow every 4th row:", counts)
