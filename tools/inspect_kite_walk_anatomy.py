#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/kite"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/kite"

for part in ["chassis", "head_unit", "costume", "optic_core", "weapon", "winding_key", "back_curio"]:
    sub = os.listdir(f"{BASE_DIR}/{part}")
    pngs = [f for f in sub if f.endswith(".png") and not f.endswith("_512.png")]
    for p in pngs:
        im = Image.open(f"{BASE_DIR}/{part}/{p}").convert("RGBA")
        print(f"{part:12s} {p:45s} size={im.size} bbox={im.getbbox()}")

idle = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")
idle_512 = Image.open(f"{POSES_DIR}/idle_512.png").convert("RGBA")
print(f"idle.png size={idle.size} bbox={idle.getbbox()}")
print(f"idle_512.png size={idle_512.size} bbox={idle_512.getbbox()}")
