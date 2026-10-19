#!/usr/bin/env python3
from PIL import Image
import numpy as np

b = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/body/paint_brass_gold.png").convert("RGBA")
arr = np.array(b)

holes = (arr[150:450, 150:350, 3] == 0)
print(f"Holes inside body/paint_brass_gold.png: {np.sum(holes)}")
