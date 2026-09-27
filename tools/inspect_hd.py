#!/usr/bin/env python3
from PIL import Image

p = "/opt/side/bravesoul-game/game/assets/sprites/player/showcase/hedgehog_idle_hd.png"
im = Image.open(p)
print(f"{p}: size={im.size}, mode={im.mode}, bbox={im.getbbox()}")
