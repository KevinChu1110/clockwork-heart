#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/hedgehog"
comp = Image.open(f"{BASE_DIR}/proof_paperdoll_hedgehog_composite.png").convert("RGBA")
arr = np.array(comp)

shadow = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print(f"Hedgehog baseline ground shadow (118..127): {shadow}")

# Analyze weapon center and orientation
wpn = Image.open(f"{BASE_DIR}/weapon/weapon_hedgehog_ratchet_needle_dart.png").convert("RGBA")
wpn_box = wpn.getbbox()
print(f"Weapon bbox: {wpn_box}")

# Analyze key center
key = Image.open(f"{BASE_DIR}/winding_key/key_hedgehog_ratchet_and_pawl_cross.png").convert("RGBA")
key_box = key.getbbox()
print(f"Key bbox: {key_box}")

# Analyze curio center
curio = Image.open(f"{BASE_DIR}/back_curio/curio_hedgehog_spring_steel_quill_pack.png").convert("RGBA")
curio_box = curio.getbbox()
print(f"Curio bbox: {curio_box}")
