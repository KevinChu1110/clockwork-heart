#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

base_dir = '/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/seahorse'
comp = Image.open(f'{base_dir}/proof_paperdoll_seahorse_composite.png').convert('RGBA')
print('Composite size:', comp.size, 'bbox:', comp.getbbox())

arr = np.array(comp)
shadow = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print('Composite shadow (118..127):', shadow)

for slot in ['back_curio', 'chassis', 'costume', 'head_unit', 'optic_core', 'weapon', 'winding_key']:
    slot_dir = f'{base_dir}/{slot}'
    files = [f for f in os.listdir(slot_dir) if f.endswith('.png') and not f.endswith('_512.png')]
    for f in files:
        im = Image.open(f'{slot_dir}/{f}').convert('RGBA')
        print(f'{slot:12s} {f:45s} size={im.size} bbox={im.getbbox()}')
