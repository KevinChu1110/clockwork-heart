#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bat"

# Load slices
head_im = Image.open(f"{BASE_DIR}/head_unit/head_bat_sonar_parabolic_crest.png").convert("RGBA")
core_im = Image.open(f"{BASE_DIR}/optic_core/face_bat_dual_amber_optic_lens.png").convert("RGBA")
chassis_im = Image.open(f"{BASE_DIR}/chassis/chassis_bat_astral_polymer_default.png").convert("RGBA")
costume_im = Image.open(f"{BASE_DIR}/costume/costume_bat_orbital_stealth_harness.png").convert("RGBA")
weapon_im = Image.open(f"{BASE_DIR}/weapon/weapon_bat_superconducting_pulse_dart.png").convert("RGBA")
key_im = Image.open(f"{BASE_DIR}/winding_key/key_bat_orbital_pulsar_key.png").convert("RGBA")
curio_im = Image.open(f"{BASE_DIR}/back_curio/curio_bat_articulated_starwing_mantle.png").convert("RGBA")

# Measure landmarks
print("Head bbox:", head_im.getbbox())
print("Chassis bbox:", chassis_im.getbbox())
print("Weapon bbox:", weapon_im.getbbox())
print("Curio bbox:", curio_im.getbbox())
print("Key bbox:", key_im.getbbox())

# Let's find specific points
# Eye locations in core_im
c_arr = np.array(core_im)
ys, xs = np.where(c_arr[:, :, 3] > 100)
# Group into left eye and right eye
left_eye_mask = xs < 64
right_eye_mask = xs >= 64
lx, ly = np.mean(xs[left_eye_mask]), np.mean(ys[left_eye_mask])
rx, ry = np.mean(xs[right_eye_mask]), np.mean(ys[right_eye_mask])
print(f"Left eye center: ({lx:.1f}, {ly:.1f}), Right eye center: ({rx:.1f}, {ry:.1f})")

# Ear tips in head_im
h_arr = np.array(head_im)
h_ys, h_xs = np.where(h_arr[:, :, 3] > 100)
# Left ear tip (lowest y where xs < 64)
left_ear_pts = [(x, y) for x, y in zip(h_xs, h_ys) if x < 64]
left_ear_tip = min(left_ear_pts, key=lambda p: p[1])
right_ear_pts = [(x, y) for x, y in zip(h_xs, h_ys) if x >= 64]
right_ear_tip = min(right_ear_pts, key=lambda p: p[1])
print(f"Left ear tip: {left_ear_tip}, Right ear tip: {right_ear_tip}")

# Feet in chassis_im
ch_arr = np.array(chassis_im)
f_ys, f_xs = np.where(ch_arr[:, :, 3] > 100)
feet_pts = [(x, y) for x, y in zip(f_xs, f_ys) if y >= 110]
l_foot = [(x, y) for x, y in feet_pts if x < 64]
r_foot = [(x, y) for x, y in feet_pts if x >= 64]
print(f"Left foot mean: ({np.mean([p[0] for p in l_foot]):.1f}, {np.mean([p[1] for p in l_foot]):.1f})")
print(f"Right foot mean: ({np.mean([p[0] for p in r_foot]):.1f}, {np.mean([p[1] for p in r_foot]):.1f})")
