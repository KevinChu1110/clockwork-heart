#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
RHINO_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rhino"

comp = Image.open(f"{RHINO_DIR}/proof_paperdoll_rhino_composite.png").convert("RGBA")
comp_arr = np.array(comp)

# Look at head_unit and back_curio
head = Image.open(f"{RHINO_DIR}/head_unit/head_rhino_crucible_battering_crest.png").convert("RGBA")
optic = Image.open(f"{RHINO_DIR}/optic_core/face_rhino_dual_amber_pyro_optic.png").convert("RGBA")
chassis = Image.open(f"{RHINO_DIR}/chassis/chassis_rhino_molten_iron_default.png").convert("RGBA")
costume = Image.open(f"{RHINO_DIR}/costume/costume_rhino_crucible_smith_plate.png").convert("RGBA")
weapon = Image.open(f"{RHINO_DIR}/weapon/weapon_rhino_crucible_breaker_axe.png").convert("RGBA")
curio = Image.open(f"{RHINO_DIR}/back_curio/curio_rhino_steam_furnace_exhaust.png").convert("RGBA")
key = Image.open(f"{RHINO_DIR}/winding_key/key_rhino_crucible_crosshair_key.png").convert("RGBA")

print("Head bbox:", head.getbbox())
print("Optic bbox:", optic.getbbox())
print("Chassis bbox:", chassis.getbbox())
print("Costume bbox:", costume.getbbox())
print("Weapon bbox:", weapon.getbbox())
print("Curio bbox:", curio.getbbox())
print("Key bbox:", key.getbbox())
