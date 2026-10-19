#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

for name in ["proof_paperdoll_boar_composite.png", "proof_chassis_swap_boar.png", "proof_boar_variants_matrix.png", "proof_boar_costume_comparison.png"]:
    p = f"{BOAR_DIR}/{name}"
    im = Image.open(p)
    print(name, im.size, im.mode)
