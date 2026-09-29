#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

WS_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bdc24189"
BASE_DIR = f"{WS_ROOT}/game/assets/sprites/player/paperdoll/scarab"

components = {
    "key": f"{BASE_DIR}/winding_key/key_scarab_crucible_cross_fire_brass.png",
    "curio": f"{BASE_DIR}/back_curio/curio_scarab_twin_vent_exhaust_tail.png",
    "chassis": f"{BASE_DIR}/chassis/chassis_scarab_obsidian_forge_default.png",
    "head": f"{BASE_DIR}/head_unit/head_scarab_quenched_obsidian_cowl.png",
    "costume": f"{BASE_DIR}/costume/costume_scarab_crucible_artisan_apron.png",
    "optic": f"{BASE_DIR}/optic_core/face_scarab_amber_crystal_visor.png",
    "weapon": f"{BASE_DIR}/weapon/weapon_scarab_crucible_obsidian_focus.png",
}

for name, path in components.items():
    im = Image.open(path).convert("RGBA")
    bbox = im.getbbox()
    print(f"{name:8s}: bbox={bbox}, size={im.size}")

# Composite image check
composite = Image.open(f"{BASE_DIR}/proof_paperdoll_scarab_composite.png").convert("RGBA")
print(f"composite bbox: {composite.getbbox()}")
