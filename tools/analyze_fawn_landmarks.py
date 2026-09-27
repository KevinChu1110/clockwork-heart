from PIL import Image
import numpy as np

fawn_base = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fawn"

slices = {
    "head": f"{fawn_base}/head_unit/head_fawn_vernier_caliper_horns.png",
    "chassis": f"{fawn_base}/chassis/chassis_fawn_timber_tinplate_default.png",
    "costume": f"{fawn_base}/costume/costume_fawn_emerald_scout_tunic.png",
    "optic": f"{fawn_base}/optic_core/face_fawn_amber_lens_alert_eyes.png",
    "weapon": f"{fawn_base}/weapon/weapon_fawn_vernier_shortbow.png",
    "key": f"{fawn_base}/winding_key/key_fawn_clover_leaf_brass.png",
    "curio": f"{fawn_base}/back_curio/curio_fawn_floating_pinecone_chime.png",
}

for name, path in slices.items():
    img = Image.open(path)
    arr = np.array(img)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 20)
    if len(ys) > 0:
        center_y = int(np.mean(ys))
        center_x = int(np.mean(xs))
        bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
        print(f"{name:10s}: bbox={bbox}, center=({center_x}, {center_y}), pixels={len(ys)}")
