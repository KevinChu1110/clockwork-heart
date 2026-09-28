#!/usr/bin/env python3
from typing import cast
from PIL import Image

sc = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/showcase/courser_idle_hd.png")
print("size:", sc.size, "mode:", sc.mode)
c1 = cast(tuple[int, int, int, int], sc.getpixel((0, 0)))
c2 = cast(tuple[int, int, int, int], sc.getpixel((799, 0)))
c3 = cast(tuple[int, int, int, int], sc.getpixel((0, 1199)))
c4 = cast(tuple[int, int, int, int], sc.getpixel((799, 1199)))
print("corners alpha:", c1[3], c2[3], c3[3], c4[3])
