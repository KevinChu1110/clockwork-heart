import os
from PIL import Image
import numpy as np

base = 'game/assets/sprites/player/paperdoll/stoat'
comp = Image.open(f'{base}/proof_paperdoll_stoat_composite.png')
arr = np.array(comp)

# Let's inspect rows/cols for key features
head = Image.open(f'{base}/head_unit/head_stoat_aerodynamic_hood_ears.png')
optic = Image.open(f'{base}/optic_core/face_stoat_sapphire_crosshair_lens.png')
chassis = Image.open(f'{base}/chassis/chassis_stoat_ivory_tinplate_default.png')
weapon = Image.open(f'{base}/weapon/weapon_stoat_crescent_dagger.png')
curio = Image.open(f'{base}/back_curio/curio_stoat_flexible_segmented_tail.png')
key = Image.open(f'{base}/winding_key/key_stoat_whirlwind_tri_ring_brass.png')

print("head bbox:", head.getbbox())
print("optic bbox:", optic.getbbox())
print("chassis bbox:", chassis.getbbox())
print("weapon bbox:", weapon.getbbox())
print("curio bbox:", curio.getbbox())
print("key bbox:", key.getbbox())

# Let's find optic eyes centers
o_arr = np.array(optic)
# find non-transparent pixels in optic
oy, ox = np.where(o_arr[:, :, 3] > 100)
print(f"optic pixels x range: {ox.min()}..{ox.max()}, y range: {oy.min()}..{oy.max()}")
# Find left eye and right eye
left_eye = (int(ox[ox < 64].mean()), int(oy[ox < 64].mean()))
right_eye = (int(ox[ox > 64].mean()), int(oy[ox > 64].mean()))
print("left eye approx:", left_eye, "right eye approx:", right_eye)

# Foot contact
c_arr = np.array(chassis)
cy, cx = np.where(c_arr[:, :, 3] > 100)
feet_y = cy.max()
print("feet y:", feet_y)
feet_x_left = cx[(cx < 64) & (cy > 110)]
# Curio tail detail
curio_arr = np.array(curio)
cy_idx, cx_idx = np.where(curio_arr[:, :, 3] > 50)
print(f"curio y: {cy_idx.min()}..{cy_idx.max()}, x: {cx_idx.min()}..{cx_idx.max()}")
print("top y x:", cx_idx[cy_idx == cy_idx.min()])
print("bot y x:", cx_idx[cy_idx == cy_idx.max()])

