#!/usr/bin/env python3
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/courser"

chassis = Image.open(f"{PD_DIR}/chassis/chassis_courser_cream_gold_default.png").convert("RGBA")
head = Image.open(f"{PD_DIR}/head_unit/head_courser_brass_chanfron_mane.png").convert("RGBA")
key = Image.open(f"{PD_DIR}/winding_key/key_courser_baroque_trefoil_gold.png").convert("RGBA")
costume = Image.open(f"{PD_DIR}/costume/costume_courser_dawn_patrol_cuirass.png").convert("RGBA")
core = Image.open(f"{PD_DIR}/optic_core/face_courser_sapphire_optic_lens.png").convert("RGBA")
weapon = Image.open(f"{PD_DIR}/weapon/weapon_courser_cavalry_saber.png").convert("RGBA")
curio = Image.open(f"{PD_DIR}/back_curio/curio_courser_articulated_spring_tail.png").convert("RGBA")

print(f"chassis: {chassis.getbbox()}")
print(f"head: {head.getbbox()}")
print(f"key: {key.getbbox()}")
print(f"costume: {costume.getbbox()}")
print(f"core: {core.getbbox()}")
print(f"weapon: {weapon.getbbox()}")
print(f"curio: {curio.getbbox()}")

# Let's inspect chassis pixel distribution by Y rows
px = chassis.load()
assert px is not None
y_counts = {}
for y in range(128):
    count = sum(1 for x in range(128) if cast(tuple[int, int, int, int], px[x, y])[3] > 10)
    if count > 0:
        y_counts[y] = count

print(f"chassis y range: min={min(y_counts.keys())}, max={max(y_counts.keys())}")
for y in range(min(y_counts.keys()), max(y_counts.keys()) + 1, 5):
    print(f"  y={y}: count={y_counts.get(y, 0)}")
