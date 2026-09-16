#!/usr/bin/env python3
"""
tools/build_all_bear_chassis.py
Production script to rebuild all 3 paperdoll chassis skins for The Iron Bear (玄軸熊):
1. paint_bear_amber.png (原廠玄軸琥珀棕)
2. paint_iron_quarry.png (重裝礦山玄鐵灰)
3. paint_ivory_stock.png (原廠象牙白)

Resolves: docs/art/PAPERDOLL_CHASSIS_AUDIT.md (t_a1c16ffa, t_bfa95a74)
- Fully replaces placeholder rounded rectangle screens & yellow dots with authentic clockwork toy automaton plating.
- Zero biological fur/tissue, 100% CANON compliant.
- Metallic ball-and-socket joints, chiseled core bezel with glowing optical crystal lenses.
- Restores original hand-painted metallic legs & boots (100% purged rectangular pedal blockout).
- Cleans up stray pixels on all silhouette edges.
"""

import os
import math
from typing import cast
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
BEAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear"
CHASSIS_DIR = f"{BEAR_DIR}/chassis"
SRC_BASE = "/tmp/bear_aligned_128.png"

# Universal crisp outline
C_OUTLINE = (31, 26, 58, 255)       # Deep blue-purple #1F1A3A
C_CREASE = (55, 45, 50, 255)        # Panel seam crease

# Polished Brass Gold ramp (Universal joints, bezels, rivets across all 3 variants)
G_SPEC = (255, 248, 205, 255)       # Glint
G_LIGHT = (255, 218, 50, 255)       # Bright brass #FFD028
G_MID = (255, 160, 20, 255)         # Warm gold #FFA010
G_SHADOW = (185, 105, 15, 255)      # Deep gold shadow
G_DEEP = (110, 55, 10, 255)         # Crease shadow

# Cast Dark Iron ramp (Dampeners, neck bellows, fist clamps)
I_LIGHT = (140, 150, 168, 255)
I_MID = (85, 92, 108, 255)
I_SHADOW = (50, 55, 68, 255)
I_DEEP = (30, 34, 44, 255)

# --- Style Palettes ---
STYLES = {
    "amber": {
        # Primary: Caramel Amber Enamel
        "P_SPEC": (255, 230, 180, 255),
        "P_LIGHT": (248, 160, 68, 255),
        "P_MID": (217, 119, 36, 255),
        "P_SHADOW": (165, 80, 20, 255),
        "P_DEEP": (108, 48, 15, 255),
        # Secondary: Cream Marble White
        "S_SPEC": (255, 255, 250, 255),
        "S_LIGHT": (255, 248, 231, 255),
        "S_MID": (240, 226, 205, 255),
        "S_SHADOW": (200, 185, 160, 255),
        "S_DEEP": (150, 135, 115, 255),
        # Optical Core: Mint Emerald (matches official standee eyes)
        "C_SPEC": (235, 255, 240, 255),
        "C_LIGHT": (140, 245, 165, 255),
        "C_MID": (78, 216, 106, 255),
        "C_SHADOW": (30, 140, 60, 255),
        "C_DEEP": (14, 75, 32, 255),
    },
    "quarry": {
        # Primary: Cold-quenched Quarry Steel
        "P_SPEC": (230, 242, 255, 255),
        "P_LIGHT": (145, 172, 208, 255),
        "P_MID": (82, 104, 138, 255),
        "P_SHADOW": (48, 62, 86, 255),
        "P_DEEP": (28, 36, 52, 255),
        # Secondary: Cold Titanium White
        "S_SPEC": (252, 254, 255, 255),
        "S_LIGHT": (228, 238, 250, 255),
        "S_MID": (192, 208, 228, 255),
        "S_SHADOW": (145, 162, 188, 255),
        "S_DEEP": (100, 115, 138, 255),
        # Optical Core: Radiant Cyan / Sky Ice
        "C_SPEC": (235, 250, 255, 255),
        "C_LIGHT": (120, 215, 255, 255),
        "C_MID": (56, 160, 255, 255),
        "C_SHADOW": (20, 95, 185, 255),
        "C_DEEP": (12, 50, 115, 255),
    },
    "ivory": {
        # Primary: Warm Ivory Enamel
        "P_SPEC": (255, 252, 245, 255),
        "P_LIGHT": (248, 242, 230, 255),
        "P_MID": (228, 218, 198, 255),
        "P_SHADOW": (185, 170, 148, 255),
        "P_DEEP": (138, 124, 104, 255),
        # Secondary: Muted Warm Bronze Gold
        "S_SPEC": (255, 242, 195, 255),
        "S_LIGHT": (232, 198, 135, 255),
        "S_MID": (196, 156, 92, 255),
        "S_SHADOW": (148, 112, 60, 255),
        "S_DEEP": (102, 74, 38, 255),
        # Optical Core: Radiant Emerald Green
        "C_SPEC": (230, 255, 235, 255),
        "C_LIGHT": (115, 235, 145, 255),
        "C_MID": (54, 192, 88, 255),
        "C_SHADOW": (25, 125, 52, 255),
        "C_DEEP": (12, 70, 28, 255),
    }
}

