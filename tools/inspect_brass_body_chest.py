#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PARTS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar/maple_parts"

b = Image.open(f"{PARTS_DIR}/body/paint_brass_gold.png").convert("RGBA")
crop = b.crop((180, 250, 260, 340))
crop.save("/tmp/brass_body_chest.png")
print("Saved /tmp/brass_body_chest.png")
