#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

base = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/raccoon"

head = Image.open(f"{base}/head_unit/head_raccoon_parabolic_radar_dish.png")
key = Image.open(f"{base}/winding_key/key_raccoon_quad_solar_sail.png")
tail = Image.open(f"{base}/back_curio/curio_raccoon_coaxial_ring_antenna_tail.png")
chassis = Image.open(f"{base}/chassis/chassis_raccoon_orbit_aqua_default.png")
optic = Image.open(f"{base}/optic_core/face_raccoon_hud_polarizer_visor.png")
costume = Image.open(f"{base}/costume/costume_raccoon_space_explorer_harness.png")
weapon = Image.open(f"{base}/weapon/weapon_raccoon_anti_gravity_pulse_blaster.png")

print("Head bbox:", head.getbbox())
print("Key bbox:", key.getbbox())
print("Tail bbox:", tail.getbbox())
print("Chassis bbox:", chassis.getbbox())
print("Optic bbox:", optic.getbbox())
print("Costume bbox:", costume.getbbox())
print("Weapon bbox:", weapon.getbbox())

# Let's inspect optic core points
opt_arr = np.array(optic)
ys, xs = np.where(opt_arr[:, :, 3] > 100)
print(f"Optic core y range: {ys.min()}..{ys.max()}, x range: {xs.min()}..{xs.max()}")
print(f"Optic core center: ({xs.mean():.1f}, {ys.mean():.1f})")

# Let's inspect weapon center
wpn_arr = np.array(weapon)
ys, xs = np.where(wpn_arr[:, :, 3] > 100)
print(f"Weapon y range: {ys.min()}..{ys.max()}, x range: {xs.min()}..{xs.max()}")
print(f"Weapon center: ({xs.mean():.1f}, {ys.mean():.1f})")

# Let's inspect key center
key_arr = np.array(key)
ys, xs = np.where(key_arr[:, :, 3] > 100)
print(f"Key y range: {ys.min()}..{ys.max()}, x range: {xs.min()}..{xs.max()}")
print(f"Key center: ({xs.mean():.1f}, {ys.mean():.1f})")

# Let's inspect tail center and root
tail_arr = np.array(tail)
ys, xs = np.where(tail_arr[:, :, 3] > 100)
print(f"Tail y range: {ys.min()}..{ys.max()}, x range: {xs.min()}..{xs.max()}")
print(f"Tail center: ({xs.mean():.1f}, {ys.mean():.1f})")
