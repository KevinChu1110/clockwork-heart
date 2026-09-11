#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from PIL import Image
from cc_helper import get_connected_components

def analyze_staff():
    staff_src = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
    clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_px = staff_src.load()
    cs_px = clean_staff.load()
    assert s_px is not None and cs_px is not None
    for y in range(128):
        for x in range(128):
            if 80 <= x <= 112 and 38 <= y <= 125:
                cs_px[x, y] = cast(tuple[int, int, int, int], s_px[x, y])

    comps = get_connected_components(clean_staff, alpha_thresh=40, y_max=128)
    print(f"clean_staff components: {len(comps)}")
    for i, c in enumerate(comps):
        xs = [pt[0] for pt in c]
        ys = [pt[1] for pt in c]
        print(f"  cs Comp {i+1}: count={len(c)}, bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")

    ws_comps = get_connected_components(staff_src, alpha_thresh=40, y_max=128)
    print(f"staff_src (wpn_astral_staff.png) components: {len(ws_comps)}")
    for i, c in enumerate(ws_comps):
        xs = [pt[0] for pt in c]
        ys = [pt[1] for pt in c]
        print(f"  ws Comp {i+1}: count={len(c)}, bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")

if __name__ == "__main__":
    analyze_staff()
