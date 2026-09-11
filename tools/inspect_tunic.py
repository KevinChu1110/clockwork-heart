#!/usr/bin/env python3
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

chassis = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png").convert("RGBA")
head = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial.png").convert("RGBA")
tunic = Image.open(f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic.png").convert("RGBA")
striker = Image.open(f"{MACAQUE_DIR}/costume/costume_zen_striker.png").convert("RGBA")

# Let's inspect where tunic has alpha > 0
t_pts = [(x, y) for y in range(128) for x in range(128) if cast(tuple[int, int, int, int], tunic.getpixel((x, y)))[3] > 0]
s_pts = [(x, y) for y in range(128) for x in range(128) if cast(tuple[int, int, int, int], striker.getpixel((x, y)))[3] > 0]

print("Tunic bbox:", tunic.getbbox())
print("Striker bbox:", striker.getbbox())

# Let's check tunic min/max y:
min_ty = min(y for x, y in t_pts)
max_ty = max(y for x, y in t_pts)
print(f"Tunic y range: {min_ty}..{max_ty}")

min_sy = min(y for x, y in s_pts)
max_sy = max(y for x, y in s_pts)
print(f"Striker y range: {min_sy}..{max_sy}")
