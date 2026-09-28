#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
RHINO_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rhino"

comp = Image.open(f"{RHINO_DIR}/proof_paperdoll_rhino_composite.png").convert("RGBA")
comp_arr = np.array(comp)

print(f"Composite size: {comp.size}")
bbox = comp.getbbox()
print(f"Composite bbox: {bbox}")
left, top, right, bottom = bbox[0], bbox[1], 128 - bbox[2], 128 - bbox[3]
print(f"Composite margins: left={left}, top={top}, right={right}, bottom={bottom}")

shadow_counts = [int(np.sum(comp_arr[y, :, 3] > 20)) for y in range(118, 128)]
print(f"Composite shadow counts (118..127): {shadow_counts}")

slices = [
    ("chassis", "chassis/chassis_rhino_molten_iron_default.png"),
    ("head_unit", "head_unit/head_rhino_crucible_battering_crest.png"),
    ("costume", "costume/costume_rhino_crucible_smith_plate.png"),
    ("optic_core", "optic_core/face_rhino_dual_amber_pyro_optic.png"),
    ("weapon", "weapon/weapon_rhino_crucible_breaker_axe.png"),
    ("back_curio", "back_curio/curio_rhino_steam_furnace_exhaust.png"),
    ("winding_key", "winding_key/key_rhino_crucible_crosshair_key.png"),
]

for name, rel in slices:
    img = Image.open(f"{RHINO_DIR}/{rel}").convert("RGBA")
    b = img.getbbox()
    print(f"Slice {name:<12}: bbox={b}, center={((b[0]+b[2])//2, (b[1]+b[3])//2) if b else None}")
