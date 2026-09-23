#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tortoise"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
PARTY_DIR = f"{PLAYER_DIR}/party"
PORTRAITS_DIR = f"{REPO_ROOT}/game/assets/sprites/portraits"
BRANDING_DIR = f"{REPO_ROOT}/branding"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"
DOCS_ART_DIR = f"{REPO_ROOT}/docs/art"

os.makedirs(PARTY_DIR, exist_ok=True)
os.makedirs(PORTRAITS_DIR, exist_ok=True)
os.makedirs(BRANDING_DIR, exist_ok=True)
os.makedirs(WEB_HERO_DIR, exist_ok=True)
os.makedirs(DOCS_ART_DIR, exist_ok=True)

# 1. Load 128 slices
chassis = Image.open(f"{PD_DIR}/chassis/paint_tortoise_jade.png").convert("RGBA")
head = Image.open(f"{PD_DIR}/head_unit/head_xuanji_tortoise_stock.png").convert("RGBA")
key = Image.open(f"{PD_DIR}/winding_key/key_tai_chi_dual_fish.png").convert("RGBA")
costume = Image.open(f"{PD_DIR}/costume/costume_zen_dojo_harness.png").convert("RGBA")
core = Image.open(f"{PD_DIR}/optic_core/core_amber_quartz.png").convert("RGBA")
weapon = Image.open(f"{PD_DIR}/weapon/wpn_bagua_astrolabe.png").convert("RGBA")
curio = Image.open(f"{PD_DIR}/back_curio/curio_bagua_armillary_rings.png").convert("RGBA")

w, h = 128, 128

# 128 composite
comp128 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
comp128.alpha_composite(key)
comp128.alpha_composite(curio)
comp128.alpha_composite(chassis)
comp128.alpha_composite(head)
comp128.alpha_composite(costume)
comp128.alpha_composite(core)
comp128.alpha_composite(weapon)

# 2. Load 512 slices & build 512 composite
slices_512 = [
    f"{PD_DIR}/winding_key/key_tai_chi_dual_fish_512.png",
    f"{PD_DIR}/back_curio/curio_bagua_armillary_rings_512.png",
    f"{PD_DIR}/chassis/paint_tortoise_jade_512.png",
    f"{PD_DIR}/head_unit/head_xuanji_tortoise_stock_512.png",
    f"{PD_DIR}/costume/costume_zen_dojo_harness_512.png",
    f"{PD_DIR}/optic_core/core_amber_quartz_512.png",
    f"{PD_DIR}/weapon/wpn_bagua_astrolabe_512.png",
]
comp512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
for p in slices_512:
    comp512.alpha_composite(Image.open(p).convert("RGBA"))

print("Comp 128 bbox:", comp128.getbbox())
print("Comp 512 bbox:", comp512.getbbox())
