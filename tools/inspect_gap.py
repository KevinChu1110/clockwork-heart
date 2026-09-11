import os
import sys
from PIL import Image
from typing import cast

sys.path.insert(0, "/opt/side/bravesoul-game")
from tools.cc_helper import get_connected_components

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/skill.png")
comps = get_connected_components(im, alpha_thresh=40, y_max=118)
c0_set = set(comps[0])
c1_set = set(comps[1])

px = im.load()
# Check border between c0 and c1
min_dist = 999
closest = None
for x1, y1 in c1_set:
    for x0, y0 in c0_set:
        d = max(abs(x1 - x0), abs(y1 - y0))
        if d < min_dist:
            min_dist = d
            closest = ((x1, y1), (x0, y0))

print("Min Chebyshev distance between c0 and c1:", min_dist)
print("Closest pixels:", closest)
p1, p0 = closest
print(f"c1 pixel {p1}: alpha={px[p1[0], p1[1]][3]}")
print(f"c0 pixel {p0}: alpha={px[p0[0], p0[1]][3]}")

# Let's inspect pixels around (p1, p0)
for y in range(min(p1[1], p0[1]) - 1, max(p1[1], p0[1]) + 2):
    row = []
    for x in range(min(p1[0], p0[0]) - 1, max(p1[0], p0[0]) + 2):
        row.append(f"{px[x, y][3]:3d}")
    print(f"y={y}: " + " ".join(row))
