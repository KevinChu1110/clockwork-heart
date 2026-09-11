import os
import hashlib
import sys

sys.path.insert(0, "/opt/side/bravesoul-game")
from tools.generate_fox_combat_poses import generate_fox_poses

OUTPUT_TEMP = "/tmp/fox_test/poses_check"
os.makedirs(OUTPUT_TEMP, exist_ok=True)

# Temporarily mock OUTPUT_DIR
import tools.generate_fox_combat_poses as gf
gf.OUTPUT_DIR = OUTPUT_TEMP

generate_fox_poses()

POSES_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"
for p in ["idle", "telegraph", "attack", "recover", "skill", "hit"]:
    h_orig = hashlib.md5(open(f"{POSES_DIR}/{p}.png", "rb").read()).hexdigest()
    h_new = hashlib.md5(open(f"{OUTPUT_TEMP}/{p}.png", "rb").read()).hexdigest()
    print(f"{p:10s} match: {h_orig == h_new} (orig: {h_orig[:8]}, new: {h_new[:8]})")
