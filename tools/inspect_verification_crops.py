#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

for name in ["verification_crop_eyes.png", "verification_crop_ears.png", "verification_crop_tusks.png", "verification_crop_snout.png"]:
    im = Image.open(f"{BOAR_DIR}/{name}")
    print(f"{name}: size={im.size}, mode={im.mode}")
