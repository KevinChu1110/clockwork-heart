#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

for sub in ["head_unit", "chassis", "costume", "weapon", "winding_key", "optic_core", "back_curio"]:
    p = os.path.join(BOAR_DIR, sub)
    if os.path.exists(p):
        for f in os.listdir(p):
            if f.endswith(".png"):
                full = os.path.join(p, f)
                im = Image.open(full)
                print(f"{sub}/{f}: size={im.size}, bbox={im.getbbox()}")
