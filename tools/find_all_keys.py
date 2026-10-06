import os
from PIL import Image
import numpy as np

races = ["rabbit", "lion", "fox", "macaque", "boar", "bear", "penguin", "tortoise", "fawn"]
root = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll"

for r in races:
    d = os.path.join(root, r, "winding_key")
    if not os.path.exists(d):
        continue
    for f in os.listdir(d):
        if f.endswith("_512.png"):
            p = os.path.join(d, f)
            im = Image.open(p)
            arr = np.array(im)
            alpha = arr[:, :, 3]
            ys, xs = np.where(alpha > 20)
            if len(xs) > 0:
                # 320 coords
                cx_320 = ((xs.min() + xs.max()) / 2) * 320 / 512
                cy_320 = ((ys.min() + ys.max()) / 2) * 320 / 512
                print(f"{r:10s} {f:40s} bbox 512: ({xs.min()},{ys.min()})-({xs.max()},{ys.max()}) center 320: ({cx_320:.1f}, {cy_320:.1f})")
