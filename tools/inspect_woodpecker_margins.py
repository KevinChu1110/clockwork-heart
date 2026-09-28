#!/usr/bin/env python3
"""
Inspect composite bounding box, margins, and edges.
"""
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/woodpecker"
ref_comp = Image.open(f"{BASE_DIR}/proof_paperdoll_woodpecker_composite.png").convert("RGBA")

arr = np.array(ref_comp)
alpha = arr[:, :, 3]
print("Shape:", arr.shape)
print("BBox:", ref_comp.getbbox())
# Bbox in PIL is (left, upper, right, lower), where right and lower are exclusive!
# So (23, 8, 127, 126) means x ranges from 23 to 126 inclusive (127 exclusive).
# And y ranges from 8 to 125 inclusive (126 exclusive).
print(f"Alpha in col 126: sum = {np.sum(alpha[:, 126] > 0)}")
print(f"Alpha in col 127: sum = {np.sum(alpha[:, 127] > 0)}")
print(f"Alpha in row 126: sum = {np.sum(alpha[126, :] > 0)}")
print(f"Alpha in row 127: sum = {np.sum(alpha[127, :] > 0)}")
print(f"Alpha in col 0: sum = {np.sum(alpha[:, 0] > 0)}")
print(f"Alpha in col 1: sum = {np.sum(alpha[:, 1] > 0)}")
print(f"Alpha in row 0: sum = {np.sum(alpha[0, :] > 0)}")
print(f"Alpha in row 1: sum = {np.sum(alpha[1, :] > 0)}")

# Check Rule 4c-5 / 16:
# Safe margins: left >= 4, top >= 4, right >= 4, bottom >= 2
# left = 23 (>= 4), top = 8 (>= 4)
# 128 - right = 128 - 127 = 1 (wait! 128 - 127 = 1 < 4!)
# Let's check where the rightmost pixels come from!
for slot in ["weapon", "chassis", "head_unit", "costume", "optic_core", "back_curio", "winding_key"]:
    p = os.path.join(BASE_DIR, slot, [f for f in os.listdir(os.path.join(BASE_DIR, slot)) if f.endswith(".png") and not f.endswith("_512.png")][0])
    im = Image.open(p)
    bx = im.getbbox()
    print(f"Slot {slot:12s}: bbox = {bx}, right margin = {128 - bx[2]}")
