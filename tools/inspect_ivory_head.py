from PIL import Image
import numpy as np

p = 'game/assets/sprites/player/paperdoll/boar/head_unit/ear_boar_rivet_cowl_ivory_512.png'
im = Image.open(p).convert('RGBA')
print("ear_boar_rivet_cowl_ivory_512 bbox:", im.getbbox())

# Let's inspect rows 160 to 250 of ear_boar_rivet_cowl_ivory_512!
arr = np.array(im)
alpha = arr[:, :, 3]
for y in range(160, 250, 5):
    xs = np.where(alpha[y] > 0)[0]
    if len(xs) > 0:
        print(f"y={y}: min_x={xs.min()}, max_x={xs.max()}, count={len(xs)}")
    else:
        print(f"y={y}: EMPTY")
