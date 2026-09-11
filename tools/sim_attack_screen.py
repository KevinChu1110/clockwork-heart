from PIL import Image
import numpy as np

# Load f10
f10 = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/macaque_real_01_idle_f0010.png").convert("RGBA")
# Load the newly crafted attack pose
atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")

# In battle, PlayerBody is scaled to 200x200
atk_200 = atk.resize((200, 200), Image.Resampling.LANCZOS)

# In f10, PlayerBody was at X=224, Y=250.
# During attack lunge, PlayerBody moves to X=224+42=266 (or lunge offset), Y=250.
# Let's composite atk_200 onto a copy of f10 at X=266, Y=250:
sim_screen = f10.copy()
# Clear old player area in sim_screen with background or just paste
sim_screen.paste(atk_200, (266, 250), atk_200)

arr_sim = np.array(sim_screen)
# Reviewer box: y in [380..500], x in [150..430]
crop_sim = arr_sim[380:501, 150:431]
r = crop_sim[:, :, 0].astype(int)
g = crop_sim[:, :, 1].astype(int)
b = crop_sim[:, :, 2].astype(int)
steel_sim = (r > 185) & (g > 185) & (b > 185) & (np.abs(r - b) < 40)
cnt_sim = np.count_nonzero(steel_sim)

print(f"Simulated attack frame steel pixels in reviewer box: {cnt_sim}")
print(f"Target is > 2265 (idle was 2265). Diff = {cnt_sim - 2265}")
