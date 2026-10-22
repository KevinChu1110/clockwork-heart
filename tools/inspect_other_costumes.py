#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"

for race in ["rabbit", "lion", "boar"]:
    base = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/{race}/maple_parts/costume"
    if os.path.exists(base):
        for f in os.listdir(base):
            if f.endswith(".png"):
                im = Image.open(f"{base}/{f}")
                print(f"{race} costume {f}: size={im.size}, bbox={im.getbbox()}")
