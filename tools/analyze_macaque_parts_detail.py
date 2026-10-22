#!/usr/bin/env python3
import os
import glob
from PIL import Image

macaque_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

print("=== Analyzing Macaque Parts ===")
for category in ["chassis", "head_unit", "costume", "weapon", "optic_core", "winding_key", "back_curio"]:
    cat_dir = os.path.join(macaque_dir, category)
    if not os.path.exists(cat_dir):
        print(f"Missing category dir: {category}")
        continue
    print(f"\n--- Category: {category} ---")
    for f in sorted(os.listdir(cat_dir)):
        if f.endswith(".png"):
            p = os.path.join(cat_dir, f)
            im = Image.open(p)
            bbox = im.getbbox()
            print(f"  {f}: size={im.size}, bbox={bbox}")
