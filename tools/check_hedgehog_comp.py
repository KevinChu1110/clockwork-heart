import os
from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/hedgehog/proof_paperdoll_hedgehog_composite.png"
im = Image.open(p)
arr = np.array(im)
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("hedgehog comp bbox:", im.getbbox())
print("hedgehog comp shadow(118..127):", counts)
