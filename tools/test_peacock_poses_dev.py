#!/usr/bin/env python3
"""
Test script to prototype build_peacock_combat_poses.py
"""
import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/peacock"

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_peacock_filigree_sunburst_key.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_peacock_articulated_kaleidoscope_fan.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_peacock_glazed_porcelain_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_peacock_baroque_diadem_prism.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_peacock_marionette_court_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_peacock_kaleidoscope_gem_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_peacock_kaleidoscope_prism_focus.png").convert("RGBA")

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Base body composite
body_core_raw = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core_raw.alpha_composite(curio_src)
body_core_raw.alpha_composite(chassis_src)
body_core_raw.alpha_composite(head_src)
body_core_raw.alpha_composite(costume_src)
body_core_raw.alpha_composite(optic_src)

# Smoothly compress y < 45 so y=0 maps to y=4
w, h = body_core_raw.size
src_px = body_core_raw.load()
body_core = Image.new("RGBA", (w, h), (0, 0, 0, 0))
dst_px = body_core.load()
assert src_px is not None and dst_px is not None

for y in range(h):
    if y < 4:
        continue
    elif y < 45:
        src_y = (y - 4) * (45.0 / 41.0)
    else:
        src_y = float(y)
    y0 = int(src_y)
    y1 = min(h - 1, y0 + 1)
    fy = src_y - y0
    for x in range(w):
        p0 = cast(tuple[int, int, int, int], src_px[x, y0])
        p1 = cast(tuple[int, int, int, int], src_px[x, y1])
        rgba = tuple(int(round(p0[c] * (1 - fy) + p1[c] * fy)) for c in range(4))
        dst_px[x, y] = rgba

# Baseline shadow
comp = Image.open(f"{BASE_DIR}/proof_paperdoll_peacock_composite.png").convert("RGBA")
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = comp.load()
assert s_px is not None and c_px is not None

for y in range(118, 126):
    for x in range(4, 124):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p
        else:
            s_px[x, y] = (0, 0, 0, 0)

EXPECTED_SHADOW = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], s_px[x, y])[3] > 20) for y in range(118, 128)]
print(f"Benchmark ground shadow: {EXPECTED_SHADOW}")
