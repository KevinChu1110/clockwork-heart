#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from PIL import Image

staff_src = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
px = staff_src.load()
assert px is not None

print("wpn_astral_staff all colored pixels overview:")
for y in range(38, 125):
    for x in range(80, 112):
        p = cast(tuple[int,int,int,int], px[x, y])
        if p[3] > 100 and p[1] > p[0] + 20: # green/cyan crystal
            print(f"Crystal at ({x},{y}): {p}")
            break
