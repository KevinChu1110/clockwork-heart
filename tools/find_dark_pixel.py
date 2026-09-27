from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/kangaroo/recover.png"
im = Image.open(p)
arr = np.array(im)
alpha = arr[:, :, 3]
rgb = arr[:, :, :3]
dark_mask = (alpha > 50) & (rgb[:, :, 0] < 10) & (rgb[:, :, 1] < 10) & (rgb[:, :, 2] < 10)
ys, xs = np.where(dark_mask)
for y, x in zip(ys, xs):
    print(f"Dark pixel at x={x}, y={y}: rgba={arr[y, x]}")
