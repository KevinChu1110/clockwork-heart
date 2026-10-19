#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png").convert("RGBA")
arr = np.array(im)

sub = arr[175:205, 220:250]
print("Snout region RGB sample:")
for y in range(0, sub.shape[0], 3):
    row = ""
    for x in range(0, sub.shape[1], 3):
        r, g, b, a = sub[y, x]
        if a == 0:
            row += "  . "
        else:
            row += f"{r:3d} "
    print(f"y={175+y}: {row}")
