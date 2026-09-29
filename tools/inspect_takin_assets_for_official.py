#!/usr/bin/env python3
import os
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
poses_idle = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/takin/idle.png").convert("RGBA")
takin_idle_x3 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/takin_idle_x3.png").convert("RGBA")
party_idle = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/takin_idle.png").convert("RGBA")
poses_idle_512 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/takin/idle_512.png").convert("RGBA")
showcase_hd = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/showcase/takin_idle_hd.png").convert("RGBA")

print("poses/idle bbox:     ", poses_idle.getbbox(), poses_idle.size)
print("takin_idle_x3 bbox:  ", takin_idle_x3.getbbox(), takin_idle_x3.size)
print("party/idle bbox:     ", party_idle.getbbox(), party_idle.size)
print("poses/idle_512 bbox: ", poses_idle_512.getbbox(), poses_idle_512.size)
print("showcase_hd bbox:    ", showcase_hd.getbbox(), showcase_hd.size)

diff_pi_ti = ImageChops.difference(poses_idle, takin_idle_x3).getbbox()
print("diff(poses_idle, takin_idle_x3):", diff_pi_ti)
diff_pi_party = ImageChops.difference(poses_idle, party_idle).getbbox()
print("diff(poses_idle, party_idle):", diff_pi_party)

arr_shd = np.array(poses_idle)
counts = [int(np.sum(arr_shd[y, :, 3] > 20)) for y in range(118, 128)]
print("Shadow rows (118..127):", counts)
