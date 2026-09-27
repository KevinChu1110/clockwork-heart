from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes
import glob

for r in ["hedgehog", "otter", "raccoon", "wolf", "seahorse"]:
    for p in ["idle", "attack", "hit", "recover", "skill", "telegraph"]:
        path = f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/{r}/{p}.png"
        im = Image.open(path)
        arr = np.array(im)
        alpha = arr[:, :, 3]
        filled = binary_fill_holes(alpha > 0)
        holes = filled & (alpha == 0)
        cnt = np.sum(holes)
        if cnt > 0:
            print(f"{r:10s} {p:10s}: hole pixels = {cnt}")
