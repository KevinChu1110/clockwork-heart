#!/usr/bin/env python3
from PIL import Image
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/courser"

chassis = Image.open(f"{BASE_DIR}/chassis/chassis_courser_cream_gold_default.png").convert("RGBA")
head = Image.open(f"{BASE_DIR}/head_unit/head_courser_brass_chanfron_mane.png").convert("RGBA")
costume = Image.open(f"{BASE_DIR}/costume/costume_courser_dawn_patrol_cuirass.png").convert("RGBA")
optic = Image.open(f"{BASE_DIR}/optic_core/face_courser_sapphire_optic_lens.png").convert("RGBA")
weapon = Image.open(f"{BASE_DIR}/weapon/weapon_courser_cavalry_saber.png").convert("RGBA")
curio = Image.open(f"{BASE_DIR}/back_curio/curio_courser_articulated_spring_tail.png").convert("RGBA")
key = Image.open(f"{BASE_DIR}/winding_key/key_courser_baroque_trefoil_gold.png").convert("RGBA")

# 檢查 optic 的中心
opt_arr = np.array(optic)
ys, xs = np.where(opt_arr[:, :, 3] > 50)
print(f"Optic y range: {min(ys)}..{max(ys)}, x range: {min(xs)}..{max(xs)}")
# 雙眼大概在哪裡
left_eye_xs = xs[xs < 64]
left_eye_ys = ys[xs < 64]
right_eye_xs = xs[xs >= 64]
right_eye_ys = ys[xs >= 64]
print(f"Left eye center: ({np.mean(left_eye_xs):.1f}, {np.mean(left_eye_ys):.1f})")
print(f"Right eye center: ({np.mean(right_eye_xs):.1f}, {np.mean(right_eye_ys):.1f})")

# 檢查 weapon 的手柄位置
wpn_arr = np.array(weapon)
wys, wxs = np.where(wpn_arr[:, :, 3] > 50)
print(f"Weapon y range: {min(wys)}..{max(wys)}, x range: {min(wxs)}..{max(wxs)}")

# 檢查 key
key_arr = np.array(key)
kys, kxs = np.where(key_arr[:, :, 3] > 50)
print(f"Key y range: {min(kys)}..{max(kys)}, x range: {min(kxs)}..{max(kxs)}")
