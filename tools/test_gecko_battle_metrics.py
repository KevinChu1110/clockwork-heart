#!/usr/bin/env python3
import os
from PIL import Image, ImageChops
from typing import cast

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/gecko"

idle = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")
attack = Image.open(f"{POSES_DIR}/attack.png").convert("RGBA")

b_bbox = attack.getbbox()
left_m = b_bbox[0]
right_m = 128 - b_bbox[2]
top_m = b_bbox[1]
bottom_m = 128 - b_bbox[3]

diff_b = ImageChops.difference(idle, attack)
ch_b = sum(1 for y in range(128) for x in range(128) if any(c > 0 for c in cast(tuple[int, int, int, int], diff_b.getpixel((x, y)))))

diff_legs = ImageChops.difference(idle.crop((0, 88, 128, 128)), attack.crop((0, 88, 128, 128)))
ch_legs = sum(1 for y in range(40) for x in range(128) if any(c > 0 for c in cast(tuple[int, int, int, int], diff_legs.getpixel((x, y)))))

print(f"Attack bbox: {b_bbox}")
print(f"Margins: L={left_m}, R={right_m}, T={top_m}, B={bottom_m}")
print(f"Diff vs idle: {ch_b} px ({ch_b / (128*128) * 100:.1f}%) (target > 2500)")
print(f"Lower body diff (y>=88): {ch_legs} px (target > 500)")
