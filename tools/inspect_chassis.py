from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png")
arr = np.array(im)
print("Unique colors:", len(np.unique(arr.reshape(-1, 4), axis=0)))
# Let's check non-zero alpha pixels
nz = arr[arr[:,:,3] > 0]
print("Non-zero alpha pixels:", len(nz))
print("Sample colors:", nz[::200])

# Also check if there is a rectangle or what part has white pixels
# Let's print rows that have white
for y in range(0, 128, 8):
    row = arr[y, :]
    w = np.where(row[:, 3] > 0)[0]
    if len(w) > 0:
        print(f"y={y}: x from {w[0]} to {w[-1]}, count={len(w)}")
