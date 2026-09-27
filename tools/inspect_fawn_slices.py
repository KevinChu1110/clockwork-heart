from PIL import Image
import numpy as np
import os

repo = "/opt/side/bravesoul-game"
fawn_base = f"{repo}/game/assets/sprites/player/paperdoll/fawn"

comp_path = f"{fawn_base}/proof_paperdoll_fawn_composite.png"
if os.path.exists(comp_path):
    im = Image.open(comp_path)
    print("Composite size:", im.size, "bbox:", im.getbbox())
    arr = np.array(im)
    shadow = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
    print("Shadow counts (118..127):", shadow)
else:
    print("Composite does not exist!")

for root, dirs, files in os.walk(fawn_base):
    for f in sorted(files):
        if f.endswith(".png") and not f.endswith(".import") and not f.startswith("proof"):
            p = os.path.join(root, f)
            img = Image.open(p)
            print(f"{os.path.relpath(p, fawn_base)}: size={img.size}, bbox={img.getbbox()}")
