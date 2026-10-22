#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO = "/opt/side/bravesoul-game"
COMP_PATH = f"{REPO}/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png"
comp = Image.open(COMP_PATH).convert("RGBA")
w, h = comp.size
print(f"Composite size: {w}x{h}")

# Check alpha and colors in upper-right quadrant (x: 256..512, y: 0..256)
arr = np.array(comp)
print("Upper-right non-transparent count:", np.sum(arr[0:256, 256:512, 3] > 0))

# Also check each individual part image and its bounding box
parts = [
    "body/paint_brass_gold.png",
    "head_unit/ear_boar_rivet_cowl.png",
    "eyes/eyes_cyan_emerald.png",
    "costume/costume_viking_harness.png",
    "weapon/wpn_anvil_greathammer.png",
    "winding_key/key_classic_brass.png",
    "back_curio/curio_spring_tail.png",
]
for p in parts:
    full_p = f"{REPO}/game/assets/sprites/player/paperdoll/boar/maple_parts/{p}"
    if os.path.exists(full_p):
        im = Image.open(full_p)
        bbox = im.getbbox()
        print(f"{p}: size={im.size}, mode={im.mode}, bbox={bbox}")
    else:
        print(f"{p}: NOT FOUND")
