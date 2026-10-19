#!/usr/bin/env python3
import os
from PIL import Image

for p in ["web/media/hero/char_boar.png", "web/media/hero/boar_idle.png"]:
    full = os.path.join("/opt/side/bravesoul-game", p)
    if os.path.exists(full):
        im = Image.open(full)
        print(f"{p}: size={im.size}, bbox={im.getbbox()}")
    else:
        print(f"Missing: {p}")
