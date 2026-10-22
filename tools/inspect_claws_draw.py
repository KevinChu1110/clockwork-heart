#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

im_w128 = Image.open(f"{MACAQUE_DIR}/weapon/wpn_spring_claws.png").convert("RGBA")
im_w512 = Image.open(f"{MACAQUE_DIR}/weapon/wpn_spring_claws_512.png").convert("RGBA")

print("128 weapon size:", im_w128.size, "bbox:", im_w128.getbbox())
print("512 weapon size:", im_w512.size, "bbox:", im_w512.getbbox())

im_w128.save("/tmp/macaque_test/weapon_128.png")
im_w512.save("/tmp/macaque_test/weapon_512.png")
