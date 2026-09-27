#!/usr/bin/env python3
from PIL import Image
import numpy as np

img = Image.open('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/hound/proof_paperdoll_hound_composite.png').convert('RGBA')
arr = np.array(img)
print('Composite size:', img.size, 'bbox:', img.getbbox())
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print('Shadow counts (118..127):', counts)
for y in range(118, 128):
    xs = np.where(arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f'y={y}: min_x={xs[0]}, max_x={xs[-1]}, count={len(xs)}')
