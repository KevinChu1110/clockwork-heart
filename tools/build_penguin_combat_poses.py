#!/usr/bin/env python3
"""
build_penguin_combat_poses.py
Generates the complete 6 combat action poses for The Steam Penguin (蒸氣企鵝, Ranger)
in Clockwork Heart:
  game/assets/sprites/player/poses/penguin/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/battle/penguin/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/penguin"
BATTLE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/battle/penguin"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(BATTLE_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_penguin_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers
chassis_src = Image.open(f"{BASE_DIR}/chassis/paint_penguin_navy.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_steam_penguin_stock.png").convert("RGBA")
key_src = Image.open(f"{BASE_DIR}/winding_key/key_twin_ring_helm.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_navigator_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/core_cyan_quartz.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/wpn_twin_harpoon_gun.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_mini_steam_boiler.png").convert("RGBA")

# -----------------------------------------------------------------------------
# Clean body_no_weapon: Remove hip gun, holster, brown leather.
# Enforce 100% CANON zero-fur / zero-leather: all metal, enamel, brass, rivets.
# -----------------------------------------------------------------------------
raw_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
raw_body.alpha_composite(key_src)
raw_body.alpha_composite(curio_src)
raw_body.alpha_composite(chassis_src)
raw_body.alpha_composite(head_src)
raw_body.alpha_composite(costume_src)
raw_body.alpha_composite(optic_src)

b_arr = np.array(raw_body)

NAVY_OUTLINE = (31, 26, 58, 255)
NAVY_DARK = (42, 48, 72, 255)
NAVY_MID = (58, 72, 108, 255)
NAVY_LIGHT = (82, 106, 152, 255)
NAVY_HL = (112, 138, 185, 255)

WHITE_SHADOW = (185, 182, 185, 255)
WHITE_MID = (225, 225, 230, 255)
WHITE_LIGHT = (248, 248, 252, 255)
WHITE_HL = (255, 255, 255, 255)

BRASS_DARK = (140, 85, 18, 255)
BRASS_MID = (205, 135, 30, 255)
BRASS_LIGHT = (245, 195, 45, 255)
BRASS_HL = (255, 230, 110, 255)

# Repaint flank/hip: x: 26..58, y: 63..96
for y in range(63, 97):
    for x in range(26, 59):
        r, g, b, a = [int(v) for v in b_arr[y, x]]
        if a < 20:
            continue
        is_brown = (r > 60 and g > 30 and b < 110 and (r - b > 20) and (r - g < 80) and not (r > 160 and g > 130 and r - g < 55))
        is_grey_metal = (abs(r - g) <= 12 and abs(g - b) <= 15 and 35 <= r <= 160)
        is_gun_part = is_brown or is_grey_metal
        if is_gun_part:
            if x <= 38:
                if x == 27 or (x <= 30 and (y == 65 or y >= 93)):
                    b_arr[y, x] = NAVY_OUTLINE
                elif x <= 31:
                    b_arr[y, x] = NAVY_DARK
                elif x <= 35:
                    b_arr[y, x] = NAVY_MID
                elif x <= 37:
                    b_arr[y, x] = NAVY_LIGHT
                else:
                    b_arr[y, x] = NAVY_HL
            elif x <= 41:
                if 73 <= y <= 76:
                    if y == 73 or y == 76:
                        b_arr[y, x] = BRASS_DARK
                    elif y == 74:
                        b_arr[y, x] = BRASS_HL
                    else:
                        b_arr[y, x] = BRASS_MID
                elif y in (68, 69, 82, 83, 90, 91):
                    b_arr[y, x] = BRASS_LIGHT
                else:
                    b_arr[y, x] = NAVY_OUTLINE
            else:
                if 73 <= y <= 76:
                    if y == 73 or y == 76:
                        b_arr[y, x] = BRASS_DARK
                    elif y == 74:
                        b_arr[y, x] = BRASS_HL
                    else:
                        b_arr[y, x] = BRASS_MID
                else:
                    if y >= 91:
                        b_arr[y, x] = WHITE_SHADOW
                    elif x <= 46:
                        b_arr[y, x] = WHITE_MID
                    elif x <= 53:
                        b_arr[y, x] = WHITE_LIGHT
                    else:
                        b_arr[y, x] = WHITE_HL

# Eliminate any remaining brown leather pixels on body/wrist (except beak and feet which are brass/orange)
for y in range(50, 105):
    for x in range(128):
        r, g, b, a = [int(v) for v in b_arr[y, x]]
        if a > 20:
            is_brown = (r > 60 and g > 30 and b < 100 and (r - b > 20) and (r - g < 75) and not (r > 160 and g > 130 and r - g < 55))
            if is_brown:
                if x >= 70:
                    # Wrist cuff -> brass metal guard with rivets
                    if r > 120:
                        b_arr[y, x] = BRASS_LIGHT
                    elif r > 90:
                        b_arr[y, x] = BRASS_MID
                    else:
                        b_arr[y, x] = BRASS_DARK
                else:
                    if x <= 40:
                        b_arr[y, x] = NAVY_MID
                    else:
                        b_arr[y, x] = WHITE_MID

body_no_weapon = Image.fromarray(b_arr, "RGBA")

# -----------------------------------------------------------------------------
# Clean gun_raw: Genuine Twin Harpoon Gun (雙聯並列雙管), zero wood/leather
# -----------------------------------------------------------------------------
gun_bbox = weapon_src.getbbox()
assert gun_bbox is not None
gun_crop = weapon_src.crop(gun_bbox)
g_arr = np.array(gun_crop)

# 1. Recolor brown wood/leather grip and fore-end to dark navy steel & brass
for y in range(gun_crop.height):
    for x in range(gun_crop.width):
        r, g, b, a = [int(v) for v in g_arr[y, x]]
        if a > 20:
            is_brown = (r > 60 and g > 30 and b < 100 and (r - b > 20) and (r - g < 75) and not (r > 160 and g > 130 and r - g < 55))
            if is_brown:
                if y >= 27:
                    if r > 110:
                        g_arr[y, x] = BRASS_LIGHT
                    elif r > 80:
                        g_arr[y, x] = BRASS_MID
                    else:
                        g_arr[y, x] = BRASS_DARK
                else:
                    if r > 110:
                        g_arr[y, x] = NAVY_LIGHT
                    elif r > 80:
                        g_arr[y, x] = NAVY_MID
                    else:
                        g_arr[y, x] = NAVY_DARK

# 2. Sculpt distinct twin parallel barrels (over-under / twin side-by-side)
DARK_BORE = (22, 18, 38, 255)
STEEL_OUTLINE = (35, 32, 55, 255)
STEEL_DARK = (60, 65, 85, 255)
STEEL_MID = (100, 110, 130, 255)
STEEL_LIGHT = (150, 160, 180, 255)
STEEL_HL = (205, 215, 235, 255)

# Clear any stray pixels outside the twin barrels for x >= 36
for y in range(gun_crop.height):
    for x in range(36, gun_crop.width):
        if y < 22 or y > 31:
            g_arr[y, x] = (0, 0, 0, 0)

# Sculpt Upper Barrel: y = 22..26, x = 28..42
for x in range(28, 43):
    g_arr[22, x] = STEEL_OUTLINE
    g_arr[23, x] = STEEL_HL if x < 40 else STEEL_LIGHT
    g_arr[24, x] = STEEL_MID
    g_arr[25, x] = STEEL_DARK

# Separator groove between barrels: y = 26..27, x = 28..42
for x in range(28, 43):
    g_arr[26, x] = STEEL_OUTLINE
    g_arr[27, x] = STEEL_OUTLINE

# Sculpt Lower Barrel: y = 27..31, x = 28..42
for x in range(28, 43):
    g_arr[28, x] = STEEL_HL if x < 40 else STEEL_LIGHT
    g_arr[29, x] = STEEL_MID
    g_arr[30, x] = STEEL_DARK
    g_arr[31, x] = STEEL_OUTLINE

# Brass barrel clamp holding the twin barrels together at x = 33..34
for x in (33, 34):
    for y in range(22, 32):
        if y in (22, 31):
            g_arr[y, x] = STEEL_OUTLINE
        elif y in (23, 28):
            g_arr[y, x] = BRASS_LIGHT
        else:
            g_arr[y, x] = BRASS_MID

# Muzzle tips at x = 41..42
# Upper muzzle bore:
g_arr[22, 42] = STEEL_LIGHT
g_arr[23, 41] = STEEL_LIGHT; g_arr[23, 42] = DARK_BORE
g_arr[24, 41] = DARK_BORE;   g_arr[24, 42] = DARK_BORE
g_arr[25, 41] = STEEL_LIGHT; g_arr[25, 42] = DARK_BORE
g_arr[26, 42] = STEEL_OUTLINE

# Lower muzzle bore:
g_arr[27, 42] = STEEL_OUTLINE
g_arr[28, 41] = STEEL_LIGHT; g_arr[28, 42] = DARK_BORE
g_arr[29, 41] = DARK_BORE;   g_arr[29, 42] = DARK_BORE
g_arr[30, 41] = STEEL_LIGHT; g_arr[30, 42] = DARK_BORE
g_arr[31, 42] = STEEL_LIGHT

gun_raw = Image.fromarray(g_arr, "RGBA")

def clean_margins(img: Image.Image) -> Image.Image:
    """Clean margins strictly (L>=4, R>=4, T>=4, B>=2)."""
    out = img.copy()
    o_px = out.load()
    assert o_px is not None
    for x in range(128):
        o_px[x, 0] = (0, 0, 0, 0)
        o_px[x, 1] = (0, 0, 0, 0)
        o_px[x, 2] = (0, 0, 0, 0)
        o_px[x, 3] = (0, 0, 0, 0)
        o_px[x, 126] = (0, 0, 0, 0)
        o_px[x, 127] = (0, 0, 0, 0)
    for y in range(128):
        o_px[0, y] = (0, 0, 0, 0)
        o_px[1, y] = (0, 0, 0, 0)
        o_px[2, y] = (0, 0, 0, 0)
        o_px[3, y] = (0, 0, 0, 0)
        o_px[124, y] = (0, 0, 0, 0)
        o_px[125, y] = (0, 0, 0, 0)
        o_px[126, y] = (0, 0, 0, 0)
        o_px[127, y] = (0, 0, 0, 0)
    return out

def place_gun(gun_img: Image.Image, deg: float, target_grip: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the twin harpoon gun with zero clipping."""
    d = gun_img.copy()
    if mirror:
        d = ImageOps.mirror(d)
    dw, dh = d.size
    gx, gy = (4, 22) if not mirror else (dw - 4, 22)
    
    if deg == 0 and scale == 1.0 and not mirror:
        out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        tx, ty = target_grip
        out.paste(d, (tx - gx, ty - gy))
        return out
        
    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    large.paste(d, (128 - gx, 128 - gy))
    
    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        large = large.resize((nw, nh), Image.Resampling.LANCZOS)
        
    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tx, ty = target_grip
    out.paste(rotated, (tx - 128, ty - 128), rotated)
    return out

