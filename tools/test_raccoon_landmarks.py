#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

base = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/raccoon"
tail = Image.open(f"{base}/back_curio/curio_raccoon_coaxial_ring_antenna_tail.png")
t_arr = np.array(tail)

print("Tail non-zero pixels by segment:")
# Check y ranges
for y_band in [(63, 72), (73, 82), (83, 93)]:
    mask = (t_arr[y_band[0]:y_band[1], :, 3] > 50)
    ys, xs = np.where(mask)
    if len(xs) > 0:
        print(f"Y band {y_band}: count={len(xs)}, x range={xs.min()}..{xs.max()}, avg_x={xs.mean():.1f}, avg_y={ys.mean() + y_band[0]:.1f}")

# Check weapon pixels
weapon = Image.open(f"{base}/weapon/weapon_raccoon_anti_gravity_pulse_blaster.png")
w_arr = np.array(weapon)
ys, xs = np.where(w_arr[:, :, 3] > 50)
print(f"Weapon: count={len(xs)}, x range={xs.min()}..{xs.max()}, y range={ys.min()}..{ys.max()}, center=({xs.mean():.1f}, {ys.mean():.1f})")

# Check key pixels
key = Image.open(f"{base}/winding_key/key_raccoon_quad_solar_sail.png")
k_arr = np.array(key)
ys, xs = np.where(k_arr[:, :, 3] > 50)
print(f"Key: count={len(xs)}, x range={xs.min()}..{xs.max()}, y range={ys.min()}..{ys.max()}, center=({xs.mean():.1f}, {ys.mean():.1f})")
