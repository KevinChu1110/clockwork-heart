from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png"
im = Image.open(p).convert("RGBA")
print("Size:", im.size)
arr = np.array(im)
r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

# count steel
steel = (a > 128) & (r > 185) & (g > 185) & (b > 185) & (np.abs(r.astype(int) - b.astype(int)) < 40)
print("Total steel in macaque composite:", np.count_nonzero(steel))

# Where is steel located?
ys, xs = np.where(steel)
print(f"Steel X: [{xs.min()}..{xs.max()}], Y: [{ys.min()}..{ys.max()}]")
