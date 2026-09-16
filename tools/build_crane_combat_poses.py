#!/usr/bin/env python3
"""
tools/build_crane_combat_poses.py
Generates the complete, definitive 6 combat action poses for Cloud Crane (雲嵐鶴, ranger)
in Clockwork Heart:
  game/assets/sprites/player/poses/crane/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crane"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/crane"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_crane_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers
chassis_src = Image.open(f"{BASE_DIR}/chassis/paint_crane_porcelain.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_cloud_crane_stock.png").convert("RGBA")
key_src = Image.open(f"{BASE_DIR}/winding_key/key_tri_wing_zephyr.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_zephyr_robe.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/core_vermilion_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/wpn_zephyr_wing_bow.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_origami_crane.png").convert("RGBA")

# Composite body without weapon layer
body_no_weapon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_no_weapon.alpha_composite(key_src)
body_no_weapon.alpha_composite(curio_src)
body_no_weapon.alpha_composite(chassis_src)
body_no_weapon.alpha_composite(head_src)
body_no_weapon.alpha_composite(costume_src)
body_no_weapon.alpha_composite(optic_src)

# Extract raw bow crop
bow_bbox = weapon_src.getbbox()
assert bow_bbox is not None
bow_raw = weapon_src.crop(bow_bbox)

# Extract standardized ground contact shadow
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
assert s_px is not None and c_px is not None

for y in range(116, 126):
    for x in range(128):
        raw_p = c_px[x, y]
        p = cast(tuple[int, int, int, int], raw_p)
        if p[3] > 0 and ((p[0] < 55 and p[1] < 55 and p[2] < 70) or p[3] < 180):
            if y == 124:
                alpha = int(round(p[3] * 0.70))
                s_px[x, y] = (p[0], p[1], p[2], alpha)
            elif y == 125:
                if 50 <= x <= 80 and p[3] > 40:
                    alpha = int(round(p[3] * 0.30))
                    s_px[x, y] = (p[0], p[1], p[2], alpha)
            else:
                s_px[x, y] = p

for y in range(126, 128):
    for x in range(128):
        s_px[x, y] = (0, 0, 0, 0)

EXPECTED_SHADOW = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], s_px[x, y])[3] > 20) for y in range(118, 128)]
print(f"Benchmark ground shadow row counts (118..127): {EXPECTED_SHADOW}")

def enforce_ground_shadow(img: Image.Image) -> Image.Image:
    """Enforce exact ground contact shadow matching baseline Rule 4b-5 without flinching."""
    out = img.copy()
    o_px = out.load()
    assert o_px is not None
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            fp = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20:
                if fp[3] > 20:
                    o_px[x, y] = (0, 0, 0, 0)
            else:  # sp[3] > 20
                if fp[3] <= 20:
                    o_px[x, y] = sp
    # Clean margins strictly (L>=4, R>=4, T>=4, B>=2)
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

def place_bow(bow_img: Image.Image, deg: float, target_grip: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the zephyr wing bow with zero clipping."""
    b = bow_img.copy()
    if mirror:
        b = ImageOps.mirror(b)
    bw, bh = b.size
    gx, gy = (12, 23) if not mirror else (bw - 12, 23)
    
    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    large.paste(b, (128 - gx, 128 - gy))
    
    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        large = large.resize((nw, nh), Image.Resampling.LANCZOS)
        
    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tx, ty = target_grip
    out.paste(rotated, (tx - 128, ty - 128), rotated)
    return out

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

# Anchor corners and borders to maintain stability
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127)
]

base_landmarks = {
    "crest": (65, 22),       # Vermilion pressure valve crest
    "beak": (53, 30),        # Titanium alloy beak clamp
    "head_top": (64, 18),    # Head top stream dome
    "eye": (68, 36),         # Optic eye lens
    "throat": (64, 46),      # Neck accordion ring
    "core": (66, 51),        # Optic core gem
    "shoulder_l": (46, 60),  # Left shoulder / wing joint
    "shoulder_r": (82, 60),  # Right shoulder / wing joint
    "arm_l": (40, 72),       # Left wing blade tip
    "arm_r": (86, 72),       # Right wing blade tip
    "chest": (64, 68),       # Zephyr robe chest plate
    "pelvis": (64, 86),      # Lower chassis
    "hip_l": (52, 94),       # Left hip hinge
    "hip_r": (76, 94),       # Right hip hinge
    "knee_l": (50, 104),     # Left leg knee damper
    "knee_r": (76, 104),     # Right leg knee damper
    "foot_l": (50, 118),     # Left claw foot
    "foot_r": (76, 118),     # Right claw foot
    "key_mount": (39, 43),   # Winding key back mount
    "curio_crane": (24, 33), # Floating origami crane
    "tail_foil": (44, 84),   # Tail feather fold foil
}

