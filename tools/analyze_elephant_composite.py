#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

pd_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/elephant"
comp_path = f"{pd_dir}/proof_paperdoll_elephant_composite.png"
comp = Image.open(comp_path).convert("RGBA")
print("Composite size:", comp.size)
print("Composite bbox:", comp.getbbox())

arr = np.array(comp)
print("Margins:")
bbox = comp.getbbox()
print("  Left:", bbox[0])
print("  Top:", bbox[1])
print("  Right:", 128 - bbox[2])
print("  Bottom:", 128 - bbox[3])

# Check shadow row counts (y=118..127)
shadow_counts = []
for y in range(118, 128):
    cnt = int(np.sum(arr[y, :, 3] > 20))
    shadow_counts.append(cnt)
print("Shadow row counts (y=118..127, alpha > 20):", shadow_counts)

# Check colors and check if any boundaries are non-zero
print("Boundary checks:")
print("  Top row y=0 non-zero alpha:", np.sum(arr[0, :, 3] > 0))
print("  Top row y=1 non-zero alpha:", np.sum(arr[1, :, 3] > 0))
print("  Bottom row y=127 non-zero alpha:", np.sum(arr[127, :, 3] > 0))
print("  Bottom row y=126 non-zero alpha:", np.sum(arr[126, :, 3] > 0))
print("  Left col x=0 non-zero alpha:", np.sum(arr[:, 0, 3] > 0))
print("  Left col x=1 non-zero alpha:", np.sum(arr[:, 1, 3] > 0))
print("  Right col x=127 non-zero alpha:", np.sum(arr[:, 127, 3] > 0))
print("  Right col x=126 non-zero alpha:", np.sum(arr[:, 126, 3] > 0))
