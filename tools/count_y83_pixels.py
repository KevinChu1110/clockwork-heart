from PIL import Image
import numpy as np

atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")
arr = np.array(atk)

non_zero = np.count_nonzero(arr[83:, :, 3] > 80)
print(f"Total non-transparent pixels in y >= 83: {non_zero}")

# In comp:
comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png").convert("RGBA")
arr_c = np.array(comp)
non_zero_c = np.count_nonzero(arr_c[83:, :, 3] > 80)
print(f"Total non-transparent pixels in comp in y >= 83: {non_zero_c}")
