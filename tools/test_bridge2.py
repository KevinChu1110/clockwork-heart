#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from PIL import Image, ImageDraw
from cc_helper import get_connected_components

staff_src = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
assert s_px is not None and cs_px is not None
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = cast(tuple[int, int, int, int], s_px[x, y])

draw_cs = ImageDraw.Draw(clean_staff)
# Connect ring to mount solidly
# In wpn_astral_staff.png, mount is at x=98..105, y=55..65, crystal is at 85..106, 48..58.
# Ring is at x=84..90, y=40..61.
# Let's draw connecting bracket at (87, 56) to (100, 58)
draw_cs.polygon([(86, 54), (99, 56), (99, 60), (86, 58)], fill=(120, 80, 50, 255))
draw_cs.line([(86, 54), (99, 56)], fill=(50, 30, 20, 255), width=1)
draw_cs.line([(86, 58), (99, 60)], fill=(50, 30, 20, 255), width=1)

draw_cs.line([(92, 94), (88, 101)], fill=(115, 75, 45, 255), width=2)
draw_cs.line([(88, 106), (90, 119)], fill=(115, 75, 45, 255), width=2)

comps_cs = get_connected_components(clean_staff, alpha_thresh=40, y_max=128)
print(f"clean_staff with solid bridge components: {len(comps_cs)}")
for i, c in enumerate(comps_cs):
    xs = [pt[0] for pt in c]
    ys = [pt[1] for pt in c]
    print(f"  cs Comp {i+1}: count={len(c)}, bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")
