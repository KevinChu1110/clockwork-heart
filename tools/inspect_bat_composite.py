#!/usr/bin/env python3
from PIL import Image
import numpy as np

img = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/bat/proof_paperdoll_bat_composite.png").convert("RGBA")
arr = np.array(img)
shadow_counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Shadow row counts (118..127):", shadow_counts)
bbox = img.getbbox()
print("Composite bbox:", bbox)
print("Margins: L=", bbox[0], "T=", bbox[1], "R=", 128 - bbox[2], "B=", 128 - bbox[3])
