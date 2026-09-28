import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/sailfish"

comp = Image.open(f"{BASE_DIR}/proof_paperdoll_sailfish_composite.png")
print("Composite size:", comp.size, comp.mode)
print("Composite bbox:", comp.getbbox())

arr = np.array(comp)
shadow_counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Composite ground shadow row counts (118..127):", shadow_counts)

slices = {
    "key": f"{BASE_DIR}/winding_key/key_sailfish_abyssal_helm_trident.png",
    "curio": f"{BASE_DIR}/back_curio/curio_sailfish_clockwork_sailfin_mantle.png",
    "chassis": f"{BASE_DIR}/chassis/chassis_sailfish_abyssal_titanium_default.png",
    "head": f"{BASE_DIR}/head_unit/head_sailfish_hydrofoil_visor_crest.png",
    "costume": f"{BASE_DIR}/costume/costume_sailfish_abyssal_knight_cuirass.png",
    "optic": f"{BASE_DIR}/optic_core/face_sailfish_dual_abyssal_optic_lens.png",
    "weapon": f"{BASE_DIR}/weapon/weapon_sailfish_hydrofoil_lance.png",
}

for k, v in slices.items():
    im = Image.open(v)
    bbox = im.getbbox()
    im_arr = np.array(im)
    ys, xs = np.where(im_arr[:, :, 3] > 20)
    cy = float(np.mean(ys)) if len(ys) > 0 else 0
    cx = float(np.mean(xs)) if len(xs) > 0 else 0
    print(f"{k:10s}: bbox={bbox}, center=({cx:.1f}, {cy:.1f}), pixels={len(xs)}")
