#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/hippo"

comp512 = Image.open(f"{POSES_DIR}/idle_512.png").convert("RGBA")

# Let's inspect head region in 512
# Head in 128 was y=19..60, which in 512 is y=76..240
head_crop = comp512.crop((116, 20, 400, 260))
hb = head_crop.getbbox()
print("Head crop bbox:", hb)
if hb:
    tight = head_crop.crop(hb)
    print("Tight head size:", tight.size)

# Dialogue bust in 512: waist-up
# In 128, waist was around y=85, which in 512 is y=340
bust_crop = comp512.crop((50, 15, 465, 380))
bb = bust_crop.getbbox()
print("Bust crop bbox:", bb)
if bb:
    tight_bust = bust_crop.crop(bb)
    print("Tight bust size:", tight_bust.size)