def render_chassis_torso(style_name: str) -> Image.Image:
    pal = STYLES[style_name]
    torso = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(torso)

    # 1. Base Silhouette of Torso (y: 53..87, x: 44..84)
    torso_poly = [
        (54, 53), (74, 53),     # Neck base
        (80, 55), (84, 58),     # Right shoulder socket slope
        (85, 66), (83, 75),     # Right flank curve
        (80, 81), (77, 85),     # Lower right abdomen curve
        (72, 87), (56, 87),     # Pelvic bottom bracket
        (51, 85), (48, 81),     # Lower left abdomen curve
        (45, 75), (43, 66),     # Left flank curve
        (44, 58), (48, 55),     # Left shoulder socket slope
    ]
    d.polygon(torso_poly, fill=C_OUTLINE)

    # 2. Neck Collar & Bellows Joint (y: 52..56, x: 55..73)
    d.rounded_rectangle([55, 52, 73, 56], radius=2, fill=I_MID, outline=C_OUTLINE)
    for nx in range(56, 73):
        if nx in (63, 64, 65):
            torso.putpixel((nx, 53), I_LIGHT)
            torso.putpixel((nx, 54), pal["S_SPEC"])
            torso.putpixel((nx, 55), G_LIGHT)
        elif nx in (58, 60, 68, 70):
            torso.putpixel((nx, 54), I_SHADOW)
        else:
            torso.putpixel((nx, 54), I_LIGHT)

    # 3. Flank Reinforcement Plates (Left x: 44..50, Right x: 78..84)
    l_flank = [(45, 57), (50, 56), (49, 75), (44, 73)]
    d.polygon(l_flank, fill=pal["P_SHADOW"], outline=C_OUTLINE)
    for fy in range(58, 73):
        torso.putpixel((46, fy), pal["P_MID"])
        torso.putpixel((45, fy), pal["P_SHADOW"])
    torso.putpixel((46, 60), pal["P_LIGHT"])
    torso.putpixel((47, 61), pal["P_SPEC"])

    r_flank = [(78, 56), (83, 57), (84, 73), (79, 75)]
    d.polygon(r_flank, fill=pal["P_DEEP"], outline=C_OUTLINE)
    for fy in range(58, 73):
        torso.putpixel((81, fy), pal["P_SHADOW"])
        torso.putpixel((82, fy), pal["P_DEEP"])
    torso.putpixel((80, 60), pal["P_MID"])

    # 4. Main Curved Forged Breastplate (x: 48..80, y: 55..74)
    for y in range(55, 75):
        if y < 58:
            x_start, x_end = 51, 77
        elif y < 62:
            x_start, x_end = 48, 80
        elif y < 70:
            x_start, x_end = 47, 81
        else:
            x_start, x_end = 49, 79

        for x in range(x_start, x_end + 1):
            if x == x_start or x == x_end or y == 55 or y == 74:
                torso.putpixel((x, y), C_OUTLINE)
                continue

            dx = (x - 62.0) / 14.0
            dy = (y - 60.0) / 11.0
            dist = math.sqrt(dx * dx + dy * dy)

            if x < 63:
                if y in (56, 57) and x in (58, 59, 60, 61):
                    col = pal["P_SPEC"]
                elif dist < 0.65:
                    col = pal["P_LIGHT"]
                elif dist < 1.15:
                    col = pal["P_MID"]
                else:
                    col = pal["P_SHADOW"]
            else:
                if dist < 0.75:
                    col = pal["P_MID"]
                elif dist < 1.30:
                    col = pal["P_SHADOW"]
                else:
                    col = pal["P_DEEP"]

            if y in (72, 73):
                col = pal["P_SHADOW"] if x < 63 else pal["P_DEEP"]

            torso.putpixel((x, y), col)

    # Decorative brass rivets along chest rim
    for rx, ry in [(52, 58), (56, 57), (72, 57), (76, 58)]:
        torso.putpixel((rx, ry), G_LIGHT)
        torso.putpixel((rx, ry - 1), G_SPEC)
        torso.putpixel((rx, ry + 1), C_OUTLINE)

    # 5. Chest Optical Energy Core & Brass Bezel (Center: 64, 65)
    d.ellipse([57, 58, 71, 72], fill=C_OUTLINE)
    d.ellipse([58, 59, 70, 71], fill=G_MID)

    # Bezel highlights & shadows
    d.arc([58, 59, 70, 71], start=160, end=320, fill=G_SPEC, width=1)
    d.arc([58, 59, 70, 71], start=180, end=300, fill=G_LIGHT, width=1)
    d.arc([58, 59, 70, 71], start=0, end=140, fill=G_DEEP, width=1)
    d.arc([58, 59, 70, 71], start=20, end=120, fill=G_SHADOW, width=1)

    torso.putpixel((64, 59), G_SPEC)
    torso.putpixel((64, 71), G_DEEP)
    torso.putpixel((58, 65), G_LIGHT)
    torso.putpixel((70, 65), G_SHADOW)

    # Core Aperture socket
    d.ellipse([60, 61, 68, 69], fill=pal["C_DEEP"], outline=C_OUTLINE)

    # Glowing Crystal Lens
    d.ellipse([61, 62, 67, 68], fill=pal["C_MID"])
    d.ellipse([62, 63, 66, 67], fill=pal["C_LIGHT"])
    torso.putpixel((63, 64), pal["C_SPEC"])
    torso.putpixel((64, 64), pal["C_SPEC"])
    torso.putpixel((64, 63), pal["S_SPEC"])

    # 6. Shoulder Ball-and-Socket Joints (Polished Brass Spheres)
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
        d.line([(cx - 2, cy), (cx + 2, cy)], fill=C_OUTLINE)
        torso.putpixel((cx, cy - 1), G_SPEC)
        torso.putpixel((cx, cy + 1), G_DEEP)

    draw_ball_joint(39, 59, 5)
    draw_ball_joint(85, 59, 5)

    # 7. Abdomen & Maintenance Hatch Panel (y: 74..84, x: 49..79)
    for y in range(74, 85):
        for x in range(50, 79):
            if x in (50, 78) or y in (74, 84):
                torso.putpixel((x, y), C_OUTLINE)
            elif x < 64:
                torso.putpixel((x, y), pal["P_MID"])
            else:
                torso.putpixel((x, y), pal["P_SHADOW"])

    # Maintenance Hatch Door
    d.rounded_rectangle([55, 75, 73, 83], radius=2, fill=pal["S_MID"], outline=C_OUTLINE)
    for hy in range(76, 83):
        for hx in range(56, 73):
            if hx in (56, 57) and hy in (76, 77):
                torso.putpixel((hx, hy), pal["S_SPEC"])
            elif hx < 64:
                torso.putpixel((hx, hy), pal["S_LIGHT"])
            elif hx < 70:
                torso.putpixel((hx, hy), pal["S_MID"])
            else:
                torso.putpixel((hx, hy), pal["S_SHADOW"])

    d.line([(57, 79), (71, 79)], fill=C_CREASE)
    torso.putpixel((64, 79), G_LIGHT)
    torso.putpixel((63, 79), G_SPEC)

    for sx, sy in [(56, 76), (72, 76), (56, 82), (72, 82)]:
        torso.putpixel((sx, sy), G_MID)
        torso.putpixel((sx, sy - 1), G_SPEC)

    # 8. Miniature Hydraulic Dampeners (Left & Right Flanks)
    d.line([(51, 77), (49, 84)], fill=C_OUTLINE, width=2)
    d.line([(52, 77), (50, 84)], fill=G_LIGHT, width=1)
    torso.putpixel((52, 78), G_SPEC)
    torso.putpixel((50, 83), G_SHADOW)

    d.line([(77, 77), (79, 84)], fill=C_OUTLINE, width=2)
    d.line([(76, 77), (78, 84)], fill=G_MID, width=1)
    torso.putpixel((78, 83), G_DEEP)

    # 9. Central Gyroscopic Waist Pivot Bearing (center: 64, 84, radius: 4)
    d.ellipse([60, 80, 68, 88], fill=C_OUTLINE)
    d.ellipse([61, 81, 67, 87], fill=G_MID)
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            if dx * dx + dy * dy <= 9:
                px = 64 + dx
                py = 84 + dy
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

    d.line([(61, 84), (67, 84)], fill=C_OUTLINE)
    torso.putpixel((64, 84), G_SPEC)

    # 10. Pelvic Bottom Bracket (y: 84..88, x: 53..75)
    d.rounded_rectangle([53, 85, 75, 88], radius=2, fill=pal["P_SHADOW"], outline=C_OUTLINE)
    for px in range(54, 75):
        if px < 64:
            torso.putpixel((px, 86), pal["P_MID"])
            torso.putpixel((px, 87), pal["P_SHADOW"])
        else:
            torso.putpixel((px, 86), pal["P_SHADOW"])
            torso.putpixel((px, 87), pal["P_DEEP"])
    torso.putpixel((56, 86), G_LIGHT)
    torso.putpixel((72, 86), G_MID)

    d.ellipse([60, 91, 68, 97], fill=G_MID, outline=C_OUTLINE, width=1)
    d.ellipse([62, 92, 66, 96], fill=G_SHADOW)
    torso.putpixel((63, 93), G_SPEC)

    return torso

