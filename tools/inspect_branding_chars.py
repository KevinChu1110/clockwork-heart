#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

for r in ["rabbit", "tiger", "bear", "crane", "penguin"]:
    p = f"/opt/side/bravesoul-game/branding/char_{r}.png"
    if os.path.exists(p):
        im = Image.open(p)
        arr = np.array(im)
        corner = arr[0, 0]
        # find non-corner pixels
        diff = np.max(np.abs(arr.astype(int) - corner.astype(int)), axis=2)
        char_y, char_x = np.where(diff > 15)
        print(f"[{r:7s}] size={im.size} mode={im.mode} corner_bg={corner} char_bbox=({char_x.min()}, {char_y.min()}, {char_x.max()}, {char_y.max()}) w={char_x.max()-char_x.min()+1} h={char_y.max()-char_y.min()+1}")
