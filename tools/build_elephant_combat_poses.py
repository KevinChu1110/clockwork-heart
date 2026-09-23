#!/usr/bin/env python3
"""
tools/build_elephant_combat_poses.py
Generates the complete, definitive 6 combat action poses for Colossus Elephant (鋼岳象, 11th Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/elephant/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/elephant/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/elephant"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/elephant"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_elephant_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers
chassis_src = Image.open(f"{BASE_DIR}/chassis/paint_elephant_brass.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_colossus_elephant_stock.png").convert("RGBA")
key_src = Image.open(f"{BASE_DIR}/winding_key/key_heavy_cross_wheel.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_cog_workshop_overalls.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/core_sky_quartz.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/wpn_colossus_cleaver_axe.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_dual_pressure_gauge.png").convert("RGBA")

# Composite body without weapon layer
body_no_weapon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_no_weapon.alpha_composite(key_src)
body_no_weapon.alpha_composite(curio_src)
body_no_weapon.alpha_composite(chassis_src)
body_no_weapon.alpha_composite(head_src)
body_no_weapon.alpha_composite(costume_src)
body_no_weapon.alpha_composite(optic_src)

# Extract raw axe crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
axe_raw = weapon_src.crop(wpn_bbox)

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

def place_axe(axe_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the Colossus Cleaver Axe with zero clipping."""
    b = axe_img.copy()
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
    "head_top": (64, 24),
    "eye_l": (54, 45),
    "eye_r": (72, 45),
    "snout": (64, 52),
    "trunk_tip": (58, 80),
    "ear_l": (30, 48),
    "ear_r": (92, 48),
    "throat": (64, 52),
    "core": (63, 70),
    "shoulder_l": (38, 66),
    "shoulder_r": (82, 66),
    "arm_l": (38, 80),
    "arm_r": (80, 78),
    "torso": (62, 78),
    "pelvis": (62, 88),
    "hip_l": (46, 94),
    "hip_r": (76, 94),
    "knee_l": (46, 104),
    "knee_r": (76, 104),
    "foot_l": (46, 114),
    "foot_r": (76, 114),
    "key_mount": (34, 38),
    "key_wing": (26, 24),
    "curio_top": (22, 54),
    "curio_mid": (20, 78),
    "curio_bot": (22, 102),
}

