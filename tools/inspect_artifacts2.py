#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO = "/opt/side/bravesoul-game"

# Check where the rectangular cutout might be in comp or individual parts
comp = Image.open(f"{REPO}/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png").convert("RGBA")
comp_arr = np.array(comp)

# Look at alpha channel around x: 300..512, y: 0..250
# Are there straight horizontal or vertical lines of alpha in the image?
alpha = comp_arr[:, :, 3]

# Check edges in alpha
for y in range(0, 250):
    diffs = np.diff(alpha[y, :])
    large_jumps = np.where(np.abs(diffs) > 200)[0]
    # check if there is a vertical edge across many rows
    
# Let's save a visual map of alpha
alpha_img = Image.fromarray(alpha)
alpha_img.save("/tmp/comp_alpha.png")
print("Saved /tmp/comp_alpha.png")

# Also let's inspect the eyes:
eyes_im = Image.open(f"{REPO}/game/assets/sprites/player/paperdoll/boar/maple_parts/eyes/eyes_cyan_emerald.png")
print(f"eyes_cyan_emerald bbox: {eyes_im.getbbox()}")

# Also let's check rabbit, fox, and lion eyes to compare how they were done!
for race in ["rabbit", "fox", "lion"]:
    race_dir = f"{REPO}/game/assets/sprites/player/paperdoll/{race}/maple_parts/eyes"
    if os.path.exists(race_dir):
        print(f"Race {race} eyes: {os.listdir(race_dir)}")
        e1 = Image.open(f"{race_dir}/eyes_cyan_emerald.png")
        print(f"  {race} eyes_cyan_emerald size={e1.size}, bbox={e1.getbbox()}")
