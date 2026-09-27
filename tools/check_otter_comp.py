import os
from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/proof_paperdoll_otter_composite.png"
im = Image.open(p)
arr = np.array(im)
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("otter composite shadow(118..127):", counts)
print("otter composite bbox:", im.getbbox())