def generate_poses():
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (Baseline stable poise, axe held in right hand)
    # =========================================================================
    idle_canvas = body_no_weapon.copy()
    axe_idle = place_axe(axe_raw, deg=0, target_center=(96, 71), scale=1.0, mirror=False)
    idle_canvas = Image.alpha_composite(idle_canvas, axe_idle)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (飛輪重斧引力蓄勁 Axe Prime & Steam Compression)
    # Deep coiled crouch, trunk curled back inhaling, axe raised overhead, steam compression
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-4, 5), "eye_l": (-4, 5), "eye_r": (-4, 5),
        "snout": (-4, 5), "trunk_tip": (-8, 1),        # Trunk curls back inhaling
        "ear_l": (-7, 4), "ear_r": (-1, 5),
        "throat": (-3, 6), "core": (-3, 6),
        "shoulder_l": (4, 4), "arm_l": (10, 2),        # Left arm braces forward
        "shoulder_r": (-6, 5), "arm_r": (-10, -2),     # Right arm raises to grip
        "torso": (-3, 6), "pelvis": (-3, 6),
        "hip_l": (-5, 6), "hip_r": (2, 5),
        "knee_l": (-6, 5), "knee_r": (3, 4),
        "foot_l": (-4, 1), "foot_r": (2, 0),
        "key_mount": (-3, 5), "key_wing": (-4, 4),
        "curio_top": (6, -4), "curio_mid": (8, -2), "curio_bot": (6, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Axe raised high and angled backward overhead
    axe_tele = place_axe(axe_raw, deg=36, target_center=(82, 52), scale=1.04, mirror=False)

    # High pressure steam compression rings & spinning gear spark FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Concentric charging steam arcs around axe gear
    t_draw.arc([64, 34, 100, 70], start=45, end=330, fill=(255, 208, 40, 230), width=2)
    t_draw.arc([60, 30, 104, 74], start=60, end=310, fill=(255, 160, 16, 210), width=2)
    t_draw.arc([68, 38, 96, 66], start=20, end=340, fill=(56, 160, 255, 220), width=1)
    # Spinning gear teeth sparks
    t_draw.point([(82, 36), (86, 68), (70, 52), (94, 52), (66, 40), (98, 62), (74, 66), (90, 38)], fill=(255, 255, 255, 255))
    t_draw.line([(82, 36), (98, 62)], fill=(255, 208, 40, 160), width=1)
    t_draw.line([(66, 40), (90, 38)], fill=(255, 160, 16, 180), width=1)
    # Heavy cross key rapid spin aura
    t_draw.arc([16, 16, 36, 36], start=10, end=350, fill=(255, 208, 40, 200), width=2)
    # Chest gem cyan pulse
    t_draw.ellipse([57, 73, 69, 85], fill=(56, 160, 255, 180))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.6))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, axe_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (開山碎嶽劈裂 Mountain Cleave & Shockwave)
    # Massive downward cleave forward, trunk blasting steam jet, ground impact spark
    # =========================================================================
    shifts_attack = {
        "head_top": (8, 2), "eye_l": (9, 2), "eye_r": (9, 2),
        "snout": (11, 3), "trunk_tip": (16, 5),        # Trunk extends forward blasting steam
        "ear_l": (4, 1), "ear_r": (12, 2),
        "throat": (9, 3), "core": (8, 3),
        "shoulder_l": (-6, 3), "arm_l": (-11, 5),      # Left arm flings back
        "shoulder_r": (10, 2), "arm_r": (14, 5),       # Right arm chops down
        "torso": (7, 3), "pelvis": (5, 2),
        "hip_l": (-5, 2), "hip_r": (8, 2),
        "knee_l": (-7, 2), "knee_r": (10, 1),
        "foot_l": (-6, 0), "foot_r": (8, 0),
        "key_mount": (5, 2), "key_wing": (3, 2),
        "curio_top": (-6, -2), "curio_mid": (-5, 1), "curio_bot": (-3, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Axe slammed downward-forward (margins: right <= 123)
    axe_attack = place_axe(axe_raw, deg=-32, target_center=(98, 76), scale=1.04, mirror=False)

    # Cleave impact shockwave & supersonic steam jet FX
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Supersonic steam blast from trunk
    a_draw.line([(74, 85), (105, 90)], fill=(240, 248, 255, 240), width=3)
    a_draw.line([(76, 85), (107, 90)], fill=(255, 255, 255, 255), width=1)
    # Slicing golden impact arc in front of axe blade
    a_draw.arc([88, 54, 122, 102], start=280, end=80, fill=(255, 208, 40, 240), width=3)
    a_draw.arc([92, 58, 122, 98], start=290, end=70, fill=(255, 255, 255, 255), width=1)
    # Ground fissure shockwave ripples
    a_draw.line([(90, 114), (116, 114)], fill=(255, 160, 16, 230), width=2)
    a_draw.line([(96, 116), (120, 116)], fill=(255, 208, 40, 210), width=1)
    # High-heat impact sparks
    a_draw.ellipse([96, 72, 104, 80], fill=(255, 255, 220, 255))
    a_draw.point([(106, 68), (103, 84), (112, 70), (107, 80), (116, 68)], fill=(255, 208, 40, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.5))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, axe_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (巨輪天崩地裂斬 Grand Colossus Quake Overdrive)
    # Elevated leap step, axe rotating overhead 360 whirlwind strike, erupting gears
    # =========================================================================
    shifts_skill = {
        "head_top": (0, -4), "eye_l": (0, -4), "eye_r": (0, -4),
        "snout": (0, -3), "trunk_tip": (2, -5),        # Trunk trumpeting high
        "ear_l": (-6, -4), "ear_r": (6, -4),          # Ears flared wide
        "throat": (0, -3), "core": (0, -2),
        "shoulder_l": (-8, -4), "arm_l": (-14, -5),   # Arms swept wide
        "shoulder_r": (8, -4), "arm_r": (14, -4),
        "torso": (0, -2), "pelvis": (0, -1),
        "hip_l": (-4, -1), "hip_r": (4, -1),
        "knee_l": (-5, -1), "knee_r": (5, -1),
        "foot_l": (-4, 0), "foot_r": (4, 0),
        "key_mount": (-1, 0), "key_wing": (-2, 0),
        "curio_top": (-8, -4), "curio_mid": (-10, -2), "curio_bot": (-6, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Overhead whirlwind overdrive axe
    axe_skill = place_axe(axe_raw, deg=-72, target_center=(88, 48), scale=1.06, mirror=False)

    # Grand golden overdrive vortex & flying gear particles
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    # Outer 360 golden overdrive slash vortex (y>=16 for Rule 4b-9)
    s_draw.arc([16, 20, 118, 96], start=140, end=355, fill=(255, 208, 40, 230), width=3)
    s_draw.arc([22, 26, 112, 90], start=160, end=340, fill=(255, 160, 16, 200), width=2)
    s_draw.arc([28, 32, 106, 84], start=180, end=320, fill=(56, 160, 255, 210), width=1)
    # Erupting golden gear motes
    s_draw.point([(88, 26), (72, 34), (104, 38), (42, 54), (106, 68), (32, 68)], fill=(255, 255, 255, 255))
    s_draw.ellipse([84, 22, 92, 30], fill=(255, 208, 40, 220))
    s_draw.ellipse([68, 30, 76, 38], fill=(255, 160, 16, 200))
    s_draw.ellipse([100, 34, 108, 42], fill=(255, 208, 40, 220))
    # Ground quake fracture line
    s_draw.line([(32, 114), (96, 114)], fill=(255, 208, 40, 220), width=2)
    s_draw.line([(40, 116), (88, 116)], fill=(255, 160, 16, 180), width=1)
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.6))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, axe_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (四柱活塞抗壓減震 Hydraulic Piston Absorber)
    # Low-center impact absorption, ears clamped inward, axe held in parry guard, steam venting
    # =========================================================================
    shifts_hit = {
        "head_top": (-8, 2), "eye_l": (-8, 2), "eye_r": (-8, 2),
        "snout": (-7, 3), "trunk_tip": (-4, 2),        # Trunk retreats slightly
        "ear_l": (4, 1), "ear_r": (-4, 1),             # Ears clamp forward defensively
        "throat": (-6, 3), "core": (-6, 3),
        "shoulder_l": (-5, 3), "arm_l": (-2, 4),       # Arms tuck into defensive guard
        "shoulder_r": (-5, 2), "arm_r": (-5, 2),
        "torso": (-5, 3), "pelvis": (-4, 3),
        "hip_l": (-7, 3), "hip_r": (-3, 3),
        "knee_l": (-8, 2), "knee_r": (-4, 2),
        "foot_l": (-6, 0), "foot_r": (-2, 0),
        "key_mount": (-7, 2), "key_wing": (-7, 2),
        "curio_top": (-10, 8), "curio_mid": (-9, 6), "curio_bot": (-6, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Axe held diagonally across chest in defensive parry guard
    axe_hit = place_axe(axe_raw, deg=28, target_center=(74, 68), scale=0.98, mirror=False)

    # Deflection spark flash & exhaust steam vents
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Parry flash at weapon blade/haft
    h_draw.ellipse([68, 62, 82, 76], fill=(255, 240, 180, 255))
    h_draw.line([(58, 69), (92, 69)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(75, 52), (75, 86)], fill=(255, 255, 230, 240), width=2)
    h_draw.arc([56, 50, 94, 88], start=0, end=360, fill=(255, 208, 40, 180), width=2)
    # Deflected iron sparks
    h_draw.point([(60, 58), (86, 56), (90, 78), (62, 82), (82, 88), (64, 52), (88, 84), (70, 90)], fill=(255, 255, 200, 255))
    # Steam puffs from relief valve (y>=18)
    h_draw.ellipse([26, 24, 40, 38], fill=(230, 245, 255, 190))
    h_draw.ellipse([20, 20, 30, 30], fill=(245, 250, 255, 220))
    h_draw.ellipse([16, 18, 24, 26], fill=(255, 255, 255, 240))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.6))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, axe_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (液壓回穩復位 Hydraulic Stance Reset)
    # Steady grounded reset, ear plates re-opening, trunk reaching forward gracefully
    # =========================================================================
    shifts_recover = {
        "head_top": (2, 3), "eye_l": (2, 3), "eye_r": (2, 3),
        "snout": (2, 3), "trunk_tip": (3, 3),
        "ear_l": (-3, 3), "ear_r": (4, 3),
        "throat": (2, 4), "core": (2, 4),
        "shoulder_l": (-4, 4), "arm_l": (-8, 5),
        "shoulder_r": (4, 4), "arm_r": (6, 5),
        "torso": (2, 4), "pelvis": (2, 4),
        "hip_l": (-4, 4), "hip_r": (5, 4),
        "knee_l": (-6, 3), "knee_r": (6, 3),
        "foot_l": (-4, 1), "foot_r": (5, 1),
        "key_mount": (2, 3), "key_wing": (2, 3),
        "curio_top": (3, 3), "curio_mid": (3, 3), "curio_bot": (3, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_recover = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Axe held firmly at ready waist position
    axe_recover = place_axe(axe_raw, deg=-15, target_center=(92, 75), scale=1.0, mirror=False)

    # Cooling steam puffs & grounding recovery ripples
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Ground energy ripples
    r_draw.arc([36, 108, 92, 124], start=10, end=170, fill=(56, 160, 255, 180), width=2)
    r_draw.arc([42, 112, 86, 126], start=20, end=160, fill=(78, 216, 106, 160), width=1)
    # Cooling steam puffs from hydraulic pistons
    r_draw.ellipse([26, 42, 38, 54], fill=(230, 240, 250, 170))
    r_draw.ellipse([20, 36, 30, 46], fill=(240, 245, 255, 190))
    r_draw.ellipse([88, 76, 98, 86], fill=(230, 240, 250, 160))
    r_draw.ellipse([80, 84, 90, 94], fill=(240, 245, 255, 150))
    # Soft blue pulse at core
    r_draw.ellipse([60, 71, 68, 79], fill=(56, 160, 255, 160))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.6))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, warped_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, axe_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING COLOSSUS ELEPHANT 6 COMBAT ACTION POSES ===")
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
    # 1. 768-wide strip (all 6 poses in a row: 128 x 6 = 768)
    pose_order = ["idle", "telegraph", "attack", "skill", "hit", "recover"]
    strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    for i, p_name in enumerate(pose_order):
        strip.paste(poses[p_name], (i * 128, 0))

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_elephant_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    # 2. Magenta background proof sheet
    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_elephant_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")

    print("\n✓ ALL 6 COMBAT POSES SUCCESSFULLY GENERATED FOR COLOSSUS ELEPHANT!")
