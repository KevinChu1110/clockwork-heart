#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

base = "game/assets/sprites/player/paperdoll/lemur"
slices = {
    "curio": f"{base}/back_curio/curio_lemur_neon_ring_fiber_tail.png",
    "chassis": f"{base}/chassis/chassis_lemur_orbit_polymer_default.png",
    "head": f"{base}/head_unit/head_lemur_orbit_radar_cowl.png",
    "costume": f"{base}/costume/costume_lemur_astro_stealth_harness.png",
    "optic": f"{base}/optic_core/face_lemur_amber_pulsar_visors.png",
    "key": f"{base}/winding_key/key_lemur_tri_ring_orbit_brass.png",
    "weapon": f"{base}/weapon/weapon_lemur_orbital_pulse_daggers.png",
}

print("=== LEMUR COMPONENT ANALYSIS ===")
for name, path in slices.items():
    im = Image.open(path).convert("RGBA")
    arr = np.array(im)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 20)
    if len(xs) > 0:
        cx = float(np.mean(xs))
        cy = float(np.mean(ys))
        min_x, max_x = int(np.min(xs)), int(np.max(xs))
        min_y, max_y = int(np.min(ys)), int(np.max(ys))
        print(f"{name:10s}: center=({cx:5.1f}, {cy:5.1f}), bbox=({min_x:2d}, {min_y:2d}, {max_x:2d}, {max_y:2d}), size=({max_x-min_x+1}x{max_y-min_y+1}), total_opaque={len(xs)}")
    else:
        print(f"{name:10s}: EMPTY")

party_im = Image.open("game/assets/sprites/player/party/lemur_idle.png").convert("RGBA")
arr_p = np.array(party_im)
alpha_p = arr_p[:, :, 3]
ys_p, xs_p = np.where(alpha_p > 20)
print(f"party_idle: center=({float(np.mean(xs_p)):5.1f}, {float(np.mean(ys_p)):5.1f}), bbox=({int(np.min(xs_p))}, {int(np.min(ys_p))}, {int(np.max(xs_p))}, {int(np.max(ys_p))})")