# Baseline ground contact shadow
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
assert s_px is not None and c_px is not None
for y in range(118, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        s_px[x, y] = p

EXPECTED_SHADOW = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], s_px[x, y])[3] > 20) for y in range(118, 128)]
print(f"Benchmark Penguin ground shadow row counts (118..127): {EXPECTED_SHADOW}")

assert s_px is not None
def enforce_ground_shadow(img: Image.Image) -> Image.Image:
    """Enforce exact ground contact shadow matching baseline Rule 4b-5."""
    out = img.copy()
    o_px = out.load()
    assert o_px is not None
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            fp = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20 and fp[3] > 20:
                o_px[x, y] = (0, 0, 0, 0)
            elif sp[3] > 20 and fp[3] <= 20:
                o_px[x, y] = sp
    return clean_margins(out)

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

# Anchor corners and borders for IDW
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127)
]

base_landmarks = {
    "head_top": (60, 18),
    "goggles_l": (54, 38),
    "goggles_r": (68, 38),
    "beak": (60, 48),
    "head_base": (60, 56),
    "chest_core": (62, 68),
    "shoulder_l": (36, 58),
    "shoulder_r": (78, 60),
    "flipper_l": (22, 68),
    "flipper_r": (80, 72),
    "belly": (58, 80),
    "pelvis": (56, 96),
    "foot_l": (38, 110),
    "foot_r": (66, 110),
    "key": (18, 26),
    "curio_boiler": (20, 50),
}

