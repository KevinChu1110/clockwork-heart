#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
from verify_fox_action_poses import measure_staff_linearity

hit_bb = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/hit.png")
print("bb91222 hit.png staff linearity:", measure_staff_linearity(hit_bb))

px = hit_bb.load()
for y in range(30, 124):
    xs = []
    for x in range(hit_bb.width):
        p = px[x, y]
        if p[3] > 120 and (120 <= p[0] <= 195 and 75 <= p[1] <= 155 and 25 <= p[2] <= 95):
            xs.append(x)
    if xs and len(xs) <= 14:
        print(f"y={y}: xs={xs}, center={sum(xs)/len(xs):.1f}")
