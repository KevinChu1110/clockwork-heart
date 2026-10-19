#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

vk = Image.open(f"{BOAR_DIR}/verification_crop_key.png")
print("vk size:", vk.size, "bbox:", vk.getbbox())
# 縮小看看它的細節
vk.save("/tmp/boar_vk_full.png")
