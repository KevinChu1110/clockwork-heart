#!/usr/bin/env python3
from PIL import Image
import numpy as np

lion_core = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/lion/optic_core/core_cyan_emerald_512.png").convert("RGBA")
print("Lion core bbox:", lion_core.getbbox())
lion_core.crop(lion_core.getbbox()).save("/tmp/lion_core_crop.png")
