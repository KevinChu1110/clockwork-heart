#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

for name in sorted(os.listdir(BOAR_DIR)):
    if name.endswith(".png"):
        p = os.path.join(BOAR_DIR, name)
        im = Image.open(p)
        print(f"{name}: size={im.size}, bbox={im.getbbox()}")
