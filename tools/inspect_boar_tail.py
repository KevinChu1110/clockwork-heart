#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
p_boar_tail = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar/maple_parts/back_curio/curio_spring_tail.png"
im_bt = Image.open(p_boar_tail)
print("Boar tail size:", im_bt.size, "bbox:", im_bt.getbbox())
