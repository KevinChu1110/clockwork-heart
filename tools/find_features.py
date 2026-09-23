#!/usr/bin/env python3
import numpy as np
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/docs/art/xuanji_tortoise_concept.png").convert("RGBA")
print("Concept size:", im.size)

# Find key coordinates in concept
# In concept art, key is at upper right or upper left?
# Let's inspect where the golden key is!
arr = np.array(im)
r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
# Brass gold: r > 180, g > 130, b < 80
brass = (r > 180) & (g > 130) & (b < 80)
ys, xs = np.where(brass)
print(f"Brass pixels total: {len(xs)}")
# Filter for y in top half (y < 400)
top_brass = brass & (np.arange(arr.shape[0])[:, None] < 350)
tys, txs = np.where(top_brass)
print(f"Top brass y in [{np.min(tys)}, {np.max(tys)}], x in [{np.min(txs)}, {np.max(txs)}]")

# Also inspect floating crystal weapon
# Emerald mint: g > 180, r < 140, b > 100
mint = (g > 180) & (r < 140) & (b > 80)
mys, mxs = np.where(mint)
print(f"Mint crystal total: {len(mxs)}")
print(f"Mint y in [{np.min(mys)}, {np.max(mys)}], x in [{np.min(mxs)}, {np.max(mxs)}]")
