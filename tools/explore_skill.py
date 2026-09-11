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

def test_skill(ear_dy=0, body_dy_scale=0.5, staff_hand=(86, 68), staff_deg=-45):
    shifts_skill = {
        "ear_l": (-2, ear_dy), "ear_r": (3, ear_dy), "forehead": (1, int(round(ear_dy * 0.9))),
        "eye_l": (0, int(round(ear_dy * 0.8))), "eye_r": (2, int(round(ear_dy * 0.8))), "snout": (2, int(round(ear_dy * 1.1))),
        "neck": (1, int(round(-5 * body_dy_scale))), "core": (1, int(round(-4 * body_dy_scale))),
        "shoulder_l": (-2, int(round(-5 * body_dy_scale))), "shoulder_r": (4, int(round(-7 * body_dy_scale))),
        "key_mount": (-1, int(round(-4 * body_dy_scale))), "key_top": (-1, int(round(-4 * body_dy_scale))), "key_bot": (-1, int(round(-4 * body_dy_scale))),
        "pelvis": (0, int(round(-3 * body_dy_scale))), "hip_l": (-1, int(round(-3 * body_dy_scale))), "hip_r": (1, int(round(-3 * body_dy_scale))),
        "tail_base": (-1, -4), "tail_mid": (-7, -10), "tail_tip": (-12, -16),
        "knee_l": (0, 0), "foot_l": (0, 0),
        "knee_r": (0, 0), "foot_r": (0, 0),
        "hand": (4, staff_hand[1] - 86),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    staff = place_rigid_staff(clean_staff, deg=staff_deg, target_hand=staff_hand)
    
    skill_aura = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(skill_aura)
    a_draw.ellipse([98, 18, 114, 34], fill=(80, 235, 255, 140))
    a_draw.ellipse([102, 22, 110, 30], fill=(230, 255, 255, 220))
    a_draw.ellipse([50, 62, 72, 84], fill=(50, 220, 240, 80))
    skill_aura = skill_aura.filter(ImageFilter.GaussianBlur(0.8))

    skill_shadow = build_contact_shadow(cx=60, cy=119, rx=34, ry=4, blur=0.6)
    skill_img = Image.alpha_composite(skill_shadow, warped)
    skill_img = Image.alpha_composite(skill_img, staff)
    skill_img = Image.alpha_composite(skill_img, skill_aura)
    
    # Measure
    px = skill_img.load()
    min_x, min_y, max_x, max_y = 128, 128, -1, -1
    for y in range(118):
        for x in range(128):
            if px[x, y][3] > 10:
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
    h = max_y - min_y + 1
    
    diff = ImageChops.difference(idle_img, skill_img)
    diff_data = [x for x in diff.convert("L").getdata() if x > 10]
    diff_px = len(diff_data)
    
    resid = measure_staff_linearity(skill_img)
    comps = get_connected_components(skill_img, alpha_thresh=40, y_max=118)
    sh_rows = measure_shadow_rows(skill_img)
    
    print(f"ear_dy={ear_dy:+2d}, body_scale={body_dy_scale:.2f} -> "
          f"top_y={min_y:2d}, bot_y={max_y:2d}, h={h:3d} | diff={diff_px:5d} | "
          f"resid={resid:.2f} | comps={len(comps)} | sh0={sh_rows[0]}")

for edy in [-2, -1, 0, 1, 2]:
    for bscale in [0.0, 0.5, 0.8, 1.0]:
        test_skill(ear_dy=edy, body_dy_scale=bscale)
