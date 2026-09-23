#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

w, h = 128, 128
clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
cs_d = ImageDraw.Draw(clean_shadow)
cs_d.ellipse([64 - 36, 115 - 5, 64 + 36, 115 + 5], fill=(31, 26, 58, 130))
clean_shadow = clean_shadow.filter(ImageFilter.GaussianBlur(1.4))

arr = np.array(clean_shadow)
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Simulated shadow row counts (y=118..127):", counts)

# Also let's check the master composite shadow counts:
comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/elephant/proof_paperdoll_elephant_composite.png")
c_arr = np.array(comp)
master_counts = [int(np.sum(c_arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Master composite shadow row counts (y=118..127):", master_counts)
