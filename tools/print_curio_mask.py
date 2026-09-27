from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/owl/back_curio/curio_owl_floating_micro_orrery.png"
im = Image.open(p).convert("RGBA")
arr = np.array(im)
alpha = arr[:, :, 3]
bb = im.getbbox()
assert bb is not None
sub = alpha[bb[1]:bb[3], bb[0]:bb[2]]
for row in sub:
    line = "".join("#" if v > 20 else "." for v in row)
    print(line)
