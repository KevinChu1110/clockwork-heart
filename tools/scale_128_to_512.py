#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

slots = [
    ("key", f"{BOAR_DIR}/winding_key/key_classic_brass.png"),
    ("tail", f"{BOAR_DIR}/back_curio/curio_spring_tail.png"),
    ("chassis", f"{BOAR_DIR}/chassis/paint_brass_gold.png"),
    ("head", f"{BOAR_DIR}/head_unit/ear_boar_rivet_cowl_brass.png"),
    ("costume_harness", f"{BOAR_DIR}/costume/costume_viking_harness.png"),
    ("costume_ironclad", f"{BOAR_DIR}/costume/costume_viking_ironclad.png"),
    ("optic", f"{BOAR_DIR}/optic_core/core_cyan_emerald.png"),
    ("weapon", f"{BOAR_DIR}/weapon/wpn_anvil_greathammer.png"),
]

for name, path in slots:
    im = Image.open(path).convert("RGBA")
    b128 = im.getbbox()
    if b128:
        b512 = (b128[0] * 4, b128[1] * 4, b128[2] * 4, b128[3] * 4)
        print(f"{name:16}: 128 bbox={b128} -> 512 bbox={b512}, 512 size=({b512[2]-b512[0]}, {b512[3]-b512[1]})")
