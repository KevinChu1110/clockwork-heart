from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/owl/idle_512.png").convert("RGBA")
arr = np.array(im)
# Find pixels where alpha > 0 and color is near dark navy
mask = (arr[:, :, 3] > 50) & (arr[:, :, 0] < 40) & (arr[:, :, 1] < 40) & (arr[:, :, 2] < 70)
print("Count in idle_512:", np.sum(mask))
ys, xs = np.where(mask)
print(f"idle_512 dark pixels: x in [{xs.min()}, {xs.max()}], y in [{ys.min()}, {ys.max()}]")
