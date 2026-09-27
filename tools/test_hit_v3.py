from PIL import Image, ImageDraw, ImageFilter
import numpy as np

from build_cat_combat_poses import (
    key_src, curio_src, chassis_src, head_src, costume_src,
    anchors, base_landmarks, warp_image_idw,
    place_stiletto, stiletto_raw, enforce_ground_shadow
)

# 1. Create hit squint optic
optic = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat/optic_core/face_cat_slit_optic_emerald.png").convert("RGBA")
optic_arr = np.array(optic)
mask = optic_arr[:, :, 3] > 20

hit_optic = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
h_arr = np.array(hit_optic)
h_arr[mask] = [30, 32, 42, 255] # dark socket plate
hit_optic = Image.fromarray(h_arr)

draw = ImageDraw.Draw(hit_optic)
# Draw sharp impact squint "> <"
draw.line([(48, 37), (55, 40)], fill=(78, 216, 106, 255), width=2)
draw.line([(48, 43), (55, 40)], fill=(78, 216, 106, 255), width=2)
draw.line([(49, 38), (54, 40)], fill=(255, 255, 230, 255), width=1)
draw.line([(49, 42), (54, 40)], fill=(255, 255, 230, 255), width=1)

draw.line([(79, 37), (72, 40)], fill=(78, 216, 106, 255), width=2)
draw.line([(79, 43), (72, 40)], fill=(78, 216, 106, 255), width=2)
draw.line([(78, 38), (73, 40)], fill=(255, 255, 230, 255), width=1)
draw.line([(78, 42), (73, 40)], fill=(255, 255, 230, 255), width=1)

# 2. Composite body with hit_optic
body_hit_base = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_hit_base.alpha_composite(key_src)
body_hit_base.alpha_composite(curio_src)
body_hit_base.alpha_composite(chassis_src)
body_hit_base.alpha_composite(head_src)
body_hit_base.alpha_composite(hit_optic)
body_hit_base.alpha_composite(costume_src)

shifts_hit = {
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
    dx, dy = shifts_hit.get(name, (0, 0))
    src_pts.append((bx, by))
    dst_pts.append((bx + dx, by + dy))

warped_hit = warp_image_idw(body_hit_base, src_pts, dst_pts, power=2.0, epsilon=4.0)

# Stiletto placed in vertical parry guard at right edge of torso (76, 66)
stiletto_hit = place_stiletto(stiletto_raw, deg=75, target_center=(76, 66), scale=0.96, mirror=False)

# Deflection impact cross-star spark, shockwave arcs & expanding rings at (84, 62)
hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
h_draw = ImageDraw.Draw(hit_fx)
cx, cy = 84, 62

# Expanding kinetic shockwave arcs in front of blade contact point
h_draw.arc([cx - 22, cy - 22, cx + 22, cy + 22], start=280, end=80, fill=(78, 216, 106, 210), width=2)
h_draw.arc([cx - 28, cy - 28, cx + 28, cy + 28], start=290, end=70, fill=(255, 208, 40, 200), width=2)
h_draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=0, end=360, fill=(255, 208, 40, 220), width=2)

# Main cross-star spark rays
h_draw.line([(cx - 18, cy), (cx + 18, cy)], fill=(255, 255, 230, 245), width=2)
h_draw.line([(cx, cy - 18), (cx, cy + 18)], fill=(255, 255, 230, 245), width=2)

# Diagonal sparks
h_draw.line([(cx - 11, cy - 11), (cx + 11, cy + 11)], fill=(78, 216, 106, 220), width=1)
h_draw.line([(cx - 11, cy + 11), (cx + 11, cy - 11)], fill=(255, 208, 40, 220), width=1)

# Core white hot impact flash
h_draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255))

# Flying metal spark particles
for pt in [(cx - 20, cy - 8), (cx + 18, cy - 14), (cx - 14, cy + 16), (cx + 16, cy + 14), (cx - 8, cy - 18), (cx + 20, cy + 6)]:
    h_draw.point(pt, fill=(255, 208, 40, 255))
    h_draw.point((pt[0]+1, pt[1]), fill=(255, 255, 255, 230))

# Kinetic exhaust steam from back damper (32, 60)
h_draw.line([(32, 60), (16, 56)], fill=(230, 240, 255, 170), width=2)
hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
hit_canvas = Image.alpha_composite(hit_canvas, stiletto_hit)
hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
final_hit = enforce_ground_shadow(hit_canvas)
final_hit.save("/opt/side/bravesoul-game/tools/test_hit_v3.png")
print("Saved test_hit_v3.png, bbox=", final_hit.getbbox())
