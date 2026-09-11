#!/usr/bin/env python3
import sys
import os
import math
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from cc_helper import get_connected_components

REPO_ROOT = "/opt/side/bravesoul-game"
OUTPUT_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"

staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")

# 1. Inspect bridging between comp B and comp A in clean_staff
# In wpn_astral_staff.png, comp 1 is (84,40,90,61) and comp 2 is (87,48,107,95).
# If we bridge x=86..98, y=48..56 with bronze bracket/filigree:
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
assert s_px is not None and cs_px is not None
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = cast(tuple[int, int, int, int], s_px[x, y])

# Bridge the staff ring to the gemstone mount in clean_staff:
# Ring is around (84..90, 40..61), gem mount is around (92..104, 50..70).
# Let's inspect the gap between (88, 48..58) and (93, 48..58)
draw_cs = ImageDraw.Draw(clean_staff)
# Bracket connecting ring to mount:
draw_cs.line([(87, 52), (94, 54)], fill=(110, 75, 45, 255), width=2)
draw_cs.line([(87, 58), (95, 62)], fill=(145, 110, 65, 255), width=2)
# Also bridge the shaft gaps at y=96..98 and y=109..116 so the staff is 100% connected
draw_cs.line([(92, 94), (88, 101)], fill=(115, 75, 45, 255), width=2)
draw_cs.line([(88, 106), (90, 119)], fill=(115, 75, 45, 255), width=2)

comps_cs = get_connected_components(clean_staff, alpha_thresh=40, y_max=128)
print(f"clean_staff with bridge components: {len(comps_cs)}")
for i, c in enumerate(comps_cs):
    xs = [pt[0] for pt in c]
    ys = [pt[1] for pt in c]
    print(f"  cs Comp {i+1}: count={len(c)}, bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")
