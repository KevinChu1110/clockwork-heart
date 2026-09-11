#!/usr/bin/env python3
from PIL import Image

key = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/winding_key/key_classic_brass.png")
tail = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/back_curio/curio_spring_tail.png")

print("key at (97, 51):", key.getpixel((97, 51)))
print("tail at (97, 51):", tail.getpixel((97, 51)))

# check neighbors of (97, 51) in tail
for dy in range(-2, 3):
    for dx in range(-2, 3):
        print(f"({97+dx}, {51+dy}): tail={tail.getpixel((97+dx, 51+dy))[3]}, key={key.getpixel((97+dx, 51+dy))[3]}")
