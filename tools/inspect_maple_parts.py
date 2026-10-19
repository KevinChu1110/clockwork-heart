#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"

for race in ["rabbit", "fox", "lion"]:
    mp = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/{race}/maple_parts"
    if os.path.exists(mp):
        print(f"=== {race} maple_parts ===")
        for sub in os.listdir(mp):
            subp = os.path.join(mp, sub)
            if os.path.isdir(subp):
                for f in os.listdir(subp):
                    if f.endswith(".png"):
                        im = Image.open(os.path.join(subp, f))
                        print(f"  {sub}/{f}: size={im.size}, bbox={im.getbbox()}")
