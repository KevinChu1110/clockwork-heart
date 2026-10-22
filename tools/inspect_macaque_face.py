#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

# 看看 proof_paperdoll_macaque_composite.png 的尺寸
im_comp = Image.open(f"{MACAQUE_DIR}/proof_paperdoll_macaque_composite.png")
print("Composite size:", im_comp.size)

# 看看 head_unit 和 chassis 裡頭部/面部的特徵
im_head = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_512.png")
print("Head 512 bbox:", im_head.getbbox())

im_chassis = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock_512.png")
print("Chassis 512 bbox:", im_chassis.getbbox())

# 看看 verification_crop_ears.png 等
for crop in ["verification_crop_ears.png", "verification_crop_claws.png", "verification_crop_tail.png", "verification_crop_key.png", "verification_crop_bamboo_bronze.png", "verification_crop_dawn_monk_tunic.png", "verification_crop_zen_striker.png"]:
    p = f"{MACAQUE_DIR}/{crop}"
    if os.path.exists(p):
        ic = Image.open(p)
        print(f"Crop {crop}: size={ic.size}")
