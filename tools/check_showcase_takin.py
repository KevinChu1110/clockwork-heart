#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/showcase/takin_idle_hd.png")
print("size:", im.size, "mode:", im.mode)
print("corners:")
print(" (0, 0):", im.getpixel((0, 0)))
print(" (799, 0):", im.getpixel((799, 0)))
print(" (0, 1199):", im.getpixel((0, 1199)))
print(" (799, 1199):", im.getpixel((799, 1199)))
