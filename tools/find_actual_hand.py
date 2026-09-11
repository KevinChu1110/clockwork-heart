#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from test_crafted_hit import staff_hit

px = staff_hit.load()
assert px is not None

print("Pixels in staff_hit around hand (colors matching hand / red wrist):")
# In staff_src, hand had red/crimson and bronze colors:
# (77, 12, 19), (103, 25, 29), (135, 88, 58), (155, 104, 65)
hand_pixels = []
for y in range(128):
    for x in range(128):
        p = cast(tuple[int,int,int,int], px[x, y])
        if p[3] > 100:
            # check if it's hand or red wrist
            is_red = (p[0] > 70 and p[1] < 45 and p[2] < 45)
            is_hand = (p[0] > 100 and p[1] > 60 and p[2] < 80 and p[1] > p[2] + 15)
            if is_red or is_hand:
                hand_pixels.append((x, y, p, "red" if is_red else "hand"))

print(f"Total hand/wrist pixels: {len(hand_pixels)}")
for x, y, p, tag in hand_pixels:
    print(f"({x},{y}): {tag} RGBA={p}")
