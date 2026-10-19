#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

iron = Image.open(f"{BOAR_DIR}/costume/costume_viking_ironclad_512.png")
chassis = Image.open(f"{BOAR_DIR}/chassis/paint_brass_gold_512.png")

iron.save("/tmp/raw_ironclad_512.png")
chassis.save("/tmp/raw_chassis_512.png")
print("Saved raw_ironclad_512.png and raw_chassis_512.png")
