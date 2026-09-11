from PIL import Image
import numpy as np

f78 = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/macaque_real_02_attack_f0078.png").convert("RGBA")
arr78 = np.array(f78)

# In f78, find where player pixels are:
# PlayerSlot: let's check non-background in x in [150..550], y in [200..600]
crop78 = arr78[200:600, 150:550]
r, g, b = crop78[:, :, 0].astype(int), crop78[:, :, 1].astype(int), crop78[:, :, 2].astype(int)
steel = (r > 185) & (g > 185) & (b > 185) & (np.abs(r - b) < 40)
ys, xs = np.where(steel)
print("f78 [150..550, 200..600] total steel:", len(ys))
if len(ys) > 0:
    print(f"X: [{xs.min()+150}..{xs.max()+150}], Y: [{ys.min()+200}..{ys.max()+200}]")
