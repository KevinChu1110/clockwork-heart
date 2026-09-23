#!/usr/bin/env python3
import numpy as np
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/docs/art/xuanji_tortoise_concept.png").convert("RGBA")
flipped = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
arr = np.array(flipped)

# Let's inspect rows around the bottom of the turtle in concept art (y around 600..720)
for y in range(600, 720, 15):
    row = arr[y, :]
    non_white = np.where((row[:, 0] < 235) | (row[:, 1] < 235) | (row[:, 2] < 235))[0]
    if len(non_white) > 0:
        print(f"Concept Row {y}: non-white x range [{np.min(non_white)}, {np.max(non_white)}], count={len(non_white)}")
