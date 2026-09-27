#!/usr/bin/env python3
"""
tools/build_wolf_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Scrap Wolf (荒原鋼狼, 22nd Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/wolf/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/wolf/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/wolf"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/wolf"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_wolf_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_wolf_heavy_pojun_cross.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_wolf_segmented_spring_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_wolf_warm_orange_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_wolf_gear_mane_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_wolf_scavenger_scrap_plate_armor.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_wolf_twin_blue_optic_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_wolf_scrap_sawblade_greatsword.png").convert("RGBA")

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Extract raw tail curio crop
curio_bbox = curio_src.getbbox()
assert curio_bbox is not None
curio_raw = curio_src.crop(curio_bbox)

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
    "head_top": (64, 18),
    "ear_l": (44, 24),
    "ear_r": (84, 24),
    "eye_l": (54, 40),
    "eye_r": (73, 40),
    "snout": (64, 48),
    "throat": (64, 58),
    "core": (63, 73),
    "shoulder_l": (46, 68),
    "shoulder_r": (80, 68),
    "arm_l": (42, 80),
    "arm_r": (86, 76),
    "torso": (63, 80),
    "pelvis": (63, 94),
    "hip_l": (46, 96),
    "hip_r": (78, 96),
    "foot_l": (44, 114),
    "foot_r": (80, 114),
    "tail_root": (38, 80),
    "tail_mid": (28, 78),
    "tail_tip": (16, 70),
    "key_mount": (76, 46),
    "key_wing": (84, 33),
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
    # 1. IDLE (流浪騎士·荒原戒備步態 / Scrap Knight Sentry Stance)
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (出招蓄勁 / 齒輪咬合蓄勢蓄力 Gear-Lock Heavy Cleave Windup)
    # Deep crouch (y+7, x-2), head lowered (-2, 7), tail coiled tight (-3, 6),
    # Sawblade greatsword drawn back ready to cleave (-24 deg),
    # Po Jun cross key torqued counter-clockwise (-24 deg),
    # Star sky blue optic lens focus reticle with target crosshair at (108, 62).
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 7), "ear_l": (-3, 6), "ear_r": (-1, 6),
        "eye_l": (-2, 7), "eye_r": (-2, 7), "snout": (-2, 7), "throat": (-2, 7),
        "core": (-2, 7),
        "shoulder_l": (-2, 6), "arm_l": (1, 5),
        "shoulder_r": (-4, 6), "arm_r": (-6, 5),
        "torso": (-2, 7), "pelvis": (-2, 7),
        "hip_l": (-4, 5), "hip_r": (3, 5),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_root": (-3, 5), "tail_mid": (-5, 6), "tail_tip": (-6, 5),
        "key_mount": (-2, 6), "key_wing": (-3, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Po Jun key torqued counter-clockwise (-24 deg)
    key_tele = place_rotated_element(key_raw, deg=-24, target_center=(81, 38), scale=1.0)
    # Sawblade greatsword drawn back and tilted (-22 deg)
    blade_tele = place_rotated_element(weapon_raw, deg=-22, target_center=(89, 82), scale=1.02)

    # Optic lens targeting reticle & gear tension coils
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Aiming trajectory beam in star sky blue and white
    t_draw.line([(88, 76), (118, 62)], fill=(56, 160, 255, 210), width=1)
    t_draw.line([(96, 72), (122, 60)], fill=(255, 208, 40, 230), width=2)
    t_draw.line([(102, 68), (122, 59)], fill=(255, 255, 255, 255), width=1)
    # Crosshair reticle at target point (110, 60)
    cx, cy = 110, 60
    t_draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(56, 160, 255, 220), width=1)
    t_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=(255, 208, 40, 230), width=1)
    t_draw.line([(cx - 12, cy), (cx + 12, cy)], fill=(56, 160, 255, 240), width=1)
    t_draw.line([(cx, cy - 12), (cx, cy + 12)], fill=(56, 160, 255, 240), width=1)
    # Heavy spring torque arcs around key and mane cowl
    t_draw.arc([68, 22, 96, 50], start=200, end=350, fill=(255, 208, 40, 220), width=2)
    t_draw.arc([72, 26, 92, 46], start=210, end=340, fill=(255, 160, 16, 200), width=1)
    # Twin blue optic lens bright focus glint
    t_draw.ellipse([51, 46, 57, 52], fill=(56, 160, 255, 240))
    t_draw.ellipse([70, 46, 76, 52], fill=(56, 160, 255, 240))
    t_draw.ellipse([52, 47, 56, 51], fill=(255, 255, 255, 255))
    t_draw.ellipse([71, 47, 75, 51], fill=(255, 255, 255, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, blade_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (普攻出手 / 鋸齒破甲重斬 Sawblade Scrap Heavy Cleave)
    # Forward thrust: torso rocks forward (+13, 0), right arm cleaves sawblade forward (+16, -2)!
    # Segmented tail counter-balances horizontally backwards (+8, -2).
    # Po Jun cross key spins forward (+36 deg).
    # Stamped tungsten steel sawblade kinetic slash trail and metal sparks.
    # =========================================================================
    shifts_attack = {
        "head_top": (13, 0), "ear_l": (11, -1), "ear_r": (14, 0),
        "eye_l": (13, 0), "eye_r": (13, 0), "snout": (14, 1), "throat": (13, 1),
        "core": (12, 0),
        "shoulder_l": (13, 0), "arm_l": (15, -2),
        "shoulder_r": (5, 0), "arm_r": (16, -2),
        "torso": (11, 0), "pelvis": (9, 0),
        "hip_l": (10, -1), "hip_r": (-5, 0),
        "foot_l": (6, 0), "foot_r": (-6, 0),
        "tail_root": (8, -2), "tail_mid": (5, -4), "tail_tip": (3, -6),
        "key_mount": (10, 0), "key_wing": (8, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=36, target_center=(92, 31), scale=1.0)
    blade_attack = place_rotated_element(weapon_raw, deg=16, target_center=(104, 78), scale=1.06)

    # Scrap metal slash arc, golden sparks, and tungsten friction particles
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Heavy cleave slash arc in dopamine gold, warm orange and pure white
    a_draw.arc([74, 46, 124, 102], start=280, end=70, fill=(255, 208, 40, 245), width=3)
    a_draw.arc([78, 50, 122, 98], start=290, end=60, fill=(255, 160, 16, 230), width=2)
    a_draw.arc([82, 54, 120, 94], start=300, end=50, fill=(255, 255, 255, 255), width=1)
    a_draw.line([(88, 80), (124, 76)], fill=(255, 208, 40, 230), width=2)
    a_draw.line([(96, 78), (124, 75)], fill=(255, 255, 255, 255), width=1)
    # Metal friction sparks flying from sawblade teeth
    for pt in [(116, 50), (122, 62), (121, 80), (115, 92), (106, 44), (96, 40)]:
        a_draw.point(pt, fill=(255, 208, 40, 255))
        a_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 240, 200, 220))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, blade_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (怒氣大招 / 破軍狂風裂地斬 Po Jun Tempest Ground-Fissure Burst)
    # Airborne leap (y-8, x+0), sawblade greatsword raised overhead ready to smash (-45 deg),
    # Po Jun heavy cross key rotating at high overdrive (+76 deg)!
    # Concentric sawblade shockwave arcs & ground-fissure burst lines!
    # =========================================================================
    shifts_skill = {
        "head_top": (0, -8), "ear_l": (-3, -9), "ear_r": (3, -8),
        "eye_l": (0, -8), "eye_r": (0, -8), "snout": (0, -7), "throat": (0, -7),
        "core": (0, -7),
        "shoulder_l": (-3, -7), "arm_l": (-7, -5),
        "shoulder_r": (4, -7), "arm_r": (7, -10),
        "torso": (0, -7), "pelvis": (0, -6),
        "hip_l": (-4, -5), "hip_r": (4, -5),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "tail_root": (-3, -6), "tail_mid": (-6, -10), "tail_tip": (-4, -13),
        "key_mount": (1, -7), "key_wing": (3, -8),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=76, target_center=(83, 22), scale=1.0)
    blade_skill = place_rotated_element(weapon_raw, deg=-45, target_center=(90, 52), scale=1.08)

    # Tempest shockwave rings & ground-fissure kinetic energy
    sk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sk_fx)
    # Rotating sawblade tempest shockwave arcs
    s_draw.arc([32, 14, 118, 100], start=210, end=350, fill=(255, 208, 40, 235), width=3)
    s_draw.arc([36, 18, 114, 96], start=215, end=345, fill=(255, 255, 255, 255), width=1)
    s_draw.arc([24, 26, 110, 112], start=190, end=330, fill=(56, 160, 255, 220), width=2)
    s_draw.arc([42, 10, 122, 90], start=220, end=340, fill=(255, 94, 138, 200), width=2)
    # Kinetic burst nodes
    for pt in [(42, 30), (74, 16), (104, 28), (116, 52), (86, 74)]:
        s_draw.point(pt, fill=(255, 208, 40, 255))
        s_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 255, 255, 220))
    sk_fx = sk_fx.filter(ImageFilter.GaussianBlur(0.4))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, blade_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, sk_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊硬直 / 鋼狼格擋吸震 Scrap Guard Impact & Stagger)
    # Body recoils backwards (-14, -5), optic lenses show blue squinting combat indicators,
    # Po Jun key rattled counter-clockwise (-42 deg), sawblade parries defensively (+68 deg).
    # Impact sparks and coral shock rings at (82, 64).
    # =========================================================================
    optic_arr = np.array(optic_src)
    mask = optic_arr[:, :, 3] > 20
    hit_optic = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_arr = np.array(hit_optic)
    h_arr[mask] = [31, 26, 58, 255] # dark socket background
    hit_optic = Image.fromarray(h_arr)
    draw_ho = ImageDraw.Draw(hit_optic)
    # Squinting combat strain / pain indicators (> <) in star sky blue #38A0FF and bright core
    draw_ho.line([(51, 37), (58, 40)], fill=(56, 160, 255, 255), width=2)
    draw_ho.line([(51, 43), (58, 40)], fill=(56, 160, 255, 255), width=2)
    draw_ho.line([(52, 38), (57, 40)], fill=(210, 240, 255, 255), width=1)
    draw_ho.line([(52, 42), (57, 40)], fill=(210, 240, 255, 255), width=1)
    draw_ho.line([(76, 37), (69, 40)], fill=(56, 160, 255, 255), width=2)
    draw_ho.line([(76, 43), (69, 40)], fill=(56, 160, 255, 255), width=2)
    draw_ho.line([(75, 38), (70, 40)], fill=(210, 240, 255, 255), width=1)
    draw_ho.line([(75, 42), (70, 40)], fill=(210, 240, 255, 255), width=1)

    body_hit_base = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    body_hit_base.alpha_composite(curio_src)
    body_hit_base.alpha_composite(chassis_src)
    body_hit_base.alpha_composite(head_src)
    body_hit_base.alpha_composite(costume_src)
    body_hit_base.alpha_composite(hit_optic)

    shifts_hit = {
        "head_top": (-14, -5), "ear_l": (-16, -7), "ear_r": (-12, -5),
        "eye_l": (-13, -5), "eye_r": (-13, -5), "snout": (-11, -4), "throat": (-9, -3),
        "core": (-7, -2),
        "shoulder_l": (-7, 0), "arm_l": (-3, 2),
        "shoulder_r": (-4, -2), "arm_r": (2, -3),
        "torso": (-4, 0), "pelvis": (2, 2),
        "hip_l": (-3, 2), "hip_r": (4, 2),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "tail_root": (-7, 4), "tail_mid": (-9, 7), "tail_tip": (-5, 10),
        "key_mount": (-11, -4), "key_wing": (-13, -5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_hit_base, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_hit = place_rotated_element(key_raw, deg=-42, target_center=(71, 26), scale=1.0)
    blade_hit = place_rotated_element(weapon_raw, deg=68, target_center=(78, 68), scale=0.96)

    # Impact starburst and scrap steel deflection flare
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 82, 64
    h_draw.arc([cx - 22, cy - 22, cx + 22, cy + 22], start=280, end=80, fill=(255, 160, 16, 210), width=2)
    h_draw.arc([cx - 28, cy - 28, cx + 28, cy + 28], start=290, end=70, fill=(255, 94, 138, 200), width=2)
    h_draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=0, end=360, fill=(255, 208, 40, 220), width=2)
    h_draw.line([(cx - 18, cy), (cx + 18, cy)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx, cy - 18), (cx, cy + 18)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx - 11, cy - 11), (cx + 11, cy + 11)], fill=(56, 160, 255, 220), width=1)
    h_draw.line([(cx - 11, cy + 11), (cx + 11, cy - 11)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255))
    for pt in [(cx - 18, cy - 8), (cx + 18, cy - 12), (cx - 12, cy + 16), (cx + 16, cy + 14), (cx - 8, cy - 16), (cx + 20, cy + 6)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.point((pt[0]+1, pt[1]), fill=(255, 255, 255, 230))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, blade_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (受擊復位 / 散熱排氣與重心重構 Escapement Vent Reset)
    # Stance restabilizes (+1, +5), sawblade dropped into low resting carry (-14 deg),
    # escapement cooling steam from gear mane cowl and chest vents.
    # =========================================================================
    shifts_recover = {
        "head_top": (1, 5), "ear_l": (0, 5), "ear_r": (2, 5),
        "eye_l": (1, 5), "eye_r": (1, 5), "snout": (1, 5), "throat": (1, 5),
        "core": (1, 5),
        "shoulder_l": (-2, 5), "arm_l": (-3, 5),
        "shoulder_r": (2, 5), "arm_r": (4, 6),
        "torso": (1, 5), "pelvis": (1, 5),
        "hip_l": (-2, 4), "hip_r": (2, 4),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_root": (1, 5), "tail_mid": (2, 6), "tail_tip": (1, 7),
        "key_mount": (2, 4), "key_wing": (2, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=-8, target_center=(83, 35), scale=1.0)
    blade_rec = place_rotated_element(weapon_raw, deg=-14, target_center=(94, 84), scale=0.98)

    # Cooling escapement mist & micro-sparks
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for sx, sy in [(34, 42), (94, 44), (64, 88)]:
        r_draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 240, 220, 140))
        r_draw.ellipse([sx - 2, sy - 6, sx + 3, sy - 1], fill=(255, 255, 255, 160))
    for pt in [(32, 38), (96, 40), (62, 84), (98, 78)]:
        r_draw.point(pt, fill=(255, 255, 255, 220))
        r_draw.point((pt[0]+1, pt[1]), fill=(255, 208, 40, 200))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.5))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, blade_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING THE SCRAP WOLF 6 COMBAT ACTION POSES ===")
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

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_wolf_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_wolf_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
