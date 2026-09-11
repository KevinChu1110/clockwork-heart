#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from PIL import Image

staff_src = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
px = staff_src.load()
assert px is not None

print("clean_staff y=55..75:")
for y in range(55, 75):
    row = []
    for x in range(80, 112):
        p = cast(tuple[int,int,int,int], px[x, y])
        if p[3] > 40:
            row.append(f"{x}:{p[3]}")
    print(f"y={y}: " + " ".join(row))
