import os
import sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter
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

# Clean staff with rigid bridges (matching attack and hit)
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = s_px[x, y]

staff_rigid = clean_staff.copy()
draw_cs = ImageDraw.Draw(staff_rigid)
draw_cs.polygon([(86, 54), (99, 56), (99, 60), (86, 58)], fill=(120, 80, 50, 255))
draw_cs.line([(86, 54), (99, 56)], fill=(50, 30, 20, 255), width=1)
draw_cs.line([(86, 58), (99, 60)], fill=(50, 30, 20, 255), width=1)
draw_cs.line([(91, 95), (88, 99)], fill=(115, 75, 45, 255), width=2)
draw_cs.line([(88, 108), (89, 117)], fill=(115, 75, 45, 255), width=2)

idle_img = Image.open(f"{OUTPUT_DIR}/idle.png")

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

def eval_skill_refined(ear_dy=0, leg_spread=2, tail_dy=-16):
    shifts = {
        "ear_l": (-3, ear_dy), "ear_r": (3, ear_dy), "forehead": (1, ear_dy),
        "eye_l": (1, ear_dy), "eye_r": (3, ear_dy), "snout": (4, ear_dy),
        "neck": (2, -2), "core": (2, -2), 
        "shoulder_l": (-3, -3), "shoulder_r": (6, -4),
        "key_mount": (-3, -3), "key_top": (-4, -3), "key_bot": (-4, -3),
        "pelvis": (1, -1),
        "hip_l": (-4, -1), "knee_l": (-6, 0), "foot_l": (-3, 0),
        "hip_r": (4, -1), "knee_r": (6, 0), "foot_r": (3, 0),
        "tail_base": (-2, -4), 
        "tail_mid": (-12, int(round(tail_dy * 0.7))), 
        "tail_tip": (-20, tail_dy),
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
    
    px = comp.load()
    min_x, min_y, max_x, max_y = 128, 128, -1, -1
    for y in range(118):
        for x in range(128):
            if px[x, y][3] > 10:
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
    h = max_y - min_y + 1
    
    diff = ImageChops.difference(idle_img, comp)
    diff_data = [x for x in diff.convert("L").getdata() if x > 10]
    diff_px = len(diff_data)
    
    resid = measure_staff_linearity(comp)
    comps = get_connected_components(comp, alpha_thresh=40, y_max=118)
    sh_rows = measure_shadow_rows(comp)
    
    print(f"ear_dy={ear_dy:+d}, tail_dy={tail_dy} -> top_y={min_y:2d}, bot_y={max_y:2d}, h={h:3d} | "
          f"diff={diff_px:5d} | resid={resid:.2f} | comps={len(comps)} | sh0={sh_rows[0]}")

for edy in [-1, 0, 1]:
    for tdy in [-14, -18, -22]:
        eval_skill_refined(ear_dy=edy, tail_dy=tdy)
