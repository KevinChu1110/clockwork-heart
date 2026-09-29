from PIL import Image
import numpy as np

base = "game/assets/sprites/player/paperdoll/takin"
slices = [
    ("curio", f"{base}/back_curio/curio_takin_dual_bamboo_oil_flasks.png"),
    ("chassis", f"{base}/chassis/chassis_takin_bronze_cast_default.png"),
    ("head", f"{base}/head_unit/head_takin_brass_twisted_horn_cowl.png"),
    ("costume", f"{base}/costume/costume_takin_zen_pioneer_heavy_robe.png"),
    ("optic", f"{base}/optic_core/face_takin_emerald_quartz_visors.png"),
    ("key", f"{base}/winding_key/key_takin_tri_leaf_zen_brass.png"),
    ("weapon", f"{base}/weapon/weapon_takin_zen_bamboo_cleaving_axe.png"),
]

for name, path in slices:
    im = Image.open(path)
    bbox = im.getbbox()
    print(f"{name:10s}: size={im.size}, bbox={bbox}")

party_im = Image.open("game/assets/sprites/player/party/takin_idle.png")
print("party_idle: bbox=", party_im.getbbox())
arr = np.array(party_im)
shd = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("party_idle shadow (118..127):", shd)

takin_idle = Image.open("game/assets/sprites/player/takin_idle.png")
arr_id = np.array(takin_idle)
shd_id = [int(np.sum(arr_id[y, :, 3] > 20)) for y in range(118, 128)]
print("takin_idle shadow (118..127):", shd_id)
