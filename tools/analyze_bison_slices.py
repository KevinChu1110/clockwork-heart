#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bison"

slices = {
    "chassis": "chassis/chassis_bison_rusted_tinplate_default.png",
    "head": "head_unit/head_bison_riveted_brow_horn_crest.png",
    "key": "winding_key/key_bison_heavy_cross_t_bar_cast_iron.png",
    "costume": "costume/costume_bison_junkyard_demolition_cuirass.png",
    "core": "optic_core/face_bison_amber_pressure_gauge_eye.png",
    "weapon": "weapon/weapon_bison_wasteland_anvil_crusher_hammer.png",
    "curio": "back_curio/curio_bison_twin_vent_exhaust_stack.png",
}

for name, rel_p in slices.items():
    p = os.path.join(PD_DIR, rel_p)
    im = Image.open(p)
    bbox = im.getbbox()
    print(f"{name:10s}: size={im.size}, mode={im.mode}, bbox={bbox}")
    if bbox:
        cx = (bbox[0] + bbox[2]) / 2
        cy = (bbox[1] + bbox[3]) / 2
        print(f"            center=({cx:.1f}, {cy:.1f}), w={bbox[2]-bbox[0]}, h={bbox[3]-bbox[1]}")
