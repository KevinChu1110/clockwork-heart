#!/usr/bin/env python3
from PIL import Image

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"
chassis = Image.open(f"{BASE}/chassis/paint_tortoise_jade.png").convert("RGBA")
head = Image.open(f"{BASE}/head_unit/head_xuanji_tortoise_stock.png").convert("RGBA")
key = Image.open(f"{BASE}/winding_key/key_tai_chi_dual_fish.png").convert("RGBA")
curio = Image.open(f"{BASE}/back_curio/curio_bagua_armillary_rings.png").convert("RGBA")
costume = Image.open(f"{BASE}/costume/costume_zen_dojo_harness.png").convert("RGBA")
optic = Image.open(f"{BASE}/optic_core/core_amber_quartz.png").convert("RGBA")

body_no_weapon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_no_weapon.alpha_composite(key)
body_no_weapon.alpha_composite(curio)
body_no_weapon.alpha_composite(chassis)
body_no_weapon.alpha_composite(head)
body_no_weapon.alpha_composite(costume)
body_no_weapon.alpha_composite(optic)

px = body_no_weapon.load()

test_points = {
    "head_top": (64, 26),
    "eye_l": (56, 38),
    "eye_r": (72, 38),
    "snout": (64, 48),
    "throat": (64, 54),
    "core": (63, 62),
    "shoulder_l": (36, 68),
    "shoulder_r": (84, 68),
    "arm_l": (30, 78),
    "arm_r": (90, 78),
    "torso": (64, 76),
    "pelvis": (64, 88),
    "hip_l": (46, 96),
    "hip_r": (80, 96),
    "knee_l": (46, 108),
    "knee_r": (80, 108),
    "foot_l": (48, 118),
    "foot_r": (80, 118),
    "key_mount": (32, 38),
    "key_wing": (20, 28),
    "curio_top": (22, 54),
    "curio_mid": (16, 78),
    "curio_bot": (20, 102),
}

for name, (x, y) in test_points.items():
    p = px[x, y]
    print(f"  {name:15s} ({x:3d}, {y:3d}): RGBA={p}")
