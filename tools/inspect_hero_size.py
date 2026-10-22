#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/web/media/hero/char_boar.png")
print("char_boar.png size:", im.size, "mode:", im.mode)
