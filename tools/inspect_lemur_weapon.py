#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("game/assets/sprites/player/paperdoll/lemur/weapon/weapon_lemur_orbital_pulse_daggers.png").convert("RGBA")
arr = np.array(im)
alpha = arr[:, :, 3]

# Split left and right at x=64
left_mask = (alpha > 20) & (np.arange(128)[None, :] < 64)
right_mask = (alpha > 20) & (np.arange(128)[None, :] >= 64)

ys_l, xs_l = np.where(left_mask)
ys_r, xs_r = np.where(right_mask)

print(f"Left dagger: bbox=({np.min(xs_l)}, {np.min(ys_l)}, {np.max(xs_l)}, {np.max(ys_r)}), count={len(xs_l)}")
print(f"Right dagger: bbox=({np.min(xs_r)}, {np.min(ys_r)}, {np.max(xs_r)}, {np.max(ys_r)}), count={len(xs_r)}")
