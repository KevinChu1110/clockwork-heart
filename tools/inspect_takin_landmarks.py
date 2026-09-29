#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/takin"

head_im = Image.open(f"{BASE_DIR}/head_unit/head_takin_brass_twisted_horn_cowl.png").convert("RGBA")
optic_im = Image.open(f"{BASE_DIR}/optic_core/face_takin_emerald_quartz_visors.png").convert("RGBA")
costume_im = Image.open(f"{BASE_DIR}/costume/costume_takin_zen_pioneer_heavy_robe.png").convert("RGBA")
chassis_im = Image.open(f"{BASE_DIR}/chassis/chassis_takin_bronze_cast_default.png").convert("RGBA")
curio_im = Image.open(f"{BASE_DIR}/back_curio/curio_takin_dual_bamboo_oil_flasks.png").convert("RGBA")
key_im = Image.open(f"{BASE_DIR}/winding_key/key_takin_tri_leaf_zen_brass.png").convert("RGBA")
wpn_im = Image.open(f"{BASE_DIR}/weapon/weapon_takin_zen_bamboo_cleaving_axe.png").convert("RGBA")

# Let's inspect significant landmarks
# 1. Horn tips (topmost pixels of head)
h_arr = np.array(head_im)
h_ys, h_xs = np.where(h_arr[:, :, 3] > 50)
print(f"Head top row: min_y={min(h_ys)}")
top_xs = np.where(h_arr[min(h_ys), :, 3] > 50)[0]
print(f"Top row xs: {top_xs}")

# Find left horn tip and right horn tip
horn_l = None
horn_r = None
for y in range(min(h_ys), min(h_ys) + 15):
    xs = np.where(h_arr[y, :, 3] > 50)[0]
    if len(xs) > 0:
        if min(xs) < 55 and horn_l is None:
            horn_l = (min(xs), y)
        if max(xs) > 75 and horn_r is None:
            horn_r = (max(xs), y)

print(f"Horn left tip approx: {horn_l}")
print(f"Horn right tip approx: {horn_r}")

# Head cowl cheeks / bottom
print(f"Head bottom y={max(h_ys)}")

# Chassis shoulders, arms, legs
c_arr = np.array(chassis_im)
c_ys, c_xs = np.where(c_arr[:, :, 3] > 50)
print(f"Chassis y range: {min(c_ys)}..{max(c_ys)}, x range: {min(c_xs)}..{max(c_xs)}")

# Costume shoulders, chest, hem
cs_arr = np.array(costume_im)
cs_ys, cs_xs = np.where(cs_arr[:, :, 3] > 50)
print(f"Costume y range: {min(cs_ys)}..{max(cs_ys)}, x range: {min(cs_xs)}..{max(cs_xs)}")

# Curio flasks
cu_arr = np.array(curio_im)
cu_ys, cu_xs = np.where(cu_arr[:, :, 3] > 50)
print(f"Curio y range: {min(cu_ys)}..{max(cu_ys)}, x range: {min(cu_xs)}..{max(cu_xs)}")

# Weapon axe blade and handle
w_arr = np.array(wpn_im)
w_ys, w_xs = np.where(w_arr[:, :, 3] > 50)
print(f"Weapon y range: {min(w_ys)}..{max(w_ys)}, x range: {min(w_xs)}..{max(w_xs)}")
