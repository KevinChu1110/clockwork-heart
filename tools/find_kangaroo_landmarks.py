import os
from PIL import Image
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/kangaroo"

chassis = Image.open(f"{BASE_DIR}/chassis/chassis_kangaroo_caramel_bronze_default.png").convert("RGBA")
head = Image.open(f"{BASE_DIR}/head_unit/head_kangaroo_steampunk_boxer_visor.png").convert("RGBA")
optic = Image.open(f"{BASE_DIR}/optic_core/optic_kangaroo_amber_dial_core.png").convert("RGBA")
costume = Image.open(f"{BASE_DIR}/costume/costume_kangaroo_champion_belt_harness.png").convert("RGBA")
weapon = Image.open(f"{BASE_DIR}/weapon/weapon_kangaroo_piston_brass_knuckle.png").convert("RGBA")
curio = Image.open(f"{BASE_DIR}/back_curio/curio_kangaroo_steam_exhaust_backpack.png").convert("RGBA")
key = Image.open(f"{BASE_DIR}/winding_key/key_kangaroo_champion_double_ring.png").convert("RGBA")

# Let's inspect detailed landmarks
def get_component_info(img, name):
    arr = np.array(img)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 20)
    print(f"[{name}] count={len(xs)} x={xs.min()}..{xs.max()} y={ys.min()}..{ys.max()} mean_x={xs.mean():.1f} mean_y={ys.mean():.1f}")

get_component_info(head, "Head")
get_component_info(optic, "Optic")
get_component_info(costume, "Costume")
get_component_info(chassis, "Chassis")
get_component_info(weapon, "Weapon")
get_component_info(curio, "Curio")
get_component_info(key, "Key")

# Head ears:
h_arr = np.array(head)
# Left ear (viewer left, creature right ear) vs Right ear (viewer right)
y_top = np.where(h_arr[:25, :, 3] > 20)
print(f"Head top/ears: x in {y_top[1].min()}..{y_top[1].max()}, y in {y_top[0].min()}..{y_top[0].max()}")

# Ears separation:
ear_l_pts = np.where((h_arr[:30, :55, 3] > 20))
ear_r_pts = np.where((h_arr[:30, 65:, 3] > 20))
if len(ear_l_pts[0]) > 0:
    print(f"Ear L: x={ear_l_pts[1].mean():.1f}, y={ear_l_pts[0].mean():.1f}")
if len(ear_r_pts[0]) > 0:
    print(f"Ear R: x={65 + ear_r_pts[1].mean():.1f}, y={ear_r_pts[0].mean():.1f}")

# Optic dials (eyes):
o_arr = np.array(optic)
# Eyes vs Heart core
eye_pts = np.where((o_arr[:55, :, 3] > 20))
core_pts = np.where((o_arr[55:, :, 3] > 20))
print(f"Optic eyes: x={eye_pts[1].mean():.1f}, y={eye_pts[0].mean():.1f}")
print(f"Optic core: x={core_pts[1].mean():.1f}, y={55 + core_pts[0].mean():.1f}")

# Chassis arms and tail
c_arr = np.array(chassis)
# Tail (x < 35)
tail_pts = np.where((c_arr[:, :35, 3] > 20))
print(f"Tail: x={tail_pts[1].mean():.1f}, y={tail_pts[0].mean():.1f}")
# Left fist/arm (x ~ 40..55, y ~ 65..80)
# Right arm (x ~ 75..95, y ~ 65..80)
arm_l_pts = np.where((c_arr[60:85, 35:55, 3] > 20))
arm_r_pts = np.where((c_arr[60:85, 75:95, 3] > 20))
if len(arm_l_pts[0]) > 0:
    print(f"Arm L (guarding fist): x={35 + arm_l_pts[1].mean():.1f}, y={60 + arm_l_pts[0].mean():.1f}")
if len(arm_r_pts[0]) > 0:
    print(f"Arm R (lead boxer fist): x={75 + arm_r_pts[1].mean():.1f}, y={60 + arm_r_pts[0].mean():.1f}")

# Feet (y > 110)
foot_l_pts = np.where((c_arr[110:122, 40:56, 3] > 20))
foot_r_pts = np.where((c_arr[110:122, 64:82, 3] > 20))
print(f"Foot L: x={40 + foot_l_pts[1].mean():.1f}, y={110 + foot_l_pts[0].mean():.1f}")
print(f"Foot R: x={64 + foot_r_pts[1].mean():.1f}, y={110 + foot_r_pts[0].mean():.1f}")
