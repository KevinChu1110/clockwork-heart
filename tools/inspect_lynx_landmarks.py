#!/usr/bin/env python3
import os
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
LYNX_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lynx"

SLICES = [
    ("chassis", "chassis_lynx_marionette_walnut_default"),
    ("head_unit", "head_lynx_bazaar_marionette_tufted_cowl"),
    ("winding_key", "key_lynx_twin_ring_chime_brass"),
    ("costume", "costume_lynx_marionette_acrobat_vest"),
    ("optic_core", "face_lynx_emerald_quartz_eyemask"),
    ("weapon", "weapon_lynx_dawn_marionette_steel_claws"),
    ("back_curio", "curio_lynx_pendulum_bobtail_balance")
]

print("=== LYNX SLICE BOUNDING BOXES & CENTROIDS ===")
for slot, item_id in SLICES:
    path_128 = f"{LYNX_PD}/{slot}/{item_id}.png"
    im = Image.open(path_128).convert("RGBA")
    bbox = im.getbbox()
    arr = np.array(im)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 10)
    cy, cx = float(np.mean(ys)), float(np.mean(xs))
    print(f"  {slot:12s}: bbox={bbox}, centroid=({cx:.1f}, {cy:.1f}), pixels={len(xs)}")

# Check ground shadow of party/lynx_idle.png
party_idle = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/lynx_idle.png").convert("RGBA")
arr_pi = np.array(party_idle)
shadow_pi = [int(np.sum(arr_pi[y, :, 3] > 20)) for y in range(118, 128)]
print(f"\nParty idle bbox: {party_idle.getbbox()}")
print(f"Party idle ground shadow (118..127): {shadow_pi}")

# Check composite
comp = Image.open(f"{LYNX_PD}/proof_paperdoll_lynx_composite.png").convert("RGBA")
arr_comp = np.array(comp)
shadow_comp = [int(np.sum(arr_comp[y, :, 3] > 20)) for y in range(118, 128)]
print(f"Composite bbox: {comp.getbbox()}")
print(f"Composite ground shadow (118..127): {shadow_comp}")
