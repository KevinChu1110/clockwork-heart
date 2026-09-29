import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/swan"

slices = {
    "key": Image.open(f"{BASE_DIR}/winding_key/key_swan_octave_dual_loop_brass.png").convert("RGBA"),
    "curio": Image.open(f"{BASE_DIR}/back_curio/curio_swan_spring_steel_ballet_wings.png").convert("RGBA"),
    "chassis": Image.open(f"{BASE_DIR}/chassis/chassis_swan_silver_enamel_default.png").convert("RGBA"),
    "head": Image.open(f"{BASE_DIR}/head_unit/head_swan_tiara_beak_visor.png").convert("RGBA"),
    "costume": Image.open(f"{BASE_DIR}/costume/costume_swan_theatre_herald_cuirass.png").convert("RGBA"),
    "optic": Image.open(f"{BASE_DIR}/optic_core/face_swan_prismatic_crystal_monocle.png").convert("RGBA"),
    "weapon": Image.open(f"{BASE_DIR}/weapon/weapon_swan_octave_spiral_lance.png").convert("RGBA"),
}

for name, im in slices.items():
    arr = np.array(im)
    ys, xs = np.where(arr[:, :, 3] > 20)
    print(f"{name:10s}: x=[{xs.min()}..{xs.max()}] (center={xs.mean():.1f}), y=[{ys.min()}..{ys.max()}] (center={ys.mean():.1f})")

# Let's inspect head & beak:
head_arr = np.array(slices["head"])
# Find topmost pixel
ys, xs = np.where(head_arr[:, :, 3] > 20)
top_idx = ys.argmin()
print(f"Head top: x={xs[top_idx]}, y={ys[top_idx]}")

# Find rightmost pixel (likely beak tip or visor)
right_idx = xs.argmax()
print(f"Head rightmost (beak tip): x={xs[right_idx]}, y={ys[right_idx]}")

# Optic core center
optic_arr = np.array(slices["optic"])
oys, oxs = np.where(optic_arr[:, :, 3] > 20)
print(f"Optic core center: x={oxs.mean():.1f}, y={oys.mean():.1f}, bbox=({oxs.min()}, {oys.min()}, {oxs.max()}, {oys.max()})")

# Chassis feet
chassis_arr = np.array(slices["chassis"])
cys, cxs = np.where(chassis_arr[:, :, 3] > 20)
bot_ys = np.where(cys > 105)[0]
print(f"Chassis bottom y={cys.max()}, x=[{cxs[bot_ys].min()}..{cxs[bot_ys].max()}]")

# Curio wings
curio_arr = np.array(slices["curio"])
uys, uxs = np.where(curio_arr[:, :, 3] > 20)
print(f"Curio wings bbox: x=[{uxs.min()}..{uxs.max()}], y=[{uys.min()}..{uys.max()}]")

# Weapon lance
wpn_arr = np.array(slices["weapon"])
wys, wxs = np.where(wpn_arr[:, :, 3] > 20)
print(f"Weapon bbox: x=[{wxs.min()}..{wxs.max()}], y=[{wys.min()}..{wys.max()}]")
print(f"Weapon tip (top): x={wxs[wys.argmin()]}, y={wys.min()}")
print(f"Weapon bottom / grip: x={wxs[wys.argmax()]}, y={wys.max()}")
