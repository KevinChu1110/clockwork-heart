#!/usr/bin/env python3
from PIL import Image

core = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/optic_core/core_cyan_emerald.png").convert("RGBA")
print("core size:", core.size)
print("core bbox:", core.getbbox())
