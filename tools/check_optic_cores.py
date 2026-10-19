#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

c1 = Image.open(f"{BOAR_DIR}/optic_core/core_cyan_emerald_512.png")
c2 = Image.open(f"{BOAR_DIR}/optic_core/core_molten_crimson_512.png")
print("core_cyan_emerald_512:", c1.size, c1.getbbox())
print("core_molten_crimson_512:", c2.size, c2.getbbox())
