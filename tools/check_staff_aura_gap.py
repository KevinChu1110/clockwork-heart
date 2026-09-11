import os
import sys
from PIL import Image
from typing import cast

sys.path.insert(0, "/opt/side/bravesoul-game")
from tools.generate_fox_combat_poses import place_rigid_staff, REPO_ROOT

staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = s_px[x, y]

staff_skill = place_rigid_staff(clean_staff, deg=-45, target_hand=(86, 68))
spx = staff_skill.load()
for y in range(25, 45):
    row = [x for x in range(95, 120) if cast(tuple[int,int,int,int], spx[x, y])[3] > 40]
    print(f"y={y}: staff x in {row}")
