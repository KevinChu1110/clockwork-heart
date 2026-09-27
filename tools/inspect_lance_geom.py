#!/usr/bin/env python3
from PIL import Image

wpn = Image.open('/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/hound/weapon/weapon_hound_stellar_beacon_lance.png').convert('RGBA')
bbox = wpn.getbbox()
print("Weapon bbox:", bbox)
# Grip was designed at (28, 74)
# Lance tip at (4, 42)
# Counterweight at (48, 88)
cropped = wpn.crop(bbox)
print("Cropped size:", cropped.size)
# Relative grip position in cropped image:
rx = 28 - bbox[0]
ry = 74 - bbox[1]
print(f"Relative grip in cropped: ({rx}, {ry})")