def map_limbs_pixel(r: int, g: int, b: int, a: int, x: int, y: int, style: str) -> tuple[int, int, int, int]:
    """
    Transforms base authentic limb pixel into the appropriate style palette:
    - Retains brass/gold accents & knee bearing joints.
    - Accurately remaps body plating to Quarry Steel or Ivory Enamel.
    - Keeps deep blue-purple outline (#1F1A3A).
    """
    if a <= 15:
        return (0, 0, 0, 0)

    # Ground soft contact shadow at base
    if y >= 115 and (r < 60 and g < 60 and b < 80):
        return (r, g, b, a)

    lum = int(0.299 * r + 0.587 * g + 0.114 * b)

    # 1. Dark outline / seam groove: crisp #1F1A3A
    if lum < 50 or (r <= 35 and g <= 30 and b <= 60):
        return (31, 26, 58, a)

    # 2. Brass / gold accents / knee ball joints / rivets
    is_brass = (r > 185 and g > 145 and b < 85)
    if is_brass:
        return (r, g, b, a)

    if style == "amber":
        return (r, g, b, a)

    elif style == "quarry":
        # White/cream knee cap & boots highlights -> Titanium cold white
        if r > 215 and g > 205 and b > 190:
            f_w = (lum - 200) / 55.0
            wr = int(195 + f_w * 50)
            wg = int(210 + f_w * 40)
            wb = int(235 + f_w * 20)
            return (max(0, min(255, wr)), max(0, min(255, wg)), max(0, min(255, wb)), a)

        # Dark steel boots soles & joints
        if r < 90 and g < 100 and b < 120 and r < g + 15:
            return (32, 36, 48, a)

        # Main amber plating -> Quarry Iron Steel (#36445A ~ #98ADC8)
        f = max(0.0, min(1.0, (lum - 40) / 165.0))
        sr = int(36 + f * 98)
        sg = int(48 + f * 118)
        sb = int(70 + f * 148)
        if lum > 160:
            sr = min(230, sr + 40)
            sg = min(240, sg + 42)
            sb = min(255, sb + 35)
        return (sr, sg, sb, a)

    elif style == "ivory":
        # White/cream knee cap & highlights -> Glazed ivory white
        if r > 215 and g > 205 and b > 190:
            f_w = max(0.0, min(1.0, (lum - 190) / 65.0))
            return (int(235 + f_w * 20), int(230 + f_w * 22), int(220 + f_w * 25), a)

        # Dark soles & seams
        if r < 90 and g < 100 and b < 120 and r < g + 15:
            return (40, 36, 46, a)

        # Amber plating -> Warm ivory enamel (#A89882 ~ #EFE5D4)
        f = max(0.0, min(1.0, (lum - 40) / 165.0))
        ir = int(160 + f * 85)
        ig = int(145 + f * 90)
        ib = int(125 + f * 95)
        if lum > 160:
            ir = min(255, ir + 15)
            ig = min(252, ig + 18)
            ib = min(245, ib + 25)
        return (ir, ig, ib, a)

    return (r, g, b, a)

