#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/gecko"
slices = {
    "key": Image.open(f"{BASE_DIR}/winding_key/key_gecko_dual_ring_relief_valve_brass.png").convert("RGBA"),
    "curio": Image.open(f"{BASE_DIR}/back_curio/curio_gecko_segmented_gear_balance_tail.png").convert("RGBA"),
    "chassis": Image.open(f"{BASE_DIR}/chassis/chassis_gecko_brass_patina_default.png").convert("RGBA"),
    "head": Image.open(f"{BASE_DIR}/head_unit/head_gecko_conduit_scout_crest_cowl.png").convert("RGBA"),
    "costume": Image.open(f"{BASE_DIR}/costume/costume_gecko_highpressure_stealth_harness.png").convert("RGBA"),
    "optic": Image.open(f"{BASE_DIR}/optic_core/face_gecko_dual_slit_aperture_quartz_lens.png").convert("RGBA"),
    "weapon": Image.open(f"{BASE_DIR}/weapon/weapon_gecko_conduit_ratchet_dart.png").convert("RGBA"),
}

for name, im in slices.items():
    arr = np.array(im)
    ys, xs = np.where(arr[:, :, 3] > 20)
    print(f"{name:10s}: x=[{xs.min():3d}..{xs.max():3d}] (center={xs.mean():.1f}), y=[{ys.min():3d}..{ys.max():3d}] (center={ys.mean():.1f})")

comp = Image.open(f"{BASE_DIR}/proof_paperdoll_gecko_composite.png").convert("RGBA")
comp_arr = np.array(comp)
cys, cxs = np.where(comp_arr[:, :, 3] > 20)
print(f"composite : x=[{cxs.min():3d}..{cxs.max():3d}], y=[{cys.min():3d}..{cys.max():3d}]")

# Check shadow row counts
shadow_counts = [int(np.sum(comp_arr[y, :, 3] > 20)) for y in range(118, 128)]
print(f"composite shadow rows (118..127): {shadow_counts}")

idle_party = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/party/gecko_idle.png").convert("RGBA")
p_arr = np.array(idle_party)
p_shadow = [int(np.sum(p_arr[y, :, 3] > 20)) for y in range(118, 128)]
print(f"party idle shadow rows (118..127): {p_shadow}")

# Check weapon bbox and properties
wpn_arr = np.array(slices["weapon"])
wys, wxs = np.where(wpn_arr[:, :, 3] > 20)
print(f"weapon bbox: x=[{wxs.min()}..{wxs.max()}], y=[{wys.min()}..{wys.max()}], center=({wxs.mean():.1f}, {wys.mean():.1f})")

# Check key bbox and properties
key_arr = np.array(slices["key"])
kys, kxs = np.where(key_arr[:, :, 3] > 20)
print(f"key bbox: x=[{kxs.min()}..{kxs.max()}], y=[{kys.min()}..{kys.max()}], center=({kxs.mean():.1f}, {kys.mean():.1f})")

# Check curio bbox and properties
cur_arr = np.array(slices["curio"])
uys, uxs = np.where(cur_arr[:, :, 3] > 20)
print(f"curio bbox: x=[{uxs.min()}..{uxs.max()}], y=[{uys.min()}..{uys.max()}], center=({uxs.mean():.1f}, {uys.mean():.1f})")

# Check head bbox and properties
hd_arr = np.array(slices["head"])
hys, hxs = np.where(hd_arr[:, :, 3] > 20)
print(f"head bbox: x=[{hxs.min()}..{hxs.max()}], y=[{hys.min()}..{hys.max()}], center=({hxs.mean():.1f}, {hys.mean():.1f})")

# Check optic bbox and properties
op_arr = np.array(slices["optic"])
oys, oxs = np.where(op_arr[:, :, 3] > 20)
print(f"optic bbox: x=[{oxs.min()}..{oxs.max()}], y=[{oys.min()}..{oys.max()}], center=({oxs.mean():.1f}, {oys.mean():.1f})")
