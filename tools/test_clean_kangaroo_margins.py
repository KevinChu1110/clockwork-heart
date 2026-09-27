from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/kangaroo/proof_paperdoll_kangaroo_composite.png"
comp = Image.open(p).convert("RGBA")
arr = np.array(comp)

# Clean margins strictly (L>=4, R>=4, T>=4, B>=2)
arr[0:4, :, :] = 0
arr[126:128, :, :] = 0
arr[:, 0:4, :] = 0
arr[:, 124:128, :] = 0

counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Kangaroo cleaned shadow(118..127):", counts)
temp_im = Image.fromarray(arr)
bbox = temp_im.getbbox()
print("Cleaned bbox:", bbox)
print(f"Margins: L={bbox[0]}, T={bbox[1]}, R={128-bbox[2]}, B={128-bbox[3]}")
