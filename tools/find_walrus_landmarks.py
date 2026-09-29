#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/walrus"

head_im = Image.open(f"{BASE_DIR}/head_unit/head_walrus_tungsten_tusk_cowl.png").convert("RGBA")
optic_im = Image.open(f"{BASE_DIR}/optic_core/face_walrus_quartz_dome_eyes.png").convert("RGBA")
costume_im = Image.open(f"{BASE_DIR}/costume/costume_walrus_abyssal_peacoat_cuirass.png").convert("RGBA")
chassis_im = Image.open(f"{BASE_DIR}/chassis/chassis_walrus_icebreaker_alloy_default.png").convert("RGBA")
curio_im = Image.open(f"{BASE_DIR}/back_curio/curio_walrus_dual_ballast_tanks.png").convert("RGBA")
key_im = Image.open(f"{BASE_DIR}/winding_key/key_walrus_anchor_handwheel_brass.png").convert("RGBA")
wpn_im = Image.open(f"{BASE_DIR}/weapon/weapon_walrus_abyssal_icebreaker_cutlass.png").convert("RGBA")

print("--- Bounding Boxes ---")
print("Head bbox:   ", head_im.getbbox())
print("Optic bbox:  ", optic_im.getbbox())
print("Costume bbox:", costume_im.getbbox())
print("Chassis bbox:", chassis_im.getbbox())
print("Curio bbox:  ", curio_im.getbbox())
print("Key bbox:    ", key_im.getbbox())
print("Weapon bbox: ", wpn_im.getbbox())

# Let's inspect features on head:
# Tusk tips, cowl top, cheeks, snout
head_arr = np.array(head_im)
head_alpha = head_arr[:, :, 3]
ys, xs = np.where(head_alpha > 50)
print(f"Head y-range: {min(ys)} .. {max(ys)}, x-range: {min(xs)} .. {max(xs)}")

# Tusks are lowest part of head_unit (near max ys)
tusk_ys, tusk_xs = np.where((head_alpha > 50) & (head_arr[:, :, 1] > 180) & (head_arr[:, :, 0] > 180))
# Let's find bottom-most points of head
print(f"Head lowest points (tusks?): y={max(ys)}")
low_xs = np.where(head_alpha[max(ys), :] > 50)[0]
print(f"Lowest x points at y={max(ys)}: {low_xs}")

# Optic eyes
optic_arr = np.array(optic_im)
optic_alpha = optic_arr[:, :, 3]
oys, oxs = np.where(optic_alpha > 50)
print(f"Optic y-range: {min(oys)} .. {max(oys)}, x-range: {min(oxs)} .. {max(oxs)}")
# Left eye, Right eye centers
left_eye_xs = oxs[oxs < 64]
right_eye_xs = oxs[oxs >= 64]
print(f"Left eye center: x={np.mean(left_eye_xs):.1f}, Right eye center: x={np.mean(right_eye_xs):.1f}, y={np.mean(oys):.1f}")

# Weapon: handle / grip point
wpn_arr = np.array(wpn_im)
wys, wxs = np.where(wpn_arr[:, :, 3] > 50)
print(f"Weapon y-range: {min(wys)} .. {max(wys)}, x-range: {min(wxs)} .. {max(wxs)}")
# Grip is usually near bottom-left of weapon
grip_ys, grip_xs = np.where((wpn_arr[:, :, 3] > 50) & (wpn_arr[:, :, 0] > 150) & (wpn_arr[:, :, 1] < 150))
print(f"Weapon grip area: x~{np.mean(wxs[wys > 75]):.1f}, y~{np.mean(wys[wys > 75]):.1f}")

# Key: center hub
key_arr = np.array(key_im)
kys, kxs = np.where(key_arr[:, :, 3] > 50)
print(f"Key center: x={np.mean(kxs):.1f}, y={np.mean(kys):.1f}")
