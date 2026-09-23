#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"

comp = Image.open(f"{BASE}/proof_paperdoll_tortoise_composite.png").convert("RGBA")
chassis = Image.open(f"{BASE}/chassis/paint_tortoise_jade.png").convert("RGBA")
head = Image.open(f"{BASE}/head_unit/head_xuanji_tortoise_stock.png").convert("RGBA")
key = Image.open(f"{BASE}/winding_key/key_tai_chi_dual_fish.png").convert("RGBA")
curio = Image.open(f"{BASE}/back_curio/curio_bagua_armillary_rings.png").convert("RGBA")
costume = Image.open(f"{BASE}/costume/costume_zen_dojo_harness.png").convert("RGBA")
optic = Image.open(f"{BASE}/optic_core/core_amber_quartz.png").convert("RGBA")
wpn = Image.open(f"{BASE}/weapon/wpn_bagua_astrolabe.png").convert("RGBA")

# Build body without weapon
body_no_weapon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_no_weapon.alpha_composite(key)
body_no_weapon.alpha_composite(curio)
body_no_weapon.alpha_composite(chassis)
body_no_weapon.alpha_composite(head)
body_no_weapon.alpha_composite(costume)
body_no_weapon.alpha_composite(optic)

print(f"body_no_weapon bbox: {body_no_weapon.getbbox()}")

# Weapon bbox and center
wb = wpn.getbbox()
assert wb is not None
print(f"weapon bbox: {wb}, size={wb[2]-wb[0]}x{wb[3]-wb[1]}, center={(wb[0]+wb[2])//2}, {(wb[1]+wb[3])//2}")

# Head bbox
hb = head.getbbox()
assert hb is not None
print(f"head bbox: {hb}, center={(hb[0]+hb[2])//2}, {(hb[1]+hb[3])//2}")

# Chassis bbox
cb = chassis.getbbox()
assert cb is not None
print(f"chassis bbox: {cb}")

# Check margins of composite
comp_box = comp.getbbox()
assert comp_box is not None
left, top, right, bottom = comp_box[0], comp_box[1], 128 - comp_box[2], 128 - comp_box[3]
print(f"composite margins: left={left}, top={top}, right={right}, bottom={bottom}")
