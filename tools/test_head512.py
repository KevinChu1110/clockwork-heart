#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
comp512 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/gecko/idle_512.png").convert("RGBA")
arr = np.array(comp512)

# Head is y <= 250 in 512
head_mask = (arr[:, :, 3] > 20) & (np.arange(512)[:, None] <= 250)
ys, xs = np.where(head_mask)
print(f"Head region y in [{ys.min()}..{ys.max()}], x in [{xs.min()}..{xs.max()}]")
print(f"Full bounding box: ({xs.min()}, {ys.min()}, {xs.max()+1}, {ys.max()+1})")
