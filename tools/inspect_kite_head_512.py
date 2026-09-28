#!/usr/bin/env python3
from PIL import Image

idle_512 = Image.open("game/assets/sprites/player/poses/kite/idle_512.png").convert("RGBA")
head_512 = Image.open("game/assets/sprites/player/paperdoll/kite/head_unit/head_kite_raptor_cowl_beak_512.png").convert("RGBA")
optic_512 = Image.open("game/assets/sprites/player/paperdoll/kite/optic_core/face_kite_amber_quartz_rangefinder_512.png").convert("RGBA")

print("Head 512 bbox:", head_512.getbbox())
print("Optic 512 bbox:", optic_512.getbbox())
