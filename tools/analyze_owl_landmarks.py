import os
from PIL import Image

REPO = "/opt/side/bravesoul-game"
BASE = f"{REPO}/game/assets/sprites/player/paperdoll/owl"

slices = [
    ("chassis", "chassis/chassis_owl_brass_lamellae_default.png"),
    ("head_unit", "head_unit/head_owl_brass_plume_antennas.png"),
    ("winding_key", "winding_key/key_owl_sun_moon_astrolabe_gold.png"),
    ("costume", "costume/costume_owl_dawn_astronomer_robe.png"),
    ("optic_core", "optic_core/face_owl_clockface_lens_dusk_gold.png"),
    ("weapon", "weapon/weapon_owl_armillary_escapement_scepter.png"),
    ("back_curio", "back_curio/curio_owl_floating_micro_orrery.png")
]

for name, rel in slices:
    p = f"{BASE}/{rel}"
    im = Image.open(p).convert("RGBA")
    bb = im.getbbox()
    cx = (bb[0] + bb[2]) / 2.0 if bb else 0
    cy = (bb[1] + bb[3]) / 2.0 if bb else 0
    print(f"{name:12s}: bbox={bb}, center=({cx:.1f}, {cy:.1f})")
