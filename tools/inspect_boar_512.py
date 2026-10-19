#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

files = [
    "chassis/paint_brass_gold_512.png",
    "chassis/paint_ivory_stock_512.png",
    "chassis/paint_molten_crimson_512.png",
    "head_unit/ear_boar_rivet_cowl_512.png",
    "head_unit/ear_boar_rivet_cowl_brass_512.png",
    "head_unit/ear_boar_rivet_cowl_crimson_512.png",
    "head_unit/ear_boar_rivet_cowl_ivory_512.png",
    "optic_core/core_cyan_emerald_512.png",
    "optic_core/core_molten_crimson_512.png",
    "weapon/wpn_anvil_greathammer_512.png",
    "winding_key/key_classic_brass_512.png",
    "costume/costume_viking_harness_512.png",
    "costume/costume_viking_ironclad_512.png",
    "back_curio/curio_spring_tail.png"
]

for rel in files:
    path = os.path.join(BOAR_DIR, rel)
    if not os.path.exists(path):
        print(f"MISSING: {rel}")
        continue
    im = Image.open(path)
    bbox = im.getbbox()
    print(f"{rel}: size={im.size}, mode={im.mode}, bbox={bbox}")
