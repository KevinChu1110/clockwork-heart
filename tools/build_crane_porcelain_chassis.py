#!/usr/bin/env python3
"""
tools/build_crane_porcelain_chassis.py
Renders high-detail, fully shaded porcelain chassis (paint_crane_porcelain.png) for Cloud Crane.
Replaces unfinished flat placeholder rectangles/dots with authentic clockwork toy automaton plating.
- Warm/cold glazed porcelain plates (#F5F8FB ~ #8C9EAF)
- Polished brass ball joints & gyroscopic waist bearing (#FFD028 / #FFA010 / #8C4C08)
- Glowing cyan diamond energy core socket (#5EB4FF / #38A0FF)
- Deep blue-purple crisp outline (#1F1A3A)
- 100% CANON compliant: zero biological fur/feathers/flesh
"""

import os
import math
from typing import cast
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
CRANE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crane"
OUT_PORCELAIN = f"{CRANE_DIR}/chassis/paint_crane_porcelain.png"

def render_porcelain_torso() -> Image.Image:
    torso = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(torso)

    # Crisp outlines & seams
    C_OUTLINE = (31, 26, 58, 255)       # Deep blue-purple #1F1A3A
    C_CREASE = (55, 50, 80, 255)        # Soft inner panel crease

    # Porcelain White Enamel ramp
    P_SPEC = (255, 255, 255, 255)       # Glaze specular highlight
    P_LIGHT = (245, 248, 252, 255)      # Porcelain highlight
    P_MID = (222, 230, 240, 255)        # Porcelain midtone
    P_SHADOW = (185, 198, 214, 255)     # Core shadow
    P_DEEP = (140, 155, 175, 255)       # Ambient occlusion / crease

    # Cobalt / Azure Blue ramp (avian accents)
    A_SPEC = (180, 225, 255, 255)
    A_LIGHT = (94, 180, 255, 255)       # Sky blue highlight
    A_MID = (41, 121, 255, 255)         # Radiant cobalt midtone
    A_SHADOW = (22, 70, 170, 255)       # Deep azure shadow
    A_DEEP = (15, 38, 95, 255)

    # Polished Brass / Gold ramp (joints, gimbal, bezel)
    G_SPEC = (255, 248, 200, 255)       # Specular reflection
    G_LIGHT = (255, 218, 50, 255)       # Bright brass #FFD028
    G_MID = (255, 160, 20, 255)         # Warm gold #FFA010
    G_SHADOW = (185, 105, 15, 255)      # Deep gold shadow
    G_DEEP = (110, 55, 10, 255)         # Crease shadow

    # Cyan Energy Core ramp
    C_GLOW_SPEC = (230, 250, 255, 255)
    C_GLOW_LIGHT = (100, 210, 255, 255)
    C_GLOW_MID = (56, 160, 255, 255)
    C_GLOW_DEEP = (18, 65, 140, 255)

    # Titanium neck bellows / collar
    T_LIGHT = (165, 180, 195, 255)
    T_MID = (115, 130, 148, 255)
    T_SHADOW = (75, 88, 105, 255)

    # 1. Base Silhouette of Torso (y: 54..85)
    body_poly = [
        (58, 54), (70, 54),
        (76, 56), (79, 60),
        (76, 70),
        (72, 75), (71, 80),
        (73, 83), (72, 85),
        (56, 85), (55, 83),
        (57, 80), (56, 75),
        (52, 70),
        (49, 60), (52, 56),
    ]
    d.polygon(body_poly, fill=C_OUTLINE)

    # 2. Neck Collar & Bellows Support (y: 53..56, x: 58..70)
    d.rounded_rectangle([58, 53, 70, 57], radius=2, fill=T_MID, outline=C_OUTLINE)
    for x in range(60, 69):
        if x in (63, 64, 65):
            torso.putpixel((x, 54), T_LIGHT)
            torso.putpixel((x, 55), P_LIGHT)
        else:
            torso.putpixel((x, 54), T_MID)
            torso.putpixel((x, 55), T_SHADOW)

    # 3. Flank Cobalt Plates (x: 50..55, 73..78)
    l_flank = [(52, 58), (56, 57), (55, 70), (52, 69)]
    d.polygon(l_flank, fill=A_MID, outline=C_OUTLINE)
    for y in range(59, 68):
        torso.putpixel((53, y), A_LIGHT)
        torso.putpixel((54, y), A_MID)
    torso.putpixel((53, 60), A_SPEC)

    r_flank = [(72, 57), (76, 58), (76, 69), (73, 70)]
    d.polygon(r_flank, fill=A_MID, outline=C_OUTLINE)
    for y in range(59, 68):
        torso.putpixel((74, y), A_MID)
        torso.putpixel((75, y), A_SHADOW)
    torso.putpixel((74, 60), A_LIGHT)

    # 4. Porcelain Breastplate (x: 55..73, y: 56..73)
    for y in range(56, 74):
        if y < 60:
            x_min, x_max = 56, 72
        elif y < 68:
            x_min, x_max = 55, 73
        elif y < 71:
            x_min, x_max = 56, 72
        else:
            x_min, x_max = 57, 71

        for x in range(x_min, x_max + 1):
            if x == x_min or x == x_max or y == 56 or y == 73:
                torso.putpixel((x, y), C_OUTLINE)
                continue

            if x == 64:
                if y > 68 or y < 60:
                    torso.putpixel((x, y), C_CREASE)
                    continue

            dx = (x - 62) / 6.0
            dy = (y - 58) / 8.0
            dist = math.sqrt(dx * dx + dy * dy)

            if x < 64:
                if y in (57, 58) and x in (60, 61, 62):
                    col = P_SPEC
                elif dist < 0.8:
                    col = P_LIGHT
                elif dist < 1.4:
                    col = P_MID
                else:
                    col = P_SHADOW
            else:
                if dist < 0.9:
                    col = P_MID
                elif dist < 1.6:
                    col = P_SHADOW
                else:
                    col = P_DEEP

            if y in (71, 72):
                col = P_SHADOW if x < 64 else P_DEEP

            torso.putpixel((x, y), col)

    # 5. Chest Clockwork Heart / Energy Core Bezel & Socket (center: 64, 65)
    diamond_outer = [(64, 59), (71, 65), (64, 71), (57, 65)]
    d.polygon(diamond_outer, fill=C_OUTLINE)

    diamond_frame = [(64, 60), (70, 65), (64, 70), (58, 65)]
    d.polygon(diamond_frame, fill=G_MID)

    # Bevel highlights & shadows
    d.line([(59, 64), (64, 60)], fill=G_SPEC)
    d.line([(60, 65), (64, 61)], fill=G_LIGHT)
    d.line([(64, 70), (70, 65)], fill=G_DEEP)
    d.line([(64, 69), (69, 65)], fill=G_SHADOW)
    d.line([(64, 60), (70, 65)], fill=G_LIGHT)
    d.line([(58, 65), (64, 70)], fill=G_MID)

    # Inner core aperture
    core_aperture = [(64, 61), (68, 65), (64, 69), (60, 65)]
    d.polygon(core_aperture, fill=C_GLOW_DEEP)

    # Glowing Cyan Core Gem
    core_inner = [(64, 62), (67, 65), (64, 68), (61, 65)]
    d.polygon(core_inner, fill=C_GLOW_MID)
    d.polygon([(64, 63), (66, 65), (64, 67), (62, 65)], fill=C_GLOW_LIGHT)
    torso.putpixel((63, 64), C_GLOW_SPEC)
    torso.putpixel((64, 64), C_GLOW_SPEC)

    # 6. Shoulder Ball-and-Socket Joints
    def draw_ball_joint(cx: int, cy: int, r: int):
        d.ellipse([cx - r - 1, cy - r - 1, cx + r + 1, cy + r + 1], fill=C_OUTLINE)
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r:
                    px = cx + dx
                    py = cy + dy
                    lf = (-dx - dy) / float(r * 1.5)
                    if dx == -1 and dy == -1:
                        col = G_SPEC
                    elif lf > 0.4:
                        col = G_LIGHT
                    elif lf > -0.2:
                        col = G_MID
                    elif lf > -0.7:
                        col = G_SHADOW
                    else:
                        col = G_DEEP
                    torso.putpixel((px, py), col)
        torso.putpixel((cx, cy), C_OUTLINE)
        torso.putpixel((cx, cy - 1), G_LIGHT)

    draw_ball_joint(48, 59, 4)
    draw_ball_joint(78, 61, 4)

    # 7. Abdomen & Clockwork Waist Mechanism (y: 73..85)
    for y in range(74, 77):
        for x in range(58, 71):
            if x in (58, 70) or y == 76:
                torso.putpixel((x, y), C_OUTLINE)
            elif x < 64:
                torso.putpixel((x, y), P_MID)
            else:
                torso.putpixel((x, y), P_SHADOW)
    torso.putpixel((62, 74), P_LIGHT)
    torso.putpixel((63, 74), P_LIGHT)

    # Miniature Hydraulic / Spring Dampeners
    d.line([(57, 76), (56, 82)], fill=C_OUTLINE, width=2)
    d.line([(58, 76), (57, 82)], fill=G_LIGHT, width=1)
    torso.putpixel((57, 77), G_SPEC)
    torso.putpixel((56, 81), G_SHADOW)

    d.line([(71, 76), (72, 82)], fill=C_OUTLINE, width=2)
    d.line([(70, 76), (71, 82)], fill=G_MID, width=1)
    torso.putpixel((71, 81), G_DEEP)

    # Central Gyroscopic Waist Pivot Bearing (center: 64, 79, radius: 4)
    d.rounded_rectangle([60, 76, 68, 83], radius=3, fill=C_OUTLINE)
    d.ellipse([60, 76, 68, 83], fill=G_MID, outline=C_OUTLINE)
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            if dx * dx + dy * dy <= 9:
                px = 64 + dx
                py = 79 + dy
                lf = (-dx - dy) / 4.0
                if dx == -1 and dy == -1:
                    col = G_SPEC
                elif lf > 0.3:
                    col = G_LIGHT
                elif lf > -0.2:
                    col = G_MID
                else:
                    col = G_SHADOW
                torso.putpixel((px, py), col)

    d.line([(61, 79), (67, 79)], fill=C_OUTLINE)
    torso.putpixel((64, 79), G_SPEC)

    # Lower pelvic bracket (y: 83..85, x: 57..71)
    d.rounded_rectangle([57, 83, 71, 85], radius=2, fill=P_MID, outline=C_OUTLINE)
    for x in range(59, 70):
        if x < 65:
            torso.putpixel((x, 84), P_MID)
        else:
            torso.putpixel((x, 84), P_SHADOW)
    torso.putpixel((59, 84), G_LIGHT)
    torso.putpixel((69, 84), G_MID)

    return torso

