#!/usr/bin/env python3
import os
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

print("Key bbox:", key.getbbox())
print("Weapon bbox:", weapon.getbbox())
print("Curio bbox:", curio.getbbox())
print("Optic bbox:", optic.getbbox())
print("Head bbox:", head.getbbox())
print("Costume bbox:", costume.getbbox())
print("Chassis bbox:", chassis.getbbox())

# find centers of mass of key, weapon, optic
for name, img in [("key", key), ("weapon", weapon), ("curio", curio), ("optic", optic), ("head", head), ("costume", costume)]:
    arr = np.array(img)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 20)
    print(f"{name:10s} center of mass: x={np.mean(xs):.1f}, y={np.mean(ys):.1f}")
