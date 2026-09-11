#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from PIL import Image
from check_staff_hit import staff_hit

px = staff_hit.load()
assert px is not None
print("staff_hit pixels between y=35 and y=45:")
for y in range(35, 46):
    row = []
    for x in range(100, 125):
        p = cast(tuple[int, int, int, int], px[x, y])
        if p[3] > 0:
            row.append(f"x={x}:a={p[3]}")
    if row:
        print(f"y={y}: " + ", ".join(row))
    else:
        print(f"y={y}: EMPTY")
