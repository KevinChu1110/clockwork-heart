from PIL import Image, ImageChops
import numpy as np

im_idle = Image.open("/opt/side/bravesoul-game/proofs/combat_poses_512/proof_combat_pangolin_idle_crop.png")
im_atk = Image.open("/opt/side/bravesoul-game/proofs/combat_poses_512/proof_combat_pangolin_attack_crop.png")
im_hit = Image.open("/opt/side/bravesoul-game/proofs/combat_poses_512/proof_combat_pangolin_hit_crop.png")

print("idle size:", im_idle.size, "mode:", im_idle.mode)
print("atk size:", im_atk.size, "mode:", im_atk.mode)
print("hit size:", im_hit.size, "mode:", im_hit.mode)

arr_idle = np.array(im_idle)
arr_atk = np.array(im_atk)
arr_hit = np.array(im_hit)

print("idle == atk?", np.array_equal(arr_idle[:200, :200], arr_atk[:200, :200]))
print("idle == hit?", np.array_equal(arr_idle[:200, :200], arr_hit[:200, :200]))
