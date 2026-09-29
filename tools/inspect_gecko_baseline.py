#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/gecko"

idle128 = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")
arr128 = np.array(idle128)
print("idle 128 size:", idle128.size, "bbox:", idle128.getbbox())

shadow_counts = [int(np.sum(arr128[y, :, 3] > 20)) for y in range(118, 128)]
print("Shadow row counts (118..127):", shadow_counts)

idle512 = Image.open(f"{POSES_DIR}/idle_512.png").convert("RGBA")
print("idle 512 size:", idle512.size, "bbox:", idle512.getbbox())

attack128 = Image.open(f"{POSES_DIR}/attack.png").convert("RGBA")
print("attack 128 size:", attack128.size, "bbox:", attack128.getbbox())

attack512 = Image.open(f"{POSES_DIR}/attack_512.png").convert("RGBA")
print("attack 512 size:", attack512.size, "bbox:", attack512.getbbox())
