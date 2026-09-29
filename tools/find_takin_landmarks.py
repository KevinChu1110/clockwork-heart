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

print("--- Bounding Boxes ---")
print("Head bbox:   ", head_im.getbbox())
print("Optic bbox:  ", optic_im.getbbox())
print("Costume bbox:", costume_im.getbbox())
print("Chassis bbox:", chassis_im.getbbox())
print("Curio bbox:  ", curio_im.getbbox())
print("Key bbox:    ", key_im.getbbox())
print("Weapon bbox: ", wpn_im.getbbox())

composite = Image.open(f"{BASE_DIR}/proof_paperdoll_takin_composite.png").convert("RGBA")
print("Composite bbox:", composite.getbbox())

party_idle = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/takin_idle.png").convert("RGBA")
print("Party idle bbox:", party_idle.getbbox())
arr_shd = np.array(party_idle)
print("Party idle shadow (118..127):", [int(np.sum(arr_shd[y, :, 3] > 20)) for y in range(118, 128)])

# Inspect key center
key_arr = np.array(key_im)
kys, kxs = np.where(key_arr[:, :, 3] > 50)
print(f"Key center: x={np.mean(kxs):.1f}, y={np.mean(kys):.1f}, x-range: {min(kxs)}..{max(kxs)}, y-range: {min(kys)}..{max(kys)}")

# Inspect weapon center / grip
wpn_arr = np.array(wpn_im)
wys, wxs = np.where(wpn_arr[:, :, 3] > 50)
print(f"Weapon center: x={np.mean(wxs):.1f}, y={np.mean(wys):.1f}, x-range: {min(wxs)}..{max(wxs)}, y-range: {min(wys)}..{max(wys)}")

# Inspect head
head_arr = np.array(head_im)
hys, hxs = np.where(head_arr[:, :, 3] > 50)
print(f"Head center: x={np.mean(hxs):.1f}, y={np.mean(hys):.1f}, x-range: {min(hxs)}..{max(hxs)}, y-range: {min(hys)}..{max(hys)}")

# Inspect optic
optic_arr = np.array(optic_im)
oys, oxs = np.where(optic_arr[:, :, 3] > 50)
print(f"Optic center: x={np.mean(oxs):.1f}, y={np.mean(oys):.1f}, x-range: {min(oxs)}..{max(oxs)}, y-range: {min(oys)}..{max(oys)}")
