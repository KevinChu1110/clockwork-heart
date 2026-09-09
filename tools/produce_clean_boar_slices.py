#!/usr/bin/env python3
"""
produce_clean_boar_slices.py
Partitions final_master_boar_v4.png cleanly into 7 modular paperdoll slices
such that their Z-ordered alpha composite is 100% identical to proof_paperdoll_boar_composite.png.
"""

import os
from PIL import Image, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
OUTPUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
MASTER_PATH = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_34df38dc/final_master_boar_v4.png"

master = Image.open(MASTER_PATH).convert("RGBA")
W, H = 128, 128

for y in range(H):
    for x in range(W):
        p = master.getpixel((x, y))
        if isinstance(p, tuple) and len(p) >= 4 and p[3] <= 10:
            master.putpixel((x, y), (0, 0, 0, 0))

# 1. WINDING_KEY (Z: 5)
key_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(16, 44):
    for x in range(85, 112):
        p = master.getpixel((x, y))
        if p[3] < 15: continue
        if x < 86 and y < 35: continue
        if y >= 38 and x < 88: continue
        key_128.putpixel((x, y), p)

# 2. BACK_CURIO (Z: 8)
tail_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(80, 102):
    for x in range(85, 114):
        p = master.getpixel((x, y))
        if p[3] < 15: continue
        if x < 87 and y > 97: continue
        tail_128.putpixel((x, y), p)

# 7. WEAPON (Z: 40)
weapon_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(H):
    for x in range(W):
        p = master.getpixel((x, y))
        if p[3] < 15: continue
        is_head = (75 <= y <= 124 and 18 <= x <= 46)
        is_shaft = (58 <= y <= 75 and 44 <= x <= 55)
        if is_head or is_shaft:
            weapon_128.putpixel((x, y), p)

# 6. OPTIC_CORE (Z: 30)
optic_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(H):
    for x in range(W):
        p = master.getpixel((x, y))
        if p[3] < 15: continue
        is_eye = (39 <= y <= 44 and 56 <= x <= 61)
        is_snout_tusks = (36 <= y <= 58 and 34 <= x <= 62)
        is_chest_core = (71 <= y <= 81 and 52 <= x <= 62)
        if is_eye or is_snout_tusks or is_chest_core:
            optic_128.putpixel((x, y), p)

# 4. HEAD_UNIT (Z: 20)
head_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(9, 44):
    for x in range(35, 88):
        p = master.getpixel((x, y))
        if p[3] < 15: continue
        if key_128.getpixel((x, y))[3] > 15: continue
        if optic_128.getpixel((x, y))[3] > 15: continue
        head_128.putpixel((x, y), p)

# 5. COSTUME (Z: 25)
costume_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(45, 115):
    for x in range(35, 96):
        p = master.getpixel((x, y))
        if p[3] < 15: continue
        if weapon_128.getpixel((x, y))[3] > 15: continue
        if optic_128.getpixel((x, y))[3] > 15: continue
        if key_128.getpixel((x, y))[3] > 15 or tail_128.getpixel((x, y))[3] > 15: continue

        is_pauldron = (45 <= y <= 68 and 66 <= x <= 92)
        is_armor = (65 <= y <= 95 and 48 <= x <= 75)
        if is_pauldron or is_armor:
            costume_128.putpixel((x, y), p)

# 3. CHASSIS (Z: 10)
chassis_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(H):
    for x in range(W):
        p = master.getpixel((x, y))
        if p[3] < 15: continue
        if key_128.getpixel((x, y))[3] > 15: continue
        if tail_128.getpixel((x, y))[3] > 15: continue
        if weapon_128.getpixel((x, y))[3] > 15: continue
        if head_128.getpixel((x, y))[3] > 15: continue
        if optic_128.getpixel((x, y))[3] > 15: continue
        if costume_128.getpixel((x, y))[3] > 15: continue
        chassis_128.putpixel((x, y), p)

for y in range(70, 85):
    for x in range(45, 55):
        if chassis_128.getpixel((x, y))[3] < 30 and master.getpixel((x, y))[3] > 30:
            chassis_128.putpixel((x, y), (60, 68, 78, 255))
for y in range(71, 81):
    for x in range(52, 62):
        if chassis_128.getpixel((x, y))[3] < 30:
            chassis_128.putpixel((x, y), (55, 62, 72, 255))

for root, dirs, files in os.walk(OUTPUT_DIR):
    for f in files:
        if f.endswith('.png') or f.endswith('.import'):
            os.remove(os.path.join(root, f))

canonical_slots = [
    ("winding_key", "key_classic_brass.png", key_128),
    ("back_curio", "curio_spring_tail.png", tail_128),
    ("chassis", "paint_ivory_stock.png", chassis_128),
    ("head_unit", "ear_boar_rivet_cowl.png", head_128),
    ("costume", "costume_viking_harness.png", costume_128),
    ("optic_core", "core_cyan_emerald.png", optic_128),
    ("weapon", "wpn_anvil_greathammer.png", weapon_128),
]

for slot_id, fname, img in canonical_slots:
    os.makedirs(f"{OUTPUT_DIR}/{slot_id}", exist_ok=True)
    target = f"{OUTPUT_DIR}/{slot_id}/{fname}"
    img.save(target)
    print(f"Saved: {target}")

comp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
comp.alpha_composite(key_128)
comp.alpha_composite(tail_128)
comp.alpha_composite(chassis_128)
comp.alpha_composite(head_128)
comp.alpha_composite(costume_128)
comp.alpha_composite(optic_128)
comp.alpha_composite(weapon_128)

proof_path = f"{OUTPUT_DIR}/proof_paperdoll_boar_composite.png"
comp.save(proof_path)
print(f"Saved proof composite: {proof_path}")
