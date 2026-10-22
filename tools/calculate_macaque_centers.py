#!/usr/bin/env python3
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

slots = [
    ("chassis", "paint_ivory_stock.png"),
    ("head_unit", "ear_macaque_coaxial.png"),
    ("costume", "costume_dawn_monk_tunic.png"),
    ("optic_core", "core_cyan_emerald.png"),
    ("weapon", "wpn_spring_claws.png"),
    ("winding_key", "key_classic_brass.png"),
    ("back_curio", "curio_spring_tail.png"),
]

for slot, fn in slots:
    p = f"{MACAQUE_DIR}/{slot}/{fn}"
    im = Image.open(p)
    bbox = im.getbbox()
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    cx = (bbox[0] + bbox[2]) / 2.0
    cy = (bbox[1] + bbox[3]) / 2.0
    print(f"{slot:12s} in 128x128: bbox={bbox}, size=({w}, {h}), center=({cx:.1f}, {cy:.1f})")
    print(f"             in 512x512: bbox=({bbox[0]*4}, {bbox[1]*4}, {bbox[2]*4}, {bbox[3]*4}), center=({cx*4:.1f}, {cy*4:.1f})")
