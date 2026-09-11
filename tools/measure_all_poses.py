import os
import sys
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
sys.path.insert(0, REPO_ROOT)

from tools.generate_fox_combat_poses import place_rigid_staff, warp_image_idw

staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")

clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
assert s_px is not None and cs_px is not None
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = cast(tuple[int, int, int, int], s_px[x, y])

b_px = body_clean.load()
assert b_px is not None
for y in range(112, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], b_px[x, y])
        if p[3] > 0:
            is_solid_paw = (46 <= x <= 58 or 69 <= x <= 80) and y <= 122 and p[0] < 125 and p[1] < 105 and p[2] < 80
            if not is_solid_paw:
                b_px[x, y] = (0, 0, 0, 0)

anchors = [(0, 0), (127, 0), (0, 127), (127, 127)]
base_landmarks = {
    "ear_l": (48, 12), "ear_r": (76, 12), "forehead": (62, 28),
    "eye_l": (50, 46), "eye_r": (72, 46), "snout": (60, 56),
    "neck": (60, 64), "core": (60, 75), "shoulder_l": (42, 70), "shoulder_r": (78, 68),
    "key_mount": (30, 62), "key_top": (22, 56), "key_bot": (22, 68),
    "pelvis": (60, 94),
    "tail_base": (33, 90), "tail_mid": (26, 102), "tail_tip": (22, 114),
    "hip_l": (48, 95), "knee_l": (50, 106), "foot_l": (52, 117),
    "hip_r": (72, 94), "knee_r": (76, 106), "foot_r": (76, 117),
    "hand": (90, 86),
}

shifts_telegraph = {
    "ear_l": (10, 8), "ear_r": (12, 8), "forehead": (12, 8),
    "eye_l": (12, 7), "eye_r": (14, 7), "snout": (15, 7),
    "neck": (12, 7), "core": (12, 6), "shoulder_l": (8, 7), "shoulder_r": (14, 6),
    "key_mount": (7, 6), "key_top": (5, 6), "key_bot": (5, 6),
    "pelvis": (6, 8), "hip_l": (4, 8), "hip_r": (8, 8),
    "tail_base": (1, 6), "tail_mid": (-6, 2), "tail_tip": (-12, -4),
    "knee_l": (-4, 6), "foot_l": (-2, 2),
    "knee_r": (6, 5), "foot_r": (4, 2),
    "hand": (-14, 0),
}

shifts_recover = {
    "ear_l": (-3, -1), "ear_r": (-2, -1), "forehead": (-2, -1),
    "eye_l": (-2, -1), "eye_r": (-2, -1), "snout": (-1, -1),
    "neck": (-1, 0), "core": (-1, 0), "shoulder_l": (-2, 0), "shoulder_r": (0, 0),
    "key_mount": (-1, 0), "key_top": (-2, 0), "key_bot": (-2, 0),
    "pelvis": (0, 1), "hip_l": (-1, 1), "hip_r": (1, 1),
    "tail_base": (1, 0), "tail_mid": (2, -1), "tail_tip": (3, -2),
    "knee_l": (0, 1), "foot_l": (0, 0),
    "knee_r": (0, 1), "foot_r": (0, 0),
    "hand": (-2, 0),
}

shifts_skill = {
    "ear_l": (-10, -6), "ear_r": (-6, -7), "forehead": (-6, -6),
    "eye_l": (-6, -5), "eye_r": (-4, -5), "snout": (-3, -5),
    "neck": (-4, -4), "core": (-3, -3), "shoulder_l": (-5, -4), "shoulder_r": (2, -4),
    "key_mount": (-6, -3), "key_top": (-7, -3), "key_bot": (-7, -3),
    "pelvis": (-2, 1), "hip_l": (-4, 2), "hip_r": (0, 2),
    "tail_base": (-4, -2), "tail_mid": (-6, -6), "tail_tip": (-8, -12),
    "knee_l": (-4, 2), "foot_l": (-2, 0),
    "knee_r": (0, 2), "foot_r": (0, 0),
    "hand": (-4, -18),
}

