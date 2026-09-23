#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"

comp = Image.open(f"{BASE}/proof_paperdoll_tortoise_composite.png").convert("RGBA")
print(f"Composite: size={comp.size}, bbox={comp.getbbox()}")

# Shadow analysis
c_px = comp.load()
shadow_counts = []
for y in range(118, 128):
    c = 0
    for x in range(128):
        p = c_px[x, y]
        if p[3] > 20:
            c += 1
    shadow_counts.append(c)
print(f"Shadow counts (118..127): {shadow_counts}")

# Check idle_x3 shadow
idle_x3 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/tortoise_idle_x3.png").convert("RGBA")
ix_px = idle_x3.load()
ix_counts = []
for y in range(118, 128):
    c = 0
    for x in range(128):
        p = ix_px[x, y]
        if p[3] > 20:
            c += 1
    ix_counts.append(c)
print(f"tortoise_idle_x3 shadow counts (118..127): {ix_counts}")

# Check weapon
wpn = Image.open(f"{BASE}/weapon/wpn_bagua_astrolabe.png").convert("RGBA")
print(f"Weapon: size={wpn.size}, bbox={wpn.getbbox()}")

# Check all slices
for s in ["winding_key/key_tai_chi_dual_fish.png",
          "back_curio/curio_bagua_armillary_rings.png",
          "chassis/paint_tortoise_jade.png",
          "head_unit/head_xuanji_tortoise_stock.png",
          "costume/costume_zen_dojo_harness.png",
          "optic_core/core_amber_quartz.png",
          "weapon/wpn_bagua_astrolabe.png"]:
    im = Image.open(f"{BASE}/{s}").convert("RGBA")
    print(f"  {s:45s} bbox={im.getbbox()}")
