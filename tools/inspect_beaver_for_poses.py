#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

BASE_DIR = "game/assets/sprites/player/paperdoll/beaver"
comp = Image.open(f"{BASE_DIR}/proof_paperdoll_beaver_composite.png").convert("RGBA")
print("Composite size:", comp.size)
arr = np.array(comp)
shadow_counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Shadow row counts (118..127):", shadow_counts)

bbox = comp.getbbox()
print("Composite bbox:", bbox)
if bbox:
    print(f"Margins: L={bbox[0]}, T={bbox[1]}, R={128-bbox[2]}, B={128-bbox[3]}")

for name in ["chassis", "head_unit", "costume", "optic_core", "weapon", "back_curio", "winding_key"]:
    folder = f"{BASE_DIR}/{name}"
    for f in sorted(os.listdir(folder)):
        if f.endswith(".png") and not f.endswith("_512.png") and not f.startswith("proof"):
            p = Image.open(f"{folder}/{f}").convert("RGBA")
            print(f"{name:12s} ({f}): size={p.size}, bbox={p.getbbox()}")
