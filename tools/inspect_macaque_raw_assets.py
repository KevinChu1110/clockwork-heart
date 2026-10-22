#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

files = [
    f"{MACAQUE_DIR}/chassis/paint_ivory_stock_512.png",
    f"{MACAQUE_DIR}/chassis/paint_bamboo_bronze_512.png",
    f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_512.png",
    f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_bronze_512.png",
    f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_ivory_512.png",
    f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic_512.png",
    f"{MACAQUE_DIR}/costume/costume_zen_striker_512.png",
    f"{MACAQUE_DIR}/weapon/wpn_spring_claws_512.png",
    f"{MACAQUE_DIR}/optic_core/core_cyan_emerald_512.png",
]

for p in files:
    if not os.path.exists(p):
        print("MISSING:", p)
        continue
    im = Image.open(p).convert("RGBA")
    bbox = im.getbbox()
    print(f"{os.path.basename(p):35s}: size={im.size}, bbox={bbox}")
