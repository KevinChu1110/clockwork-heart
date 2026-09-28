#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/gecko"

chassis = Image.open(f"{BASE_DIR}/chassis/chassis_gecko_brass_patina_default.png").convert("RGBA")
head = Image.open(f"{BASE_DIR}/head_unit/head_gecko_conduit_scout_crest_cowl.png").convert("RGBA")
optic = Image.open(f"{BASE_DIR}/optic_core/face_gecko_dual_slit_aperture_quartz_lens.png").convert("RGBA")
costume = Image.open(f"{BASE_DIR}/costume/costume_gecko_highpressure_stealth_harness.png").convert("RGBA")
curio = Image.open(f"{BASE_DIR}/back_curio/curio_gecko_segmented_gear_balance_tail.png").convert("RGBA")
weapon = Image.open(f"{BASE_DIR}/weapon/weapon_gecko_conduit_ratchet_dart.png").convert("RGBA")
key = Image.open(f"{BASE_DIR}/winding_key/key_gecko_dual_ring_relief_valve_brass.png").convert("RGBA")

# Let's inspect head top, snout, optic
h_arr = np.array(head)
h_ys, h_xs = np.where(h_arr[:, :, 3] > 20)
print(f"Head top: x={h_xs[h_ys.argmin()]}, y={h_ys.min()}")
print(f"Head bottom: x={h_xs[h_ys.argmax()]}, y={h_ys.max()}")

o_arr = np.array(optic)
o_ys, o_xs = np.where(o_arr[:, :, 3] > 20)
print(f"Optic y-range: [{o_ys.min()}..{o_ys.max()}], x-range: [{o_xs.min()}..{o_xs.max()}]")
# find left and right slits
mid_x = int(o_xs.mean())
l_mask = (o_arr[:, :, 3] > 20) & (np.arange(128)[None, :] < mid_x)
r_mask = (o_arr[:, :, 3] > 20) & (np.arange(128)[None, :] >= mid_x)
ly, lx = np.where(l_mask)
ry, rx = np.where(r_mask)
print(f"Left slit center: ({lx.mean():.1f}, {ly.mean():.1f}), Right slit center: ({rx.mean():.1f}, {ry.mean():.1f})")

# Tail landmarks
u_arr = np.array(curio)
u_ys, u_xs = np.where(u_arr[:, :, 3] > 20)
print(f"Tail tip (leftmost): ({u_xs.min()}, {u_ys[u_xs.argmin()]})")
print(f"Tail root (rightmost): ({u_xs.max()}, {u_ys[u_xs.argmax()]})")

# Chassis feet
c_arr = np.array(chassis)
c_ys, c_xs = np.where(c_arr[:, :, 3] > 20)
feet_mask = (c_arr[:, :, 3] > 20) & (np.arange(128)[:, None] > 110)
fy, fx = np.where(feet_mask)
fl_mask = fx < 64
fr_mask = fx >= 64
print(f"Left foot center: ({fx[fl_mask].mean():.1f}, {fy[fl_mask].mean():.1f})")
print(f"Right foot center: ({fx[fr_mask].mean():.1f}, {fy[fr_mask].mean():.1f})")

# Weapon
w_arr = np.array(weapon)
w_ys, w_xs = np.where(w_arr[:, :, 3] > 20)
print(f"Weapon center: ({w_xs.mean():.1f}, {w_ys.mean():.1f})")

# Key
k_arr = np.array(key)
k_ys, k_xs = np.where(k_arr[:, :, 3] > 20)
print(f"Key center: ({k_xs.mean():.1f}, {k_ys.mean():.1f})")
