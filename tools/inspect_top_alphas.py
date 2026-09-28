#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
RHINO_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rhino"

head = Image.open(f"{RHINO_DIR}/head_unit/head_rhino_crucible_battering_crest.png").convert("RGBA")
curio = Image.open(f"{RHINO_DIR}/back_curio/curio_rhino_steam_furnace_exhaust.png").convert("RGBA")

head_arr = np.array(head)
curio_arr = np.array(curio)

print("Head y=0..5 alpha:")
for y in range(6):
    print(f"y={y}: {head_arr[y, :, 3].tolist()}")

print("Curio y=0..5 alpha:")
for y in range(6):
    print(f"y={y}: {curio_arr[y, :, 3].tolist()}")
