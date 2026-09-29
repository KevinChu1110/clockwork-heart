#!/usr/bin/env python3
from PIL import Image
import numpy as np

base = "game/assets/sprites/player/paperdoll/lemur"
curio_src = Image.open(f"{base}/back_curio/curio_lemur_neon_ring_fiber_tail.png").convert("RGBA")
chassis_src = Image.open(f"{base}/chassis/chassis_lemur_orbit_polymer_default.png").convert("RGBA")
head_src = Image.open(f"{base}/head_unit/head_lemur_orbit_radar_cowl.png").convert("RGBA")
costume_src = Image.open(f"{base}/costume/costume_lemur_astro_stealth_harness.png").convert("RGBA")
optic_src = Image.open(f"{base}/optic_core/face_lemur_amber_pulsar_visors.png").convert("RGBA")
key_src = Image.open(f"{base}/winding_key/key_lemur_tri_ring_orbit_brass.png").convert("RGBA")
weapon_src = Image.open(f"{base}/weapon/weapon_lemur_orbital_pulse_daggers.png").convert("RGBA")

# Measure specific regions
def get_box(im, name):
    bbox = im.getbbox()
    print(f"{name:15s}: bbox={bbox}")
    return bbox

get_box(head_src, "head")
get_box(optic_src, "optic")
get_box(costume_src, "costume")
get_box(chassis_src, "chassis")
get_box(curio_src, "curio_tail")
get_box(key_src, "key")
get_box(weapon_src, "weapon")

# Find top edge of head radar ears
arr_h = np.array(head_src)
alpha_h = arr_h[:, :, 3]
ys, xs = np.where(alpha_h > 20)
print(f"Head top row: min y = {np.min(ys)}, xs at min y = {xs[ys == np.min(ys)]}")
# Leftmost and rightmost ear tips
min_x = np.min(xs)
max_x = np.max(xs)
print(f"Head left ear tip: ({min_x}, {ys[xs == min_x][0]}), right ear tip: ({max_x}, {ys[xs == max_x][0]})")

# Find tail key points
arr_t = np.array(curio_src)
alpha_t = arr_t[:, :, 3]
ys_t, xs_t = np.where(alpha_t > 20)
print(f"Tail top: ({xs_t[ys_t == np.min(ys_t)][0]}, {np.min(ys_t)}), bot: ({xs_t[ys_t == np.max(ys_t)][0]}, {np.max(ys_t)}), leftmost: ({np.min(xs_t)}, {ys_t[xs_t == np.min(xs_t)][0]})")

# Find feet
arr_c = np.array(chassis_src)
alpha_c = arr_c[:, :, 3]
ys_c, xs_c = np.where(alpha_c > 20)
print(f"Chassis bottom feet row: max y = {np.max(ys_c)}, xs at max y = {xs_c[ys_c == np.max(ys_c)]}")
