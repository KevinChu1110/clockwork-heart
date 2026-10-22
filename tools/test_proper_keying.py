#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/web/media/hero/char_boar.png").convert("RGBA")
arr = np.array(im)

# Flood fill from the corners or threshold
# Corner color is [246, 230, 197]
# Let's check distance to [247, 232, 200]
bg_dist = np.sqrt(
    (arr[:, :, 0].astype(float) - 247)**2 +
    (arr[:, :, 1].astype(float) - 232)**2 +
    (arr[:, :, 2].astype(float) - 200)**2
)

# Background has small distance, or anything with R > 225, G > 210, B > 175 and low saturation
is_bg = (arr[:, :, 0] > 225) & (arr[:, :, 1] > 210) & (arr[:, :, 2] > 175) & \
        (np.abs(arr[:, :, 0].astype(int) - arr[:, :, 1].astype(int)) < 30) & \
        (np.abs(arr[:, :, 1].astype(int) - arr[:, :, 2].astype(int)) < 45)

print("Total pixels:", arr.shape[0] * arr.shape[1])
print("Background pixels detected:", np.sum(is_bg))

arr_keyed = arr.copy()
arr_keyed[is_bg, 3] = 0
keyed_im = Image.fromarray(arr_keyed, mode="RGBA")
print("Keyed bbox:", keyed_im.getbbox())
keyed_im.save("/tmp/properly_keyed_boar.png")
