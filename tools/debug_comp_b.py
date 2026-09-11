#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from PIL import Image
from check_staff_hit import staff_hit

px = staff_hit.load()
assert px is not None
print("Pixels in bbox (105, 27, 123, 37):")
for y in range(27, 38):
    for x in range(105, 124):
        p = cast(tuple[int,int,int,int], px[x, y])
        if p[3] > 40:
            print(f"({x},{y}): {p}")
