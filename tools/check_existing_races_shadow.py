import os
from PIL import Image
import numpy as np

races = ["wolf", "hedgehog", "otter", "raccoon", "seahorse"]
for r in races:
    p = f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/{r}/idle.png"
    if os.path.exists(p):
        im = Image.open(p)
        arr = np.array(im)
        counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
        print(f"{r:10s} idle bbox={im.getbbox()} shadow(118..127)={counts}")
