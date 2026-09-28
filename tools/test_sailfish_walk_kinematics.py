#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/sailfish"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/sailfish"

# Load slices
chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_sailfish_abyssal_titanium_default.png").convert("RGBA")
head_128 = Image.open(f"{PD_DIR}/head_unit/head_sailfish_hydrofoil_visor_crest.png").convert("RGBA")
key_128 = Image.open(f"{PD_DIR}/winding_key/key_sailfish_abyssal_helm_trident.png").convert("RGBA")
costume_128 = Image.open(f"{PD_DIR}/costume/costume_sailfish_abyssal_knight_cuirass.png").convert("RGBA")
core_128 = Image.open(f"{PD_DIR}/optic_core/face_sailfish_dual_abyssal_optic_lens.png").convert("RGBA")
weapon_128 = Image.open(f"{PD_DIR}/weapon/weapon_sailfish_hydrofoil_lance.png").convert("RGBA")
curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_sailfish_clockwork_sailfin_mantle.png").convert("RGBA")

comp128 = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")

w, h = 128, 128
clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
c_px = comp128.load()
s_px = clean_shadow.load()
for y in range(118, 128):
    for x in range(128):
        p = c_px[x, y]
        if p[3] > 20:
            s_px[x, y] = p

base_shadow = [sum(1 for x in range(128) if clean_shadow.getpixel((x, y))[3] > 20) for y in range(118, 128)]
print("Base shadow:", base_shadow)

# Decompose chassis:
# Torso, Pelvis, Left Leg, Right Leg, and Tail
# Chassis bbox is (17, 45, 94, 123)
ch_px = chassis_128.load()

leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pelvis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
tail_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

for y in range(h):
    for x in range(w):
        p = ch_px[x, y]
        if p[3] == 0:
            continue
        if y >= 118:
            continue
        if y < 94:
            torso_chassis.putpixel((x, y), p)
        if 88 <= y <= 104 and 35 <= x <= 75:
            pelvis.putpixel((x, y), p)
        if 88 <= y <= 112 and x < 35:
            tail_chassis.putpixel((x, y), p)
        if 96 <= y <= 117:
            if x <= 56:
                leg_l.putpixel((x, y), p)
            else:
                leg_r.putpixel((x, y), p)

print("Torso bbox:", torso_chassis.getbbox())
print("Pelvis bbox:", pelvis.getbbox())
print("Tail bbox:", tail_chassis.getbbox())
print("Leg L bbox:", leg_l.getbbox())
print("Leg R bbox:", leg_r.getbbox())
