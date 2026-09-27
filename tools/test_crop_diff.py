from PIL import Image
import numpy as np

idle = np.array(Image.open("/opt/side/bravesoul-game/proofs/combat_poses_512/proof_combat_cat_idle_crop.png"))
atk = np.array(Image.open("/opt/side/bravesoul-game/proofs/combat_poses_512/proof_combat_cat_attack_crop.png"))

min_h = min(idle.shape[0], atk.shape[0])
min_w = min(idle.shape[1], atk.shape[1])

diff = np.abs(idle[:min_h, :min_w].astype(int) - atk[:min_h, :min_w].astype(int))
print("Diff pixels idle vs atk:", np.sum(np.any(diff > 0, axis=-1)))
