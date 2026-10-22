#!/usr/bin/env python3
import os
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

# 載入 512 原畫
# chassis: paint_ivory_stock_512.png
# head_unit: ear_macaque_coaxial_512.png
# costume: costume_dawn_monk_tunic_512.png, costume_zen_striker_512.png
# optic_core: core_cyan_emerald_512.png
# weapon: wpn_spring_claws_512.png
# winding_key: key_classic_brass_512.png
# back_curio: curio_spring_tail.png (128x128)

files_512 = {
    "chassis_ivory": f"{MACAQUE_DIR}/chassis/paint_ivory_stock_512.png",
    "chassis_bronze": f"{MACAQUE_DIR}/chassis/paint_bamboo_bronze_512.png",
    "head_coaxial": f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_512.png",
    "head_bronze": f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_bronze_512.png",
    "head_ivory": f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_ivory_512.png",
    "costume_tunic": f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic_512.png",
    "costume_zen": f"{MACAQUE_DIR}/costume/costume_zen_striker_512.png",
    "core": f"{MACAQUE_DIR}/optic_core/core_cyan_emerald_512.png",
    "weapon": f"{MACAQUE_DIR}/weapon/wpn_spring_claws_512.png",
    "key": f"{MACAQUE_DIR}/winding_key/key_classic_brass_512.png",
    "tail_128": f"{MACAQUE_DIR}/back_curio/curio_spring_tail.png"
}

for name, path in files_512.items():
    if os.path.exists(path):
        im = Image.open(path)
        bbox = im.getbbox()
        print(f"{name:16s}: size={im.size}, bbox={bbox}")
    else:
        print(f"{name:16s}: NOT FOUND at {path}")
