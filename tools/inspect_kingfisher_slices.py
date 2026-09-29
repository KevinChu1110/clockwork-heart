#!/usr/bin/env python3
import os
from PIL import Image

base = "game/assets/sprites/player/paperdoll/kingfisher"
files = {
    "key": "winding_key/key_kingfisher_zen_taichi_gear_brass.png",
    "curio": "back_curio/curio_kingfisher_bamboo_wings_spring_tail.png",
    "chassis": "chassis/chassis_kingfisher_enamel_default.png",
    "head": "head_unit/head_kingfisher_beak_lance_cowl.png",
    "costume": "costume/costume_kingfisher_dojo_lacquer_cuirass.png",
    "optic": "optic_core/face_kingfisher_zen_slate_goggles.png",
    "weapon": "weapon/weapon_kingfisher_bamboo_spring_lance.png",
    "composite": "proof_paperdoll_kingfisher_composite.png",
}

for k, v in files.items():
    p = os.path.join(base, v)
    im = Image.open(p)
    print(f"{k:10s}: size={im.size}, mode={im.mode}, bbox={im.getbbox()}")
