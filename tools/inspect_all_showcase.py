import os
from PIL import Image
import numpy as np

showcase_dir = "game/assets/sprites/player/showcase"
for f in sorted(os.listdir(showcase_dir)):
    if f.endswith(".png"):
        p = os.path.join(showcase_dir, f)
        img = Image.open(p)
        arr = np.array(img)
        alpha = arr[:, :, 3]
        cols = np.where(alpha.max(axis=0) > 0)[0]
        rows = np.where(alpha.max(axis=1) > 0)[0]
        x_min, x_max = cols[0], cols[-1]
        y_min, y_max = rows[0], rows[-1]
        print(f"{f:25s}: size={img.size}, X=[{x_min}..{x_max}] (margin L={x_min}, R={img.size[0]-1-x_max}), Y=[{y_min}..{y_max}] (margin T={y_min}, B={img.size[1]-1-y_max})")
