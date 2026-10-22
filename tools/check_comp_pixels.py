#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png").convert("RGBA")
arr = np.array(im)
print("Image size:", im.size)
# Print min, max of RGB in corners
print("Top-left color:", arr[0, 0])
print("Top-right color:", arr[0, 511])
print("Bottom-left color:", arr[511, 0])
print("Bottom-right color:", arr[511, 511])

# Is there transparency?
print("Has transparency:", np.any(arr[:, :, 3] < 255))
# Check unique alpha values
print("Unique alphas:", np.unique(arr[:, :, 3]))
