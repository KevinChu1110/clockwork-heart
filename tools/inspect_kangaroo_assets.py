import os
from PIL import Image
import numpy as np

base_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/kangaroo"
print("=== Kangaroo Paperdoll Assets Inspection ===")
for root, dirs, files in os.walk(base_dir):
    for f in sorted(files):
        if f.endswith(".png"):
            p = os.path.join(root, f)
            im = Image.open(p)
            print(f"{f:55s} {im.size} bbox={im.getbbox()}")

comp_path = os.path.join(base_dir, "proof_paperdoll_kangaroo_composite.png")
if os.path.exists(comp_path):
    comp = Image.open(comp_path).convert("RGBA")
    arr = np.array(comp)
    print(f"\nComposite bbox: {comp.getbbox()}")
    shadow_counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"Shadow counts (y=118..127): {shadow_counts}")
    # check dark pixels in composite
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]
    dark_pixels = np.sum((alpha > 20) & (np.max(rgb, axis=-1) < 10))
    print(f"Ultra-dark pixels (<10) with alpha>20: {dark_pixels}")
