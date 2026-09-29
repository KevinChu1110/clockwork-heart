#!/usr/bin/env python3
import os
import sys
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
race = sys.argv[1] if len(sys.argv) > 1 else "hippo"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/{race}"

chassis_file = None
chassis_dir = os.path.join(PD_DIR, "chassis")
if os.path.isdir(chassis_dir):
    for f in sorted(os.listdir(chassis_dir)):
        if f.startswith("chassis_") and f.endswith(".png") and not f.endswith("_512.png"):
            chassis_file = os.path.join(chassis_dir, f)
            break

if chassis_file and os.path.exists(chassis_file):
    chassis = Image.open(chassis_file).convert("RGBA")
    arr = np.array(chassis)
    print(f"Chassis ({race}) bbox:", chassis.getbbox())
    for y in range(40, 128, 5):
        row_px = np.sum(arr[y, :, 3] > 10)
        xs = np.where(arr[y, :, 3] > 10)[0]
        min_x = xs.min() if len(xs) > 0 else 0
        max_x = xs.max() if len(xs) > 0 else 0
        print(f"y={y:3d}: count={row_px:2d}, x_span=[{min_x:2d}, {max_x:2d}]")
