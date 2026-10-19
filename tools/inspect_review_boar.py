#!/usr/bin/env python3
import os
from PIL import Image

BOAR_REVIEW = "/opt/side/bravesoul-game/proofs/eight_races_paperdoll_review/boar"

for f in sorted(os.listdir(BOAR_REVIEW)):
    if f.endswith(".png"):
        p = os.path.join(BOAR_REVIEW, f)
        im = Image.open(p)
        print(f"{f:38}: size={im.size}, mode={im.mode}, bbox={im.getbbox()}")
