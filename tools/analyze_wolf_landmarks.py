import os
from PIL import Image
import numpy as np

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/wolf"

for name in ["weapon/weapon_wolf_scrap_sawblade_greatsword.png",
             "winding_key/key_wolf_heavy_pojun_cross.png",
             "back_curio/curio_wolf_segmented_spring_tail.png",
             "optic_core/face_wolf_twin_blue_optic_lens.png",
             "head_unit/head_wolf_gear_mane_cowl.png",
             "costume/costume_wolf_scavenger_scrap_plate_armor.png",
             "chassis/chassis_wolf_warm_orange_default.png"]:
    p = os.path.join(BASE, name)
    im = Image.open(p).convert("RGBA")
    bbox = im.getbbox()
    print(f"--- {name} ---")
    print("  bbox:", bbox)
    arr = np.array(im)
    ys, xs = np.where(arr[:, :, 3] > 20)
    print(f"  center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")
    print(f"  min_x={np.min(xs)}, max_x={np.max(xs)}, min_y={np.min(ys)}, max_y={np.max(ys)}")
