#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageChops

FOX_POSES_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"
for p in ["idle", "telegraph", "attack", "recover", "skill"]:
    fpath = f"{FOX_POSES_DIR}/{p}.png"
    im = Image.open(fpath)
    print(f"{p}: size={im.size}, bbox={im.getbbox()}")
