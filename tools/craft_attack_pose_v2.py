import os
import math
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player/poses/fox")

staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
battle_im = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/fox_battle.png").convert("RGBA")
body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")

# Clean staff with bridged gaps
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
assert s_px is not None and cs_px is not None
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = cast(tuple[int, int, int, int], s_px[x, y])

draw_cs = ImageDraw.Draw(clean_staff)
# Bridge floating ring to staff head
draw_cs.polygon([(86, 54), (99, 56), (99, 60), (86, 58)], fill=(120, 80, 50, 255))
draw_cs.line([(86, 54), (99, 56)], fill=(50, 30, 20, 255), width=1)
draw_cs.line([(86, 58), (99, 60)], fill=(50, 30, 20, 255), width=1)
# Bridge shaft gaps
draw_cs.line([(91, 95), (88, 99)], fill=(115, 75, 45, 255), width=2)
draw_cs.line([(88, 108), (89, 117)], fill=(115, 75, 45, 255), width=2)

def build_contact_shadow(cx: int = 60, cy: int = 119, rx: int = 36, ry: int = 5, blur: float = 0.6) -> Image.Image:
    shadow_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow_canvas)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(160, 137, 108, 180))
    draw.ellipse([cx - int(rx * 0.78), cy - int(ry * 0.8), cx + int(rx * 0.78), cy + int(ry * 0.8)], fill=(156, 133, 102, 230))
    draw.ellipse([cx - int(rx * 0.5), cy - int(ry * 0.6), cx + int(rx * 0.5), cy + int(ry * 0.6)], fill=(152, 130, 99, 255))
    return shadow_canvas.filter(ImageFilter.GaussianBlur(blur))

def place_rigid_staff(staff_img: Image.Image, deg: float, target_hand: tuple[int, int], scale: float = 1.0) -> Image.Image:
    large_canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    large_canvas.paste(staff_img, (128 - 93, 128 - 88))
    if scale != 1.0:
        sw = int(round(256 * scale))
        sh = int(round(256 * scale))
        large_canvas = large_canvas.resize((sw, sh), Image.Resampling.LANCZOS)
    rotated = large_canvas.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out_128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hx, hy = target_hand
    out_128.paste(rotated, (hx - 128, hy - 128), rotated)
    return out_128

def warp_image_idw(src_img: Image.Image, src_points: list[tuple[int, int]], dst_points: list[tuple[int, int]], power: float = 2.0, epsilon: float = 4.0) -> Image.Image:
    w, h = src_img.size
    out_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    displacements = [(sx - dx, sy - dy) for (sx, sy), (dx, dy) in zip(src_points, dst_points)]
    src_pixels = src_img.load()
    out_pixels = out_img.load()
    assert src_pixels is not None and out_pixels is not None
    
    for y in range(h):
        for x in range(w):
            total_w = 0.0
            dx_accum = 0.0
            dy_accum = 0.0
            exact_match = None
            
            for i, (qx, qy) in enumerate(dst_points):
                dist_sq = (x - qx) ** 2 + (y - qy) ** 2
                if dist_sq < 1e-4:
                    exact_match = displacements[i]
                    break
                weight = 1.0 / (dist_sq ** (power / 2.0) + epsilon)
                total_w += weight
                dx_accum += weight * displacements[i][0]
                dy_accum += weight * displacements[i][1]
            
            if exact_match is not None:
                src_x = x + exact_match[0]
                src_y = y + exact_match[1]
            else:
                src_x = x + dx_accum / total_w
                src_y = y + dy_accum / total_w
            
            x0 = int(math.floor(src_x))
            y0 = int(math.floor(src_y))
            x1 = x0 + 1
            y1 = y0 + 1
            
            if 0 <= x0 < w - 1 and 0 <= y0 < h - 1:
                fx = src_x - x0
                fy = src_y - y0
                p00 = cast(tuple[int, int, int, int], src_pixels[x0, y0])
                p10 = cast(tuple[int, int, int, int], src_pixels[x1, y0])
                p01 = cast(tuple[int, int, int, int], src_pixels[x0, y1])
                p11 = cast(tuple[int, int, int, int], src_pixels[x1, y1])
                
                rgba = []
                for c in range(4):
                    val = (p00[c] * (1 - fx) * (1 - fy) +
                           p10[c] * fx * (1 - fy) +
                           p01[c] * (1 - fx) * fy +
                           p11[c] * fx * fy)
                    rgba.append(int(round(val)))
                out_pixels[x, y] = tuple(rgba)
            elif 0 <= x0 < w and 0 <= y0 < h:
                out_pixels[x, y] = src_pixels[x0, y0]
                
    return out_img

