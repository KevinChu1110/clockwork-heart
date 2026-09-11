#!/usr/bin/env python3
from PIL import Image

char_m = Image.open("/opt/side/bravesoul-game/branding/char_macaque.png").convert("RGBA")
print("char_macaque size:", char_m.size)
print("char_macaque bbox:", char_m.getbbox())
