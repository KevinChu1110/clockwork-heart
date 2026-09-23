#!/usr/bin/env python3
from PIL import Image
import numpy as np

chassis = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise/chassis/paint_tortoise_jade.png").convert("RGBA")
arr = np.array(chassis)

print("Chassis size:", chassis.size)
print("Chassis bbox:", chassis.getbbox())

# Check shadow rows at y >= 115
for y in range(115, 128):
    row_alpha = arr[y, :, 3]
    count = np.sum(row_alpha > 20)
    print(f"y={y}: opaque count={count}")
