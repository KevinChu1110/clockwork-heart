#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/bat"
SLICES = [
    ("chassis", "chassis_bat_astral_polymer_default"),
    ("head_unit", "head_bat_sonar_parabolic_crest"),
    ("winding_key", "key_bat_orbital_pulsar_key"),
    ("costume", "costume_bat_orbital_stealth_harness"),
    ("optic_core", "face_bat_dual_amber_optic_lens"),
    ("weapon", "weapon_bat_superconducting_pulse_dart"),
    ("back_curio", "curio_bat_articulated_starwing_mantle")
]

for slot, item_id in SLICES:
    path = f"{BASE_DIR}/{slot}/{item_id}.png"
    im = Image.open(path).convert("RGBA")
    bbox = im.getbbox()
    arr = np.array(im)
    alpha = arr[:, :, 3] > 8
    ys, xs = np.where(alpha)
    if len(xs) > 0:
        cx, cy = np.mean(xs), np.mean(ys)
        print(f"[{slot:<12}] bbox={bbox} center=({cx:.1f}, {cy:.1f})")
    else:
        print(f"[{slot:<12}] empty")
