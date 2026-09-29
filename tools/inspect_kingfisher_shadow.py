#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

player_dir = "game/assets/sprites/player"
for fname in ["kingfisher_idle.png", "kingfisher_idle_x3.png", "party/kingfisher_idle.png"]:
    p = os.path.join(player_dir, fname)
    if os.path.exists(p):
        im = Image.open(p)
        arr = np.array(im)
        print(f"{fname:30s}: size={im.size}, mode={im.mode}, bbox={im.getbbox()}")
        if im.size == (128, 128):
            counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
            print(f"  shadow (118..127): {counts}")
