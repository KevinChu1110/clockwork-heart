#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
LION_PARTS = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion/maple_parts"

for p in ["body/paint_brass_gold.png", "costume/costume_royal_guard.png", "costume/costume_nutcracker_guard.png", "weapon/wpn_knight_lance.png"]:
    im = Image.open(f"{LION_PARTS}/{p}")
    print(p, im.size, im.getbbox())
    im.save(f"/tmp/lion_debug_{os.path.basename(p)}")
