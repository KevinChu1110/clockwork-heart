import os
from PIL import Image
import numpy as np

path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat/proof_paperdoll_cat_composite.png"
im = Image.open(path).convert("RGBA")
print(f"Cat composite size: {im.size}, mode: {im.mode}")
bbox = im.getbbox()
print(f"Bbox: {bbox}")
arr = np.array(im)
alpha = arr[:, :, 3]
print(f"Top row with alpha>20: {np.where(np.any(alpha>20, axis=1))[0][0]}")
print(f"Bottom row with alpha>20: {np.where(np.any(alpha>20, axis=1))[0][-1]}")
print(f"Left col with alpha>20: {np.where(np.any(alpha>20, axis=0))[0][0]}")
print(f"Right col with alpha>20: {np.where(np.any(alpha>20, axis=0))[0][-1]}")

shadow = [int(np.sum(alpha[y, :] > 20)) for y in range(118, 128)]
print(f"Cat baseline shadow row counts (118..127): {shadow}")

# Check slices
slices = {
    "key": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat/winding_key/key_cat_crescent_twin_ring_gold.png",
    "curio": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat/back_curio/curio_cat_segmented_gyro_tail.png",
    "chassis": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat/chassis/chassis_cat_obsidian_steel_default.png",
    "head": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat/head_unit/head_cat_brass_acoustic_ears.png",
    "costume": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat/costume/costume_cat_skyspire_prowler_vest.png",
    "optic": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat/optic_core/face_cat_slit_optic_emerald.png",
    "weapon": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat/weapon/weapon_cat_shadowspring_stiletto.png",
}

for name, p in slices.items():
    s_im = Image.open(p).convert("RGBA")
    s_bbox = s_im.getbbox()
    print(f"Slice {name:8s}: bbox={s_bbox}")
