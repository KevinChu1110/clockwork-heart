import os
from PIL import Image
import numpy as np

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/wolf"
comp = Image.open(f"{BASE}/proof_paperdoll_wolf_composite.png")
print("Composite size:", comp.size, "bbox:", comp.getbbox())

slices = ["chassis", "head_unit", "winding_key", "costume", "optic_core", "weapon", "back_curio"]
for s in slices:
    files = [f for f in os.listdir(f"{BASE}/{s}") if f.endswith(".png") and not f.endswith("_512.png")]
    for f in sorted(files):
        im = Image.open(f"{BASE}/{s}/{f}")
        arr = np.array(im)
        alpha = arr[:, :, 3] > 20
        ys, xs = np.where(alpha)
        cy, cx = np.mean(ys), np.mean(xs)
        print(f"{s:12s} {f:45s} size={im.size} bbox={im.getbbox()} center=({cx:.1f}, {cy:.1f})")

# Check ground shadow counts
comp_arr = np.array(comp)
shadow_counts = [int(np.sum(comp_arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Wolf Composite ground shadow (118..127):", shadow_counts)
