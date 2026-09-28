#!/usr/bin/env python3
"""
tools/build_beaver_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Woodchopper Beaver (第三十八族 劈木河狸, beaver)
in Clockwork Heart:
  game/assets/sprites/player/poses/beaver/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/beaver/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
Enhanced with expressive kinematic exaggeration and rich mechanical articulation.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/beaver"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/beaver"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_beaver_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_beaver_sawtooth_cog_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_beaver_perforated_paddle_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_beaver_brass_timber_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_beaver_chisel_teeth_lumber_cap.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_beaver_deepwood_sapper_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_beaver_amber_surveyor_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_beaver_log_greataxe.png").convert("RGBA")

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
    "head_top": (64, 12),
    "ears_l": (46, 18),
    "ears_r": (82, 18),
    "teeth": (64, 52),
    "chin": (64, 58),
    "eye_l": (55, 40),
    "eye_r": (75, 40),
    "snout": (64, 44),
    "throat": (64, 60),
    "core": (64, 72),
    "shoulder_l": (44, 66),
    "shoulder_r": (84, 66),
    "arm_l": (38, 76),
    "arm_r": (88, 76),
    "hand_r": (96, 68),
    "torso": (64, 78),
    "pelvis": (64, 92),
    "hip_l": (48, 98),
    "hip_r": (80, 98),
    "foot_l": (48, 116),
    "foot_r": (78, 116),
    "curio_tail_top": (36, 85),
    "curio_tail_mid": (28, 98),
    "curio_tail_tip": (20, 112),
    "key_mount": (84, 34),
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
    # 1. IDLE (劈木河狸·工兵工坊 / Sapper Poise)
    # Baseline stable poised stance from canonical composite.
    # Winding key placed at (84, 34).
    # Weapon placed at (101, 59) to keep R >= 4px margin.
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(84, 34), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(101, 59), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)

    # Ambient subtle brass and amber lens gleam FX
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    # Greataxe blade tip glimmer at (102, 34)
    i_draw.line([(102, 31), (102, 37)], fill=(255, 253, 248, 220), width=1)
    i_draw.line([(99, 34), (105, 34)], fill=(255, 208, 40, 240), width=1)
    i_draw.point((102, 34), fill=(255, 255, 255, 255))
    # Amber eye lens reflection
    i_draw.point((55, 39), fill=(255, 160, 16, 220))
    i_draw.point((75, 39), fill=(255, 160, 16, 220))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (伐木蓄勢·沉身拉斧預備 / Timber Cleave Pre-swing Windup)
    # Deep crouch: head & torso sink down and coil back (-4, +7).
    # Greataxe raised high over shoulder in maximum tension (deg=-38, x-8, y-12).
    # Sawtooth key counter-winds (-45 deg, x-4, y+5).
    # Paddle tail presses flat against ground for leverage.
    # FX: Gold & amber targeting reticle, kinetic steam/ember trails, ground tension.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-4, 7), "ears_l": (-4, 7), "ears_r": (-4, 7),
        "teeth": (-4, 7), "chin": (-4, 7),
        "eye_l": (-4, 7), "eye_r": (-4, 7),
        "snout": (-4, 7), "throat": (-4, 7),
        "core": (-3, 6),
        "shoulder_l": (-4, 6), "shoulder_r": (-5, 6),
        "arm_l": (2, 6), "arm_r": (-6, 5),
        "hand_r": (-6, 5),
        "torso": (-3, 5), "pelvis": (-3, 4),
        "hip_l": (-4, 3), "hip_r": (1, 3),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "curio_tail_top": (2, 4), "curio_tail_mid": (3, 3), "curio_tail_tip": (4, 1),
        "key_mount": (-4, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_tele = place_rotated_element(key_raw, deg=-45, target_center=(80, 39), scale=1.0)
    axe_tele = place_rotated_element(weapon_raw, deg=-38, target_center=(93, 47), scale=1.04)

    # Targeting reticle & cleave trajectory FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Heavy axe cleave arc trajectory towards forward ground target
    t_draw.line([(68, 48), (100, 54)], fill=(255, 160, 16, 210), width=1)
    t_draw.line([(100, 54), (114, 72)], fill=(255, 208, 40, 230), width=2)
    # Targeting crosshair at impact point (110, 76)
    cx, cy = 110, 76
    t_draw.arc([cx - 7, cy - 7, cx + 7, cy + 7], start=20, end=340, fill=(255, 94, 138, 220), width=1)
    t_draw.arc([cx - 3, cy - 3, cx + 3, cy + 3], start=40, end=320, fill=(255, 208, 40, 230), width=1)
    t_draw.line([(cx - 8, cy), (cx + 8, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 8), (cx, cy + 8)], fill=(255, 208, 40, 240), width=1)
    # Scraping wood chips and spark particles
    for sx, sy in [(40, 115), (46, 114), (52, 116), (74, 115), (82, 114), (92, 50), (114, 40)]:
        t_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 240))
        t_draw.point((sx, sy), fill=(255, 208, 40, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, axe_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (原木重劈·巨斧破空猛擊 / Lumberjack Axe Cleave & Downward Smash)
    # Tremendous forward lunge and downward body torque (+13, +1):
    # Head & shoulders aggressively thrust forward-down, greataxe cleaves from overhead down (+34 deg, x-3, y+10).
    # Sawtooth key spins +55 deg.
    # Paddle tail flips back and up for aerodynamic counter-weight (-6, -3).
    # FX: Blazing golden-amber arc slash wave, ground-burst sonic shockwave, flying wood/metal sparks.
    # =========================================================================
    shifts_attack = {
        "head_top": (13, 1), "ears_l": (12, 1), "ears_r": (14, 1),
        "teeth": (14, 2), "chin": (14, 2),
        "eye_l": (13, 1), "eye_r": (13, 1),
        "snout": (14, 2), "throat": (13, 2),
        "core": (12, 2),
        "shoulder_l": (13, 1), "shoulder_r": (8, 2),
        "arm_l": (15, -1), "arm_r": (-3, 2),
        "hand_r": (14, 0),
        "torso": (10, 2), "pelvis": (7, 1),
        "hip_l": (8, 0), "hip_r": (-2, 0),
        "foot_l": (5, 0), "foot_r": (-3, 0),
        "curio_tail_top": (-5, -2), "curio_tail_mid": (-6, -3), "curio_tail_tip": (-7, -3),
        "key_mount": (10, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_atk = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_atk = place_rotated_element(key_raw, deg=55, target_center=(94, 34), scale=1.0)
    axe_atk = place_rotated_element(weapon_raw, deg=34, target_center=(98, 69), scale=1.04)

    # Dynamic heavy cleave slash FX
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Huge crescent golden-amber axe blade trail
    a_draw.arc([66, 18, 122, 102], start=270, end=90, fill=(255, 208, 40, 240), width=3)
    a_draw.arc([68, 20, 120, 100], start=280, end=80, fill=(255, 160, 16, 230), width=2)
    a_draw.arc([72, 24, 116, 96], start=290, end=70, fill=(255, 253, 248, 255), width=1)
    # Downward cleave impact sonic rings
    a_draw.ellipse([94, 78, 114, 94], outline=(255, 208, 40, 210), width=1)
    a_draw.ellipse([97, 81, 111, 91], outline=(255, 253, 248, 230), width=1)
    # Impact sparks & sawdust debris
    for px, py in [(96, 70), (104, 62), (110, 52), (114, 68), (118, 80), (102, 88), (90, 85)]:
        a_draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 253, 248, 255))
        a_draw.point((px, py), fill=(255, 160, 16, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.3))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, axe_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. RECOVER (劈後震盪·蒸汽排壓回架 / Sapper Steam Vent & Re-brace)
    # Heavy hydraulic recoil: knees deeply flexed, torso lowered & braced (-4, +6).
    # Greataxe planted firmly on ground with head downward (deg=16, x-4, y+9).
    # Sawtooth key rebounds with spring damping (+18 deg, x-3, y+4).
    # Paddle tail spreads wide on ground.
    # FX: Soft hydraulic steam exhaust puffs, ground tremor ripple, cooling amber core.
    # =========================================================================
    shifts_recover = {
        "head_top": (-4, 6), "ears_l": (-4, 6), "ears_r": (-4, 6),
        "teeth": (-4, 6), "chin": (-4, 6),
        "eye_l": (-4, 6), "eye_r": (-4, 6),
        "snout": (-4, 6), "throat": (-4, 6),
        "core": (-4, 5),
        "shoulder_l": (-4, 5), "shoulder_r": (-4, 5),
        "arm_l": (-4, 5), "arm_r": (-4, 5),
        "hand_r": (-4, 5),
        "torso": (-3, 4), "pelvis": (-3, 3),
        "hip_l": (-3, 2), "hip_r": (-2, 2),
        "foot_l": (-1, 0), "foot_r": (0, 0),
        "curio_tail_top": (-2, 3), "curio_tail_mid": (-2, 3), "curio_tail_tip": (-1, 2),
        "key_mount": (-3, 4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_rec = place_rotated_element(key_raw, deg=18, target_center=(81, 38), scale=1.0)
    axe_rec = place_rotated_element(weapon_raw, deg=16, target_center=(97, 68), scale=1.0)

    # Steam venting & cooling dissipation FX
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Steam exhaust puffs from back chassis & sapper boiler
    for (cx, cy, rad) in [(78, 54, 4), (84, 48, 5), (90, 42, 6), (38, 58, 4), (32, 52, 5)]:
        r_draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(255, 253, 248, 110), outline=(220, 235, 255, 160), width=1)
    # Ground tremor lines near feet
    r_draw.line([(34, 117), (56, 117)], fill=(255, 208, 40, 160), width=1)
    r_draw.line([(70, 117), (94, 117)], fill=(255, 208, 40, 160), width=1)
    r_draw.line([(94, 92), (108, 92)], fill=(255, 160, 16, 180), width=1)
    # Dissipating spark specks
    for px, py in [(82, 50), (88, 44), (40, 56), (98, 74)]:
        r_draw.point((px, py), fill=(255, 208, 40, 200))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.4))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, axe_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    # =========================================================================
    # 5. SKILL (鋸齒超載·全功率輪轉狂斬 / Sawtooth Overdrive Rotary Cleave)
    # Massive torque & airborne leap: body lifts upward (+5, -7),
    # Greataxe held in horizontal rotary cleave spin (deg=-62, x-3, y-12).
    # Sawtooth key spins +95 deg with high-speed rotation.
    # Paddle tail flares out in wide arc (-8, -4).
    # FX: Overdrive gear halo rings, brilliant amber-cyan starbursts, rotational speedlines.
    # =========================================================================
    shifts_skill = {
        "head_top": (5, -7), "ears_l": (4, -7), "ears_r": (6, -7),
        "teeth": (5, -6), "chin": (5, -6),
        "eye_l": (5, -7), "eye_r": (5, -7),
        "snout": (5, -6), "throat": (5, -6),
        "core": (4, -5),
        "shoulder_l": (5, -5), "shoulder_r": (1, -5),
        "arm_l": (6, -5), "arm_r": (-3, -4),
        "hand_r": (5, -5),
        "torso": (4, -4), "pelvis": (3, -3),
        "hip_l": (3, -2), "hip_r": (0, -2),
        "foot_l": (2, -1), "foot_r": (-1, -1),
        "curio_tail_top": (-7, -3), "curio_tail_mid": (-8, -4), "curio_tail_tip": (-9, -4),
        "key_mount": (4, -5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_skill = place_rotated_element(key_raw, deg=95, target_center=(88, 29), scale=1.06)
    axe_skill = place_rotated_element(weapon_raw, deg=-62, target_center=(98, 47), scale=1.05)

    # Overdrive rotary clockwork & spark blast FX
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    k_draw = ImageDraw.Draw(skill_fx)
    # Double gear-teeth energy ring around chest core (68, 67)
    ox, oy = 68, 67
    k_draw.arc([ox - 22, oy - 22, ox + 22, oy + 22], start=0, end=360, fill=(255, 208, 40, 220), width=2)
    k_draw.arc([ox - 16, oy - 16, ox + 16, oy + 16], start=0, end=360, fill=(255, 160, 16, 230), width=1)
    k_draw.arc([ox - 10, oy - 10, ox + 10, oy + 10], start=0, end=360, fill=(255, 253, 248, 250), width=1)
    # Radiating gear rays
    for angle_deg in range(0, 360, 45):
        rad = math.radians(angle_deg)
        x1 = ox + int(round(18 * math.cos(rad)))
        y1 = oy + int(round(18 * math.sin(rad)))
        x2 = ox + int(round(26 * math.cos(rad)))
        y2 = oy + int(round(26 * math.sin(rad)))
        k_draw.line([(x1, y1), (x2, y2)], fill=(255, 208, 40, 240), width=2)
    # Whirling blade circular arc
    k_draw.arc([52, 20, 122, 88], start=210, end=40, fill=(255, 253, 248, 240), width=2)
    k_draw.arc([50, 18, 124, 91], start=220, end=30, fill=(56, 160, 255, 210), width=1)
    # Exploding multi-colored toy starburst particles
    for px, py, col in [
        (46, 28, (255, 208, 40)), (84, 18, (255, 253, 248)), (112, 34, (255, 94, 138)),
        (116, 58, (56, 160, 255)), (106, 78, (255, 208, 40)), (40, 58, (255, 160, 16)),
        (54, 83, (255, 253, 248)), (68, 14, (255, 208, 40))
    ]:
        k_draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col + (240,))
        k_draw.point((px, py), fill=(255, 255, 255, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.3))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, axe_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 6. HIT (受擊震退·裝甲金屬板件火花 / Kinetic Impact & Plating Sparks)
    # Violent backward recoil: head thrown far back (-15, -4), torso arched back (-11, -2).
    # Greataxe jarred back and tilted (deg=-42, x-17, y-8).
    # Sawtooth key knocked counter-clockwise (-30 deg, x-15, y-3).
    # Paddle tail curls forward for balance (+4, +2).
    # Ground shadow strictly anchored (Rule 4b-5).
    # FX: Piercing impact starburst at chest armor, brass fracture shockwave, flying sparks.
    # =========================================================================
    shifts_hit = {
        "head_top": (-15, -4), "ears_l": (-15, -4), "ears_r": (-15, -4),
        "teeth": (-14, -3), "chin": (-14, -3),
        "eye_l": (-15, -4), "eye_r": (-15, -4),
        "snout": (-14, -3), "throat": (-14, -3),
        "core": (-11, -2),
        "shoulder_l": (-12, -3), "shoulder_r": (-9, -2),
        "arm_l": (-11, -3), "arm_r": (-13, -2),
        "hand_r": (-13, -2),
        "torso": (-10, -2), "pelvis": (-7, -1),
        "hip_l": (-6, 0), "hip_r": (-4, 0),
        "foot_l": (-2, 0), "foot_r": (0, 0),
        "curio_tail_top": (4, 2), "curio_tail_mid": (5, 2), "curio_tail_tip": (6, 1),
        "key_mount": (-15, -3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_hit = place_rotated_element(key_raw, deg=-30, target_center=(69, 31), scale=1.0)
    axe_hit = place_rotated_element(weapon_raw, deg=-42, target_center=(84, 51), scale=1.02)

    # Kinetic impact flash & plating spark FX
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Violent white-gold impact epicenter at chest armor (66, 65)
    hx, hy = 66, 65
    # 4-pointed sharp impact diamond
    h_draw.polygon([(hx, hy - 14), (hx + 4, hy - 4), (hx + 14, hy), (hx + 4, hy + 4),
                    (hx, hy + 14), (hx - 4, hy + 4), (hx - 14, hy), (hx - 4, hy - 4)],
                   fill=(255, 255, 255, 250), outline=(255, 208, 40, 240))
    # Diagonal secondary star points
    h_draw.line([(hx - 10, hy - 10), (hx + 10, hy + 10)], fill=(255, 253, 248, 240), width=2)
    h_draw.line([(hx - 10, hy + 10), (hx + 10, hy - 10)], fill=(255, 253, 248, 240), width=2)
    # Kinetic shockwave rings
    h_draw.ellipse([hx - 9, hy - 9, hx + 9, hy + 9], outline=(255, 94, 138, 230), width=2)
    h_draw.ellipse([hx - 16, hy - 16, hx + 16, hy + 16], outline=(255, 160, 16, 210), width=1)
    # Scattered sparks flying outward
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
    hit_canvas = Image.alpha_composite(hit_canvas, axe_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    return poses


def main():
    print("Building 6 combat action poses for The Woodchopper Beaver (第三十八族 劈木河狸)...")
    poses = generate_poses()

    for name, img in poses.items():
        # 1. Save 128x128
        out_path = f"{OUT_DIR}/{name}.png"
        img.save(out_path)
        bbox = img.getbbox()
        print(f"✓ Saved {name:10s} (128x128) -> {out_path} (bbox={bbox})")

        # 2. Save 512x512 with LANCZOS resampling (forbidden NEAREST)
        out_512 = f"{OUT_DIR}/{name}_512.png"
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        img_512.save(out_512)
        print(f"✓ Saved {name:10s}_512 (512x512 LANCZOS) -> {out_512}")

    # 3. Create proof sheet (768x128 Transparent)
    proof_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    pose_order = ["idle", "telegraph", "attack", "recover", "skill", "hit"]
    for i, p in enumerate(pose_order):
        proof_768.paste(poses[p], (i * 128, 0), poses[p])
    proof_path_768 = f"{REPO_ROOT}/game/assets/sprites/player/proof_beaver_combat_poses_768.png"
    proof_768.save(proof_path_768)
    print(f"✓ Saved composite proof sheet -> {proof_path_768}")

    # 4. Create magenta proof sheet (768x128 Magenta #FF00FF)
    proof_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p in enumerate(pose_order):
        proof_mag.paste(poses[p], (i * 128, 0), poses[p])
    proof_path_mag = f"{REPO_ROOT}/game/assets/sprites/player/proof_beaver_combat_poses_magenta.png"
    proof_mag.save(proof_path_mag)
    print(f"✓ Saved magenta proof sheet -> {proof_path_mag}")

    print("\n🎉 ALL 6 COMBAT POSES & PROOFS BUILT SUCCESSFULLY FOR BEAVER!")


if __name__ == "__main__":
    main()
