#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/viper"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/viper"

print("--- Poses Inspection ---")
for p in ["idle", "attack", "hit", "recover", "skill", "telegraph"]:
    im = Image.open(f"{POSES_DIR}/{p}.png")
    im512 = Image.open(f"{POSES_DIR}/{p}_512.png")
    print(f"Pose {p:10s}: 128 bbox={im.getbbox()}, 512 bbox={im512.getbbox()}")

print("\n--- Slices Inspection (128) ---")
slices = [
    ("chassis", f"{PD_DIR}/chassis/chassis_viper_bamboo_lacquer_default.png"),
    ("head", f"{PD_DIR}/head_unit/head_viper_carved_bamboo_crest_hood.png"),
    ("key", f"{PD_DIR}/winding_key/key_viper_bamboo_leaf_fan.png"),
    ("costume", f"{PD_DIR}/costume/costume_viper_zen_dojo_shinobi_wrap.png"),
    ("core", f"{PD_DIR}/optic_core/face_viper_emerald_glass_optic.png"),
    ("weapon", f"{PD_DIR}/weapon/weapon_viper_gale_bamboo_dagger.png"),
    ("curio", f"{PD_DIR}/back_curio/curio_viper_articulated_bamboo_tail.png"),
]

for name, path in slices:
    im = Image.open(path)
    im512 = Image.open(path.replace(".png", "_512.png"))
    print(f"Slice {name:10s}: 128 bbox={im.getbbox()}, 512 bbox={im512.getbbox()}")

idle = Image.open(f"{POSES_DIR}/idle.png")
shadow_128 = [sum(1 for x in range(128) if idle.getpixel((x, y))[3] > 20) for y in range(118, 128)]
print(f"\nIdle Ground Shadow (118..127): {shadow_128}")
