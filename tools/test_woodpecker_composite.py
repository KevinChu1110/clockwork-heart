#!/usr/bin/env python3
"""
Test woodpecker composite consistency.
"""
import os
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/woodpecker"

key = Image.open(f"{BASE_DIR}/winding_key/key_woodpecker_high_frequency_percussion_key.png").convert("RGBA")
curio = Image.open(f"{BASE_DIR}/back_curio/curio_woodpecker_riveted_tinplate_prop_tail.png").convert("RGBA")
chassis = Image.open(f"{BASE_DIR}/chassis/chassis_woodpecker_tinplate_brass_default.png").convert("RGBA")
head = Image.open(f"{BASE_DIR}/head_unit/head_woodpecker_scarlet_crest_cowl.png").convert("RGBA")
costume = Image.open(f"{BASE_DIR}/costume/costume_woodpecker_skyspire_inspector_harness.png").convert("RGBA")
optic = Image.open(f"{BASE_DIR}/optic_core/face_woodpecker_precision_gauge_monocle.png").convert("RGBA")
weapon = Image.open(f"{BASE_DIR}/weapon/weapon_woodpecker_resonance_pneumatic_heavy_gun.png").convert("RGBA")

comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
comp.alpha_composite(key)
comp.alpha_composite(curio)
comp.alpha_composite(chassis)
comp.alpha_composite(head)
comp.alpha_composite(costume)
comp.alpha_composite(optic)
comp.alpha_composite(weapon)

ref_comp = Image.open(f"{BASE_DIR}/proof_paperdoll_woodpecker_composite.png").convert("RGBA")
diff = ImageChops.difference(comp, ref_comp)
print("Difference with proof_paperdoll_woodpecker_composite bbox:", diff.getbbox())
if diff.getbbox() is None:
    print("✓ 100% exact match with proof_paperdoll_woodpecker_composite!")
else:
    print("Mismatch!")
