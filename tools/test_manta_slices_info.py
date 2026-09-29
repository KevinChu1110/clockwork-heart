#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/manta"

for slot, item in [
    ("chassis", "chassis_manta_titanium_default.png"),
    ("head_unit", "head_manta_hydrofoil_horn_cowl.png"),
    ("winding_key", "key_manta_starfish_gear_brass.png"),
    ("costume", "costume_manta_diver_harness_cuirass.png"),
    ("optic_core", "face_manta_high_pressure_quartz_goggles.png"),
    ("weapon", "weapon_manta_hydro_compound_bow.png"),
    ("back_curio", "curio_manta_flexible_wings_antenna_tail.png")
]:
    im = Image.open(f"{PD_DIR}/{slot}/{item}")
    print(f"{slot:12s}: size={im.size}, bbox={im.getbbox()}")
