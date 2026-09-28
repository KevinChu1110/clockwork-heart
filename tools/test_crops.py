#!/usr/bin/env python3
import os
import math
from typing import cast
from PIL import Image, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/armadillo"

key_src = Image.open(f"{BASE_DIR}/winding_key/key_armadillo_crucible_four_leaf_key.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_armadillo_segmented_cast_iron_carapace.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_armadillo_crucible_iron_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_armadillo_quenched_visor_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_armadillo_foundry_anvil_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_armadillo_amber_refractory_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_armadillo_black_iron_heavy_sword.png").convert("RGBA")

# Extract raw crops
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)
wpn_center = ((wpn_bbox[0] + wpn_bbox[2]) / 2.0, (wpn_bbox[1] + wpn_bbox[3]) / 2.0)

key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)
key_center = ((key_bbox[0] + key_bbox[2]) / 2.0, (key_bbox[1] + key_bbox[3]) / 2.0)

print(f"wpn_bbox={wpn_bbox}, wpn_center={wpn_center}")
print(f"key_bbox={key_bbox}, key_center={key_center}")

# Body core: curio, chassis, head, costume, optic
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)

# Full composite with key and weapon
full_comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
full_comp.alpha_composite(key_src)
full_comp.alpha_composite(body_core)
full_comp.alpha_composite(weapon_src)

proof_comp = Image.open(f"{BASE_DIR}/proof_paperdoll_armadillo_composite.png").convert("RGBA")
diff = ImageChops.difference(full_comp, proof_comp)
print(f"Diff vs proof_paperdoll_armadillo_composite: {diff.getbbox()}")
