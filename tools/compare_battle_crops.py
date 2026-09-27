from PIL import Image, ImageChops
import numpy as np

idle_crop = Image.open("/opt/side/bravesoul-game/proofs/combat_poses_512/proof_combat_cat_idle_crop.png")
atk_crop = Image.open("/opt/side/bravesoul-game/proofs/combat_poses_512/proof_combat_cat_attack_crop.png")
hit_crop = Image.open("/opt/side/bravesoul-game/proofs/combat_poses_512/proof_combat_cat_hit_crop.png")

diff_atk = ImageChops.difference(idle_crop, atk_crop)
diff_hit = ImageChops.difference(idle_crop, hit_crop)

print("Idle vs Attack crop diff bbox:", diff_atk.getbbox())
print("Idle vs Hit crop diff bbox:", diff_hit.getbbox())
