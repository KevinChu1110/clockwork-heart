from PIL import Image
import numpy as np

comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png").convert("RGBA")
arr = np.array(comp)

steel = (arr[:, :, 3] > 128) & (arr[:, :, 0] > 185) & (arr[:, :, 1] > 185) & (arr[:, :, 2] > 185) & (np.abs(arr[:, :, 0].astype(int) - arr[:, :, 2].astype(int)) < 40)
ys, xs = np.where(steel)

print("Composite steel Y distribution:")
for y in range(0, 128, 8):
    c = np.count_nonzero((ys >= y) & (ys < y + 8))
    if c > 0:
        print(f"y in [{y:2d}..{y+7:2d}]: count={c}")
