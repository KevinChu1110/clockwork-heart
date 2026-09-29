from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes, label

im = Image.open("game/assets/sprites/player/poses/takin/skill.png")
arr = np.array(im)
alpha = arr[:, :, 3]
filled = binary_fill_holes(alpha > 10)
holes = filled & (alpha <= 10)
print("Total holes in current skill:", np.sum(holes))

lbl, num = label(holes)
for i in range(1, num + 1):
    cnt = np.sum(lbl == i)
    if cnt > 10:
        cys, cxs = np.where(lbl == i)
        print(f"Hole component {i}: cnt={cnt}, y in [{min(cys)}..{max(cys)}], x in [{min(cxs)}..{max(cxs)}]")
