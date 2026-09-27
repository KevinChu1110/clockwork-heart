import os
from PIL import Image
import numpy as np

path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/pangolin/proof_paperdoll_pangolin_composite.png"
im = Image.open(path).convert("RGBA")
print(f"Pangolin composite size: {im.size}, mode: {im.mode}")
bbox = im.getbbox()
print(f"Bbox: {bbox}")
arr = np.array(im)
alpha = arr[:, :, 3]
print(f"Top row with alpha>20: {np.where(np.any(alpha>20, axis=1))[0][0]}")
print(f"Bottom row with alpha>20: {np.where(np.any(alpha>20, axis=1))[0][-1]}")
print(f"Left col with alpha>20: {np.where(np.any(alpha>20, axis=0))[0][0]}")
print(f"Right col with alpha>20: {np.where(np.any(alpha>20, axis=0))[0][-1]}")

shadow = [int(np.sum(alpha[y, :] > 20)) for y in range(118, 128)]
print(f"Pangolin baseline shadow row counts (118..127): {shadow}")

slices = {
    "key": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/pangolin/winding_key/key_pangolin_coil_scale_spiral_gold.png",
    "curio": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/pangolin/back_curio/curio_pangolin_segmented_scale_tail.png",
    "chassis": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/pangolin/chassis/chassis_pangolin_dune_orange_default.png",
    "head": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/pangolin/head_unit/head_pangolin_brass_acoustic_ears.png",
    "costume": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/pangolin/costume/costume_pangolin_scavenger_tinker_vest.png",
    "optic": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/pangolin/optic_core/face_pangolin_sky_blue_optic_domes.png",
    "weapon": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/pangolin/weapon/weapon_pangolin_dune_drill_claw.png",
}

for name, p in slices.items():
    s_im = Image.open(p).convert("RGBA")
    s_bbox = s_im.getbbox()
    print(f"Slice {name:8s}: bbox={s_bbox}")
