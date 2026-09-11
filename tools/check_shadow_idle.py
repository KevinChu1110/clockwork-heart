import os
from PIL import Image
import numpy as np

for r in ["rabbit", "lion", "fox", "boar", "macaque"]:
    for i in [0, 1]:
        p = f"/tmp/test_idle_{r}_{i}.png"
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
            arr = np.array(im)
            # check alpha at bottom rows
            bottom_alpha = arr[118:, :, 3]
            dark_bottom = (bottom_alpha > 20).sum()
            print(f"{r} set {i}: size={im.size}, bottom dark pixels={dark_bottom}")
