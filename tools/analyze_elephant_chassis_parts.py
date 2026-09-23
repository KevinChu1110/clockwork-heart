#!/usr/bin/env python3
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/elephant"

chassis = Image.open(f"{PD_DIR}/chassis/paint_elephant_brass.png").convert("RGBA")
arr = np.array(chassis)

print("Chassis bbox:", chassis.getbbox())
# Find where opaque pixels are for each row from y=40 to 127
for y in range(45, 126, 5):
    xs = np.where(arr[y, :, 3] > 30)[0]
    if len(xs) > 0:
        print(f"y={y:3d}: x min={xs[0]:2d}, max={xs[-1]:2d}, span={xs[-1]-xs[0]+1:2d}, count={len(xs):2d}")

# Let's inspect where the legs start and end
# Check row y=90..120
print("\nLeg row analysis:")
for y in range(85, 125, 2):
    xs = np.where(arr[y, :, 3] > 30)[0]
    if len(xs) > 0:
        # Check gap between left and right leg if any
        gaps = []
        for i in range(len(xs)-1):
            if xs[i+1] - xs[i] > 1:
                gaps.append((xs[i], xs[i+1]))
        print(f"y={y:3d}: x=[{xs[0]}..{xs[-1]}] gaps={gaps}")
