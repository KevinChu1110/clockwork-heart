#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")
w, h = im.size

# Let's inspect where pixels are
print(f"Canvas size: {w}x{h}")
# Non-transparent bbox
print(f"Opaque bbox: {im.getbbox()}")

# Let's check arm coordinates:
# Left arm (character's right): x ~ 27..42, y ~ 45..95
# Right arm (character's left): x ~ 78..99, y ~ 45..95
# Head: x ~ 30..88, y ~ 13..55
# Torso/belly: x ~ 40..78, y ~ 55..100
# Feet/legs: x ~ 40..75, y ~ 100..124
