#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

WS_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bdc24189"
BASE_DIR = f"{WS_ROOT}/game/assets/sprites/player/paperdoll/scarab"

head_im = Image.open(f"{BASE_DIR}/head_unit/head_scarab_quenched_obsidian_cowl.png").convert("RGBA")
optic_im = Image.open(f"{BASE_DIR}/optic_core/face_scarab_amber_crystal_visor.png").convert("RGBA")
costume_im = Image.open(f"{BASE_DIR}/costume/costume_scarab_crucible_artisan_apron.png").convert("RGBA")
chassis_im = Image.open(f"{BASE_DIR}/chassis/chassis_scarab_obsidian_forge_default.png").convert("RGBA")
curio_im = Image.open(f"{BASE_DIR}/back_curio/curio_scarab_twin_vent_exhaust_tail.png").convert("RGBA")
key_im = Image.open(f"{BASE_DIR}/winding_key/key_scarab_crucible_cross_fire_brass.png").convert("RGBA")
wpn_im = Image.open(f"{BASE_DIR}/weapon/weapon_scarab_crucible_obsidian_focus.png").convert("RGBA")

print("Head bbox:", head_im.getbbox())
print("Optic bbox:", optic_im.getbbox())
print("Costume bbox:", costume_im.getbbox())
print("Chassis bbox:", chassis_im.getbbox())
print("Curio bbox:", curio_im.getbbox())
print("Key bbox:", key_im.getbbox())
print("Weapon bbox:", wpn_im.getbbox())

# Let's inspect center of mass / key features
def center_of_mass(img):
    arr = np.array(img)[:, :, 3]
    ys, xs = np.where(arr > 20)
    if len(xs) == 0: return None
    return float(np.mean(xs)), float(np.mean(ys))

print("Key center:", center_of_mass(key_im))
print("Curio center:", center_of_mass(curio_im))
print("Head center:", center_of_mass(head_im))
print("Optic center:", center_of_mass(optic_im))
print("Costume center:", center_of_mass(costume_im))
print("Weapon center:", center_of_mass(wpn_im))
