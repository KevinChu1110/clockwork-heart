#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

slots = [
    ("winding_key", "key_classic_brass.png"),
    ("back_curio", "curio_spring_tail.png"),
    ("chassis", "/tmp/test_pure_bronze.png"),
    ("head_unit", "ear_macaque_coaxial.png"),
    ("costume", "costume_zen_striker.png"),
    ("optic_core", "core_cyan_emerald.png"),
    ("weapon", "wpn_spring_claws.png"),
]

comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
for slot, fn in slots:
    if fn.startswith("/"):
        p = fn
    else:
        p = f"{BASE_DIR}/{slot}/{fn}"
    comp = Image.alpha_composite(comp, Image.open(p).convert("RGBA"))

comp.save("/tmp/test_zen_striker_comp.png")
print("Saved /tmp/test_zen_striker_comp.png")
