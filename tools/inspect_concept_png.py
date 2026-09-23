#!/usr/bin/env python3
import os
from PIL import Image

for f in sorted(os.listdir("/opt/side/bravesoul-game/docs/art")):
    if "concept" in f and f.endswith(".png"):
        p = os.path.join("/opt/side/bravesoul-game/docs/art", f)
        im = Image.open(p)
        print(f"{f:35s}: size={im.size} mode={im.mode} bbox={im.getbbox()}")
