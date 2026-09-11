#!/usr/bin/env python3
import sys
import os
import math
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from cc_helper import get_connected_components

REPO_ROOT = "/opt/side/bravesoul-game"
OUTPUT_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"

staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")

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

# 1. Clean staff with solid filigree bracket
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
assert s_px is not None and cs_px is not None
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = cast(tuple[int, int, int, int], s_px[x, y])

draw_cs = ImageDraw.Draw(clean_staff)
draw_cs.polygon([(86, 54), (99, 56), (99, 60), (86, 58)], fill=(120, 80, 50, 255))
draw_cs.line([(86, 54), (99, 56)], fill=(50, 30, 20, 255), width=1)
draw_cs.line([(86, 58), (99, 60)], fill=(50, 30, 20, 255), width=1)
draw_cs.line([(92, 94), (88, 101)], fill=(115, 75, 45, 255), width=2)
draw_cs.line([(88, 106), (90, 119)], fill=(115, 75, 45, 255), width=2)

# 2. Rotate body by +14 deg (counter-clockwise in PIL)
large_hit = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
large_hit.paste(body_clean, (64, 64))
rotated_hit = large_hit.rotate(14, resample=Image.Resampling.BICUBIC, center=(64 + 52, 64 + 118))
hit_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
hit_body.paste(rotated_hit, (-64, -64), rotated_hit)

# 3. Staff at deg=-65, target_hand=(84, 58)
staff_hit = place_rigid_staff(clean_staff, deg=-65, target_hand=(84, 58), scale=0.98)

# 4. Now let's draw the arm and sleeve connecting right shoulder to target_hand (84, 58)!
# In hit_body:
# Right shoulder / torso edge is around x=68..76, y=62..72
# Target hand is at (84, 58).
# Sleeve extends from shoulder to wrist:
# Sleeve body: polygon connecting (70, 64), (82, 56), (85, 62), (72, 72)
arm_layer = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
draw_arm = ImageDraw.Draw(arm_layer)

# Sleeve outer dark contour / border
sleeve_poly = [(69, 63), (81, 55), (86, 61), (73, 73)]
draw_arm.polygon([(68, 62), (82, 54), (88, 62), (72, 74)], fill=(40, 25, 22, 255))
# Sleeve fabric (warm cream / beige matching costume)
draw_arm.polygon([(70, 64), (81, 56), (85, 61), (73, 71)], fill=(150, 132, 105, 255))
# Gold trim at the cuff near target hand
draw_arm.polygon([(79, 56), (83, 55), (86, 60), (82, 61)], fill=(210, 175, 65, 255))
# Dark shadow under sleeve
draw_arm.line([(72, 72), (85, 61)], fill=(40, 25, 22, 255), width=1)
# Upper outline of sleeve
draw_arm.line([(69, 63), (81, 55)], fill=(40, 25, 22, 255), width=1)

# Hand wrist joint connecting gold cuff to hand grip:
draw_arm.polygon([(82, 57), (85, 57), (86, 60), (83, 60)], fill=(135, 88, 58, 255))

# Composite layers:
# shadow -> hit_body -> arm_layer -> staff_hit
# Note: Does arm go over body and under staff?
# Yes! The arm connects from the body shoulder to the hand, and the staff is held in the hand.
hit_shadow = build_contact_shadow(cx=50, cy=119, rx=34, ry=5, blur=0.6)
hit_img = Image.alpha_composite(hit_shadow, hit_body)
hit_img = Image.alpha_composite(hit_img, arm_layer)
hit_img = Image.alpha_composite(hit_img, staff_hit)

comps = get_connected_components(hit_img, alpha_thresh=40, y_max=118)
print(f"\nFinal hit_img components count (alpha > 40, y < 118): {len(comps)}")
for i, c in enumerate(comps):
    xs = [pt[0] for pt in c]
    ys = [pt[1] for pt in c]
    print(f"  Comp {i+1}: count={len(c)}, bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")
