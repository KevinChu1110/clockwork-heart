#!/usr/bin/env python3
import numpy as np
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/docs/art/xuanji_tortoise_concept.png").convert("RGBA")
# Crop upper left, upper center, upper right
w, h = im.size
# Top left: x in [150, 500], y in [50, 400]
im.crop((150, 50, 500, 400)).save("/tmp/part_top_left.png")
# Top right: x in [700, 1100], y in [50, 400]
im.crop((700, 50, 1100, 400)).save("/tmp/part_top_right.png")
print("Saved parts")
