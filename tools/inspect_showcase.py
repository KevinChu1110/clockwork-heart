#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfb84d21"

for name in ["kingfisher", "manta", "firefly"]:
    p = os.path.join(REPO, f"game/assets/sprites/player/showcase/{name}_idle_hd.png")
    if os.path.exists(p):
        im = Image.open(p)
        arr = np.array(im)
        print(f"--- {name} showcase HD ---")
        print(f"Size: {im.size}, Mode: {im.mode}")
        corners = [arr[0,0,3], arr[0,-1,3], arr[-1,0,3], arr[-1,-1,3]]
        print(f"Corners alpha: {corners}")
        bbox = im.getbbox()
        print(f"BBox: {bbox}")
        transparent_px = np.sum(arr[:, :, 3] == 0)
        opaque_px = np.sum(arr[:, :, 3] > 0)
        print(f"Transparent px: {transparent_px}, Opaque px: {opaque_px}")
