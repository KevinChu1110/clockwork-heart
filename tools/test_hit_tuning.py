from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

from build_cat_combat_poses import (
    body_no_weapon, anchors, base_landmarks, warp_image_idw,
    place_stiletto, stiletto_raw, enforce_ground_shadow
)

shifts_hit_v2 = {
    "head_top": (-16, -6), "ear_l": (-18, -8), "ear_r": (-14, -6),
    "eye_l": (-15, -5), "eye_r": (-15, -5), "snout": (-13, -4), "throat": (-11, -3),
    "core": (-8, -2),
    "shoulder_l": (-8, 0), "arm_l": (-4, 2),
    "shoulder_r": (-6, -2), "arm_r": (2, -3),
    "torso": (-5, 0), "pelvis": (2, 2),
    "hip_l": (-4, 2), "hip_r": (4, 2),
    "foot_l": (-3, 0), "foot_r": (2, 0),
    "tail_root": (-8, 4), "tail_mid": (-10, 8), "tail_tip": (-6, 12),
    "key_mount": (-12, -4), "key_wing": (-14, -6),
}

src_pts = list(anchors)
dst_pts = list(anchors)
for name, (bx, by) in base_landmarks.items():
    dx, dy = shifts_hit_v2.get(name, (0, 0))
    src_pts.append((bx, by))
    dst_pts.append((bx + dx, by + dy))

warped = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

# Stiletto placed in vertical parry guard at right edge of torso (78, 66)
# deg=75, so blade points almost straight up with slight tilt forward
stiletto_hit = place_stiletto(stiletto_raw, deg=75, target_center=(76, 66), scale=0.96, mirror=False)

# Deflection spark bursting off the front edge of the blade at (84, 62)
hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
h_draw = ImageDraw.Draw(hit_fx)
cx, cy = 84, 62
# Radiant impact flash & spark rays
h_draw.line([(cx - 16, cy), (cx + 16, cy)], fill=(255, 255, 230, 245), width=2)
h_draw.line([(cx, cy - 16), (cx, cy + 16)], fill=(255, 255, 230, 245), width=2)
h_draw.line([(cx - 10, cy - 10), (cx + 10, cy + 10)], fill=(78, 216, 106, 220), width=1)
h_draw.line([(cx - 10, cy + 10), (cx + 10, cy - 10)], fill=(255, 208, 40, 220), width=1)
h_draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=0, end=360, fill=(255, 208, 40, 200), width=2)
h_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255, 255))
for pt in [(cx - 18, cy - 8), (cx + 16, cy - 12), (cx - 12, cy + 14), (cx + 14, cy + 12), (cx - 8, cy - 16), (cx + 18, cy + 6)]:
    h_draw.point(pt, fill=(255, 208, 40, 255))
    h_draw.point((pt[0]+1, pt[1]), fill=(255, 255, 255, 230))
# Kinetic exhaust steam from back damper (32, 60)
h_draw.line([(32, 60), (16, 56)], fill=(230, 240, 255, 170), width=2)
hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
canvas = Image.alpha_composite(canvas, warped)
canvas = Image.alpha_composite(canvas, stiletto_hit)
canvas = Image.alpha_composite(canvas, hit_fx)
res = enforce_ground_shadow(canvas)
res.save("/opt/side/bravesoul-game/tools/test_hit_v2.png")
print("Saved test_hit_v2.png, bbox=", res.getbbox())
