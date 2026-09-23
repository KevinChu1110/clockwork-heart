#!/usr/bin/env python3
from PIL import Image
import numpy as np

TORTOISE_PD = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"
chassis_jade = Image.open(f"{TORTOISE_PD}/chassis/paint_tortoise_jade.png").convert("RGBA")
robe_im = Image.open(f"{TORTOISE_PD}/costume/costume_bagua_master_robe.png").convert("RGBA")

c_arr = np.array(chassis_jade)
r_arr = np.array(robe_im)

dup = (r_arr[:,:,3] > 20) & (c_arr[:,:,3] > 20) & np.all(r_arr == c_arr, axis=-1)
coords = np.argwhere(dup)
print("Duplicate pixel coordinates [y, x]:", coords)
for y, x in coords:
    print(f"  at ({x}, {y}): color={tuple(r_arr[y, x])}")
