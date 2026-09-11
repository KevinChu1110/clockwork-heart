#!/usr/bin/env python3
from PIL import Image

mac_ear = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/head_unit/ear_macaque_coaxial.png").convert("RGBA")
print("Macaque ear bbox:", mac_ear.getbbox())
