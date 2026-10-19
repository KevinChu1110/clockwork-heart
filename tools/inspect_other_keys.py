#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"

for r in ["rabbit", "fox", "lion"]:
    p = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/{r}/maple_parts/winding_key/key_classic_brass.png"
    im = Image.open(p)
    im.save(f"/tmp/{r}_key_sample.png")
    print(r, im.size, im.getbbox())