anchors = [(0, 0), (127, 0), (0, 127), (127, 127),
           (0, 32), (127, 32), (0, 64), (127, 64), (0, 96), (127, 96)]
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

shifts_attack = {
    "ear_l": (14, 0), "ear_r": (16, 0), "forehead": (16, 0),
    "eye_l": (16, 1), "eye_r": (18, 1), "snout": (20, 2),
    "neck": (16, 2), "core": (14, 2), "shoulder_l": (10, 3), "shoulder_r": (18, 2),
    "key_mount": (8, 2), "key_top": (6, 2), "key_bot": (6, 2),
    "pelvis": (8, 3), 
    "hip_l": (-2, 4), "knee_l": (-8, 4), "foot_l": (-12, 0),
    "hip_r": (14, 3), "knee_r": (18, 2), "foot_r": (16, 0),
    "tail_base": (0, 2), "tail_mid": (-10, -2), "tail_tip": (-18, -6),
    "hand": (10, 0),
}

src_pts = list(anchors)
dst_pts = list(anchors)
for name, (bx, by) in base_landmarks.items():
    dx, dy = shifts_attack.get(name, (0, 0))
    src_pts.append((bx, by))
    dst_pts.append((bx + dx, by + dy))

warped_atk = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)

# Staff thrust forward horizontally:
target_hand = (82, 78)
staff_atk = place_rigid_staff(clean_staff, deg=-62, target_hand=target_hand, scale=0.98)

# Arm layer to connect right shoulder to hand/cuff:
arm_layer = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
draw_arm = ImageDraw.Draw(arm_layer)

sleeve_poly = [(92, 68), (97, 72), (88, 83), (80, 81), (80, 75), (86, 70)]
draw_arm.polygon(sleeve_poly, fill=(30, 22, 28, 255))
draw_arm.polygon([(93, 69), (96, 72), (87, 82), (81, 80), (81, 76), (87, 71)], fill=(55, 75, 95, 255))
draw_arm.line([(81, 76), (81, 80)], fill=(200, 160, 60, 255), width=2)
draw_arm.ellipse([79, 75, 85, 81], fill=(160, 120, 65, 255))
draw_arm.ellipse([80, 76, 84, 80], fill=(210, 175, 90, 255))

# Subtle magic energy spark at crystal tip
spark_layer = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
draw_sp = ImageDraw.Draw(spark_layer)
draw_sp.ellipse([116, 54, 124, 62], fill=(80, 235, 255, 120))
draw_sp.ellipse([118, 56, 122, 60], fill=(220, 255, 255, 200))
spark_layer = spark_layer.filter(ImageFilter.GaussianBlur(0.6))

# Contact shadow
atk_shadow = build_contact_shadow(cx=66, cy=120, rx=44, ry=6, blur=0.7)

comp_atk = Image.alpha_composite(atk_shadow, warped_atk)
comp_atk = Image.alpha_composite(comp_atk, arm_layer)
comp_atk = Image.alpha_composite(comp_atk, staff_atk)
comp_atk = Image.alpha_composite(comp_atk, spark_layer)
comp_atk.save("/tmp/test_attack_candidate_v2.png")
print("Saved /tmp/test_attack_candidate_v2.png with fully unified rigid staff")
