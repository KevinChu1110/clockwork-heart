#!/usr/bin/env python3
"""
tools/build_kite_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Thermal Kite (第四十二族 熱流赤鳶, kite)
in Clockwork Heart:
  game/assets/sprites/player/poses/kite/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/kite/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
Enhanced with expressive ranger archery kinematics, crucible thermal updraft mechanics, and rich toy articulation.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/kite"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/kite"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load individual slice layers (128x128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_kite_turbine_relief_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_kite_spring_steel_cooling_wings.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_kite_copper_obsidian_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_kite_raptor_cowl_beak.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_kite_welder_cape_belt.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_kite_amber_quartz_rangefinder.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_kite_crucible_recurve_bow.png").convert("RGBA")

# Extract raw weapon crop & center
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Standardized ground contact shadow from cleaned baseline body idle asset (purged of right-side bow artifacts)
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
idle_ref_path = f"{REPO_ROOT}/game/assets/sprites/player/party/kite_idle.png"
if os.path.exists(idle_ref_path):
    ref_im = Image.open(idle_ref_path).convert("RGBA")
else:
    ref_im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    shd = ImageDraw.Draw(ref_im)
    shd.ellipse([40, 110, 88, 121], fill=(31, 26, 58, 110))

s_px = shadow_master.load()
c_px = ref_im.load()
assert s_px is not None and c_px is not None

# Clean baseline shadow to guarantee Rule 4c-5 / 16 (L>=4, T>=4, R>=4, B>=2)
# Strictly filter to the central body contact shadow (x in range 4..95), eliminating weapon grounding fragments
for y in range(118, 128):
    for x in range(4, 95):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p
        else:
            s_px[x, y] = (0, 0, 0, 0)

for x in range(128):
    s_px[x, 126] = (0, 0, 0, 0)
    s_px[x, 127] = (0, 0, 0, 0)
for y in range(128):
    s_px[0, y] = (0, 0, 0, 0)
    s_px[1, y] = (0, 0, 0, 0)
    s_px[2, y] = (0, 0, 0, 0)
    s_px[3, y] = (0, 0, 0, 0)
    s_px[124, y] = (0, 0, 0, 0)
    s_px[125, y] = (0, 0, 0, 0)
    s_px[126, y] = (0, 0, 0, 0)
    s_px[127, y] = (0, 0, 0, 0)

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
    "head_crest": (64, 15),
    "head_top": (64, 20),
    "cowl_l": (43, 28),
    "cowl_r": (83, 28),
    "beak_root": (72, 38),
    "beak_tip": (86, 38),
    "chin": (64, 52),
    "rangefinder_r": (75, 38),
    "optic_l": (54, 40),
    "throat": (64, 55),
    "chest_core": (64, 68),
    "gear_pin": (64, 60),
    "shoulder_l": (44, 64),
    "shoulder_r": (82, 64),
    "wing_l_root": (38, 68),
    "wing_l_tip": (20, 78),
    "wing_r_root": (80, 68),
    "wing_r_tip": (92, 85),
    "arm_r": (85, 58),
    "hand_r": (96, 54),
    "torso": (64, 76),
    "pelvis": (64, 92),
    "foot_l": (48, 107),
    "foot_r": (78, 107),
    "key_mount": (72, 35),
}

# Base body without weapon and winding key (z: curio=8, chassis=10, head=20, costume=25, optic=30)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (赤鳶巡檢·靜立盤候 / Thermal Kite Poised Stance)
    # Baseline stable poised ranger stance matching composite.
    # Winding key placed at (72, 35).
    # Recurve bow placed upright at side (100, 68), y2 <= 117 (no ground clipping).
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(72, 35), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(100, 68), scale=0.98)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)

    # Ambient subtle amber quartz gleam & volcanic brass glimmer FX
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    # Rangefinder lens gleam at (75, 38)
    i_draw.line([(75, 36), (75, 40)], fill=(255, 253, 248, 220), width=1)
    i_draw.line([(73, 38), (77, 38)], fill=(255, 160, 16, 240), width=1)
    i_draw.point((75, 38), fill=(255, 255, 255, 255))
    # Alloy scissor beak tip glint at (86, 38)
    i_draw.point((86, 38), fill=(255, 208, 40, 230))
    # Chest gear pin glint at (64, 60)
    i_draw.point((64, 60), fill=(255, 250, 185, 220))
    # Bow riser brass gem glint at (94, 68)
    i_draw.point((94, 68), fill=(255, 208, 40, 230))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (拉弦蓄勢·熱流聚能 / Thermal Tension Windup)
    # Deep crouch: head & torso sink down and coil back (-5, +6).
    # Bow drawn forward-down in high tension, string pulled back.
    # Winding key counter-winds (-45 deg, x-4, y+5).
    # Wings spread low and gather thermal updraft.
    # FX: Amber quartz targeting trajectory, coiling thermal sparks, red-orange heat haze.
    # =========================================================================
    shifts_telegraph = {
        "head_crest": (-5, 6), "head_top": (-5, 6), "cowl_l": (-5, 6), "cowl_r": (-5, 6),
        "beak_root": (-5, 6), "beak_tip": (-5, 6), "chin": (-5, 6),
        "rangefinder_r": (-5, 6), "optic_l": (-5, 6), "throat": (-5, 6),
        "chest_core": (-4, 5), "gear_pin": (-4, 5),
        "shoulder_l": (6, 3), "shoulder_r": (-7, 5),
        "wing_l_root": (4, 4), "wing_l_tip": (-4, 2),
        "wing_r_root": (-5, 4), "wing_r_tip": (-8, 6),
        "arm_r": (-8, 5), "hand_r": (-12, 6),
        "torso": (-4, 5), "pelvis": (-3, 4),
        "foot_l": (-3, 2), "foot_r": (1, 2),
        "key_mount": (-4, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_tele = place_rotated_element(key_raw, deg=-45, target_center=(68, 40), scale=1.0)
    # Bow angled forward-up in draw stance, grip at (92, 66)
    bow_tele = place_rotated_element(weapon_raw, deg=-22, target_center=(92, 66), scale=0.98)

    # Taut bowstring & thermal charge FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Luminous bowstring drawn back to (72, 74)
    t_draw.line([(96, 32), (72, 74)], fill=(255, 235, 160, 230), width=1)
    t_draw.line([(94, 102), (72, 74)], fill=(255, 235, 160, 230), width=1)
    # Blazing thermal arrow shaft & glowing arrow head (stay well within margins)
    t_draw.line([(72, 74), (114, 56)], fill=(255, 160, 16, 240), width=2)
    t_draw.line([(74, 74), (113, 56)], fill=(255, 253, 248, 255), width=1)
    t_draw.polygon([(116, 55), (107, 50), (110, 59)], fill=(255, 208, 40, 255))
    # Concentric heat charge rings around arrowhead
    t_draw.arc([94, 38, 118, 68], start=80, end=330, fill=(255, 94, 138, 210), width=2)
    t_draw.arc([90, 34, 118, 72], start=100, end=310, fill=(255, 160, 16, 200), width=2)
    # Crosshair reticle at target vector
    t_draw.line([(104, 56), (116, 56)], fill=(255, 208, 40, 220), width=1)
    t_draw.line([(110, 49), (110, 63)], fill=(255, 208, 40, 220), width=1)
    # Thermal spark specks (strictly y <= 108)
    for sx, sy in [(74, 72), (70, 78), (82, 66), (96, 46), (108, 48), (62, 82), (78, 88), (56, 102), (74, 104)]:
        t_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 250, 185, 240))
        t_draw.point((sx, sy), fill=(255, 160, 16, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, bow_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (破空炎矢·烈風疾射 / Blazing Gale Release)
    # Explosive forward thrust (+14, +1):
    # Head & torso lunges forward, bow snaps forward with recoil shockwave.
    # Winding key spins forward (+60 deg, x+10, y-1).
    # Left wing pushes forward, right wing whips back for aerodynamic counter-balance.
    # FX: Blazing supersonic heat beam arrow, sonic cone rings, bursting forge sparks.
    # =========================================================================
    shifts_attack = {
        "head_crest": (12, 1), "head_top": (12, 1), "cowl_l": (12, 1), "cowl_r": (12, 1),
        "beak_root": (13, 1), "beak_tip": (14, 1), "chin": (13, 1),
        "rangefinder_r": (13, 1), "optic_l": (13, 1), "throat": (13, 1),
        "chest_core": (11, 1), "gear_pin": (12, 1),
        "shoulder_l": (14, 0), "shoulder_r": (8, 2),
        "wing_l_root": (5, 0), "wing_l_tip": (-7, -3),
        "wing_r_root": (8, 1), "wing_r_tip": (2, -2),
        "arm_r": (-4, 2), "hand_r": (6, 0),
        "torso": (9, 2), "pelvis": (6, 1),
        "foot_l": (4, 0), "foot_r": (-3, 0),
        "key_mount": (10, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_atk = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_atk = place_rotated_element(key_raw, deg=60, target_center=(82, 34), scale=1.0)
    # Bow snapped forward, safe margin (x <= 118)
    bow_atk = place_rotated_element(weapon_raw, deg=-10, target_center=(96, 66), scale=0.98)

    # Supersonic thermal arrow & pressure cone blast FX (strictly x <= 119)
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Blazing thermal streak piercing forward
    a_draw.line([(86, 66), (119, 62)], fill=(255, 160, 16, 240), width=4)
    a_draw.line([(88, 66), (119, 62)], fill=(255, 253, 248, 255), width=2)
    # Expanding pressure shock cones
    a_draw.arc([90, 48, 110, 84], start=275, end=85, fill=(255, 94, 138, 230), width=3)
    a_draw.arc([98, 46, 118, 82], start=280, end=80, fill=(255, 208, 40, 220), width=2)
    # Rear exhaust back-thrust wind streaks
    a_draw.line([(40, 72), (18, 76)], fill=(255, 235, 160, 180), width=2)
    a_draw.line([(36, 76), (16, 82)], fill=(255, 160, 16, 160), width=2)
    # Forge spark bursts (all y <= 108, x <= 118)
    for px, py in [(94, 60), (100, 54), (106, 48), (112, 58), (116, 68), (102, 78), (90, 75)]:
        a_draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 253, 248, 255))
        a_draw.point((px, py), fill=(255, 208, 40, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.3))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, bow_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. RECOVER (收弓迴旋·氣動緩衝 / Thermal Aerodynamic Dampening)
    # Hydraulic recoil: knees flexed, body lowered and cushioned (-4, +6).
    # Recurve bow held safely in guard position (+10 deg, x-6, y+6), y2 <= 114.
    # Winding key rebounds with spring damping (+20 deg, x-3, y+4).
    # Cooling wings fold low to vent heated steam from foundry flight.
    # FX: Soft steam puffs from cape & chassis vents.
    # =========================================================================
    shifts_recover = {
        "head_crest": (-4, 6), "head_top": (-4, 6), "cowl_l": (-4, 6), "cowl_r": (-4, 6),
        "beak_root": (-4, 6), "beak_tip": (-4, 6), "chin": (-4, 6),
        "rangefinder_r": (-4, 6), "optic_l": (-4, 6), "throat": (-4, 6),
        "chest_core": (-4, 5), "gear_pin": (-4, 5),
        "shoulder_l": (-4, 5), "shoulder_r": (-4, 5),
        "wing_l_root": (-3, 4), "wing_l_tip": (-3, 3),
        "wing_r_root": (-3, 4), "wing_r_tip": (-2, 3),
        "arm_r": (-4, 5), "hand_r": (-4, 5),
        "torso": (-3, 4), "pelvis": (-3, 3),
        "foot_l": (-2, 1), "foot_r": (0, 1),
        "key_mount": (-3, 4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_rec = place_rotated_element(key_raw, deg=20, target_center=(69, 39), scale=1.0)
    # Recurve bow held in balanced guard position, well above y=118
    bow_rec = place_rotated_element(weapon_raw, deg=-10, target_center=(92, 65), scale=0.96)

    # Steam venting FX (strictly y <= 108 to avoid ground noise)
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Steam exhaust puffs from back turbine & chassis
    for (cx, cy, rad) in [(74, 50, 4), (80, 44, 5), (86, 38, 5), (38, 54, 4), (32, 48, 4), (54, 98, 4), (72, 98, 4)]:
        r_draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(255, 253, 248, 110), outline=(255, 235, 180, 150), width=1)
    # Dissipating spark specks (all y <= 108)
    for px, py in [(78, 48), (84, 42), (40, 52), (58, 92), (68, 94)]:
        r_draw.point((px, py), fill=(255, 160, 16, 200))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.4))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, bow_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    # =========================================================================
    # 5. SKILL (天頂熱流·赤鳶狂瀾奧義 / Thermal Updraft Overdrive Barrage)
    # Massive thermal updraft lift (+3, -7):
    # Wings fully flared and extended in articulated spring-steel majesty (-8, -7).
    # Bow drawn full overhead pointing skyward (deg=-60, center=(75, 52), scale=0.94),
    # guaranteed safe margins: left >= 20, right >= 8, top >= 20, bot >= 30.
    # Winding key spins +115 deg in turbine overdrive mode.
    # FX: Concentric solar-gear heat rings, radiating thermal arrows, volcanic starbursts.
    # =========================================================================
    shifts_skill = {
        "head_crest": (3, -7), "head_top": (3, -7), "cowl_l": (3, -7), "cowl_r": (3, -7),
        "beak_root": (3, -6), "beak_tip": (3, -6), "chin": (3, -6),
        "rangefinder_r": (3, -7), "optic_l": (3, -7), "throat": (3, -6),
        "chest_core": (3, -5), "gear_pin": (3, -6),
        "shoulder_l": (3, -5), "shoulder_r": (0, -5),
        "wing_l_root": (2, -5), "wing_l_tip": (-8, -7),
        "wing_r_root": (3, -5), "wing_r_tip": (6, -6),
        "arm_r": (-4, -4), "hand_r": (2, -5),
        "torso": (3, -4), "pelvis": (2, -3),
        "foot_l": (2, -1), "foot_r": (-1, -1),
        "key_mount": (3, -6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_skill = place_rotated_element(key_raw, deg=115, target_center=(75, 29), scale=1.05)
    bow_skill = place_rotated_element(weapon_raw, deg=-60, target_center=(75, 52), scale=0.94)

    # Overdrive thermal updraft & gear solar nova FX
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    k_draw = ImageDraw.Draw(skill_fx)
    # Double gear-teeth solar heat ring around chest core (67, 63)
    ox, oy = 67, 63
    k_draw.arc([ox - 22, oy - 22, ox + 22, oy + 22], start=0, end=360, fill=(255, 160, 16, 230), width=2)
    k_draw.arc([ox - 16, oy - 16, ox + 16, oy + 16], start=0, end=360, fill=(255, 208, 40, 230), width=1)
    k_draw.arc([ox - 10, oy - 10, ox + 10, oy + 10], start=0, end=360, fill=(255, 253, 248, 250), width=1)
    # Radiating solar thermal energy rays
    for angle_deg in range(0, 360, 45):
        rad = math.radians(angle_deg)
        x1 = ox + int(round(18 * math.cos(rad)))
        y1 = oy + int(round(18 * math.sin(rad)))
        x2 = ox + int(round(26 * math.cos(rad)))
        y2 = oy + int(round(26 * math.sin(rad)))
        k_draw.line([(x1, y1), (x2, y2)], fill=(255, 160, 16, 240), width=2)
    # Whirling heat ring updraft arc (kept within margins)
    k_draw.arc([46, 16, 116, 86], start=210, end=40, fill=(255, 253, 248, 240), width=2)
    k_draw.arc([44, 14, 118, 89], start=220, end=30, fill=(255, 94, 138, 220), width=1)
    # Exploding multi-colored toy starburst particles (all y <= 108, x <= 118)
    for px, py, col in [
        (46, 26, (255, 160, 16)), (84, 16, (255, 253, 248)), (106, 32, (255, 94, 138)),
        (112, 56, (255, 208, 40)), (102, 76, (78, 216, 106)), (38, 56, (255, 160, 16)),
        (52, 81, (255, 253, 248)), (68, 12, (255, 208, 40))
    ]:
        k_draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col + (240,))
        k_draw.point((px, py), fill=(255, 255, 255, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.3))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, bow_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 6. HIT (受擊失衡·黑曜震盪 / Obsidian Impact Shock)
    # Violent backward recoil: head thrown far back (-15, -4), torso arched back (-11, -2).
    # Recurve bow jarred back and tilted (deg=-30, center=(80, 62), scale=0.96),
    # safe margins: left >= 50, right >= 15, top >= 20, bot >= 20.
    # Winding key knocked counter-clockwise (-32 deg, x-14, y-4).
    # Wings fold forward defensively (+4, +3).
    # Ground shadow strictly anchored (Rule 4b-5).
    # FX: Piercing impact starburst at chest armor, brass fracture shockwave, flying sparks.
    # =========================================================================
    shifts_hit = {
        "head_crest": (-15, -4), "head_top": (-15, -4), "cowl_l": (-15, -4), "cowl_r": (-15, -4),
        "beak_root": (-14, -3), "beak_tip": (-14, -3), "chin": (-14, -3),
        "rangefinder_r": (-15, -4), "optic_l": (-15, -4), "throat": (-14, -3),
        "chest_core": (-11, -2), "gear_pin": (-11, -2),
        "shoulder_l": (-12, -3), "shoulder_r": (-9, -2),
        "wing_l_root": (-8, -2), "wing_l_tip": (3, 2),
        "wing_r_root": (-6, -2), "wing_r_tip": (5, 2),
        "arm_r": (-13, -2), "hand_r": (-13, -2),
        "torso": (-10, -2), "pelvis": (-7, -1),
        "foot_l": (-2, 0), "foot_r": (0, 0),
        "key_mount": (-14, -4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_hit = place_rotated_element(key_raw, deg=-32, target_center=(58, 31), scale=1.0)
    bow_hit = place_rotated_element(weapon_raw, deg=-30, target_center=(80, 62), scale=0.96)

    # Kinetic impact flash & plating spark FX
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Violent white-coral impact epicenter at chest armor (66, 64)
    hx, hy = 66, 64
    # 4-pointed sharp impact diamond
    h_draw.polygon([(hx, hy - 14), (hx + 4, hy - 2), (hx + 16, hy), (hx + 4, hy + 2),
                    (hx, hy + 14), (hx - 4, hy + 2), (hx - 16, hy), (hx - 4, hy - 2)],
                   fill=(255, 253, 248, 255))
    h_draw.polygon([(hx, hy - 8), (hx + 2, hy - 1), (hx + 9, hy), (hx + 2, hy + 1),
                    (hx, hy + 8), (hx - 2, hy + 1), (hx - 9, hy), (hx - 2, hy - 1)],
                   fill=(255, 94, 138, 240))
    # Shockwave ripples
    h_draw.ellipse([hx - 11, hy - 11, hx + 11, hy + 11], outline=(255, 208, 40, 230), width=1)
    h_draw.ellipse([hx - 16, hy - 16, hx + 16, hy + 16], outline=(255, 160, 16, 210), width=1)
    # Scattered sparks flying outward (all y <= 108)
    for sx, sy in [
        (hx + 12, hy - 14), (hx + 18, hy - 6), (hx + 16, hy + 12),
        (hx - 14, hy - 16), (hx - 20, hy + 4), (hx - 12, hy + 16),
        (hx + 8, hy - 20), (hx - 8, hy - 18)
    ]:
        h_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 255))
        h_draw.point((sx, sy), fill=(255, 208, 40, 255))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.3))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, bow_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    return poses


def build_and_save():
    print("=== BUILDING 6 DEFINITIVE COMBAT ACTION POSES FOR THE THERMAL KITE ===")
    poses = generate_poses()

    pose_names = ["idle", "telegraph", "attack", "recover", "skill", "hit"]

    for name in pose_names:
        im128 = poses[name]
        p128_path = os.path.join(OUT_DIR, f"{name}.png")
        im128.save(p128_path, "PNG")

        # 512x512 LANCZOS high-definition asset
        im512 = im128.resize((512, 512), Image.Resampling.LANCZOS)
        p512_path = os.path.join(OUT_DIR, f"{name}_512.png")
        im512.save(p512_path, "PNG")

        c128 = len(np.unique(np.array(im128).reshape(-1, 4), axis=0))
        c512 = len(np.unique(np.array(im512).reshape(-1, 4), axis=0))
        bbox = im128.getbbox()
        assert bbox is not None
        print(f"✓ Saved {name:10s} (128x128 bbox={bbox}, colors={c128}) & {name}_512 (colors={c512}, smooth={c512/c128:.1f}x)")

    # Generate 6-in-1 proof strips (768x128 Transparent & Magenta)
    strip_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    for i, name in enumerate(pose_names):
        strip_768.paste(poses[name], (i * 128, 0))
    proof_768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_kite_combat_poses_768.png"
    strip_768.save(proof_768_path, "PNG")

    strip_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    strip_mag.alpha_composite(strip_768)
    proof_mag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_kite_combat_poses_magenta.png"
    strip_mag.save(proof_mag_path, "PNG")

    print(f"\n✓ Saved 6-in-1 Transparent Proof Strip: {proof_768_path}")
    print(f"✓ Saved 6-in-1 Magenta Proof Strip:     {proof_mag_path}")
    print("=== FINISHED BUILDING KITE COMBAT POSES ===")


if __name__ == "__main__":
    build_and_save()
