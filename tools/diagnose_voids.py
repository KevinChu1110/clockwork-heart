from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes, label

im = Image.open("game/assets/sprites/player/poses/chameleon/attack.png").convert("RGBA")
arr = np.array(im)
alpha = arr[:, :, 3]
filled = binary_fill_holes(alpha > 10)
holes = filled & (alpha <= 10)
lbl, num = label(holes)

print(f"Attack total holes: {np.sum(holes)}, number of clusters: {num}")
for i in range(1, num + 1):
    cys, cxs = np.where(lbl == i)
    print(f"Cluster {i}: size={len(cxs)}, x in [{cxs.min()}, {cxs.max()}], y in [{cys.min()}, {cys.max()}]")
