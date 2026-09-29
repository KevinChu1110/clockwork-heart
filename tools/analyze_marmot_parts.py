#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/marmot"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/marmot"

parts = ["chassis", "head_unit", "optic_core", "costume", "back_curio", "winding_key", "weapon"]
for p in parts:
    path = None
    for f in os.listdir(f"{PD_DIR}/{p}"):
        if f.endswith(".png") and not f.endswith("_512.png") and not f.endswith(".import"):
            path = f"{PD_DIR}/{p}/{f}"
            break
    if path:
        im = Image.open(path)
        bbox = im.getbbox()
        print(f"{p:15s}: bbox={bbox}")

idle = Image.open(f"{POSES_DIR}/idle.png")
print(f"idle           : bbox={idle.getbbox()}")
attack = Image.open(f"{POSES_DIR}/attack.png")
print(f"attack         : bbox={attack.getbbox()}")
