#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/raven"

key_src = Image.open(f"{BASE_DIR}/winding_key/key_raven_armillary_sphere_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_raven_articulated_steampunk_wings.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_raven_obsidian_brass_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_raven_astronomer_hood_beak.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_raven_horologist_scholar_robe.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_raven_astrolabe_monocle_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_raven_armillary_wand.png").convert("RGBA")

wpn_bbox = weapon_src.getbbox()
print("weapon bbox:", wpn_bbox, "size:", (wpn_bbox[2]-wpn_bbox[0], wpn_bbox[3]-wpn_bbox[1]))
key_bbox = key_src.getbbox()
print("key bbox:", key_bbox, "size:", (key_bbox[2]-key_bbox[0], key_bbox[3]-key_bbox[1]))

# composite order according to paperdoll_slots:
# z-index:
# 1. key (z=5)
# 2. curio (z=8)
# 3. chassis (z=10)
# 4. costume (z=30)
# 5. optic (z=45)
# 6. head (z=50)
# 7. weapon (z=60)
# Let us check proof_paperdoll_raven_composite.png
comp_im = Image.open(f"{BASE_DIR}/proof_paperdoll_raven_composite.png").convert("RGBA")
manual_comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
manual_comp.alpha_composite(key_src)
manual_comp.alpha_composite(curio_src)
manual_comp.alpha_composite(chassis_src)
manual_comp.alpha_composite(costume_src)
manual_comp.alpha_composite(head_src)
manual_comp.alpha_composite(optic_src)
manual_comp.alpha_composite(weapon_src)

diff = np.sum(np.abs(np.array(comp_im, dtype=int) - np.array(manual_comp, dtype=int)))
print("diff between official composite and manual composite (head before optic):", diff)

manual_comp2 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
manual_comp2.alpha_composite(key_src)
manual_comp2.alpha_composite(curio_src)
manual_comp2.alpha_composite(chassis_src)
manual_comp2.alpha_composite(costume_src)
manual_comp2.alpha_composite(optic_src)
manual_comp2.alpha_composite(head_src)
manual_comp2.alpha_composite(weapon_src)
diff2 = np.sum(np.abs(np.array(comp_im, dtype=int) - np.array(manual_comp2, dtype=int)))
print("diff between official composite and manual composite (optic before head):", diff2)
