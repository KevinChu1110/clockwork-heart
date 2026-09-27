from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes, label

p = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/kangaroo/attack.png"
im = Image.open(p)
arr = np.array(im)
alpha = arr[:, :, 3]
filled = binary_fill_holes(alpha > 10)
holes = filled & (alpha <= 10)
lbl, num = label(holes)
for i in range(1, num + 1):
    cys, cxs = np.where(lbl == i)
    print(f"Cluster {i}: count={len(cxs)} center=({cxs.mean():.1f}, {cys.mean():.1f}) X={cxs.min()}..{cxs.max()} Y={cys.min()}..{cys.max()}")
