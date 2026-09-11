import os
import sys
from PIL import Image

sys.path.insert(0, "/opt/side/bravesoul-game")
from tools.generate_fox_combat_poses import (
    build_contact_shadow, place_rigid_staff, warp_image_idw,
    REPO_ROOT, OUTPUT_DIR
)

staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")

clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = s_px[x, y]

# Check body_clean bbox
print("body_clean bbox:", body_clean.getbbox())

# Let's inspect where top pixels come from in skill and recover
im_skill = Image.open(f"{OUTPUT_DIR}/skill.png")
im_rec = Image.open(f"{OUTPUT_DIR}/recover.png")

# In skill, let's see staff bbox vs body bbox vs aura bbox
# In generate_fox_combat_poses.py:
# staff_skill = place_rigid_staff(clean_staff, deg=-45, target_hand=(86, 68))
staff_skill = place_rigid_staff(clean_staff, deg=-45, target_hand=(86, 68))
print("staff_skill bbox:", staff_skill.getbbox())

# What about aura?
# a_draw.ellipse([98, 18, 114, 34]...
# So aura is at y >= 18.

# What about warped_skill?
# Let's check warped_skill bbox!
base_landmarks = {
    "ear_l": (48, 12), "ear_r": (76, 12), "forehead": (62, 28),
    "eye_l": (50, 46), "eye_r": (72, 46), "snout": (60, 56),
    "neck": (60, 64), "core": (60, 75), "shoulder_l": (42, 70), "shoulder_r": (78, 68),
    "key_mount": (30, 62), "key_top": (22, 56), "key_bot": (22, 68),
    "pelvis": (60, 94),
    "tail_base": (33, 90), "tail_mid": (26, 102), "tail_tip": (22, 114),
    "hip_l": (48, 95), "knee_l": (50, 106), "foot_l": (52, 117),
    "hip_r": (68, 95), "knee_r": (72, 106), "foot_r": (74, 117),
    "hand": (90, 86),
}
anchors = [(0, 0), (127, 0), (0, 127), (127, 127)]
shifts_skill = {
    "ear_l": (-2, -8), "ear_r": (3, -8), "forehead": (1, -7),
    "eye_l": (0, -7), "eye_r": (2, -7), "snout": (2, -10),
    "neck": (1, -5), "core": (1, -4), "shoulder_l": (-2, -5), "shoulder_r": (4, -7),
    "key_mount": (-1, -4), "key_top": (-1, -4), "key_bot": (-1, -4),
    "pelvis": (0, -3), "hip_l": (-1, -3), "hip_r": (1, -3),
    "tail_base": (-1, -4), "tail_mid": (-7, -10), "tail_tip": (-12, -16),
    "knee_l": (0, -2), "foot_l": (0, -1),
    "knee_r": (0, -2), "foot_r": (0, -1),
    "hand": (4, -22),
}
src_pts = list(anchors)
dst_pts = list(anchors)
for name, (bx, by) in base_landmarks.items():
    dx, dy = shifts_skill.get(name, (0, 0))
    src_pts.append((bx, by))
    dst_pts.append((bx + dx, by + dy))

warped_skill = warp_image_idw(body_clean, src_pts, dst_pts)
print("warped_skill bbox:", warped_skill.getbbox())

# Let's inspect warped_skill min_y and staff_skill min_y
def get_min_y(im):
    px = im.load()
    for y in range(128):
        for x in range(128):
            if px[x, y][3] > 10:
                return y
    return -1

print("warped_skill min_y:", get_min_y(warped_skill))
print("staff_skill min_y:", get_min_y(staff_skill))
