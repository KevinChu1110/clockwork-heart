#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

vk = Image.open(f"{BOAR_DIR}/verification_crop_key.png")
print("vk size:", vk.size, "bbox:", vk.getbbox())

k128 = Image.open(f"{BOAR_DIR}/winding_key/key_classic_brass.png")
k512 = Image.open(f"{BOAR_DIR}/winding_key/key_classic_brass_512.png")

k128_crop = k128.crop(k128.getbbox())
print("k128 cropped size:", k128_crop.size)

k512_crop = k512.crop(k512.getbbox())
print("k512 cropped size:", k512_crop.size)
