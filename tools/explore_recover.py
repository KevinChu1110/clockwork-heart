import os
import sys
from PIL import Image, ImageChops
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

def test_recover(scale_y=0.65, extra_dx=1.0, staff_hand=(88, 98), staff_deg=0):
    shifts_recover = {
        "ear_l": (-2 * extra_dx, int(round(22 * scale_y))),
        "ear_r": (2 * extra_dx, int(round(22 * scale_y))),
        "forehead": (0, int(round(22 * scale_y))),
        "eye_l": (-1 * extra_dx, int(round(20 * scale_y))),
        "eye_r": (1 * extra_dx, int(round(20 * scale_y))),
        "snout": (0, int(round(20 * scale_y))),
        "neck": (0, int(round(18 * scale_y))),
        "core": (0, int(round(16 * scale_y))),
        "shoulder_l": (-4 * extra_dx, int(round(16 * scale_y))),
        "shoulder_r": (4 * extra_dx, int(round(16 * scale_y))),
        "key_mount": (-4 * extra_dx, int(round(15 * scale_y))),
        "key_top": (-4 * extra_dx, int(round(15 * scale_y))),
        "key_bot": (-4 * extra_dx, int(round(15 * scale_y))),
        "pelvis": (0, int(round(14 * scale_y))),
        "hip_l": (-8 * extra_dx, int(round(12 * scale_y))),
        "hip_r": (8 * extra_dx, int(round(12 * scale_y))),
        "tail_base": (0, int(round(12 * scale_y))),
        "tail_mid": (-8 * extra_dx, int(round(8 * scale_y))),
        "tail_tip": (-12 * extra_dx, int(round(4 * scale_y))),
        "knee_l": (-9 * extra_dx, int(round(8 * scale_y))),
        "foot_l": (-4 * extra_dx, 2),
        "knee_r": (9 * extra_dx, int(round(8 * scale_y))),
        "foot_r": (4 * extra_dx, 2),
        "hand": (-2 * extra_dx, int(round(16 * scale_y))),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    staff = place_rigid_staff(clean_staff, deg=staff_deg, target_hand=staff_hand)
    shadow = build_contact_shadow(cx=60, cy=121, rx=44, ry=6, blur=0.7)
    
    comp = Image.alpha_composite(shadow, warped)
    comp = Image.alpha_composite(comp, staff)
    
    # Measure
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
    
    print(f"scale_y={scale_y:.2f}, extra_dx={extra_dx:.1f}, hand={staff_hand}, deg={staff_deg} -> "
          f"top_y={min_y:2d}, bot_y={max_y:2d}, h={h:3d} | diff={diff_px:5d} | "
          f"resid={resid:.2f} | comps={len(comps)} | sh0={sh_rows[0]}")

for sy in [0.4, 0.5, 0.55, 0.6, 0.65, 0.7]:
    for edx in [1.0, 1.2, 1.4]:
        test_recover(scale_y=sy, extra_dx=edx, staff_hand=(88, int(86 + 16 * sy)), staff_deg=0)
