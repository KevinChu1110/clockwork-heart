from PIL import Image
import numpy as np

f10 = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/macaque_real_01_idle_f0010.png").convert("RGBA")
comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png").convert("RGBA")

# Resize comp to 200x200
comp_200 = comp.resize((200, 200), Image.Resampling.LANCZOS)
arr_f = np.array(f10)
arr_c = np.array(comp_200)

mask_c = arr_c[:, :, 3] > 100

best_d = 1e9
best_pos = None

# Search in f10 around player slot
for y in range(150, 300):
    for x in range(150, 300):
        sub = arr_f[y:y+200, x:x+200]
        diff = np.mean(np.abs(sub[mask_c, :3].astype(int) - arr_c[mask_c, :3].astype(int)))
        if diff < best_d:
            best_d = diff
            best_pos = (x, y)

print(f"PlayerBody exact position in f0010: X={best_pos[0]}, Y={best_pos[1]}, diff={best_d:.2f}")
