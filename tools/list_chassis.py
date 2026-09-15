from PIL import Image
import numpy as np

for r in ["rabbit", "fox", "lion", "boar"]:
    path = f"/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/{r}/chassis"
    import os
    files = os.listdir(path)
    print(r, files)
