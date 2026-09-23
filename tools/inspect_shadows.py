#!/usr/bin/env python3
from PIL import Image
import numpy as np

for r in ["tiger", "bear", "crane", "rabbit", "lion"]:
    p = f"/opt/side/bravesoul-game/game/assets/sprites/player/party/{r}_idle.png"
    im = Image.open(p)
    arr = np.array(im)
    counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(115, 128)]
    print(f"[{r:7s}] bbox={im.getbbox()} shadow(115..127)={counts}")
