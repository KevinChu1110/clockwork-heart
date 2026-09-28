#!/usr/bin/env python3
from PIL import Image, ImageChops

comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/sailfish/proof_paperdoll_sailfish_composite.png")
idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/sailfish/idle.png")

diff = ImageChops.difference(comp, idle)
print("Difference between proof_paperdoll_sailfish_composite and poses/idle:", diff.getbbox())