def generate_poses():
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (Baseline elegant standing poise, bow held upright at side)
    # =========================================================================
    idle_canvas = body_no_weapon.copy()
    bow_idle = place_bow(bow_raw, deg=0, target_grip=(92, 75), scale=1.0, mirror=False)
    idle_canvas = Image.alpha_composite(idle_canvas, bow_idle)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (Deep Coiled Tension, Drawing String Forward-Down, Aura)
    # =========================================================================
    shifts_telegraph = {
        "crest": (-6, 5), "beak": (-7, 5), "head_top": (-6, 5), "eye": (-6, 5),
        "throat": (-5, 6), "core": (-4, 6), "chest": (-4, 7),
        "shoulder_l": (8, 2), "arm_l": (15, 0),        # Left wing pushes bow strongly forward
        "shoulder_r": (-9, 6), "arm_r": (-16, 8),     # Right wing draws string far back
        "pelvis": (-4, 7), "hip_l": (-7, 7), "hip_r": (2, 7),
        "knee_l": (-9, 7), "knee_r": (3, 6),
        "foot_l": (-6, 1), "foot_r": (2, 0),
        "key_mount": (-4, 6), "curio_crane": (18, -12), "tail_foil": (-5, 6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Bow drawn forward-upwards
    bow_tele = place_bow(bow_raw, deg=-24, target_grip=(98, 68), scale=1.04, mirror=False)

    # Drawn string & condensed wind arrow energy
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Taut bowstring pulled back to draw hand at (70, 76)
    t_draw.line([(94, 44), (70, 76)], fill=(230, 245, 255, 230), width=1)
    t_draw.line([(94, 92), (70, 76)], fill=(230, 245, 255, 230), width=1)
    # Condensed wind arrow shaft and glowing tip
    t_draw.line([(70, 76), (119, 58)], fill=(56, 160, 255, 250), width=2)
    t_draw.line([(72, 76), (118, 58)], fill=(255, 255, 255, 255), width=1)
    t_draw.polygon([(120, 58), (111, 53), (114, 61)], fill=(255, 255, 255, 255))
    # Concentric charging wind rings & suction particles
    t_draw.arc([98, 40, 124, 72], start=90, end=345, fill=(78, 216, 106, 220), width=2)
    t_draw.arc([92, 36, 124, 76], start=110, end=325, fill=(56, 160, 255, 200), width=2)
    t_draw.arc([64, 60, 88, 88], start=20, end=340, fill=(255, 255, 255, 230), width=1)
    t_draw.point([(70, 68), (74, 82), (68, 78), (112, 54), (116, 68), (62, 74), (80, 84)], fill=(255, 208, 40, 250))
    # Trailing wind ribbons behind right elbow
    t_draw.line([(68, 76), (48, 82)], fill=(56, 160, 255, 180), width=2)
    t_draw.line([(66, 78), (44, 86)], fill=(200, 235, 255, 160), width=1)
    # Winding key rapid spin aura
    t_draw.arc([24, 34, 52, 62], start=10, end=350, fill=(255, 208, 40, 220), width=2)
    # Vermilion crest pressure glow
    t_draw.ellipse([52, 16, 70, 34], fill=(255, 94, 138, 190))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.6))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, bow_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (Deep Forward Thrust Piercing Release, Recoil Surge)
    # =========================================================================
    shifts_attack = {
        "crest": (12, 0), "beak": (15, 0), "head_top": (12, 0), "eye": (13, 0),
        "throat": (11, 1), "core": (11, 1), "chest": (11, 1),
        "shoulder_l": (15, 0), "arm_l": (18, -1),   # Left wing lunges far right
        "shoulder_r": (-8, 3), "arm_r": (-16, 5),   # Right arm flings back with elastic snap
        "pelvis": (6, 1), "hip_l": (-6, 1), "hip_r": (10, 1),
        "knee_l": (-10, 1), "knee_r": (12, 0),
        "foot_l": (-10, 0), "foot_r": (12, 0),
        "key_mount": (6, 1), "curio_crane": (-10, -5), "tail_foil": (3, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Bow snapping forward with recoil (stay within right margin <= 123)
    bow_attack = place_bow(bow_raw, deg=-14, target_grip=(104, 68), scale=1.0, mirror=False)

    # Sonic arrow trail & zephyr wind shock rings
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Penetrating supersonic arrow streak
    a_draw.line([(96, 68), (122, 64)], fill=(56, 160, 255, 240), width=4)
    a_draw.line([(98, 68), (123, 64)], fill=(255, 255, 255, 255), width=2)
    # Large sonic pressure cone
    a_draw.arc([98, 50, 116, 82], start=275, end=85, fill=(78, 216, 106, 220), width=3)
    a_draw.arc([106, 48, 122, 80], start=280, end=80, fill=(56, 160, 255, 220), width=2)
    # Back-thrust wind ribbon
    a_draw.line([(40, 72), (18, 76)], fill=(200, 235, 255, 180), width=2)
    a_draw.line([(36, 76), (16, 82)], fill=(56, 160, 255, 160), width=2)
    # Friction sparks
    a_draw.ellipse([98, 64, 106, 72], fill=(255, 255, 220, 255))
    a_draw.point([(108, 60), (105, 74), (114, 62), (109, 70), (118, 58)], fill=(255, 208, 40, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.5))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, bow_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (Tianyuan Zephyr Tempest / Aerial Glide Sniper / Full Wing Blade Spread)
    # =========================================================================
    shifts_skill = {
        "crest": (0, -8), "beak": (0, -8), "head_top": (0, -9), "eye": (0, -8),
        "throat": (0, -8), "core": (0, -7), "chest": (0, -7),
        "shoulder_l": (-10, -9), "arm_l": (-16, -10), # Swept wing blade expansion high left
        "shoulder_r": (10, -9), "arm_r": (16, -8),    # Wing blade expansion high right
        "pelvis": (0, -6), "hip_l": (-3, -6), "hip_r": (3, -6),
        "knee_l": (-4, -7), "knee_r": (4, -7),
        "foot_l": (-3, -7), "foot_r": (3, -7),
        "key_mount": (-1, -7), "curio_crane": (-10, -11), "tail_foil": (0, -5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Overhead celestial sniper bow stance
    bow_skill = place_bow(bow_raw, deg=-38, target_grip=(98, 56), scale=1.06, mirror=False)

    # Tianyuan tempest storm cyclone & swirling feather blade vortex
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    # Swirling tempest vortex arcs
    s_draw.arc([16, 18, 120, 96], start=135, end=355, fill=(56, 160, 255, 200), width=3)
    s_draw.arc([22, 22, 116, 92], start=145, end=335, fill=(78, 216, 106, 230), width=2)
    s_draw.arc([30, 28, 108, 86], start=155, end=315, fill=(255, 255, 255, 240), width=1)
    # Glowing feather blades swirling in the cyclone
    s_draw.polygon([(112, 34), (121, 30), (115, 38)], fill=(255, 255, 255, 255))
    s_draw.polygon([(24, 66), (16, 72), (26, 74)], fill=(56, 160, 255, 230))
    s_draw.polygon([(92, 20), (102, 16), (96, 24)], fill=(78, 216, 106, 230))
    s_draw.polygon([(14, 40), (22, 34), (20, 44)], fill=(255, 208, 40, 240))
    # Updraft wind rings beneath claws
    s_draw.arc([36, 104, 90, 120], start=25, end=155, fill=(200, 235, 255, 190), width=2)
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.7))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, bow_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (Heavy Impact Recoil, Defensive Bow Parry Lock, Exhaust Venting)
    # =========================================================================
    shifts_hit = {
        "crest": (-13, -4), "beak": (-14, -4), "head_top": (-13, -4), "eye": (-13, -4),
        "throat": (-12, -3), "core": (-11, -2), "chest": (-11, -2),
        "shoulder_l": (-9, 0), "arm_l": (-6, 1),     # Left wing shields core
        "shoulder_r": (-9, -1), "arm_r": (-10, -1),   # Right hand locks bow guard
        "pelvis": (-7, 0), "hip_l": (-10, 0), "hip_r": (-5, 0),
        "knee_l": (-11, 0), "knee_r": (-6, 0),
        "foot_l": (-10, 0), "foot_r": (-4, 0),
        "key_mount": (-11, -3), "curio_crane": (-14, 12), "tail_foil": (-8, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Bow diagonally across chest as defensive parry shield
    bow_hit = place_bow(bow_raw, deg=45, target_grip=(68, 64), scale=0.96, mirror=False)

    # Impact sparks & steam vent puffs
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Flash on bow parry guard
    h_draw.ellipse([64, 58, 78, 72], fill=(255, 240, 180, 255))
    h_draw.line([(54, 65), (88, 65)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(71, 48), (71, 82)], fill=(255, 255, 230, 240), width=2)
    h_draw.arc([52, 46, 90, 84], start=0, end=360, fill=(255, 208, 40, 180), width=2)
    # Scattered impact spark dots
    h_draw.point([(56, 54), (82, 52), (86, 74), (58, 78), (78, 84), (60, 48), (84, 80), (66, 86)], fill=(255, 255, 200, 255))
    # Steam puffs from vermilion relief valve and joints
    h_draw.ellipse([34, 20, 48, 34], fill=(230, 245, 255, 190))
    h_draw.ellipse([26, 14, 40, 28], fill=(245, 250, 255, 220))
    h_draw.ellipse([20, 10, 30, 20], fill=(255, 255, 255, 240))
    h_draw.ellipse([46, 46, 60, 60], fill=(230, 240, 250, 170))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.6))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, bow_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (Deep Low Skid Brake, Dampers Re-engaging, Swept Trailing Bow)
    # =========================================================================
    shifts_recover = {
        "crest": (4, 7), "beak": (5, 7), "head_top": (4, 7), "eye": (4, 7),
        "throat": (3, 7), "core": (3, 7), "chest": (3, 7),
        "shoulder_l": (-2, 7), "arm_l": (-5, 6),    # Left wing tucked close
        "shoulder_r": (7, 8), "arm_r": (10, 8),      # Right wing low trailing bow
        "pelvis": (2, 7), "hip_l": (-7, 7), "hip_r": (7, 7),
        "knee_l": (-10, 7), "knee_r": (9, 7),
        "foot_l": (-9, 1), "foot_r": (7, 1),
        "key_mount": (1, 6), "curio_crane": (-4, 8), "tail_foil": (1, 7),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_recover = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Bow trailing low and back
    bow_rec = place_bow(bow_raw, deg=80, target_grip=(84, 90), scale=0.95, mirror=False)

    # Skid spark & friction dust
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Friction sparks under foot
    r_draw.ellipse([86, 110, 98, 118], fill=(255, 208, 40, 220))
    r_draw.line([(82, 114), (102, 114)], fill=(255, 255, 200, 240), width=1)
    r_draw.point([(98, 110), (92, 109), (102, 114), (95, 115), (88, 116), (104, 112)], fill=(255, 255, 200, 250))
    # Soft dust puffs trailing from feet
    r_draw.ellipse([22, 106, 44, 120], fill=(220, 230, 240, 170))
    r_draw.ellipse([34, 108, 54, 122], fill=(230, 240, 250, 150))
    r_draw.ellipse([10, 104, 28, 116], fill=(210, 225, 235, 140))
    r_draw.arc([16, 98, 48, 118], start=120, end=300, fill=(200, 220, 235, 130), width=2)
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.6))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, warped_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, bow_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    poses = generate_poses()
    for name, im in poses.items():
        out_p = f"{OUT_DIR}/{name}.png"
        im.save(out_p, "PNG")
        bbox = im.getbbox()
        h = bbox[3] - bbox[1] if bbox else 0
        w = bbox[2] - bbox[0] if bbox else 0
        print(f"Generated {name:10s} -> {out_p}: bbox={bbox}, w={w}, h={h}")
