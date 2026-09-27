#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

base_dir = '/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/seahorse'
comp = Image.open(f'{base_dir}/proof_paperdoll_seahorse_composite.png').convert('RGBA')

# Clean margins strictly to see actual valid ground shadow
w, h = comp.size
c_clean = comp.copy()
px = c_clean.load()
for x in range(w):
    px[x, 0] = (0, 0, 0, 0)
    px[x, 1] = (0, 0, 0, 0)
    px[x, 2] = (0, 0, 0, 0)
    px[x, 3] = (0, 0, 0, 0)
    px[x, 126] = (0, 0, 0, 0)
    px[x, 127] = (0, 0, 0, 0)
for y in range(h):
    px[0, y] = (0, 0, 0, 0)
    px[1, y] = (0, 0, 0, 0)
    px[2, y] = (0, 0, 0, 0)
    px[3, y] = (0, 0, 0, 0)
    px[124, y] = (0, 0, 0, 0)
    px[125, y] = (0, 0, 0, 0)
    px[126, y] = (0, 0, 0, 0)
    px[127, y] = (0, 0, 0, 0)

arr = np.array(c_clean)
shadow = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Cleaned composite ground shadow row counts (118..127):", shadow)
print("Cleaned bbox:", c_clean.getbbox())
