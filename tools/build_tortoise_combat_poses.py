#!/usr/bin/env python3
"""
tools/build_tortoise_combat_poses.py
Generates the complete, definitive 6 combat action poses for Xuanji Tortoise (玄機龜, 10th Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/tortoise/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/tortoise/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tortoise"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/tortoise"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_tortoise_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers
chassis_src = Image.open(f"{BASE_DIR}/chassis/paint_tortoise_jade.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_xuanji_tortoise_stock.png").convert("RGBA")
key_src = Image.open(f"{BASE_DIR}/winding_key/key_tai_chi_dual_fish.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_zen_dojo_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/core_amber_quartz.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/wpn_bagua_astrolabe.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_bagua_armillary_rings.png").convert("RGBA")

# Composite body without weapon layer
body_no_weapon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_no_weapon.alpha_composite(key_src)
body_no_weapon.alpha_composite(curio_src)
body_no_weapon.alpha_composite(chassis_src)
body_no_weapon.alpha_composite(head_src)
body_no_weapon.alpha_composite(costume_src)
body_no_weapon.alpha_composite(optic_src)

# Extract raw astrolabe crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
astrolabe_raw = weapon_src.crop(wpn_bbox)

# Standardized ground contact shadow from baseline composite
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
assert s_px is not None and c_px is not None

for y in range(118, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p
        else:
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

def place_astrolabe(astrolabe_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the Bagua astrolabe with zero clipping."""
    b = astrolabe_img.copy()
    if mirror:
        b = ImageOps.mirror(b)
    bw, bh = b.size
    gx, gy = bw / 2.0, bh / 2.0
    
    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    large.paste(b, (int(round(128 - gx)), int(round(128 - gy))))
    
    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        scaled = large.resize((nw, nh), Image.Resampling.LANCZOS)
        offset = (nw - canvas_size) // 2
        large = scaled.crop((offset, offset, offset + canvas_size, offset + canvas_size))
        
    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tx, ty = target_center
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

# Anchor corners and borders for IDW
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127)
]

base_landmarks = {
    "head_top": (64, 26),
    "eye_l": (56, 38),
    "eye_r": (72, 38),
    "snout": (64, 48),
    "throat": (64, 54),
    "core": (63, 62),
    "shoulder_l": (36, 68),
    "shoulder_r": (82, 68),
    "arm_l": (30, 78),
    "arm_r": (88, 76),
    "torso": (64, 76),
    "pelvis": (64, 88),
    "hip_l": (46, 96),
    "hip_r": (78, 96),
    "knee_l": (46, 108),
    "knee_r": (80, 108),
    "foot_l": (48, 118),
    "foot_r": (80, 118),
    "key_mount": (32, 38),
    "key_wing": (20, 28),
    "curio_top": (22, 54),
    "curio_mid": (16, 78),
    "curio_bot": (20, 102),
}

