#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

WS_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bdc24189"
im = Image.open(f"{WS_ROOT}/game/assets/sprites/player/party/scarab_idle.png").convert("RGBA")
arr = np.array(im)
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print(f"Scarab party idle shadow counts (118..127): {counts}")
bbox = im.getbbox()
print(f"Scarab party idle bbox: {bbox}")
print(f"Margins: L={bbox[0]}, T={bbox[1]}, R={128-bbox[2]}, B={128-bbox[3]}")
