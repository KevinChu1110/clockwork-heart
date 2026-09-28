#!/usr/bin/env python3
from PIL import Image

sc = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/showcase/sailfish_idle_hd.png")
print("Existing showcase size:", sc.size, "mode:", sc.mode)
c1 = sc.getpixel((0, 0))
c2 = sc.getpixel((799, 0))
c3 = sc.getpixel((0, 1199))
c4 = sc.getpixel((799, 1199))
print("Corners:", c1, c2, c3, c4)
