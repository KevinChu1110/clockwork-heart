#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

comp_path = "game/assets/sprites/player/paperdoll/kingfisher/proof_paperdoll_kingfisher_composite.png"
im = Image.open(comp_path)
arr = np.array(im)
print("Composite size:", im.size)
print("Composite unique colors:", len(np.unique(arr.reshape(-1, 4), axis=0)))
optic_zone = arr[34:56, 42:86]
optic_opaque = optic_zone[:, :, 3] > 8
print("Optic zone unique colors:", len(np.unique(optic_zone[optic_opaque][:, :3], axis=0)))
