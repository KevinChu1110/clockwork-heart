#!/usr/bin/env python3
"""
Find detailed landmark candidates for badger.
"""
from PIL import Image
import numpy as np

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_80f63a7e"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/badger"

chassis = Image.open(f"{PD_DIR}/chassis/chassis_badger_polymer_space_default.png").convert("RGBA")
head = Image.open(f"{PD_DIR}/head_unit/head_badger_flathead_ballistic_visor.png").convert("RGBA")
optic = Image.open(f"{PD_DIR}/optic_core/face_badger_amber_led_matrix_visor.png").convert("RGBA")
costume = Image.open(f"{PD_DIR}/costume/costume_badger_eva_heavy_harness.png").convert("RGBA")
curio = Image.open(f"{PD_DIR}/back_curio/curio_badger_dual_coldgas_reaction_thruster.png").convert("RGBA")
weapon = Image.open(f"{PD_DIR}/weapon/weapon_badger_starbreaker_ripper_claw.png").convert("RGBA")
key = Image.open(f"{PD_DIR}/winding_key/key_badger_four_vane_antenna_gold.png").convert("RGBA")

print("Head bbox:", head.getbbox())
print("Optic bbox:", optic.getbbox())
print("Costume bbox:", costume.getbbox())
print("Curio bbox:", curio.getbbox())
print("Chassis bbox:", chassis.getbbox())
print("Weapon bbox:", weapon.getbbox())
print("Key bbox:", key.getbbox())

# Let's inspect rows around foot level y=110..120 in chassis
ch_arr = np.array(chassis)
for y in range(112, 120):
    xs = np.where(ch_arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f"y={y}: min_x={xs[0]}, max_x={xs[-1]}, count={len(xs)}, center={np.mean(xs):.1f}")
