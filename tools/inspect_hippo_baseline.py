#!/usr/bin/env python3
import os
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/hippo"

slices = [
    ("chassis", "chassis_hippo_thick_cast_brass_default.png"),
    ("head_unit", "head_hippo_ballast_safety_valve_cowl.png"),
    ("winding_key", "key_hippo_dual_valve_handwheel_brass.png"),
    ("costume", "costume_hippo_greatcog_high_pressure_cuirass.png"),
    ("optic_core", "face_hippo_dual_pressure_gauge_quartz_lens.png"),
    ("weapon", "weapon_hippo_steamvalve_piston_heavy_lance.png"),
    ("back_curio", "curio_hippo_dual_steam_exhaust_ballast_tail.png")
]

print("=== HIPPO SLICES INSPECTION ===")
for slot, fname in slices:
    p = os.path.join(BASE_DIR, slot, fname)
    if not os.path.exists(p):
        print(f"MISSING: {p}")
        continue
    im = Image.open(p).convert("RGBA")
    bbox = im.getbbox()
    arr = np.array(im)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 10)
    if len(xs) > 0:
        cx, cy = float(np.mean(xs)), float(np.mean(ys))
        print(f"{slot:12s}: bbox={bbox}, center=({cx:.1f}, {cy:.1f}), pixels={len(xs)}")

idle_path = f"{REPO_ROOT}/game/assets/sprites/player/party/hippo_idle.png"
if os.path.exists(idle_path):
    i_im = Image.open(idle_path).convert("RGBA")
    i_arr = np.array(i_im)
    i_shadow = [int(np.sum(i_arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"\nparty/hippo_idle shadow counts (118..127): {i_shadow}")
    print(f"party/hippo_idle bbox: {i_im.getbbox()}")

comp_path = f"{BASE_DIR}/proof_paperdoll_hippo_composite.png"
if os.path.exists(comp_path):
    c_im = Image.open(comp_path).convert("RGBA")
    c_arr = np.array(c_im)
    c_shadow = [int(np.sum(c_arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"\ncomposite shadow counts (118..127): {c_shadow}")
    print(f"composite bbox: {c_im.getbbox()}")
