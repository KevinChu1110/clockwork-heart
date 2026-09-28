#!/usr/bin/env python3
import os
from PIL import Image, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/kite"

comp = Image.open(f"{BASE_DIR}/proof_paperdoll_kite_composite.png").convert("RGBA")

key_src = Image.open(f"{BASE_DIR}/winding_key/key_kite_turbine_relief_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_kite_spring_steel_cooling_wings.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_kite_copper_obsidian_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_kite_raptor_cowl_beak.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_kite_welder_cape_belt.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_kite_amber_quartz_rangefinder.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_kite_crucible_recurve_bow.png").convert("RGBA")

synth = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
synth.alpha_composite(key_src)
synth.alpha_composite(curio_src)
synth.alpha_composite(chassis_src)
synth.alpha_composite(head_src)
synth.alpha_composite(costume_src)
synth.alpha_composite(optic_src)
synth.alpha_composite(weapon_src)

diff = ImageChops.difference(comp, synth)
bbox = diff.getbbox()
print("Diff bbox between proof_composite and synth:", bbox)
