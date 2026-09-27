#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/viper"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/viper"

idle = Image.open(f"{POSES_DIR}/idle.png")
idle_512 = Image.open(f"{POSES_DIR}/idle_512.png")

key = Image.open(f"{PD_DIR}/winding_key/key_viper_bamboo_leaf_fan.png")
curio = Image.open(f"{PD_DIR}/back_curio/curio_viper_articulated_bamboo_tail.png")
chassis = Image.open(f"{PD_DIR}/chassis/chassis_viper_bamboo_lacquer_default.png")
head = Image.open(f"{PD_DIR}/head_unit/head_viper_carved_bamboo_crest_hood.png")
costume = Image.open(f"{PD_DIR}/costume/costume_viper_zen_dojo_shinobi_wrap.png")
core = Image.open(f"{PD_DIR}/optic_core/face_viper_emerald_glass_optic.png")
weapon = Image.open(f"{PD_DIR}/weapon/weapon_viper_gale_bamboo_dagger.png")

comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
comp.alpha_composite(key)
comp.alpha_composite(curio)
comp.alpha_composite(chassis)
comp.alpha_composite(head)
comp.alpha_composite(costume)
comp.alpha_composite(core)
comp.alpha_composite(weapon)

from PIL import ImageChops
diff = ImageChops.difference(comp, idle)
print("Difference between 7 slices composite and idle.png:", diff.getbbox())
