#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idle_path = os.path.join(repo_root, "game/assets/sprites/player/bison_idle_x3.png")
idle = Image.open(idle_path).convert("RGBA")
arr = np.array(idle)
counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("bison idle shadow row counts (118..127):", counts)
bbox = idle.getbbox()
print("bison idle bbox:", bbox)

poses_idle = Image.open(os.path.join(repo_root, "game/assets/sprites/player/poses/bison/idle.png")).convert("RGBA")
arr_pi = np.array(poses_idle)
counts_pi = [int(np.sum(arr_pi[y, :, 3] > 20)) for y in range(118, 128)]
print("poses/bison/idle shadow counts:", counts_pi)

attack = Image.open(os.path.join(repo_root, "game/assets/sprites/player/poses/bison/attack.png")).convert("RGBA")
print("poses/bison/attack bbox:", attack.getbbox())
arr_atk = np.array(attack)
counts_atk = [int(np.sum(arr_atk[y, :, 3] > 20)) for y in range(118, 128)]
print("poses/bison/attack shadow counts:", counts_atk)
