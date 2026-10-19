#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
OUT_DEBUG = "/tmp/boar_debug_parts"
os.makedirs(OUT_DEBUG, exist_ok=True)

parts = {
    "chassis_brass": f"{BOAR_DIR}/chassis/paint_brass_gold_512.png",
    "chassis_ivory": f"{BOAR_DIR}/chassis/paint_ivory_stock_512.png",
    "chassis_crimson": f"{BOAR_DIR}/chassis/paint_molten_crimson_512.png",
    "head_brass": f"{BOAR_DIR}/head_unit/ear_boar_rivet_cowl_brass_512.png",
    "head_base": f"{BOAR_DIR}/head_unit/ear_boar_rivet_cowl_512.png",
    "key_512": f"{BOAR_DIR}/winding_key/key_classic_brass_512.png",
    "key_128": f"{BOAR_DIR}/winding_key/key_classic_brass.png",
    "core_cyan": f"{BOAR_DIR}/optic_core/core_cyan_emerald_512.png",
    "core_crimson": f"{BOAR_DIR}/optic_core/core_molten_crimson_512.png",
    "costume_ironclad": f"{BOAR_DIR}/costume/costume_viking_ironclad_512.png",
    "costume_harness": f"{BOAR_DIR}/costume/costume_viking_harness_512.png",
    "weapon": f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png",
    "tail": f"{BOAR_DIR}/back_curio/curio_spring_tail.png",
    "composite_128": f"{BOAR_DIR}/proof_paperdoll_boar_composite.png"
}

for name, path in parts.items():
    if os.path.exists(path):
        im = Image.open(path)
        print(f"{name:16}: size={im.size}, bbox={im.getbbox()}")
        # save cropped
        bbox = im.getbbox()
        if bbox:
            cropped = im.crop(bbox)
            cropped.save(f"{OUT_DEBUG}/{name}_crop.png")
