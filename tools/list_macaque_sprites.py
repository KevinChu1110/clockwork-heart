#!/usr/bin/env python3
import glob
from PIL import Image

for p in sorted(glob.glob("/opt/side/bravesoul-game/game/assets/sprites/player/*macaque*")):
    if p.endswith(".png"):
        im = Image.open(p)
        print(f"{p}: {im.size}")
