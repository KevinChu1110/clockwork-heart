#!/usr/bin/env python3
from PIL import Image

idle_x3 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_idle_x3.png").convert("RGBA")

# Let's inspect colors of the face in idle_x3:
face_cols = [idle_x3.getpixel((x, 40)) for x in range(45, 60)]
print("Face y=40 colors in idle_x3:")
for c in face_cols:
    print(f"  {c}")

# Belly in idle_x3:
belly_cols = [idle_x3.getpixel((x, 75)) for x in range(45, 60)]
print("Belly y=75 colors in idle_x3:")
for c in belly_cols:
    print(f"  {c}")

# Arm in idle_x3:
arm_cols = [idle_x3.getpixel((35, y)) for y in range(70, 85)]
print("Arm x=35 colors in idle_x3:")
for c in arm_cols:
    print(f"  {c}")
