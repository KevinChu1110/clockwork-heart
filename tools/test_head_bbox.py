#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
comp512 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/gecko/idle_512.png").convert("RGBA")

# Let's test a head crop box
crop_box = (140, 40, 360, 260)
hud_crop = comp512.crop(crop_box)
h_cbbox = hud_crop.getbbox()
print("HUD crop bbox in crop_box:", h_cbbox)

if h_cbbox:
    tight = hud_crop.crop(h_cbbox)
    print("Tight size:", tight.size)
