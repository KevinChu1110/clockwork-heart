#!/usr/bin/env python3
from PIL import Image

idle_128 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/courser/idle.png")
idle_512 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/courser/idle_512.png")
attack_128 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/courser/attack.png")
attack_512 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/courser/attack_512.png")

print(f"idle_128: size={idle_128.size}, bbox={idle_128.getbbox()}")
print(f"idle_512: size={idle_512.size}, bbox={idle_512.getbbox()}")
print(f"attack_128: size={attack_128.size}, bbox={attack_128.getbbox()}")
print(f"attack_512: size={attack_512.size}, bbox={attack_512.getbbox()}")

shadow = [sum(1 for x in range(128) if idle_128.getpixel((x, y))[3] > 20) for y in range(118, 128)]
print(f"idle_128 shadow rows 118..127: {shadow}")
