import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from typing import cast

sys.path.insert(0, "/opt/side/bravesoul-game")
from tools.generate_fox_combat_poses import (
    build_contact_shadow, place_rigid_staff, warp_image_idw,
    measure_staff_linearity, measure_shadow_rows,
    REPO_ROOT, OUTPUT_DIR
)
from tools.cc_helper import get_connected_components

staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")

# Clean staff
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = s_px[x, y]

# Clean body_clean bottom area
b_px = body_clean.load()
for y in range(112, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], b_px[x, y])
        if p[3] > 0:
            is_solid_paw = (46 <= x <= 58 or 69 <= x <= 80) and y <= 122 and p[0] < 125 and p[1] < 105 and p[2] < 80
            if not is_solid_paw:
                b_px[x, y] = (0, 0, 0, 0)

# Rigid staff with bridge (for skill)
staff_rigid = clean_staff.copy()
draw_cs = ImageDraw.Draw(staff_rigid)
draw_cs.polygon([(86, 54), (99, 56), (99, 60), (86, 58)], fill=(120, 80, 50, 255))
draw_cs.line([(86, 54), (99, 56)], fill=(50, 30, 20, 255), width=1)
draw_cs.line([(86, 58), (99, 60)], fill=(50, 30, 20, 255), width=1)
draw_cs.line([(91, 95), (88, 99)], fill=(115, 75, 45, 255), width=2)
draw_cs.line([(88, 108), (89, 117)], fill=(115, 75, 45, 255), width=2)

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

def generate_new_recover():
    shifts = {
        "ear_l": (-4, 7),
        "ear_r": (4, 7),
        "forehead": (0, 7),
        "eye_l": (-2, 6),
        "eye_r": (2, 6),
        "snout": (0, 6),
        "neck": (0, 6),
        "core": (0, 5),
        "shoulder_l": (-6, 5),
        "shoulder_r": (6, 5),
        "key_mount": (-6, 5),
        "key_top": (-6, 5),
        "key_bot": (-6, 5),
        "pelvis": (0, 4),
        "hip_l": (-12, 4),
        "hip_r": (12, 4),
        "tail_base": (0, 4),
        "tail_mid": (-12, 3),
        "tail_tip": (-17, 1),
        "knee_l": (-13, 3),
        "foot_l": (-6, 1),
        "knee_r": (13, 3),
        "foot_r": (6, 1),
        "hand": (-2, 10),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    staff = place_rigid_staff(clean_staff, deg=-2, target_hand=(88, 96))
    shadow = build_contact_shadow(cx=60, cy=121, rx=44, ry=6, blur=0.7)
    
    comp = Image.alpha_composite(shadow, warped)
    comp = Image.alpha_composite(comp, staff)
    return comp

def generate_new_skill():
    shifts = {
        "ear_l": (-3, 1), "ear_r": (3, 1), "forehead": (1, 1),
        "eye_l": (1, 1), "eye_r": (3, 1), "snout": (4, 1),
        "neck": (2, -2), "core": (2, -2), 
        "shoulder_l": (-3, -3), "shoulder_r": (6, -4),
        "key_mount": (-3, -3), "key_top": (-4, -3), "key_bot": (-4, -3),
        "pelvis": (1, -1),
        "hip_l": (-4, -1), "knee_l": (-6, 0), "foot_l": (-3, 0),
        "hip_r": (4, -1), "knee_r": (6, 0), "foot_r": (3, 0),
        "tail_base": (-2, -4), 
        "tail_mid": (-12, -13), 
        "tail_tip": (-20, -18),
        "hand": (4, -18), # hand at (94, 68)
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    staff = place_rigid_staff(staff_rigid, deg=-45, target_hand=(86, 68))
    
    # Arm layer
    arm_layer = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw_arm = ImageDraw.Draw(arm_layer)
    draw_arm.polygon([(78, 64), (84, 62), (88, 68), (86, 72), (80, 70)], fill=(30, 22, 28, 255))
    draw_arm.polygon([(79, 65), (83, 63), (87, 68), (85, 71), (81, 69)], fill=(55, 75, 95, 255))
    draw_arm.ellipse([84, 66, 88, 70], fill=(210, 175, 90, 255))

    skill_aura = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(skill_aura)
    a_draw.ellipse([98, 18, 114, 34], fill=(80, 235, 255, 140))
    a_draw.ellipse([102, 22, 110, 30], fill=(230, 255, 255, 220))
    a_draw.ellipse([50, 62, 72, 84], fill=(50, 220, 240, 80))
    skill_aura = skill_aura.filter(ImageFilter.GaussianBlur(0.8))

    skill_shadow = build_contact_shadow(cx=60, cy=119, rx=34, ry=4, blur=0.6)
    comp = Image.alpha_composite(skill_shadow, warped)
    comp = Image.alpha_composite(comp, arm_layer)
    comp = Image.alpha_composite(comp, staff)
    comp = Image.alpha_composite(comp, skill_aura)
    return comp

rec_img = generate_new_recover()
skill_img = generate_new_skill()

# Save preview
rec_img.save("/tmp/fox_test/new_recover.png")
skill_img.save("/tmp/fox_test/new_skill.png")
print("Saved /tmp/fox_test/new_recover.png and new_skill.png")
