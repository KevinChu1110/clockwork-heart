#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from PIL import Image

# Let's inspect wpn_astral_staff.png to see why y=96..98 is empty in wpn_astral_staff.png
staff_src = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
px = staff_src.load()
assert px is not None

print("Checking alphas across y in wpn_astral_staff.png:")
for y in range(90, 105):
    row = [(x, cast(tuple[int,int,int,int], px[x, y])[3]) for x in range(80, 110) if cast(tuple[int,int,int,int], px[x, y])[3] > 0]
    print(f"y={y}: {row}")
