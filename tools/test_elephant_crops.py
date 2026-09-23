#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/elephant"

key_512 = Image.open(f"{PD_DIR}/winding_key/key_heavy_cross_wheel_512.png").convert("RGBA")
curio_512 = Image.open(f"{PD_DIR}/back_curio/curio_dual_pressure_gauge_512.png").convert("RGBA")
chassis_512 = Image.open(f"{PD_DIR}/chassis/paint_elephant_brass_512.png").convert("RGBA")
head_512 = Image.open(f"{PD_DIR}/head_unit/head_colossus_elephant_stock_512.png").convert("RGBA")
costume_512 = Image.open(f"{PD_DIR}/costume/costume_cog_workshop_overalls_512.png").convert("RGBA")
core_512 = Image.open(f"{PD_DIR}/optic_core/core_sky_quartz_512.png").convert("RGBA")
wpn_512 = Image.open(f"{PD_DIR}/weapon/wpn_colossus_cleaver_axe_512.png").convert("RGBA")

comp512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
comp512.alpha_composite(key_512)
comp512.alpha_composite(curio_512)
comp512.alpha_composite(chassis_512)
comp512.alpha_composite(head_512)
comp512.alpha_composite(costume_512)
comp512.alpha_composite(core_512)
comp512.alpha_composite(wpn_512)

print("comp512 bbox:", comp512.getbbox())

# Test HUD bust (no weapon, focused head + collar)
hud_comp = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
hud_comp.alpha_composite(key_512)
hud_comp.alpha_composite(curio_512)
hud_comp.alpha_composite(chassis_512)
hud_comp.alpha_composite(head_512)
hud_comp.alpha_composite(costume_512)
hud_comp.alpha_composite(core_512)

hud_box = (60, 60, 440, 360)
hud_crop = hud_comp.crop(hud_box)
print("hud_crop size:", hud_crop.size, "bbox:", hud_crop.getbbox())

# Test Dialogue bust (waist up, no legs/feet)
# Feet end around y=496, legs start around y=360, waist is around y=340..360
dia_box = (40, 60, 485, 380)
dia_crop = comp512.crop(dia_box)
print("dia_crop size:", dia_crop.size, "bbox:", dia_crop.getbbox())
