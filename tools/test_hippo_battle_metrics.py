#!/usr/bin/env python3
import os
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/hippo"

idle = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")
attack = Image.open(f"{POSES_DIR}/attack.png").convert("RGBA")

b_bbox = attack.getbbox()
print("Attack bbox:", b_bbox)
left_m = b_bbox[0]
right_m = 128 - b_bbox[2]
top_m = b_bbox[1]
bottom_m = 128 - b_bbox[3]
print(f"Margins: left={left_m}, right={right_m}, top={top_m}, bottom={bottom_m}")

diff_b = ImageChops.difference(idle, attack)
ch_b = sum(1 for y in range(128) for x in range(128) if any(c > 0 for c in diff_b.getpixel((x, y))))
diff_legs = ImageChops.difference(idle.crop((0, 88, 128, 128)), attack.crop((0, 88, 128, 128)))
ch_legs = sum(1 for y in range(40) for x in range(128) if any(c > 0 for c in diff_legs.getpixel((x, y))))

print(f"Battle vs idle diff: changed={ch_b}px ({ch_b / (128*128) * 100:.1f}%)")
print(f"Battle lower body/chassis diff (y>=88): changed={ch_legs}px")
