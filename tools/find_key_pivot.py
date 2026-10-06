from PIL import Image
import numpy as np

im = Image.open('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/winding_key/key_classic_brass_512.png')
arr = np.array(im)
alpha = arr[:, :, 3]
ys, xs = np.where(alpha > 20)
print('X min-max:', xs.min(), xs.max(), 'center:', (xs.min() + xs.max()) / 2)
print('Y min-max:', ys.min(), ys.max(), 'center:', (ys.min() + ys.max()) / 2)

# Find center of mass or shaft
# In rabbit, the back is on the left side (character faces right/front-right)
# Shaft is on the right side of the key where it connects into the rabbit's back
rightmost_xs = xs[xs > 180]
rightmost_ys = ys[xs > 180]
print('Shaft entry near right edge: x ~', rightmost_xs.mean(), 'y ~', rightmost_ys.mean())
