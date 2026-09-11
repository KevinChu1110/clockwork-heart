import os
import sys
from PIL import Image

sys.path.insert(0, "/opt/side/bravesoul-game/tools")
from generate_fox_combat_poses import shifts_telegraph, shifts_recover, shifts_skill, base_landmarks

print("Current shifts_telegraph:", shifts_telegraph["ear_l"], shifts_telegraph["snout"])
print("Current shifts_recover:", shifts_recover["ear_l"], shifts_recover["snout"])
print("Current shifts_skill:", shifts_skill["ear_l"], shifts_skill["snout"])
