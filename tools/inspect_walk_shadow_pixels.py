#!/usr/bin/env python3
from typing import cast
from PIL import Image
import numpy as np

for i in range(4):
    im = Image.open(f"game/assets/sprites/player/kite_walk_{i}_x3.png").convert("RGBA")
    arr = np.array(im)
    sh_counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"Frame {i} shadow counts: {sh_counts}")
    
    # Check y in 110..120
    sh_110_120 = [int(np.sum(arr[y, :, 3] > 20)) for y in range(110, 118)]
    print(f"Frame {i} rows 110..117 counts: {sh_110_120}")
