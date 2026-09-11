#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from PIL import Image

body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")
px = body_clean.load()
assert px is not None

# Inspect colors around shoulder and chest and hand
print("Colors around right shoulder (x=70..82, y=65..75):")
for y in range(65, 76, 2):
    for x in range(70, 83, 2):
        p = cast(tuple[int,int,int,int], px[x, y])
        if p[3] > 100:
            print(f"({x},{y}): RGBA={p}")

print("\nColors around hand/cuff in idle (x=86..94, y=82..90):")
for y in range(82, 91, 2):
    for x in range(86, 95, 2):
        p = cast(tuple[int,int,int,int], px[x, y])
        if p[3] > 100:
            print(f"({x},{y}): RGBA={p}")
