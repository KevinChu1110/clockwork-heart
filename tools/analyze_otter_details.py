#!/usr/bin/env python3
import numpy as np
from PIL import Image

wpn_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/weapon/weapon_otter_abyssal_anchor_cleaver.png"
wpn = Image.open(wpn_path).convert("RGBA")
bbox = wpn.getbbox()
print("Weapon bbox:", bbox)
arr = np.array(wpn)
alpha = arr[:, :, 3]
ys, xs = np.where(alpha > 20)
print(f"Weapon non-transparent: x in [{xs.min()}, {xs.max()}], y in [{ys.min()}, {ys.max()}]")
print(f"Center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")

# Look at head and eyes
head_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/head_unit/head_otter_diver_bell_visor.png"
head = Image.open(head_path).convert("RGBA")
print("Head bbox:", head.getbbox())

optic_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/optic_core/face_otter_phosphor_green_gauges.png"
optic = Image.open(optic_path).convert("RGBA")
print("Optic bbox:", optic.getbbox())
o_arr = np.array(optic)
o_ys, o_xs = np.where(o_arr[:, :, 3] > 20)
print(f"Optic pixels: x in [{o_xs.min()}, {o_xs.max()}], y in [{o_ys.min()}, {o_ys.max()}]")
