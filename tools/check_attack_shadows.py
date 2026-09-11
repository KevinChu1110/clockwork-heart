import os
from PIL import Image
import numpy as np

for r in ["rabbit", "lion", "fox", "boar", "macaque"]:
    if r == "rabbit":
        p = "game/assets/sprites/player/poses/attack.png"
    else:
        p = f"game/assets/sprites/player/poses/{r}/attack.png"
    im = Image.open(p).convert("RGBA")
    arr = np.array(im)
    bottom_alpha = arr[118:, :, 3]
    dark_bottom = (bottom_alpha > 20).sum()
    print(f"{r} attack: size={im.size}, bottom dark pixels={dark_bottom}")
