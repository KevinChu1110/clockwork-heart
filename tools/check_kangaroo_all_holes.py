from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes

for p in ["idle", "attack", "hit", "recover", "skill", "telegraph"]:
    path = f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/kangaroo/{p}.png"
    im = Image.open(path)
    arr = np.array(im)
    alpha = arr[:, :, 3]
    filled = binary_fill_holes(alpha > 10)
    holes = filled & (alpha <= 10)
    cnt = np.sum(holes)
    print(f"kangaroo {p:10s}: hole pixels = {cnt}")