def generate_poses():
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (蒸汽戒備架式 Steam Sentry Ready)
    # =========================================================================
    idle_canvas = body_no_weapon.copy()
    g_idle = place_gun(gun_raw, deg=0, target_grip=(78, 70), scale=1.0, mirror=False)
    idle_canvas.alpha_composite(g_idle)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (過壓蓄勢瞄準 Overpressure Lock & Aim)
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-4, 6),
        "goggles_l": (-4, 6), "goggles_r": (-3, 6),
        "beak": (-3, 7), "head_base": (-3, 6),
        "chest_core": (-4, 6),
        "shoulder_l": (-5, 5), "shoulder_r": (-2, 5),
        "flipper_l": (3, 5), "flipper_r": (-5, 5),
        "belly": (-3, 6), "pelvis": (-3, 6),
        "foot_l": (-5, 1), "foot_r": (4, 1),
        "key": (-4, 5), "curio_boiler": (-4, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Gun raised to eye level (deg=22), two-hand stance grip at (72, 74)
    g_tele = place_gun(gun_raw, deg=22, target_grip=(72, 74), scale=1.0, mirror=False)

    # Visual FX: Overcharge pressure dial & steam vent puffs (no synthetic reticle lines)
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Steam pressure puffs from boiler vent
    t_draw.ellipse([10, 44, 20, 54], fill=(230, 240, 250, 160))
    t_draw.ellipse([6, 36, 16, 46], fill=(245, 250, 255, 190))
    # Chest core & goggle focus pulse
    t_draw.ellipse([56, 72, 64, 80], fill=(56, 160, 255, 220))
    t_draw.point([(68, 38), (69, 38), (68, 39)], fill=(255, 255, 255, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas.alpha_composite(warped_tele)
    tele_canvas.alpha_composite(g_tele)
    tele_canvas.alpha_composite(tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (雙管蒸氣轟擊 Twin Steam Blast & Recoil)
    # Twin parallel steam jets emerging distinctly from the two barrels!
    # Blast strictly within x <= 122 to preserve R>=4 margin.
    # =========================================================================
    shifts_attack = {
        "head_top": (10, 1),
        "goggles_l": (11, 1), "goggles_r": (12, 1),
        "beak": (13, 2), "head_base": (11, 2),
        "chest_core": (10, 2),
        "shoulder_l": (8, 2), "shoulder_r": (13, 2),
        "flipper_l": (-5, 3), "flipper_r": (14, 1),
        "belly": (9, 2), "pelvis": (7, 2),
        "foot_l": (-7, 0), "foot_r": (10, 0),
        "key": (6, 2), "curio_boiler": (7, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Gun recoiling with strong muzzle kick (deg=-14), target_grip=(87, 68)
    g_atk = place_gun(gun_raw, deg=-14, target_grip=(87, 68), scale=1.0, mirror=False)

    # Visual FX: Twin parallel steam jets from the two barrel bores
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)

    # Upper barrel steam jet (y=56..60, x=114..122)
    a_draw.line([(113, 58), (121, 57)], fill=(255, 255, 255, 240), width=2)
    a_draw.ellipse([115, 55, 122, 61], fill=(230, 245, 255, 180))

    # Lower barrel steam jet (y=62..66, x=113..121)
    a_draw.line([(112, 64), (120, 65)], fill=(255, 255, 255, 240), width=2)
    a_draw.ellipse([114, 62, 121, 68], fill=(230, 245, 255, 180))

    # Twin muzzle flash sparks at the bores
    a_draw.point([(113, 58), (114, 57), (112, 64), (113, 65)], fill=(255, 215, 60, 255))

    # Steam release from gun chamber vent
    a_draw.ellipse([91, 52, 97, 58], fill=(240, 248, 255, 180))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas.alpha_composite(warped_attack)
    atk_canvas.alpha_composite(g_atk)
    atk_canvas.alpha_composite(atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (天穹高壓連射 Skyward Steam Barrage)
    # =========================================================================
    shifts_skill = {
        "head_top": (-3, -6),
        "goggles_l": (-2, -6), "goggles_r": (-1, -6),
        "beak": (-1, -5), "head_base": (-1, -5),
        "chest_core": (2, -5),
        "shoulder_l": (-4, -6), "shoulder_r": (5, -6),
        "flipper_l": (2, -6), "flipper_r": (7, -8),
        "belly": (2, -4), "pelvis": (2, -3),
        "foot_l": (-3, -3), "foot_r": (4, -3),
        "key": (-3, -5), "curio_boiler": (-1, -5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Gun angled upward (-62 deg), grip at (81, 62)
    g_skill = place_gun(gun_raw, deg=-62, target_grip=(81, 62), scale=0.96, mirror=False)

    # Visual FX: Upward twin steam geyser & shockwave
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    s_draw.ellipse([86, 12, 108, 34], fill=(230, 245, 255, 170))
    s_draw.ellipse([90, 16, 104, 30], fill=(255, 255, 255, 220))
    s_draw.arc([78, 9, 116, 47], start=160, end=340, fill=(56, 160, 255, 200), width=2)
    s_draw.arc([82, 13, 112, 43], start=170, end=330, fill=(255, 208, 40, 210), width=2)
    s_draw.ellipse([12, 28, 26, 42], fill=(235, 245, 255, 160))
    s_draw.ellipse([18, 20, 28, 30], fill=(245, 250, 255, 180))
    s_draw.ellipse([58, 61, 66, 69], fill=(56, 160, 255, 220))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.6))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas.alpha_composite(warped_skill)
    skill_canvas.alpha_composite(g_skill)
    skill_canvas.alpha_composite(skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (蒸汽洩壓受擊 Piston Dampener Absorb / Guard)
    # =========================================================================
    shifts_hit = {
        "head_top": (-10, -2),
        "goggles_l": (-10, -2), "goggles_r": (-8, -2),
        "beak": (-9, -1), "head_base": (-8, -1),
        "chest_core": (-7, -1),
        "shoulder_l": (-8, -1), "shoulder_r": (-5, -1),
        "flipper_l": (-5, -1), "flipper_r": (-6, 0),
        "belly": (-6, -1), "pelvis": (-5, 0),
        "foot_l": (-7, 0), "foot_r": (-3, 0),
        "key": (-9, -1), "curio_boiler": (-9, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Gun braced defensively across chest (deg=-32), grip at (67, 74)
    g_hit = place_gun(gun_raw, deg=-32, target_grip=(67, 74), scale=0.96, mirror=False)

    # Visual FX: Impact spark & steam exhaust
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    h_draw.ellipse([58, 59, 66, 67], fill=(255, 245, 180, 230))
    h_draw.line([(54, 63), (70, 63)], fill=(255, 255, 220, 220), width=1)
    h_draw.line([(62, 55), (62, 71)], fill=(255, 255, 220, 220), width=1)
    h_draw.ellipse([6, 42, 18, 54], fill=(230, 240, 250, 160))
    h_draw.ellipse([4, 34, 14, 44], fill=(245, 250, 255, 190))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.5))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas.alpha_composite(warped_hit)
    hit_canvas.alpha_composite(g_hit)
    hit_canvas.alpha_composite(hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (錨定排氣收勢 Ground Anchor & Vent Reset)
    # =========================================================================
    shifts_recover = {
        "head_top": (4, 5),
        "goggles_l": (4, 5), "goggles_r": (5, 5),
        "beak": (5, 6), "head_base": (4, 6),
        "chest_core": (4, 6),
        "shoulder_l": (2, 5), "shoulder_r": (5, 6),
        "flipper_l": (-3, 5), "flipper_r": (6, 6),
        "belly": (3, 6), "pelvis": (3, 6),
        "foot_l": (-6, 1), "foot_r": (4, 1),
        "key": (3, 5), "curio_boiler": (3, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_recover = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Gun grounded/lowered at forward-downward angle (deg=52), grip at (81, 82)
    g_rec = place_gun(gun_raw, deg=52, target_grip=(81, 82), scale=0.96, mirror=False)

    # Visual FX: Clean cooling steam exhaust from boiler relief valves (zero ground blobs)
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Soft dissipating steam around boiler & exhaust pipes
    r_draw.ellipse([14, 66, 24, 76], fill=(230, 240, 250, 140))
    r_draw.ellipse([20, 58, 28, 66], fill=(240, 248, 255, 160))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.4))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas.alpha_composite(warped_recover)
    rec_canvas.alpha_composite(g_rec)
    rec_canvas.alpha_composite(rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    poses = generate_poses()
    for name, im in poses.items():
        out_p1 = f"{OUT_DIR}/{name}.png"
        out_p2 = f"{BATTLE_DIR}/{name}.png"
        im.save(out_p1, "PNG")
        im.save(out_p2, "PNG")
        bbox = im.getbbox()
        h = bbox[3] - bbox[1] if bbox else 0
        w = bbox[2] - bbox[0] if bbox else 0
        px_115 = sum(1 for y in range(115) for x in range(128) if cast(tuple[int, int, int, int], im.getpixel((x, y)))[3] > 8)
        print(f"✓ {name:10s}: saved, bbox={bbox}, w={w}, h={h}, y<115={px_115}")
