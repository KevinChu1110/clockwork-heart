from PIL import Image
import numpy as np

optic = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/optic_core/core_cyan_emerald.png")
arr = np.array(optic)
alpha = arr[:,:,3]
ys, xs = np.where(alpha > 0)
print(f"optic core: y from {ys.min()} to {ys.max()}, x from {xs.min()} to {xs.max()}, count={len(ys)}")
print("optic colors:", np.unique(arr[alpha > 0], axis=0)[:5])
