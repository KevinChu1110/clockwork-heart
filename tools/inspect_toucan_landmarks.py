#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/toucan"

head_im = Image.open(f"{BASE_DIR}/head_unit/head_toucan_prism_bill_visor_cowl.png").convert("RGBA")
optic_im = Image.open(f"{BASE_DIR}/optic_core/face_toucan_emerald_quartz_monocle.png").convert("RGBA")
costume_im = Image.open(f"{BASE_DIR}/costume/costume_toucan_vine_valley_scout_harness.png").convert("RGBA")
chassis_im = Image.open(f"{BASE_DIR}/chassis/chassis_toucan_canopy_alloy_default.png").convert("RGBA")
curio_im = Image.open(f"{BASE_DIR}/back_curio/curio_toucan_segmented_copper_rudder_tail.png").convert("RGBA")
key_im = Image.open(f"{BASE_DIR}/winding_key/key_toucan_tri_vane_canopy_rotor_brass.png").convert("RGBA")
wpn_im = Image.open(f"{BASE_DIR}/weapon/weapon_toucan_canopy_prism_pneumatic_arquebus.png").convert("RGBA")

# Let's inspect features on head_im
h_arr = np.array(head_im)
h_a = h_arr[:, :, 3]

# Crest feathers (top apex)
cys, cxs = np.where((h_a > 50) & (h_arr[:, :, 1] > 180) & (h_arr[:, :, 0] < 120))
print(f"Crest y-range: {min(cys)}..{max(cys)}, x-range: {min(cxs)}..{max(cxs)}, center: ({np.mean(cxs):.1f}, {np.mean(cys):.1f})")

# Bill tip (right-most)
bys, bxs = np.where(h_a > 50)
max_bx = max(bxs)
max_by = int(np.mean(bys[bxs == max_bx]))
print(f"Bill rightmost tip: ({max_bx}, {max_by})")

# Bill base & jaw
jys, jxs = np.where((h_a > 50) & (np.arange(128)[:, None] > 50) & (np.arange(128)[None, :] > 75))
print(f"Bill jaw lowest: x={np.mean(jxs):.1f}, y={max(jys)}")

# Optic eye centers
o_arr = np.array(optic_im)
oys, oxs = np.where(o_arr[:, :, 3] > 50)
l_xs = oxs[oxs < 64]
r_xs = oxs[oxs >= 64]
print(f"Left eye: ({np.mean(l_xs):.1f}, {np.mean(oys[oxs < 64]):.1f}), Right eye: ({np.mean(r_xs):.1f}, {np.mean(oys[oxs >= 64]):.1f})")

# Chassis feet / claws
c_arr = np.array(chassis_im)
c_a = c_arr[:, :, 3]
fys, fxs = np.where((c_a > 50) & (np.arange(128)[:, None] > 100))
fl_xs = fxs[fxs < 64]
fr_xs = fxs[fxs >= 64]
print(f"Left foot: ({np.mean(fl_xs):.1f}, {np.mean(fys[fxs < 64]):.1f}), Right foot: ({np.mean(fr_xs):.1f}, {np.mean(fys[fxs >= 64]):.1f})")

# Curio tail feathers
cu_arr = np.array(curio_im)
cuys, cuxs = np.where(cu_arr[:, :, 3] > 50)
print(f"Curio x-range: {min(cuxs)}..{max(cuxs)}, y-range: {min(cuys)}..{max(cuys)}")

# Weapon grip & muzzle
w_arr = np.array(wpn_im)
wys, wxs = np.where(w_arr[:, :, 3] > 50)
max_wx = max(wxs)
max_wy = int(np.mean(wys[wxs == max_wx]))
print(f"Weapon muzzle tip: ({max_wx}, {max_wy})")
# Grip: x~84..88, y~76..80
print(f"Weapon total range: x in {min(wxs)}..{max(wxs)}, y in {min(wys)}..{max(wys)}")
