#!/usr/bin/env python3
from PIL import Image
import numpy as np

p1 = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/head_unit/ear_boar_rivet_cowl_brass_512.png"
p2 = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_brass.png"

im1 = Image.open(p1).convert("RGBA")
im2 = Image.open(p2).convert("RGBA")

print("im1 (512) bbox:", im1.getbbox())
print("im2 (maple_parts) size:", im2.size, "bbox:", im2.getbbox())

# Let's see what is in im2 at the top-left or top-right
arr2 = np.array(im2)
print("im2 corner (0,0) color:", arr2[0, 0])
print("im2 corner (0,264) color:", arr2[0, 264])
print("im2 corner (199,0) color:", arr2[199, 0])
print("im2 corner (199,264) color:", arr2[199, 264])
