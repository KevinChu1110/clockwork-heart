import numpy as np
from PIL import Image

comp_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/pangolin/proof_paperdoll_pangolin_composite.png"
im = Image.open(comp_path).convert("RGBA")
arr = np.array(im)

# Let's inspect center of mass / bounding boxes of slices
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
    s_arr = np.array(s_im)
    alpha = s_arr[:, :, 3]
    ys, xs = np.where(alpha > 20)
    cy = np.mean(ys)
    cx = np.mean(xs)
    print(f"{name:8s}: center=({cx:.1f}, {cy:.1f}), min_x={xs.min()}, max_x={xs.max()}, min_y={ys.min()}, max_y={ys.max()}")
