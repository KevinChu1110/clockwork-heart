import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/firefly"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"

slots = [
    ("key", f"{BASE_DIR}/winding_key/key_firefly_floral_gear_brass.png"),
    ("curio", f"{BASE_DIR}/back_curio/curio_firefly_luminescent_resin_abdomen.png"),
    ("chassis", f"{BASE_DIR}/chassis/chassis_firefly_emerald_tinplate_default.png"),
    ("head", f"{BASE_DIR}/head_unit/head_firefly_brass_antenna_cowl.png"),
    ("costume", f"{BASE_DIR}/costume/costume_firefly_vine_harness_cuirass.png"),
    ("optic", f"{BASE_DIR}/optic_core/face_firefly_dual_lantern_quartz_eyes.png"),
    ("weapon", f"{BASE_DIR}/weapon/weapon_firefly_luminescent_vine_staff.png"),
]

print("=== FIREFLY SLICES INSPECTION ===")
for name, path in slots:
    im = Image.open(path).convert("RGBA")
    bbox = im.getbbox()
    print(f"{name:10s}: size={im.size}, bbox={bbox}")

ref_party = f"{PLAYER_DIR}/party/firefly_idle.png"
if os.path.exists(ref_party):
    im_p = Image.open(ref_party).convert("RGBA")
    arr_p = np.array(im_p)
    shadow = [int(np.sum(arr_p[y, :, 3] > 20)) for y in range(118, 128)]
    print("party/firefly_idle.png bbox:", im_p.getbbox())
    print("ground shadow counts (118..127):", shadow)

ref_idle_x3 = f"{PLAYER_DIR}/firefly_idle_x3.png"
if os.path.exists(ref_idle_x3):
    im_x3 = Image.open(ref_idle_x3).convert("RGBA")
    arr_x3 = np.array(im_x3)
    shadow_x3 = [int(np.sum(arr_x3[y, :, 3] > 20)) for y in range(118, 128)]
    print("firefly_idle_x3.png bbox:", im_x3.getbbox())
    print("ground shadow counts (118..127):", shadow_x3)