def generate_poses():
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (Baseline stable poise, astrolabe held in right hand)
    # =========================================================================
    idle_canvas = body_no_weapon.copy()
    ast_idle = place_astrolabe(astrolabe_raw, deg=0, target_center=(96, 62), scale=1.0, mirror=False)
    idle_canvas = Image.alpha_composite(idle_canvas, ast_idle)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (渾天氣象蓄勁 Bagua Energy Convergence)
    # Deep coiled crouch, shell lowering, astrolabe drawn back with charging trigrams
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-5, 6), "eye_l": (-5, 6), "eye_r": (-5, 6),
        "snout": (-5, 6), "throat": (-4, 7), "core": (-4, 7),
        "shoulder_l": (6, 4), "arm_l": (14, 2),        # Left arm braces forward
        "shoulder_r": (-8, 6), "arm_r": (-14, 7),      # Right arm coils back
        "torso": (-4, 7), "pelvis": (-4, 7),
        "hip_l": (-7, 7), "hip_r": (3, 6),
        "knee_l": (-9, 6), "knee_r": (4, 5),
        "foot_l": (-5, 1), "foot_r": (3, 0),
        "key_mount": (-4, 6), "key_wing": (-5, 5),
        "curio_top": (10, -6), "curio_mid": (12, -4), "curio_bot": (8, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Astrolabe drawn back and angled
    ast_tele = place_astrolabe(astrolabe_raw, deg=32, target_center=(84, 68), scale=1.04, mirror=False)

    # Charging celestial trigram FX & suction particles
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Concentric charging cosmic rings around astrolabe
    t_draw.arc([66, 50, 102, 86], start=45, end=330, fill=(255, 208, 40, 230), width=2)
    t_draw.arc([62, 46, 106, 90], start=60, end=310, fill=(56, 160, 255, 210), width=2)
    t_draw.arc([70, 54, 98, 82], start=20, end=340, fill=(78, 216, 106, 220), width=1)
    # Constellation spark points & suction motes
    t_draw.point([(84, 52), (88, 84), (72, 68), (96, 68), (68, 56), (100, 78), (76, 82), (92, 54)], fill=(255, 255, 255, 255))
    t_draw.line([(84, 52), (100, 78)], fill=(56, 160, 255, 160), width=1)
    t_draw.line([(68, 56), (92, 54)], fill=(255, 208, 40, 180), width=1)
    # Winding key rapid spin aura
    t_draw.arc([16, 22, 38, 44], start=10, end=350, fill=(255, 208, 40, 200), width=2)
    # Chest gem intense amber pulse
    t_draw.ellipse([55, 65, 67, 77], fill=(255, 160, 16, 180))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.6))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, ast_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (玄機星宿推演破陣 Celestial Astrolabe Burst)
    # Dynamic forward lunge, arm extending forward, projectile shockwave
    # =========================================================================
    shifts_attack = {
        "head_top": (10, 0), "eye_l": (11, 0), "eye_r": (11, 0),
        "snout": (13, 0), "throat": (11, 1), "core": (10, 1),
        "shoulder_l": (-7, 2), "arm_l": (-13, 4),      # Left arm flings back
        "shoulder_r": (12, 0), "arm_r": (17, -1),      # Right arm thrusts forward
        "torso": (8, 1), "pelvis": (6, 1),
        "hip_l": (-6, 1), "hip_r": (10, 1),
        "knee_l": (-9, 1), "knee_r": (12, 0),
        "foot_l": (-8, 0), "foot_r": (10, 0),
        "key_mount": (6, 1), "key_wing": (4, 1),
        "curio_top": (-8, -4), "curio_mid": (-6, 0), "curio_bot": (-4, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Astrolabe thrust forward-right (within right margin <= 123)
    ast_attack = place_astrolabe(astrolabe_raw, deg=-24, target_center=(103, 61), scale=1.02, mirror=False)

    # Piercing celestial shockwave & kinetic particles
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Supersonic starburst stream
    a_draw.line([(96, 61), (122, 59)], fill=(56, 160, 255, 240), width=3)
    a_draw.line([(98, 61), (123, 59)], fill=(255, 255, 255, 255), width=1)
    # Expanding kinetic pressure arc in front of astrolabe
    a_draw.arc([100, 47, 120, 75], start=275, end=85, fill=(78, 216, 106, 220), width=2)
    a_draw.arc([106, 45, 122, 77], start=280, end=80, fill=(255, 208, 40, 230), width=2)
    # Back-thrust wind ripples behind shell
    a_draw.line([(32, 74), (14, 78)], fill=(200, 235, 255, 170), width=2)
    a_draw.line([(28, 78), (12, 84)], fill=(56, 160, 255, 150), width=2)
    # Starlight friction sparks
    a_draw.ellipse([98, 57, 106, 65], fill=(255, 255, 220, 255))
    a_draw.point([(108, 53), (105, 69), (114, 55), (109, 65), (118, 53)], fill=(255, 208, 40, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.5))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, ast_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (八卦太極渾天巨陣 Grand Bagua Tai Chi Formation)
    # Elevated channeling pose, astrolabe held high, grand celestial rune rings
    # =========================================================================
    shifts_skill = {
        "head_top": (0, -4), "eye_l": (0, -4), "eye_r": (0, -4),
        "snout": (0, -3), "throat": (0, -3), "core": (0, -2),
        "shoulder_l": (-10, -4), "arm_l": (-16, -5),  # Swept wide
        "shoulder_r": (10, -4), "arm_r": (16, -3),
        "torso": (0, -2), "pelvis": (0, -1),
        "hip_l": (-4, -1), "hip_r": (4, -1),
        "knee_l": (-5, -1), "knee_r": (5, -1),
        "foot_l": (-4, 0), "foot_r": (4, 0),
        "key_mount": (-1, 0), "key_wing": (-2, 0),
        "curio_top": (-10, -4), "curio_mid": (-12, -2), "curio_bot": (-8, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Overhead celestial channeling astrolabe
    ast_skill = place_astrolabe(astrolabe_raw, deg=45, target_center=(96, 46), scale=1.06, mirror=False)

    # Grand Bagua cosmic array & swirling star rune vortex (kept at y>=16 for Rule 4b-9)
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    # Outer celestial orbit ring
    s_draw.arc([14, 22, 122, 104], start=135, end=355, fill=(56, 160, 255, 210), width=3)
    s_draw.arc([20, 26, 116, 98], start=145, end=335, fill=(78, 216, 106, 230), width=2)
    s_draw.arc([28, 30, 108, 92], start=155, end=315, fill=(255, 208, 40, 240), width=1)
    # Celestial Bagua star runes
    s_draw.polygon([(112, 34), (120, 30), (114, 38)], fill=(255, 255, 255, 255))
    s_draw.polygon([(22, 66), (14, 72), (24, 74)], fill=(56, 160, 255, 230))
    s_draw.polygon([(92, 22), (100, 18), (94, 26)], fill=(78, 216, 106, 230))
    s_draw.polygon([(16, 40), (24, 34), (22, 44)], fill=(255, 208, 40, 240))
    # Ground rising mana waves
    s_draw.arc([34, 102, 92, 120], start=25, end=155, fill=(200, 235, 255, 190), width=2)
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.7))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, ast_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (重甲受創防禦震退 Iron Shell Impact Recoil)
    # Head retreats into collar, torso recoils back, astrolabe parry guard
    # =========================================================================
    shifts_hit = {
        "head_top": (-12, 1), "eye_l": (-12, 1), "eye_r": (-12, 1),
        "snout": (-11, 2), "throat": (-10, 2), "core": (-9, 2),
        "shoulder_l": (-8, 2), "arm_l": (-5, 3),       # Tucked in defensive
        "shoulder_r": (-8, 1), "arm_r": (-8, 1),       # Locks astrolabe guard
        "torso": (-8, 2), "pelvis": (-7, 2),
        "hip_l": (-10, 2), "hip_r": (-5, 2),
        "knee_l": (-11, 1), "knee_r": (-6, 1),
        "foot_l": (-9, 0), "foot_r": (-4, 0),
        "key_mount": (-10, 1), "key_wing": (-10, 1),
        "curio_top": (-14, 10), "curio_mid": (-12, 8), "curio_bot": (-8, 4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Astrolabe held diagonally across chest as defensive parry shield
    ast_hit = place_astrolabe(astrolabe_raw, deg=36, target_center=(70, 64), scale=0.96, mirror=False)

    # Impact spark flash & exhaust steam vents (steam vents calibrated y>=18)
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Shield parry flash at impact center
    h_draw.ellipse([64, 58, 78, 72], fill=(255, 240, 180, 255))
    h_draw.line([(54, 65), (88, 65)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(71, 48), (71, 82)], fill=(255, 255, 230, 240), width=2)
    h_draw.arc([52, 46, 90, 84], start=0, end=360, fill=(255, 208, 40, 180), width=2)
    # Scattered impact deflection sparks
    h_draw.point([(56, 54), (82, 52), (86, 74), (58, 78), (78, 84), (60, 48), (84, 80), (66, 86)], fill=(255, 255, 200, 255))
    # Steam puffs from shell relief valve and joints
    h_draw.ellipse([32, 26, 46, 40], fill=(230, 245, 255, 190))
    h_draw.ellipse([24, 20, 36, 32], fill=(245, 250, 255, 220))
    h_draw.ellipse([18, 18, 28, 28], fill=(255, 255, 255, 240))
    h_draw.ellipse([44, 50, 58, 64], fill=(230, 240, 250, 170))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.6))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, ast_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (定軍重整乾坤復位 Bulwark Stabilization & Reset)
    # Grounded recovery, solid stance, astrolabe held at ready waist guard
    # =========================================================================
    shifts_recover = {
        "head_top": (3, 4), "eye_l": (3, 4), "eye_r": (3, 4),
        "snout": (3, 4), "throat": (3, 5), "core": (3, 5),
        "shoulder_l": (-5, 5), "arm_l": (-10, 6),
        "shoulder_r": (6, 5), "arm_r": (8, 6),
        "torso": (3, 5), "pelvis": (3, 5),
        "hip_l": (-6, 5), "hip_r": (7, 5),
        "knee_l": (-8, 4), "knee_r": (8, 4),
        "foot_l": (-5, 1), "foot_r": (7, 1),
        "key_mount": (3, 4), "key_wing": (3, 4),
        "curio_top": (5, 4), "curio_mid": (5, 4), "curio_bot": (5, 4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_recover = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Astrolabe held firmly at side-waist with pronounced angle
    ast_recover = place_astrolabe(astrolabe_raw, deg=-22, target_center=(90, 73), scale=0.98, mirror=False)

    # Reset steam puffs & soft stabilizing aura
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Settling energy ripples at ground
    r_draw.arc([36, 108, 92, 124], start=10, end=170, fill=(56, 160, 255, 180), width=2)
    r_draw.arc([42, 112, 86, 126], start=20, end=160, fill=(78, 216, 106, 160), width=1)
    # Cooling steam puffs from shell exhausts and joints
    r_draw.ellipse([24, 44, 38, 58], fill=(230, 240, 250, 170))
    r_draw.ellipse([18, 38, 30, 50], fill=(240, 245, 255, 190))
    r_draw.ellipse([86, 74, 98, 86], fill=(230, 240, 250, 160))
    r_draw.ellipse([76, 82, 88, 94], fill=(240, 245, 255, 150))
    # Calming amber pulse at core
    r_draw.ellipse([58, 65, 70, 77], fill=(255, 208, 40, 160))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.6))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, warped_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, ast_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING XUANJI TORTOISE 6 COMBAT ACTION POSES ===")
    poses = generate_poses()

    for p_name, img in poses.items():
        dst_128 = os.path.join(OUT_DIR, f"{p_name}.png")
        img.save(dst_128, format="PNG")
        
        # 512 LANCZOS upscale
        dst_512 = os.path.join(OUT_DIR, f"{p_name}_512.png")
        img_512 = img.resize((512, 512), resample=Image.Resampling.LANCZOS)
        img_512.save(dst_512, format="PNG")
        
        bbox = img.getbbox()
        print(f"✓ Saved {p_name:10s} -> {dst_128} (128x128, bbox={bbox}) and {dst_512} (512x512)")

    # Generate proof sheets
    # 1. 640-wide strip (all 6 poses in a row: 128 x 6 = 768 or with padding)
    pose_order = ["idle", "telegraph", "attack", "skill", "hit", "recover"]
    strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    for i, p_name in enumerate(pose_order):
        strip.paste(poses[p_name], (i * 128, 0))
    
    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_tortoise_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    # 2. Magenta background proof sheet
    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_tortoise_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
    print("\nAll 6 combat poses successfully generated and saved!")
