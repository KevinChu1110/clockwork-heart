#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/takin"

chassis_512 = Image.open(f"{PD_DIR}/chassis/chassis_takin_bronze_cast_default_512.png").convert("RGBA")
head_512 = Image.open(f"{PD_DIR}/head_unit/head_takin_brass_twisted_horn_cowl_512.png").convert("RGBA")
costume_512 = Image.open(f"{PD_DIR}/costume/costume_takin_zen_pioneer_heavy_robe_512.png").convert("RGBA")
core_512 = Image.open(f"{PD_DIR}/optic_core/face_takin_emerald_quartz_visors_512.png").convert("RGBA")

print("head_512 bbox:   ", head_512.getbbox())
print("core_512 bbox:   ", core_512.getbbox())
print("costume_512 bbox:", costume_512.getbbox())
print("chassis_512 bbox:", chassis_512.getbbox())

# Test compositing with y+12 shift for head and core
head_shift_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
head_shift_512.paste(head_512, (0, 12), head_512)
core_shift_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
core_shift_512.paste(core_512, (0, 12), core_512)

bust_hud = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
bust_hud.alpha_composite(chassis_512)
bust_hud.alpha_composite(head_shift_512)
bust_hud.alpha_composite(costume_512)
bust_hud.alpha_composite(core_shift_512)

print("bust_hud bbox:   ", bust_hud.getbbox())
