from PIL import Image
import numpy as np

img = Image.open('game/assets/sprites/player/stoat_idle_x3.png')
arr = np.array(img)
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print('stoat_idle_x3 shadow counts (118..127):', counts)

comp = Image.open('game/assets/sprites/player/paperdoll/stoat/proof_paperdoll_stoat_composite.png')
arr2 = np.array(comp)
counts2 = [int(np.sum(arr2[y, :, 3] > 20)) for y in range(118, 128)]
print('composite shadow counts (118..127):', counts2)

# Check margins
bbox = img.getbbox()
print('stoat_idle_x3 bbox:', bbox, 'margins: L=', bbox[0], 'T=', bbox[1], 'R=', 128 - bbox[2], 'B=', 128 - bbox[3])
