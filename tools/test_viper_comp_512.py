#!/usr/bin/env python3
from PIL import Image, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/viper"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/viper"

idle_512 = Image.open(f"{POSES_DIR}/idle_512.png")

key_512 = Image.open(f"{PD_DIR}/winding_key/key_viper_bamboo_leaf_fan_512.png")
curio_512 = Image.open(f"{PD_DIR}/back_curio/curio_viper_articulated_bamboo_tail_512.png")
chassis_512 = Image.open(f"{PD_DIR}/chassis/chassis_viper_bamboo_lacquer_default_512.png")
head_512 = Image.open(f"{PD_DIR}/head_unit/head_viper_carved_bamboo_crest_hood_512.png")
costume_512 = Image.open(f"{PD_DIR}/costume/costume_viper_zen_dojo_shinobi_wrap_512.png")
core_512 = Image.open(f"{PD_DIR}/optic_core/face_viper_emerald_glass_optic_512.png")
weapon_512 = Image.open(f"{PD_DIR}/weapon/weapon_viper_gale_bamboo_dagger_512.png")

comp_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
comp_512.alpha_composite(key_512)
comp_512.alpha_composite(curio_512)
comp_512.alpha_composite(chassis_512)
comp_512.alpha_composite(head_512)
comp_512.alpha_composite(costume_512)
comp_512.alpha_composite(core_512)
comp_512.alpha_composite(weapon_512)

diff = ImageChops.difference(comp_512, idle_512)
print("Difference between 7 slices composite 512 and idle_512.png:", diff.getbbox())