def build_single_chassis(style: str, out_filename: str) -> Image.Image:
    base_aligned = Image.open(SRC_BASE).convert("RGBA")
    w, h = 128, 128
    chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # 1. Ground contact shadow (centered at (64, 120), radius: 28 x 5, Gaussian blurred)
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    sd.ellipse([64 - 28, 120 - 5, 64 + 28, 120 + 5], fill=(31, 26, 58, 140))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(1.6))
    chassis.alpha_composite(shadow_layer)

    # 2. Extract and color-map authentic limbs from base_aligned
    for y in range(h):
        for x in range(w):
            # Clean stray edge pixels:
            # - x <= 28 outside arm contour
            # - x >= 93 outside arm contour
            if x <= 28 and y < 110:
                continue
            if x >= 93 and y < 110:
                continue

            raw_p = base_aligned.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4:
                continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 35:
                continue

            # Legs and boots: y in 85..121, x in 30..90
            is_leg = (85 <= y <= 121 and 30 <= x <= 90)

            # Left arm (x: 29..46, y: 56..84) and right arm (x: 74..92, y: 56..84)
            is_left_arm = (56 <= y <= 84 and 29 <= x <= 46)
            is_right_arm = (56 <= y <= 84 and 74 <= x <= 92)

            if is_leg or is_left_arm or is_right_arm:
                mapped_rgba = map_limbs_pixel(r, g, b, a, x, y, style)
                if mapped_rgba[3] > 0:
                    chassis.putpixel((x, y), mapped_rgba)

    # 3. Clean mechanical clenched fist clamps (zero placeholder rods)
    cd = ImageDraw.Draw(chassis)
    fist_fill = I_SHADOW if style != "quarry" else (35, 42, 56, 255)
    fist_line = G_LIGHT
    # Left fist
    cd.polygon([(32, 80), (35, 76), (42, 78), (44, 84), (37, 85)], fill=fist_fill, outline=C_OUTLINE)
    cd.line([(34, 82), (36, 85)], fill=fist_line, width=1)
    chassis.putpixel((36, 78), I_LIGHT)
    # Right fist
    cd.polygon([(82, 78), (89, 76), (92, 82), (88, 86), (81, 83)], fill=fist_fill, outline=C_OUTLINE)
    cd.line([(86, 82), (89, 85)], fill=fist_line, width=1)
    chassis.putpixel((85, 78), I_LIGHT)

    # 4. Composite high-detail rendered clockwork automaton torso
    torso = render_chassis_torso(style)
    chassis.alpha_composite(torso)

    out_path = f"{CHASSIS_DIR}/{out_filename}"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    chassis.save(out_path)
    print(f"✓ Successfully built and saved [{style:6s}] chassis -> {out_path}")
    print(f"  Bbox: {chassis.getbbox()}")
    return chassis

def build_all_chassis():
    print("=== BUILDING ALL 3 IRON BEAR CHASSIS SKINS (0-ART18 FIX) ===")
    c_amber = build_single_chassis("amber", "paint_bear_amber.png")
    c_quarry = build_single_chassis("quarry", "paint_iron_quarry.png")
    c_ivory = build_single_chassis("ivory", "paint_ivory_stock.png")
    print("=== ALL 3 CHASSIS SKINS GENERATED SUCCESSFULLY ===")
    return c_amber, c_quarry, c_ivory

if __name__ == "__main__":
    build_all_chassis()
