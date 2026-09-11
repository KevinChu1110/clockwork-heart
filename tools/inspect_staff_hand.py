#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from PIL import Image

staff_src = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
px = staff_src.load()
assert px is not None

print("staff_src pixels around (88..96, 80..87):")
for y in range(80, 88):
    for x in range(88, 97):
        p = cast(tuple[int,int,int,int], px[x, y])
        if p[3] > 40:
            print(f"({x},{y}): {p}")