def build_crane_porcelain_chassis(out_path: str = "") -> Image.Image:
    if not out_path:
        out_path = OUT_PORCELAIN

    orig = Image.open(OUT_PORCELAIN).convert("RGBA")
    torso = render_porcelain_torso()

    new_porcelain = Image.new("RGBA", (128, 128), (0, 0, 0, 0))

    # Copy non-torso pixels
    for y in range(128):
        for x in range(128):
            raw_p = orig.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4:
                continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a == 0:
                continue

            in_replacement_box = (44 <= x <= 84 and 53 <= y <= 85)
            if in_replacement_box:
                is_arm = False
                if x < 44 or x > 84:
                    is_arm = True
                elif x <= 43 and y >= 54:
                    is_arm = True
                elif x >= 83 and y >= 54:
                    is_arm = True
                elif x <= 48 and y >= 66:
                    is_arm = True
                elif x >= 78 and y >= 68:
                    is_arm = True

                if is_arm:
                    new_porcelain.putpixel((x, y), (r, g, b, a))
            else:
                new_porcelain.putpixel((x, y), (r, g, b, a))

    # Alpha composite the rendered torso
    new_porcelain.alpha_composite(torso)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    new_porcelain.save(out_path)
    print(f"✓ Successfully generated and saved Cloud Crane porcelain chassis: {out_path}")
    print(f"  Bbox: {new_porcelain.getbbox()}")
    return new_porcelain

if __name__ == "__main__":
    build_crane_porcelain_chassis()
