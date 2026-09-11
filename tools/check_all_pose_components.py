#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
from cc_helper import get_connected_components

FOX_POSES_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"
for p in ["idle", "telegraph", "attack", "recover", "skill", "hit"]:
    im = Image.open(f"{FOX_POSES_DIR}/{p}.png")
    comps = get_connected_components(im, alpha_thresh=40, y_max=118)
    print(f"\nPose [{p}]: {len(comps)} components (alpha > 40, y < 118)")
    for i, c in enumerate(comps):
        xs = [pt[0] for pt in c]
        ys = [pt[1] for pt in c]
        print(f"  Comp {i+1}: count={len(c)}, bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")
