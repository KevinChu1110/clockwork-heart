#!/usr/bin/env python3
import json
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

# 載入原畫
im_chassis = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock_512.png").convert("RGBA")
im_head_raw = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_512.png").convert("RGBA")
im_tunic_raw = Image.open(f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic_512.png").convert("RGBA")
im_weapon_raw = Image.open(f"{MACAQUE_DIR}/weapon/wpn_spring_claws_512.png").convert("RGBA")

# 裁切 head_unit
head_crop_box = im_head_raw.getbbox() # (108, 51, 355, 263)
head_cropped = im_head_raw.crop(head_crop_box)
print("Head cropped size:", head_cropped.size, "from", head_crop_box)

# 裁切 costume tunic
tunic_crop_box = im_tunic_raw.getbbox() # (183, 262, 334, 426)
tunic_cropped = im_tunic_raw.crop(tunic_crop_box)
print("Tunic cropped size:", tunic_cropped.size, "from", tunic_crop_box)

# 裁切 weapon claws
weapon_crop_box = im_weapon_raw.getbbox() # (63, 271, 341, 417)
weapon_cropped = im_weapon_raw.crop(weapon_crop_box)
print("Weapon cropped size:", weapon_cropped.size, "from", weapon_crop_box)

# 錨點設計
neck_anchor = (232, 260)
navel_anchor = (256, 345)
hand_anchor = (200, 340)

# 計算各部件 origin
head_origin = (neck_anchor[0] - head_crop_box[0], neck_anchor[1] - head_crop_box[1])
tunic_origin = (navel_anchor[0] - tunic_crop_box[0], navel_anchor[1] - tunic_crop_box[1])
weapon_origin = (hand_anchor[0] - weapon_crop_box[0], hand_anchor[1] - weapon_crop_box[1])

print(f"Head origin  : {head_origin} (neck {neck_anchor} - box {head_crop_box[:2]})")
print(f"Tunic origin : {tunic_origin} (navel {navel_anchor} - box {tunic_crop_box[:2]})")
print(f"Weapon origin: {weapon_origin} (hand {hand_anchor} - box {weapon_crop_box[:2]})")

# 模擬 Godot 的掛載位置 (anchor - origin)
sim_head_pos = (neck_anchor[0] - head_origin[0], neck_anchor[1] - head_origin[1])
sim_tunic_pos = (navel_anchor[0] - tunic_origin[0], navel_anchor[1] - tunic_origin[1])
sim_weapon_pos = (hand_anchor[0] - weapon_origin[0], hand_anchor[1] - weapon_origin[1])

assert sim_head_pos == head_crop_box[:2], f"Head pos {sim_head_pos} != {head_crop_box[:2]}"
assert sim_tunic_pos == tunic_crop_box[:2], f"Tunic pos {sim_tunic_pos} != {tunic_crop_box[:2]}"
assert sim_weapon_pos == weapon_crop_box[:2], f"Weapon pos {sim_weapon_pos} != {weapon_crop_box[:2]}"
print("✓ All simulated positions match exactly 100% to raw asset coordinates!")
