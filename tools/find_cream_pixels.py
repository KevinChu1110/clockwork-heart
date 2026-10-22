#!/usr/bin/env python3
from PIL import Image
import numpy as np

# Let's inspect the RGB of pixels in /tmp/crop_ur.png
crop = Image.open("/tmp/crop_ur.png").convert("RGBA")
arr = np.array(crop)

# Let's see what layers were pasted in crop_ur.
# In crop_ur_check.py:
# comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png").convert("RGBA")
# Wait! Let's check the pixels of /opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png!
print("proof_maple_boar_composite.png non-zero alphas in region (300..460, 20..180):")
print("Total pixels:", np.sum(arr[:, :, 3] > 0))

# What is the RGB where alpha > 0?
rgb = arr[arr[:, :, 3] > 0][:, :3]
print("Min RGB:", np.min(rgb, axis=0))
print("Max RGB:", np.max(rgb, axis=0))

# Check the three layers: body, head, key
for name in ["body", "head", "key"]:
    layer_crop = Image.open(f"/tmp/crop_ur_{name}.png")
    l_arr = np.array(layer_crop)
    pos_mask = l_arr[:, :, 3] > 0
    if np.any(pos_mask):
        l_rgb = l_arr[pos_mask][:, :3]
        print(f"Layer {name} RGB range: min={np.min(l_rgb, axis=0)}, max={np.max(l_rgb, axis=0)}")
        # Check if there are cream/yellowish pixels
        cream = (l_rgb[:, 0] > 230) & (l_rgb[:, 1] > 220) & (l_rgb[:, 2] > 200)
        print(f"  Layer {name} cream count: {np.sum(cream)}")
