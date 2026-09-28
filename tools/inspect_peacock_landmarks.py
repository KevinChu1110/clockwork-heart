import os
from PIL import Image
import numpy as np

base_dir = "game/assets/sprites/player/paperdoll/peacock"
comp = Image.open(f"{base_dir}/proof_paperdoll_peacock_composite.png")
print("Composite size:", comp.size, "bbox:", comp.getbbox())

slices = {
    "key": f"{base_dir}/winding_key/key_peacock_filigree_sunburst_key.png",
    "curio": f"{base_dir}/back_curio/curio_peacock_articulated_kaleidoscope_fan.png",
    "chassis": f"{base_dir}/chassis/chassis_peacock_glazed_porcelain_default.png",
    "head": f"{base_dir}/head_unit/head_peacock_baroque_diadem_prism.png",
    "costume": f"{base_dir}/costume/costume_peacock_marionette_court_cuirass.png",
    "optic": f"{base_dir}/optic_core/face_peacock_kaleidoscope_gem_lens.png",
    "weapon": f"{base_dir}/weapon/weapon_peacock_kaleidoscope_prism_focus.png",
}

for name, path in slices.items():
    im = Image.open(path)
    arr = np.array(im)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 20)
    if len(xs) > 0:
        center_x = float(np.mean(xs))
        center_y = float(np.mean(ys))
        print(f"{name:8s}: bbox={im.getbbox()} center=({center_x:.1f}, {center_y:.1f}) opaque_px={len(xs)}")
    else:
        print(f"{name:8s}: EMPTY!")

# Let's inspect ground shadow in composite
c_arr = np.array(comp)
shadow_rows = [int(np.sum(c_arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Composite shadow rows (118..127):", shadow_rows)
