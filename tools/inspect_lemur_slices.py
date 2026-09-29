from PIL import Image
import numpy as np

base = "game/assets/sprites/player/paperdoll/lemur"
slices = [
    ("curio", f"{base}/back_curio/curio_lemur_neon_ring_fiber_tail.png"),
    ("chassis", f"{base}/chassis/chassis_lemur_orbit_polymer_default.png"),
    ("head", f"{base}/head_unit/head_lemur_orbit_radar_cowl.png"),
    ("costume", f"{base}/costume/costume_lemur_astro_stealth_harness.png"),
    ("optic", f"{base}/optic_core/face_lemur_amber_pulsar_visors.png"),
    ("key", f"{base}/winding_key/key_lemur_tri_ring_orbit_brass.png"),
    ("weapon", f"{base}/weapon/weapon_lemur_orbital_pulse_daggers.png"),
]

for name, path in slices:
    im = Image.open(path)
    bbox = im.getbbox()
    print(f"{name:10s}: size={im.size}, bbox={bbox}")

party_im = Image.open("game/assets/sprites/player/party/lemur_idle.png")
print("party_idle: bbox=", party_im.getbbox())
arr = np.array(party_im)
shd = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("party_idle shadow (118..127):", shd)

lemur_idle = Image.open("game/assets/sprites/player/lemur_idle_x3.png")
print("lemur_idle_x3: bbox=", lemur_idle.getbbox())
arr_id = np.array(lemur_idle)
shd_id = [int(np.sum(arr_id[y, :, 3] > 20)) for y in range(118, 128)]
print("lemur_idle_x3 shadow (118..127):", shd_id)
