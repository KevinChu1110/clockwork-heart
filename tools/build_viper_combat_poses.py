#!/usr/bin/env python3
"""
tools/build_viper_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Bamboo Viper (第二十七族 竹影青蛇, viper)
in Clockwork Heart:
  game/assets/sprites/player/poses/viper/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/viper/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/viper"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/viper"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_viper_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_viper_bamboo_leaf_fan.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_viper_articulated_bamboo_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_viper_bamboo_lacquer_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_viper_carved_bamboo_crest_hood.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_viper_zen_dojo_shinobi_wrap.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_viper_emerald_glass_optic.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_viper_gale_bamboo_dagger.png").convert("RGBA")

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Extract raw curio crop
curio_bbox = curio_src.getbbox()
assert curio_bbox is not None
curio_raw = curio_src.crop(curio_bbox)

# Standardized ground contact shadow from cleaned baseline composite
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
assert s_px is not None and c_px is not None

# Clean baseline shadow to guarantee Rule 4c-5 / 16 (L>=4, T>=4, R>=4, B>=2)
for y in range(118, 126):  # up to 125, y=126 and 127 are 0
    for x in range(4, 124):
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
    s_pixels = shadow_master.load()
    assert o_px is not None and s_pixels is not None

    # Strictly set shadow zone (118..127) to baseline shadow pixels
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_pixels[x, y])
            fp = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20:
                if fp[3] > 20:
                    o_px[x, y] = (0, 0, 0, 0)
            else:
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

    # Sanitize any interpolation dark falloff pixels to canon outline (31, 26, 58)
    arr = np.array(out)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    bad_dark = (alpha > 30) & (rgb[:, :, 0] < 12) & (rgb[:, :, 1] < 12) & (rgb[:, :, 2] < 12)
    if np.any(bad_dark):
        arr[bad_dark, 0] = 31
        arr[bad_dark, 1] = 26
        arr[bad_dark, 2] = 58
        out = Image.fromarray(arr)

    return out


def place_rotated_element(elem_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places any element with precision."""
    b = elem_img.copy()
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
    "head_top": (64, 14),
    "hat_rim_l": (34, 30),
    "hat_rim_r": (94, 30),
    "ear_pivot_l": (40, 42),
    "ear_pivot_r": (88, 42),
    "eye_l": (52, 40),
    "eye_r": (76, 40),
    "snout": (64, 48),
    "jaw": (64, 54),
    "throat": (64, 58),
    "core": (62, 70),
    "shoulder_l": (44, 62),
    "shoulder_r": (78, 62),
    "arm_l": (38, 78),
    "arm_r": (82, 74),
    "torso": (62, 76),
    "belt_buckle": (62, 83),
    "pelvis": (62, 92),
    "foot_l": (48, 112),
    "foot_r": (70, 112),
    "tail_seg1": (52, 88),
    "tail_seg3": (36, 98),
    "tail_seg5": (22, 105),
    "tail_tip": (14, 112),
    "key_mount": (64, 58),
}

