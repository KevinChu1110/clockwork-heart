#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/hippo"
comp512 = Image.open(f"{POSES_DIR}/idle_512.png").convert("RGBA")

box = (50, 0, 460, 280)
crop = comp512.crop(box)
hb = crop.getbbox()
print("box:", box, "crop bbox in local coords:", hb)
if hb:
    abs_bbox = (box[0] + hb[0], box[1] + hb[1], box[0] + hb[2], box[1] + hb[3])
    print("Head abs bbox in comp512:", abs_bbox)
