from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes, label

im = Image.open('/opt/side/bravesoul-game/game/assets/sprites/player/poses/firefly/telegraph.png')
alpha = np.array(im)[:, :, 3]
filled = binary_fill_holes(alpha > 10)
holes = filled & (alpha <= 10)
lbl, num = label(holes)
print(f"Number of hole regions: {num}, total hole px: {np.sum(holes)}")
for i in range(1, num + 1):
    cys, cxs = np.where(lbl == i)
    print(f"Hole {i}: {len(cxs)} px, bbox y:[{min(cys)}, {max(cys)}], x:[{min(cxs)}, {max(cxs)}]")
