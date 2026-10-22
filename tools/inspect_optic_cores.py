#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

optic_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/optic_core"
for f in os.listdir(optic_dir):
    if f.endswith(".png"):
        p = f"{optic_dir}/{f}"
        im = Image.open(p)
        print(f"{f}: size={im.size}, bbox={im.getbbox()}")
        arr = np.array(im.convert("RGBA"))
        # Check non-zero pixels
        pos = np.where(arr[:, :, 3] > 0)
        if len(pos[0]) > 0:
            print(f"  Y range: {pos[0].min()}..{pos[0].max()}, X range: {pos[1].min()}..{pos[1].max()}")