# Base body without weapon and winding key (for dynamic key & weapon animation)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (靈巧蛇行盤伏姿態 / Bamboo Viper Coiled Idle)
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (預警起手 / 弓身蓄簧看破姿態 Spring Coil Windup)
    # Body compresses downward & slightly left (y+5, x-3), neck & snout tilt down.
    # Winding key torqued counter-clockwise (-25 deg, target (82, 38)).
    # Dagger drawn close to chest (-20 deg, target (80, 72), scale 1.02).
    # Targeting emerald trajectory ray, reticle & Dopamine gold energy rings.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-3, 6), "hat_rim_l": (-4, 5), "hat_rim_r": (-2, 5),
        "ear_pivot_l": (-4, 5), "ear_pivot_r": (-2, 5),
        "eye_l": (-3, 6), "eye_r": (-3, 6),
        "snout": (-3, 6), "jaw": (-3, 6), "throat": (-3, 5),
        "core": (-3, 5),
        "shoulder_l": (-4, 4), "shoulder_r": (-3, 4),
        "arm_l": (-2, 4), "arm_r": (-5, 3),
        "torso": (-2, 5), "belt_buckle": (-2, 5), "pelvis": (-2, 4),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_seg1": (-3, 4), "tail_seg3": (-4, 3), "tail_seg5": (-2, 2), "tail_tip": (0, 0),
        "key_mount": (-3, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_tele = place_rotated_element(key_raw, deg=-25, target_center=(82, 38), scale=1.0)
    dagger_tele = place_rotated_element(weapon_raw, deg=-20, target_center=(80, 72), scale=1.02)

    # Optic trajectory beams & bamboo energy charging rings
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Concentric charging rings around dagger guard
    t_draw.arc([72, 64, 94, 86], start=0, end=360, fill=(78, 216, 106, 200), width=1)
    t_draw.arc([75, 67, 91, 83], start=0, end=360, fill=(255, 208, 40, 220), width=1)
    # Targeting trajectory beam towards target point (112, 66)
    t_draw.line([(86, 75), (116, 65)], fill=(78, 216, 106, 220), width=1)
    t_draw.line([(92, 73), (118, 64)], fill=(255, 208, 40, 230), width=2)
    t_draw.line([(98, 70), (120, 63)], fill=(255, 255, 255, 255), width=1)
    # Crosshair reticle at target point (112, 65)
    cx, cy = 112, 65
    t_draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=(78, 216, 106, 220), width=1)
    t_draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], outline=(255, 208, 40, 230), width=1)
    t_draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(78, 216, 106, 240), width=1)
    t_draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(78, 216, 106, 240), width=1)
    # Bamboo energy glints & eye focus
    for gx, gy in [(40, 56), (36, 70), (96, 52), (102, 76)]:
        t_draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(175, 250, 190, 180), outline=(78, 216, 106, 220))
    t_draw.ellipse([50, 44, 54, 48], fill=(255, 255, 255, 255))
    t_draw.ellipse([74, 44, 78, 48], fill=(255, 255, 255, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, dagger_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (普攻 / 疾風竹影突刺姿態 Gale Bamboo Shadow Thrust)
    # Dynamic forward lunge: torso & head rock forward (+11, -1), right arm extends (+15, -2)!
    # Dagger thrusts forward (+24 deg, target (102, 76), scale 1.08).
    # Winding key spins forward (+38 deg, target (92, 30)).
    # Crescent emerald wind-cutter slash arc, supersonic tip trail & Dopamine gold sparks.
    # =========================================================================
    shifts_attack = {
        "head_top": (10, -1), "hat_rim_l": (9, -2), "hat_rim_r": (11, -1),
        "ear_pivot_l": (9, -1), "ear_pivot_r": (11, -1),
        "eye_l": (10, -1), "eye_r": (10, -1),
        "snout": (11, 0), "jaw": (10, 0), "throat": (9, 0),
        "core": (9, 0),
        "shoulder_l": (10, 0), "shoulder_r": (7, 0),
        "arm_l": (12, -2), "arm_r": (15, -2),
        "torso": (8, 0), "belt_buckle": (7, 0), "pelvis": (6, 0),
        "foot_l": (5, 0), "foot_r": (-4, 0),
        "tail_seg1": (5, -1), "tail_seg3": (2, -1), "tail_seg5": (0, 0), "tail_tip": (0, 0),
        "key_mount": (8, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=38, target_center=(92, 30), scale=1.0)
    dagger_attack = place_rotated_element(weapon_raw, deg=24, target_center=(102, 76), scale=1.08)

    # Emerald wind cutter slash arc & kinetic sparks
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Curved bamboo wind blade slash arc
    a_draw.arc([74, 50, 122, 98], start=280, end=75, fill=(78, 216, 106, 245), width=3)
    a_draw.arc([78, 54, 120, 94], start=290, end=65, fill=(255, 208, 40, 230), width=2)
    a_draw.arc([82, 58, 118, 90], start=300, end=55, fill=(255, 255, 255, 255), width=1)
    a_draw.line([(88, 76), (122, 72)], fill=(78, 216, 106, 230), width=2)
    a_draw.line([(94, 74), (124, 71)], fill=(255, 255, 255, 255), width=1)
    # Wind blade particles & bamboo leaves flying
    for pt in [(114, 56), (122, 66), (121, 80), (115, 90), (105, 48), (96, 44)]:
        a_draw.point(pt, fill=(255, 208, 40, 255))
        a_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(175, 250, 190, 230))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, dagger_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (怒氣大招 / 天元竹影千刃連刺 Thousand-Spring Bamboo Tempest)
    # High-speed airborne jump (y-8, x+0), dagger raised overhead (-42 deg, target (86, 50), scale 1.12).
    # Winding key spinning at overdrive (+72 deg, target (84, 20)).
    # Rotating taiji windstorm rings & cascading multi-angle emerald blade slashes!
    # =========================================================================
    shifts_skill = {
        "head_top": (0, -8), "hat_rim_l": (-2, -8), "hat_rim_r": (2, -8),
        "ear_pivot_l": (-2, -8), "ear_pivot_r": (2, -8),
        "eye_l": (0, -8), "eye_r": (0, -8),
        "snout": (0, -7), "jaw": (0, -7), "throat": (0, -7),
        "core": (0, -7),
        "shoulder_l": (-3, -7), "shoulder_r": (3, -7),
        "arm_l": (-6, -7), "arm_r": (6, -9),
        "torso": (0, -7), "belt_buckle": (0, -6), "pelvis": (0, -6),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "tail_seg1": (-2, -5), "tail_seg3": (-4, -6), "tail_seg5": (1, -4), "tail_tip": (0, 0),
        "key_mount": (1, -7),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=72, target_center=(84, 20), scale=1.0)
    dagger_skill = place_rotated_element(weapon_raw, deg=-42, target_center=(86, 50), scale=1.12)

    # Tempest shockwave rings & bamboo leaf energy storm
    sk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sk_fx)
    # Rotating tempest rings
    s_draw.arc([28, 14, 118, 104], start=190, end=350, fill=(78, 216, 106, 235), width=3)
    s_draw.arc([32, 18, 114, 100], start=195, end=345, fill=(255, 255, 255, 255), width=1)
    s_draw.arc([20, 24, 110, 114], start=170, end=330, fill=(255, 208, 40, 220), width=2)
    s_draw.arc([38, 10, 122, 94], start=200, end=340, fill=(52, 211, 153, 200), width=2)
    # Multiple slash lines from overhead stab
    s_draw.line([(86, 50), (118, 80)], fill=(78, 216, 106, 240), width=2)
    s_draw.line([(86, 50), (122, 60)], fill=(255, 208, 40, 240), width=2)
    s_draw.line([(86, 50), (110, 95)], fill=(255, 255, 255, 255), width=1)
    # Kinetic burst nodes & sparkles
    for pt in [(42, 32), (72, 14), (102, 28), (116, 52), (88, 72), (36, 60), (110, 84)]:
        s_draw.point(pt, fill=(255, 208, 40, 255))
        s_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 255, 255, 220))
    sk_fx = sk_fx.filter(ImageFilter.GaussianBlur(0.4))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, dagger_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, sk_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊硬直 / 蛇身散開避震姿態 Stagger & Damping Recoil)
    # Heavy recoil backwards (-11, -4), optic lenses show squinting combat indicators (> <),
    # Winding key knocked counter-clockwise (-36 deg, target (70, 28)),
    # Dagger deflects defensively (+52 deg, target (76, 70), scale 0.96).
    # Impact burst & kinetic sparks at (78, 64).
    # =========================================================================
    optic_arr = np.array(optic_src)
    mask = optic_arr[:, :, 3] > 20
    hit_optic = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_arr = np.array(hit_optic)
    h_arr[mask] = [31, 26, 58, 255]  # dark socket background
    hit_optic = Image.fromarray(h_arr)
    draw_ho = ImageDraw.Draw(hit_optic)
    # Squinting combat strain / pain indicators (> <) in emerald green and bright white
    # Left eye: center (52, 40)
    draw_ho.line([(49, 37), (55, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(49, 43), (55, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(50, 38), (54, 40)], fill=(255, 255, 255, 255), width=1)
    draw_ho.line([(50, 42), (54, 40)], fill=(255, 255, 255, 255), width=1)
    # Right eye: center (76, 40)
    draw_ho.line([(79, 37), (73, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(79, 43), (73, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(78, 38), (74, 40)], fill=(255, 255, 255, 255), width=1)
    draw_ho.line([(78, 42), (74, 40)], fill=(255, 255, 255, 255), width=1)

    body_hit_base = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    body_hit_base.alpha_composite(curio_src)
    body_hit_base.alpha_composite(chassis_src)
    body_hit_base.alpha_composite(head_src)
    body_hit_base.alpha_composite(costume_src)
    body_hit_base.alpha_composite(hit_optic)

    shifts_hit = {
        "head_top": (-11, -4), "hat_rim_l": (-13, -5), "hat_rim_r": (-9, -4),
        "ear_pivot_l": (-12, -4), "ear_pivot_r": (-9, -4),
        "eye_l": (-10, -4), "eye_r": (-10, -4),
        "snout": (-9, -3), "jaw": (-8, -3), "throat": (-7, -3),
        "core": (-6, -2),
        "shoulder_l": (-6, 0), "shoulder_r": (-3, -2),
        "arm_l": (-3, 2), "arm_r": (2, -2),
        "torso": (-4, 0), "belt_buckle": (-3, 1), "pelvis": (2, 2),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "tail_seg1": (-2, 2), "tail_seg3": (-4, 3), "tail_seg5": (2, 2), "tail_tip": (0, 0),
        "key_mount": (-10, -4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_hit_base, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_hit = place_rotated_element(key_raw, deg=-36, target_center=(70, 28), scale=1.0)
    dagger_hit = place_rotated_element(weapon_raw, deg=52, target_center=(76, 70), scale=0.96)

    # Impact starburst & shield sparks
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 78, 64
    h_draw.arc([cx - 18, cy - 18, cx + 18, cy + 18], start=280, end=80, fill=(255, 160, 16, 210), width=2)
    h_draw.arc([cx - 24, cy - 24, cx + 24, cy + 24], start=290, end=70, fill=(78, 216, 106, 200), width=2)
    h_draw.arc([cx - 12, cy - 12, cx + 12, cy + 12], start=0, end=360, fill=(255, 208, 40, 220), width=2)
    h_draw.line([(cx - 14, cy), (cx + 14, cy)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx, cy - 14), (cx, cy + 14)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx - 9, cy - 9), (cx + 9, cy + 9)], fill=(78, 216, 106, 220), width=1)
    h_draw.line([(cx - 9, cy + 9), (cx + 9, cy - 9)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255, 255))
    for pt in [(cx - 14, cy - 7), (cx + 14, cy - 9), (cx - 9, cy + 12), (cx + 12, cy + 10), (cx - 5, cy - 12), (cx + 16, cy + 5)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.point((pt[0]+1, pt[1]), fill=(255, 255, 255, 230))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, dagger_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (受擊恢復 / 翻身回盤穩住姿態 Stance Restabilize)
    # Stance restabilizes (+1, +4), dagger dropped to low guarding stance (-10 deg, (88, 78), scale 0.98),
    # Winding key ticks back (-6 deg, target (84, 34)).
    # Bamboo friction mist & cooling jade breath particles.
    # =========================================================================
    shifts_recover = {
        "head_top": (1, 4), "hat_rim_l": (0, 4), "hat_rim_r": (2, 4),
        "ear_pivot_l": (0, 4), "ear_pivot_r": (2, 4),
        "eye_l": (1, 4), "eye_r": (1, 4),
        "snout": (1, 4), "jaw": (1, 4), "throat": (1, 4),
        "core": (1, 4),
        "shoulder_l": (-2, 4), "shoulder_r": (2, 4),
        "arm_l": (-3, 4), "arm_r": (3, 5),
        "torso": (1, 4), "belt_buckle": (1, 4), "pelvis": (1, 4),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_seg1": (0, 3), "tail_seg3": (-1, 3), "tail_seg5": (1, 3), "tail_tip": (0, 0),
        "key_mount": (1, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=-6, target_center=(84, 34), scale=1.0)
    dagger_rec = place_rotated_element(weapon_raw, deg=-10, target_center=(88, 78), scale=0.98)

    # Cooling bamboo mist & sparkles
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for sx, sy in [(36, 48), (92, 50), (62, 88)]:
        r_draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(175, 250, 190, 140))
        r_draw.ellipse([sx - 2, sy - 6, sx + 3, sy - 1], fill=(255, 255, 255, 160))
    for pt in [(34, 44), (94, 46), (60, 84), (96, 76)]:
        r_draw.point(pt, fill=(255, 255, 255, 220))
        r_draw.point((pt[0]+1, pt[1]), fill=(78, 216, 106, 200))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.5))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, dagger_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


if __name__ == "__main__":
    print("=== BUILDING THE BAMBOO VIPER 6 COMBAT ACTION POSES ===")
    poses = generate_poses()

    for p_name, img in poses.items():
        dst_128 = os.path.join(OUT_DIR, f"{p_name}.png")
        img.save(dst_128, format="PNG")

        # 512 LANCZOS upscale
        dst_512 = os.path.join(OUT_DIR, f"{p_name}_512.png")
        img_512 = img.resize((512, 512), resample=Image.Resampling.LANCZOS)
        img_512.save(dst_512, format="PNG")

        bbox = img.getbbox()
        print(f"✓ Saved {p_name:10s} -> {dst_128} (128x128, bbox={bbox}) and {dst_512} (512x512 LANCZOS)")

    # Generate proof sheets
    pose_order = ["idle", "telegraph", "attack", "skill", "hit", "recover"]
    strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    for i, p_name in enumerate(pose_order):
        strip.paste(poses[p_name], (i * 128, 0))

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_viper_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_viper_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
