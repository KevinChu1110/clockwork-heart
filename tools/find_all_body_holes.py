#!/usr/bin/env python3
from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png"
im = Image.open(p).convert("RGBA")
arr = np.array(im)

# 找整個角色主體內部 (x: 150..350, y: 150..450) 的透明洞
body_region = arr[150:450, 150:350, 3]
hole_ys, hole_xs = np.where(body_region == 0)
print(f"Total transparent holes inside body region: {len(hole_ys)}")
if len(hole_ys) > 0:
    print(f"X: {hole_xs.min()+150}..{hole_xs.max()+150}, Y: {hole_ys.min()+150}..{hole_ys.max()+150}")
