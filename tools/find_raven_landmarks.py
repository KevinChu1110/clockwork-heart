#!/usr/bin/env python3
from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/raven"

comp = Image.open(f"{p}/proof_paperdoll_raven_composite.png")
head = Image.open(f"{p}/head_unit/head_raven_astronomer_hood_beak.png")
chassis = Image.open(f"{p}/chassis/chassis_raven_obsidian_brass_default.png")
optic = Image.open(f"{p}/optic_core/face_raven_astrolabe_monocle_lens.png")
costume = Image.open(f"{p}/costume/costume_raven_horologist_scholar_robe.png")
curio = Image.open(f"{p}/back_curio/curio_raven_articulated_steampunk_wings.png")
weapon = Image.open(f"{p}/weapon/weapon_raven_armillary_wand.png")
key = Image.open(f"{p}/winding_key/key_raven_armillary_sphere_brass.png")

def center_of_mass(im):
    arr = np.array(im)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 20)
    if len(xs) == 0:
        return (0, 0)
    return (int(round(np.mean(xs))), int(round(np.mean(ys))))

print("head center:", center_of_mass(head), "bbox:", head.getbbox())
print("chassis center:", center_of_mass(chassis), "bbox:", chassis.getbbox())
print("optic center:", center_of_mass(optic), "bbox:", optic.getbbox())
print("costume center:", center_of_mass(costume), "bbox:", costume.getbbox())
print("curio (wings) center:", center_of_mass(curio), "bbox:", curio.getbbox())
print("weapon center:", center_of_mass(weapon), "bbox:", weapon.getbbox())
print("key center:", center_of_mass(key), "bbox:", key.getbbox())

# find beak / snout tip
head_arr = np.array(head)
# find rightmost or forward protruding point of beak
ys, xs = np.where(head_arr[:, :, 3] > 100)
# look at beak area y=38..52
beak_pts = [(x, y) for y, x in zip(ys, xs) if 35 <= y <= 55]
beak_tip = max(beak_pts, key=lambda pt: pt[0])
print("beak tip:", beak_tip)

# find eyes
opt_arr = np.array(optic)
ys, xs = np.where(opt_arr[:, :, 3] > 100)
print("optic points x min..max:", min(xs), max(xs), "y min..max:", min(ys), max(ys))
