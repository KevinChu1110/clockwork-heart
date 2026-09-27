from PIL import Image
import numpy as np

REPO = "/opt/side/bravesoul-game"
p = f"{REPO}/game/assets/sprites/player/paperdoll/owl/back_curio/curio_owl_floating_micro_orrery.png"
im = Image.open(p).convert("RGBA")
arr = np.array(im)
alpha = arr[:, :, 3]
bb = im.getbbox()
assert bb is not None
print("bbox:", bb)
print("corners of bbox:")
for y in [bb[1], bb[3]-1]:
    for x in [bb[0], bb[2]-1]:
        print(f"({x}, {y}): RGBA={tuple(arr[y, x])}")
