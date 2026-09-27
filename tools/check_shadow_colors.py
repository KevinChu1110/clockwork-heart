#!/usr/bin/env python3
from PIL import Image
import numpy as np

base_dir = '/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/seahorse'
comp = Image.open(f'{base_dir}/proof_paperdoll_seahorse_composite.png').convert('RGBA')
arr = np.array(comp)
for y in range(118, 126):
    row_pixels = arr[y, :, :]
    mask = row_pixels[:, 3] > 20
    colors = row_pixels[mask]
    if len(colors) > 0:
        print(f'y={y}: count={len(colors)}, mean_rgb={np.mean(colors[:, :3], axis=0)}, mean_a={np.mean(colors[:, 3])}')
