#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/hippo"

head512 = Image.open(f"{PD_DIR}/head_unit/head_hippo_ballast_safety_valve_cowl_512.png").convert("RGBA")
core512 = Image.open(f"{PD_DIR}/optic_core/face_hippo_dual_pressure_gauge_quartz_lens_512.png").convert("RGBA")
key512 = Image.open(f"{PD_DIR}/winding_key/key_hippo_dual_valve_handwheel_brass_512.png").convert("RGBA")

print("head512 bbox:", head512.getbbox())
print("core512 bbox:", core512.getbbox())
print("key512 bbox:", key512.getbbox())
