#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"

for race in ["rabbit", "fox", "lion", "boar"]:
    p = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/{race}/maple_parts/winding_key/key_classic_brass.png"
    if os.path.exists(p):
        im = Image.open(p)
        print(f"{race} key: size={im.size}, bbox={im.getbbox()}")
