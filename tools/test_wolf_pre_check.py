import os
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/wolf"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/wolf"

comp128 = Image.open(f"{PD_DIR}/proof_paperdoll_wolf_composite.png").convert("RGBA")
attack128 = Image.open(f"{POSES_DIR}/attack.png").convert("RGBA")

diff_b = ImageChops.difference(comp128, attack128)
ch_b = sum(1 for y in range(128) for x in range(128) if any(c > 0 for c in diff_b.getpixel((x, y))))
diff_legs = ImageChops.difference(comp128.crop((0, 92, 128, 128)), attack128.crop((0, 92, 128, 128)))
ch_legs = sum(1 for y in range(36) for x in range(128) if any(c > 0 for c in diff_legs.getpixel((x, y))))

b_bbox = attack128.getbbox()
print(f"Attack 128 bbox: {b_bbox}")
print(f"Battle vs idle diff: changed={ch_b}px ({ch_b / (128*128) * 100:.1f}%)")
print(f"Battle legs diff (y>=92): changed={ch_legs}px")

comp_arr = np.array(comp128)
atk_arr = np.array(attack128)
s_comp = [int(np.sum(comp_arr[y, :, 3] > 20)) for y in range(118, 128)]
s_atk = [int(np.sum(atk_arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Shadow comp:", s_comp)
print("Shadow attack:", s_atk)
