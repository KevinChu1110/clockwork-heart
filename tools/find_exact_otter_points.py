#!/usr/bin/env python3
import numpy as np
from PIL import Image

head_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/head_unit/head_otter_diver_bell_visor.png"
h_im = Image.open(head_path).convert("RGBA")
h_arr = np.array(h_im)

chassis_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/chassis/chassis_otter_abyssal_cyan_default.png"
c_im = Image.open(chassis_path).convert("RGBA")
c_arr = np.array(c_im)

print("Head center at y=25: non-zero x in", np.where(h_arr[25, :, 3] > 20)[0])
print("Head left valve: min_x=", np.where(h_arr[:, :, 3] > 20)[1].min())
# find left valve center
ys, xs = np.where((h_arr[:, :, 3] > 20) & (np.arange(128) < 45)[None, :])
print(f"Left valve center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")

# find right valve center
ys_r, xs_r = np.where((h_arr[:, :, 3] > 20) & (np.arange(128) > 85)[None, :])
print(f"Right valve center: ({np.mean(xs_r):.1f}, {np.mean(ys_r):.1f})")

# find left arm center in chassis
ys_la, xs_la = np.where((c_arr[:, :, 3] > 20) & (np.arange(128) < 48)[None, :] & (np.arange(128) > 65)[:, None] & (np.arange(128) < 95)[:, None])
print(f"Left arm center: ({np.mean(xs_la):.1f}, {np.mean(ys_la):.1f})")

# find right hip / leg center
ys_rl, xs_rl = np.where((c_arr[:, :, 3] > 20) & (np.arange(128) > 70)[None, :] & (np.arange(128) > 90)[:, None] & (np.arange(128) < 118)[:, None])
print(f"Right leg/hip center: ({np.mean(xs_rl):.1f}, {np.mean(ys_rl):.1f})")
