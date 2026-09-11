#!/usr/bin/env python3
from PIL import Image

char_m = Image.open("/opt/side/bravesoul-game/branding/char_macaque.png").convert("RGBA")
comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png").convert("RGBA")

print("char_m size:", char_m.size)
print("comp size:", comp.size)

# Let's find bounding box of char_m
bbox_char = char_m.getbbox()
print("bbox char_m:", bbox_char)
bbox_comp = comp.getbbox()
print("bbox comp:", bbox_comp)
