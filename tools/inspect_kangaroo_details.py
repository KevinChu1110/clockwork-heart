import os
from PIL import Image
import numpy as np

base_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/kangaroo"

chassis = Image.open(f"{base_dir}/chassis/chassis_kangaroo_caramel_bronze_default.png").convert("RGBA")
head = Image.open(f"{base_dir}/head_unit/head_kangaroo_steampunk_boxer_visor.png").convert("RGBA")
optic = Image.open(f"{base_dir}/optic_core/optic_kangaroo_amber_dial_core.png").convert("RGBA")
costume = Image.open(f"{base_dir}/costume/costume_kangaroo_champion_belt_harness.png").convert("RGBA")
weapon = Image.open(f"{base_dir}/weapon/weapon_kangaroo_piston_brass_knuckle.png").convert("RGBA")

# Let's inspect landmarks:
# Where are the feet?
c_arr = np.array(chassis)
for y in range(110, 128):
    xs = np.where(c_arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f"y={y}: xs min={xs.min()}, max={xs.max()}, count={len(xs)}")

# Where is tail?
# Let's see x < 40 in chassis
tail_pts = np.where((c_arr[:, :, 3] > 20) & (np.arange(128) < 40))
print(f"Tail pixels: y min={tail_pts[0].min()}, max={tail_pts[0].max()}, x min={tail_pts[1].min()}, max={tail_pts[1].max()}")

# Head ears & chin
h_arr = np.array(head)
h_pts = np.where(h_arr[:, :, 3] > 20)
print(f"Head: y min={h_pts[0].min()}, max={h_pts[0].max()}, x min={h_pts[1].min()}, max={h_pts[1].max()}")

# Optic eyes & core
o_arr = np.array(optic)
o_pts = np.where(o_arr[:, :, 3] > 20)
print(f"Optic: y min={o_pts[0].min()}, max={o_pts[0].max()}, x min={o_pts[1].min()}, max={o_pts[1].max()}")
