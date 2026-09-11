#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from PIL import Image
from check_staff_hit import staff_hit
from cc_helper import get_connected_components

comps = get_connected_components(staff_hit, alpha_thresh=40, y_max=118)
px = staff_hit.load()
assert px is not None

for i, c in enumerate(comps):
    colors = [cast(tuple[int,int,int,int], px[x, y]) for x, y in c]
    avg_r = sum(col[0] for col in colors) / len(colors)
    avg_g = sum(col[1] for col in colors) / len(colors)
    avg_b = sum(col[2] for col in colors) / len(colors)
    xs = [x for x, y in c]
    ys = [y for x, y in c]
    print(f"sh Comp {i+1}: size={len(c)}, bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)}), avg_rgb=({avg_r:.1f}, {avg_g:.1f}, {avg_b:.1f})")
