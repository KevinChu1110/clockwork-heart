#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/takin"

curio = Image.open(f"{BASE_DIR}/back_curio/curio_takin_dual_bamboo_oil_flasks.png").convert("RGBA")
chassis = Image.open(f"{BASE_DIR}/chassis/chassis_takin_bronze_cast_default.png").convert("RGBA")
head = Image.open(f"{BASE_DIR}/head_unit/head_takin_brass_twisted_horn_cowl.png").convert("RGBA")
costume = Image.open(f"{BASE_DIR}/costume/costume_takin_zen_pioneer_heavy_robe.png").convert("RGBA")
optic = Image.open(f"{BASE_DIR}/optic_core/face_takin_emerald_quartz_visors.png").convert("RGBA")

# If head and optic are shifted down by 3 px:
head_shift = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
head_shift.paste(head, (0, 3), head)

optic_shift = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
optic_shift.paste(optic, (0, 3), optic)

body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body.alpha_composite(curio)
body.alpha_composite(chassis)
body.alpha_composite(head_shift)
body.alpha_composite(costume)
body.alpha_composite(optic_shift)

bbox = body.getbbox()
print("Body bbox with head shifted by 3px:", bbox)
print(f"Top margin: {bbox[1]}, Bottom margin: {128 - bbox[3]}, Left: {bbox[0]}, Right: {128 - bbox[2]}")
