#!/usr/bin/env python3
import os
from PIL import Image

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"

comp = Image.open(f"{BASE}/proof_paperdoll_tortoise_composite.png").convert("RGBA")
wpn = Image.open(f"{BASE}/weapon/wpn_bagua_astrolabe.png").convert("RGBA")

w_bbox = wpn.getbbox()
print(f"wpn bbox: {w_bbox}")
wb = wpn.crop(w_bbox)
print(f"cropped wpn size: {wb.size}")

# Check weapon center relative to crop
cx = wb.size[0] / 2.0
cy = wb.size[1] / 2.0
print(f"cropped weapon center: ({cx}, {cy})")
