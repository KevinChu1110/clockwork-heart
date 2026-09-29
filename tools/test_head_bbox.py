#!/usr/bin/env python3
import os
import sys
from PIL import Image

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
race = sys.argv[1] if len(sys.argv) > 1 else "hippo"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/{race}"
idle_path = f"{POSES_DIR}/idle_512.png"

if os.path.exists(idle_path):
    comp512 = Image.open(idle_path).convert("RGBA")
    if race == "gecko":
        box = (140, 40, 360, 260)
    else:
        box = (50, 0, 460, 280)
    crop = comp512.crop(box)
    hb = crop.getbbox()
    print("box:", box, "crop bbox in local coords:", hb)
    if hb:
        abs_bbox = (box[0] + hb[0], box[1] + hb[1], box[0] + hb[2], box[1] + hb[3])
        print("Head abs bbox in comp512:", abs_bbox)
