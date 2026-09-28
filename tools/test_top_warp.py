#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
RHINO_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rhino"

head_src = Image.open(f"{RHINO_DIR}/head_unit/head_rhino_crucible_battering_crest.png").convert("RGBA")
curio_src = Image.open(f"{RHINO_DIR}/back_curio/curio_rhino_steam_furnace_exhaust.png").convert("RGBA")
chassis_src = Image.open(f"{RHINO_DIR}/chassis/chassis_rhino_molten_iron_default.png").convert("RGBA")
costume_src = Image.open(f"{RHINO_DIR}/costume/costume_rhino_crucible_smith_plate.png").convert("RGBA")
optic_src = Image.open(f"{RHINO_DIR}/optic_core/face_rhino_dual_amber_pyro_optic.png").convert("RGBA")
weapon_src = Image.open(f"{RHINO_DIR}/weapon/weapon_rhino_crucible_breaker_axe.png").convert("RGBA")
key_src = Image.open(f"{RHINO_DIR}/winding_key/key_rhino_crucible_crosshair_key.png").convert("RGBA")

body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)

# Check vertical distribution of body_core
b = body_core.getbbox()
print("Original body_core bbox:", b)

# Apply a vertical compression for y < 35 such that y=0 maps to y=4 and y>=35 is unchanged
w, h = body_core.size
src_pixels = body_core.load()
out_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
out_pixels = out_img.load()

for y in range(h):
    if y < 4:
        continue # empty
    elif y < 35:
        # map y in [4, 35) from src_y in [0, 35)
        src_y = (y - 4) * (35.0 / 31.0)
    else:
        src_y = float(y)
    
    y0 = int(src_y)
    y1 = min(h - 1, y0 + 1)
    fy = src_y - y0
    
    for x in range(w):
        p0 = src_pixels[x, y0]
        p1 = src_pixels[x, y1]
        rgba = tuple(int(round(p0[c] * (1 - fy) + p1[c] * fy)) for c in range(4))
        out_pixels[x, y] = rgba

b_new = out_img.getbbox()
print("New body_core bbox:", b_new)
left, top, right, bottom = b_new[0], b_new[1], 128 - b_new[2], 128 - b_new[3]
print(f"New margins: L={left}, T={top}, R={right}, B={bottom}")

# Check shadow row counts
arr = np.array(out_img)
shadow = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print(f"Shadow counts (118..127): {shadow}")
