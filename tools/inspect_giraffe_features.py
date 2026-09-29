#!/usr/bin/env python3
import os
import numpy as np
from PIL import Image

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIRAFFE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/giraffe"

slices = [
    "winding_key/key_giraffe_three_ring_carillon_brass.png",
    "back_curio/curio_giraffe_pendulum_bob_link_tail.png",
    "chassis/chassis_giraffe_sanded_tinplate_default.png",
    "head_unit/head_giraffe_telescoping_periscope_cowl.png",
    "costume/costume_giraffe_dawn_herald_woolen_cape.png",
    "optic_core/face_giraffe_dual_periscope_quartz_lens.png",
    "weapon/weapon_giraffe_belfry_celestial_bow.png",
]

for s in slices:
    p = os.path.join(GIRAFFE_DIR, s)
    im = Image.open(p).convert("RGBA")
    bbox = im.getbbox()
    print(f"{s:55s}: bbox={bbox}, size={im.size}")

# Check composite and party idle
party_idle = f"{REPO_ROOT}/game/assets/sprites/player/party/giraffe_idle.png"
if os.path.exists(party_idle):
    p_im = Image.open(party_idle).convert("RGBA")
    print(f"party/giraffe_idle.png: bbox={p_im.getbbox()}")
    arr = np.array(p_im)
    shd = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"party shadow rows (118..127): {shd}")

comp_path = f"{GIRAFFE_DIR}/proof_paperdoll_giraffe_composite.png"
if os.path.exists(comp_path):
    c_im = Image.open(comp_path).convert("RGBA")
    print(f"composite: bbox={c_im.getbbox()}")
    arr = np.array(c_im)
    shd = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"composite shadow rows (118..127): {shd}")
