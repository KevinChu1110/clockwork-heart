#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
from cc_helper import get_connected_components

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png")
comps = get_connected_components(im, alpha_thresh=40, y_max=128)
print("wpn_astral_staff.png raw components:")
for i, c in enumerate(comps):
    xs = [x for x, y in c]
    ys = [y for x, y in c]
    print(f"Comp {i+1}: size={len(c)}, bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")
