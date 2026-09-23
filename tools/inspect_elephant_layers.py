#!/usr/bin/env python3
import os
from PIL import Image

pd_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/elephant"
for root, dirs, files in os.walk(pd_dir):
    for f in sorted(files):
        if f.endswith(".png") and not f.startswith("proof"):
            p = os.path.join(root, f)
            im = Image.open(p)
            print(f"{os.path.relpath(p, pd_dir):45s} {im.size} {im.mode} bbox={im.getbbox()}")