# 1. idle:
body_idle = body_clean
staff_idle = place_rigid_staff(clean_staff, deg=0, target_hand=(90, 86))

# 2. telegraph:
src_pts = list(anchors)
dst_pts = list(anchors)
for name, (bx, by) in base_landmarks.items():
    dx, dy = shifts_telegraph.get(name, (0, 0))
    src_pts.append((bx, by))
    dst_pts.append((bx + dx, by + dy))
body_tele = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
staff_tele = place_rigid_staff(clean_staff, deg=32, target_hand=(76, 84))

# 4. recover:
src_pts = list(anchors)
dst_pts = list(anchors)
for name, (bx, by) in base_landmarks.items():
    dx, dy = shifts_recover.get(name, (0, 0))
    src_pts.append((bx, by))
    dst_pts.append((bx + dx, by + dy))
body_rec = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
staff_rec = place_rigid_staff(clean_staff, deg=18, target_hand=(88, 86))

# 5. skill:
src_pts = list(anchors)
dst_pts = list(anchors)
for name, (bx, by) in base_landmarks.items():
    dx, dy = shifts_skill.get(name, (0, 0))
    src_pts.append((bx, by))
    dst_pts.append((bx + dx, by + dy))
body_skill = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
staff_skill = place_rigid_staff(clean_staff, deg=-45, target_hand=(86, 68))

# 6. hit (v2 candidate):
large_hit = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
large_hit.paste(body_clean, (64, 64))
rot_pos14 = large_hit.rotate(14, resample=Image.Resampling.BICUBIC, center=(64 + 52, 64 + 118))
body_hit = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_hit.paste(rot_pos14, (-64, -64), rot_pos14)
staff_hit = place_rigid_staff(clean_staff, deg=-65, target_hand=(84, 58), scale=0.98)

# 6b. hit (old):
rot_neg14 = large_hit.rotate(-14, resample=Image.Resampling.BICUBIC, center=(64 + 52, 64 + 118))
body_hit_old = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_hit_old.paste(rot_neg14, (-64, -64), rot_neg14)
staff_hit_old = place_rigid_staff(clean_staff, deg=-25, target_hand=(78, 72))

poses = [
    ("idle", staff_idle, body_idle),
    ("recover", staff_rec, body_rec),
    ("skill", staff_skill, body_skill),
    ("telegraph", staff_tele, body_tele),
    ("hit_old", staff_hit_old, body_hit_old),
    ("hit_new", staff_hit, body_hit),
]

print("=== Objective Measurements Across Poses ===")
for name, s_im, b_im in poses:
    spx = s_im.load()
    bpx = b_im.load()
    assert spx is not None and bpx is not None
    
    comp = Image.alpha_composite(b_im, s_im)
    cpx = comp.load()
    assert cpx is not None
    
    total_staff = 0
    outside_body = 0
    edge_visible = 0
    
    for y in range(128):
        for x in range(128):
            sp = cast(tuple[int,int,int,int], spx[x, y])
            if sp[3] > 40:
                total_staff += 1
                bp = cast(tuple[int,int,int,int], bpx[x, y])
                if bp[3] <= 40:
                    outside_body += 1
                    
                is_contour = False
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 128 and 0 <= ny < 128:
                            if cast(tuple[int,int,int,int], cpx[nx, ny])[3] < 30:
                                is_contour = True
                                break
                        else:
                            is_contour = True
                            break
                    if is_contour:
                        break
                if is_contour:
                    edge_visible += 1
                    
    out_pct = outside_body / total_staff * 100.0 if total_staff else 0.0
    edge_pct = edge_visible / total_staff * 100.0 if total_staff else 0.0
    print(f"{name:12s}: total staff={total_staff:3d} | outside silhouette={outside_body:3d} ({out_pct:5.1f}%) | outer edge visible={edge_visible:3d} ({edge_pct:5.1f}%)")
