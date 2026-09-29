#!/usr/bin/env python3
import os
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PETAURISTA_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/petaurista"

SLICES = [
    ("chassis", "chassis_petaurista_lacquered_bamboo_default"),
    ("head_unit", "head_petaurista_zen_bamboo_ninja_cowl"),
    ("winding_key", "key_petaurista_three_leaf_windchime_brass"),
    ("costume", "costume_petaurista_folding_glider_wing_harness"),
    ("optic_core", "face_petaurista_obsidian_goggle_cinnabar_mask"),
    ("weapon", "weapon_petaurista_zen_octagonal_bamboo_dart"),
    ("back_curio", "curio_petaurista_bamboo_weave_rudder_tail")
]

print("=== PETAURISTA SLICE BOUNDING BOXES & CENTROIDS ===")
for slot, item_id in SLICES:
    path_128 = f"{PETAURISTA_PD}/{slot}/{item_id}.png"
    im = Image.open(path_128).convert("RGBA")
    bbox = im.getbbox()
    arr = np.array(im)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 10)
    cy, cx = float(np.mean(ys)), float(np.mean(xs))
    print(f"  {slot:12s}: bbox={bbox}, centroid=({cx:.1f}, {cy:.1f}), pixels={len(xs)}")

# Check ground shadow of party/petaurista_idle.png
party_idle = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/petaurista_idle.png").convert("RGBA")
arr_pi = np.array(party_idle)
shadow_pi = [int(np.sum(arr_pi[y, :, 3] > 20)) for y in range(118, 128)]
print(f"\nParty idle bbox: {party_idle.getbbox()}")
print(f"Party idle ground shadow (118..127): {shadow_pi}")

# Check composite
comp = Image.open(f"{PETAURISTA_PD}/proof_paperdoll_petaurista_composite.png").convert("RGBA")
arr_comp = np.array(comp)
shadow_comp = [int(np.sum(arr_comp[y, :, 3] > 20)) for y in range(118, 128)]
print(f"Composite bbox: {comp.getbbox()}")
print(f"Composite ground shadow (118..127): {shadow_comp}")
