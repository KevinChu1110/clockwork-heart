from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes

p = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/kangaroo/idle.png"
im = Image.open(p)
arr = np.array(im)
alpha = arr[:, :, 3]
filled = binary_fill_holes(alpha > 10)
holes = filled & (alpha <= 10)
ys, xs = np.where(holes)
print(f"Total hole pixels: {len(xs)}")
print(f"X range: {xs.min()}..{xs.max()}, Y range: {ys.min()}..{ys.max()}")

# Inspect each hole cluster
from scipy.ndimage import label
lbl, num = label(holes)
print(f"Number of hole clusters: {num}")
for i in range(1, num + 1):
    cys, cxs = np.where(lbl == i)
    print(f"  Cluster {i}: count={len(cxs)}, center=({cxs.mean():.1f}, {cys.mean():.1f}), X={cxs.min()}..{cxs.max()}, Y={cys.min()}..{cys.max()}")
