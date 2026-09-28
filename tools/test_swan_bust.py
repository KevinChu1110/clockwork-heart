#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/swan"
costume_512 = Image.open(f"{PD_DIR}/costume/costume_swan_theatre_herald_cuirass_512.png").convert("RGBA")
print("costume_512 bbox:", costume_512.getbbox())

chassis_512 = Image.open(f"{PD_DIR}/chassis/chassis_swan_silver_enamel_default_512.png").convert("RGBA")
print("chassis_512 bbox:", chassis_512.getbbox())

comp512 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/swan/idle_512.png").convert("RGBA")

# Let's inspect where the waist / pelvis starts
# costume_512 bottom y
c_arr = np.array(costume_512)
c_ys, c_xs = np.where(c_arr[:, :, 3] > 20)
print(f"Costume y range: {c_ys.min()} .. {c_ys.max()}")

# Chassis legs vs torso
ch_arr = np.array(chassis_512)
for y in range(260, 460, 20):
    row_count = np.sum(ch_arr[y, :, 3] > 20)
    print(f"chassis y={y}: count={row_count}")
