#!/usr/bin/env python3
from PIL import Image
import numpy as np

# Load head
head = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_brass.png").convert("RGBA")
arr_h = np.array(head)

# Load body
body = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/body/paint_brass_gold.png").convert("RGBA")
arr_b = np.array(body)

# In head, find pixels where R > 220, G > 210, B > 190 and alpha > 0
cream_h = (arr_h[:, :, 0] > 220) & (arr_h[:, :, 1] > 210) & (arr_h[:, :, 2] > 190) & (arr_h[:, :, 3] > 0)
print("Head cream pixels count:", np.sum(cream_h))

# In body, find pixels where R > 220, G > 210, B > 190 and alpha > 0
cream_b = (arr_b[:, :, 0] > 220) & (arr_b[:, :, 1] > 210) & (arr_b[:, :, 2] > 190) & (arr_b[:, :, 3] > 0)
print("Body cream pixels count:", np.sum(cream_b))

# Let's see where cream pixels in head are located:
ys_h, xs_h = np.where(cream_h)
if len(ys_h) > 0:
    print(f"Head cream Y: {ys_h.min()}..{ys_h.max()}, X: {xs_h.min()}..{xs_h.max()}")

# Let's see where cream pixels in body are located:
ys_b, xs_b = np.where(cream_b)
if len(ys_b) > 0:
    print(f"Body cream Y: {ys_b.min()}..{ys_b.max()}, X: {xs_b.min()}..{xs_b.max()}")
