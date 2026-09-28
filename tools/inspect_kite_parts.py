#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/kite"

weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_kite_crucible_recurve_bow.png").convert("RGBA")
key_src = Image.open(f"{BASE_DIR}/winding_key/key_kite_turbine_relief_brass.png").convert("RGBA")

w_bbox = weapon_src.getbbox()
k_bbox = key_src.getbbox()
print("Weapon bbox:", w_bbox)
print("Key bbox:", k_bbox)
if w_bbox:
    w_crop = weapon_src.crop(w_bbox)
    print("Weapon crop size:", w_crop.size)
    print("Weapon center in 128:", (w_bbox[0] + w_bbox[2]) / 2, (w_bbox[1] + w_bbox[3]) / 2)
if k_bbox:
    k_crop = key_src.crop(k_bbox)
    print("Key crop size:", k_crop.size)
    print("Key center in 128:", (k_bbox[0] + k_bbox[2]) / 2, (k_bbox[1] + k_bbox[3]) / 2)
