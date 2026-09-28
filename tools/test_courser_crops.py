#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
idle_512 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/courser/idle_512.png").convert("RGBA")

# In 128 space:
# head: y=5..50
# core: y=33..48
# In 512 space, multiply by 4:
# head: y=20..200
# core: y=132..192
# chanfron & mane: x=150..370, y=20..220

head_crop = idle_512.crop((120, 10, 420, 240))
print(f"head crop bbox: {head_crop.getbbox()}")

bust_crop = idle_512.crop((80, 10, 460, 400))
print(f"bust crop bbox: {bust_crop.getbbox()}")
