#!/usr/bin/env python3
import os
import sys
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
race = sys.argv[1] if len(sys.argv) > 1 else "hippo"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/{race}"

if race == "gecko":
    comp512 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/gecko/idle_512.png").convert("RGBA")
    arr = np.array(comp512)
    head_mask = (arr[:, :, 3] > 20) & (np.arange(512)[:, None] <= 250)
    ys, xs = np.where(head_mask)
    print(f"Head region y in [{ys.min()}..{ys.max()}], x in [{xs.min()}..{xs.max()}]")
    print(f"Full bounding box: ({xs.min()}, {ys.min()}, {xs.max()+1}, {ys.max()+1})")
else:
    head_unit_dir = os.path.join(PD_DIR, "head_unit")
    if os.path.isdir(head_unit_dir):
        for f in os.listdir(head_unit_dir):
            if f.endswith("_512.png"):
                im = Image.open(os.path.join(head_unit_dir, f)).convert("RGBA")
                print(f"{f} bbox:", im.getbbox())
