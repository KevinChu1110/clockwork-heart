from PIL import Image
import numpy as np

f78 = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/macaque_real_02_attack_f0078.png").convert("RGBA")
arr = np.array(f78)

# Check y in [380..500], x in [150..430]
box = arr[380:501, 150:431]
r, g, b = box[:, :, 0].astype(int), box[:, :, 1].astype(int), box[:, :, 2].astype(int)

# Let's inspect where the monkey is in this box:
# Where is the monkey in f78?
# Let's print min, max of R, G, B in this box:
print("box shape:", box.shape)
print("max R in box:", r.max(), "max G in box:", g.max(), "max B in box:", b.max())

# Where did the steel pixels in f78 go?
# Let's find all steel pixels on the player side in f78 (x in [100, 500], y in [200, 500])
crop_player = arr[200:501, 100:501]
pr, pg, pb = crop_player[:, :, 0].astype(int), crop_player[:, :, 1].astype(int), crop_player[:, :, 2].astype(int)
steel = (pr > 185) & (pg > 185) & (pb > 185) & (np.abs(pr - pb) < 40)
ys, xs = np.where(steel)
print(f"Total steel in player area (y200..500, x100..500): {len(ys)}")
if len(ys) > 0:
    print(f"Y range of steel: [{ys.min()+200}..{ys.max()+200}], X range: [{xs.min()+100}..{xs.max()+100}]")
