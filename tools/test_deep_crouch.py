#!/usr/bin/env python3
"""
tools/test_deep_crouch.py
Test script for Fox Mage true deep crouch recovery pose.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")

def build_contact_shadow(cx: int = 60, cy: int = 120, rx: int = 44, ry: int = 6, blur: float = 0.7) -> Image.Image:
    shadow_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow_canvas)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(160, 137, 108, 180))
    draw.ellipse([cx - int(rx * 0.78), cy - int(ry * 0.8), cx + int(rx * 0.78), cy + int(ry * 0.8)], fill=(156, 133, 102, 230))
    draw.ellipse([cx - int(rx * 0.5), cy - int(ry * 0.6), cx + int(rx * 0.5), cy + int(ry * 0.6)], fill=(152, 130, 99, 255))
    return shadow_canvas.filter(ImageFilter.GaussianBlur(blur))

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

# Clean staff
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
assert s_px is not None and cs_px is not None
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = s_px[x, y]

# Setup landmarks for deep crouch
anchors = [(0, 0), (127, 0), (0, 127), (127, 127)]
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

shifts_crouch = {
    "ear_l": (0, 26), "ear_r": (0, 26), "forehead": (0, 25),
    "eye_l": (0, 23), "eye_r": (0, 23), "snout": (0, 22),
    "neck": (0, 19), "core": (0, 16), "shoulder_l": (-4, 16), "shoulder_r": (4, 16),
    "key_mount": (-4, 15), "key_top": (-4, 15), "key_bot": (-4, 15),
    "pelvis": (0, 14), "hip_l": (-8, 12), "hip_r": (8, 12),
    "tail_base": (0, 10), "tail_mid": (-8, 6), "tail_tip": (-14, 2),
    "knee_l": (-10, 8), "foot_l": (-4, 2),
    "knee_r": (10, 8), "foot_r": (4, 2),
    "hand": (-6, 18),
}

src_pts = list(anchors)
dst_pts = list(anchors)
for name, (bx, by) in base_landmarks.items():
    dx, dy = shifts_crouch.get(name, (0, 0))
    src_pts.append((bx, by))
    dst_pts.append((bx + dx, by + dy))

crouch_body = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)

# Staff grounded vertically in front (grip at 84, 104, base touches ground at y=122)
large_canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
large_canvas.paste(clean_staff, (128 - 93, 128 - 88))
out_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
out_staff.paste(large_canvas, (84 - 128, 104 - 128), large_canvas)

shadow = build_contact_shadow(cx=60, cy=121, rx=46, ry=6, blur=0.8)
rec_img = Image.alpha_composite(shadow, crouch_body)
rec_img = Image.alpha_composite(rec_img, out_staff)

rec_img.save("/tmp/test_deep_recover.png")
print("Saved /tmp/test_deep_recover.png, bbox:", rec_img.getbbox())
