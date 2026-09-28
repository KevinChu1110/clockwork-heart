#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
idle_512 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/courser/idle_512.png").convert("RGBA")

# Let's inspect where the character's head and upper body are:
for x1, x2 in [(50, 480), (30, 490), (0, 512)]:
    b = idle_512.crop((x1, 10, x2, 400)).getbbox()
    print(f"crop ({x1}, 10, {x2}, 400): bbox={b}")

# Head crop for HUD:
for y2 in [220, 240, 260]:
    h = idle_512.crop((100, 10, 440, y2)).getbbox()
    print(f"head crop (100, 10, 440, {y2}): bbox={h}")
