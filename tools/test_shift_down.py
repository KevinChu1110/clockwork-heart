#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
RHINO_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rhino"

comp = Image.open(f"{RHINO_DIR}/proof_paperdoll_rhino_composite.png").convert("RGBA")

# Test shifting down by 3 px
shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
shifted.paste(comp, (0, 3), comp)

bbox = shifted.getbbox()
print("Shifted bbox:", bbox)
left, top, right, bottom = bbox[0], bbox[1], 128 - bbox[2], 128 - bbox[3]
print(f"Shifted margins: L={left}, T={top}, R={right}, B={bottom}")

arr = np.array(shifted)
shadow = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print(f"Shadow counts (118..127): {shadow}")
