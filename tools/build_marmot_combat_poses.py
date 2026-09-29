#!/usr/bin/env python3
"""
tools/build_marmot_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Rockbreaker Marmot (第六十五族 碎石旱獺, marmot)
in Clockwork Heart:
  game/assets/sprites/player/poses/marmot/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/marmot/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Also generates:
  game/assets/sprites/player/marmot_battle.png & marmot_battle_512.png (battle == attack per review.md 4b-8-1)
  game/assets/sprites/player/proof_marmot_idle_vs_battle.png & proof_marmot_idle_vs_battle_512.png
  game/assets/sprites/player/proof_marmot_combat_poses_768.png & proof_marmot_combat_poses_magenta.png
  game/assets/sprites/player/proof_marmot_hit_core_crop_8x.png
Follows CANON.md, art_direction.md, ROCKBREAKER_MARMOT_DESIGN_PROPOSAL.md, and review.md quality gates:
  - 0-QA16 / 0-QA21 / 0-QA31 / 0-QA34
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
Features:
  - Weathered tinplate chassis with ivory porcelain bib & ground rivets
  - Alloy chisel visor cowl with forged brass buckteeth
  - Amber dust goggles optic core with luminous range-finding reticles
  - Scavenger canvas harness cuirass with dopamine hazard stripes
  - Cylindrical pneumatic sand-exhaust tail curio
  - Dual-pawl cog-shaped brass wind-up key with center coral pink rivet
  - Dual eccentric piston boxing gauntlets with high-pressure air relief
"""

import math
import os
import sys
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

sys.path = [p for p in sys.path if not p.startswith('/tmp')]

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/marmot"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/marmot"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PLAYER_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_marmot_dual_pawl_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_marmot_pneumatic_sand_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_marmot_quarry_tinplate_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_marmot_alloy_chisel_visor.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_marmot_scavenger_canvas_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_marmot_amber_dust_goggles.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_marmot_eccentric_piston_fists.png").convert("RGBA")

# Separate left and right gauntlets for dynamic monk martial arts articulation
fist_l_crop = weapon_src.crop((36, 64, 56, 86))
fist_r_crop = weapon_src.crop((76, 64, 96, 86))
FIST_L_PIVOT = (44.0, 76.0)
FIST_R_PIVOT = (86.0, 73.0)

# Extract ground shadow master from party marmot_idle.png
ref_shadow_im = Image.open(f"{PLAYER_DIR}/party/marmot_idle.png").convert("RGBA")
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = ref_shadow_im.load()
assert s_px is not None and c_px is not None

for y in range(118, 128):
    for x in range(128):
        s_px[x, y] = cast(tuple[int, int, int, int], c_px[x, y])

arr_shd = np.array(shadow_master)
EXPECTED_SHADOW = [int(np.sum(arr_shd[y, :, 3] > 20)) for y in range(118, 128)]
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

    # Clean outer boundary strictly (L>=4, R>=4, T>=4, B>=2)
    # y=0, 1, 2, 3 and y=126, 127
    for x in range(128):
        o_px[x, 0] = (0, 0, 0, 0)
        o_px[x, 1] = (0, 0, 0, 0)
        o_px[x, 2] = (0, 0, 0, 0)
        o_px[x, 3] = (0, 0, 0, 0)
        o_px[x, 126] = (0, 0, 0, 0)
        o_px[x, 127] = (0, 0, 0, 0)
    # x=0, 1, 2, 3 and x=124, 125, 126, 127
    for y in range(128):
        o_px[0, y] = (0, 0, 0, 0)
        o_px[1, y] = (0, 0, 0, 0)
        o_px[2, y] = (0, 0, 0, 0)
        o_px[3, y] = (0, 0, 0, 0)
        o_px[124, y] = (0, 0, 0, 0)
        o_px[125, y] = (0, 0, 0, 0)
        o_px[126, y] = (0, 0, 0, 0)
        o_px[127, y] = (0, 0, 0, 0)

    # Clean ultra-dark pixels (<10 on all channels in opaque region)
    for y in range(128):
        for x in range(128):
            p = cast(tuple[int, int, int, int], o_px[x, y])
            if p[3] > 50 and p[0] < 10 and p[1] < 10 and p[2] < 10:
                o_px[x, y] = (31, 26, 58, p[3])

    return out


def place_rotated_pivot(elem_img: Image.Image, deg: float, pivot: tuple[float, float], target: tuple[float, float], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates an element around an exact pivot point and places it at target coordinates with subpixel precision."""
    b = elem_img.copy()
    if mirror:
        b = ImageOps.mirror(b)
    px, py = pivot
    tx, ty = target

    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    paste_x = int(round(128.0 - px))
    paste_y = int(round(128.0 - py))
    large.paste(b, (paste_x, paste_y))

    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        scaled = large.resize((nw, nh), Image.Resampling.LANCZOS)
        off_x = (nw - canvas_size) // 2
        off_y = (nh - canvas_size) // 2
        large = scaled.crop((off_x, off_y, off_x + canvas_size, off_y + canvas_size))

    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    out_x = int(round(tx - 128.0))
    out_y = int(round(ty - 128.0))
    out.paste(rotated, (out_x, out_y), rotated)
    return out


def place_fist(fist_crop: Image.Image, center_src: tuple[float, float], deg: float, target: tuple[float, float], scale: float = 1.0) -> Image.Image:
    """Places an individual fist gauntlet crop with custom rotation and scale."""
    cw, ch = fist_crop.size
    px, py = cw / 2.0, ch / 2.0
    tx, ty = target

    canvas_size = 128
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    paste_x = int(round(64.0 - px))
    paste_y = int(round(64.0 - py))
    large.paste(fist_crop, (paste_x, paste_y))

    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        scaled = large.resize((nw, nh), Image.Resampling.LANCZOS)
        off_x = (nw - canvas_size) // 2
        off_y = (nh - canvas_size) // 2
        large = scaled.crop((off_x, off_y, off_x + canvas_size, off_y + canvas_size))

    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(64, 64))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    out_x = int(round(tx - 64.0))
    out_y = int(round(ty - 64.0))
    out.paste(rotated, (out_x, out_y), rotated)
    return out


def warp_image_idw(src_img: Image.Image, src_points: list[tuple[int, int]], dst_points: list[tuple[int, int]], power: float = 2.0, epsilon: float = 4.0) -> Image.Image:
    """Smooth Inverse Distance Weighting (IDW) landmark warp for mechanical body articulation."""
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


# Boundary and stabilization anchors ensuring edge stability and ground shadow preservation
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127),
    (32, 0), (96, 0), (0, 32), (0, 96),
    (127, 32), (127, 96),
    (20, 116), (64, 116), (108, 116)
]

base_landmarks = {
    # Head & Helmet & Chisel Visor & Buckteeth
    "cowl_top": (64, 17),
    "ear_l": (36, 22),
    "ear_r": (92, 22),
    "helmet_side_l": (30, 36),
    "helmet_side_r": (98, 36),
    "head_center": (64, 38),
    "optic_l": (55, 42),
    "optic_r": (73, 42),
    "buckteeth": (64, 55),
    "chin_jaw": (64, 62),
    # Torso & Scavenger Harness & Shoulders
    "throat": (64, 63),
    "shoulder_l": (42, 66),
    "shoulder_r": (86, 66),
    "chest_plate": (64, 75),
    "arm_l": (38, 76),
    "arm_r": (90, 75),
    "harness_hem": (64, 95),
    # Back Curio / Pneumatic Sand Tail
    "curio_mount": (36, 92),
    "curio_mid": (25, 92),
    "curio_tip": (15, 92),
    # Chassis & Heavy Feet
    "pelvis": (64, 96),
    "thigh_l": (48, 102),
    "thigh_r": (80, 102),
    "knee_l": (46, 110),
    "knee_r": (82, 110),
    "foot_l": (44, 116),
    "foot_r": (84, 116),
}

src_pts = [base_landmarks[k] for k in base_landmarks] + anchors

# Canonical pivots on original 128x128 elements
KEY_PIVOT = (38.3, 28.7)
WEAPON_PIVOT = (65.8, 74.3)

# Build base body_core (z: curio=8, chassis=10, head=20, costume=25, optic=30)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)


def draw_spark(draw: ImageDraw.ImageDraw, x: int, y: int, color_core=(255, 253, 248, 255), color_edge=(255, 208, 40, 230)):
    """Draws an intentional 4-point cross star spark that never looks like isolated noise."""
    draw.point((x, y), fill=color_core)
    draw.point((x - 1, y), fill=color_edge)
    draw.point((x + 1, y), fill=color_edge)
    draw.point((x, y - 1), fill=color_edge)
    draw.point((x, y + 1), fill=color_edge)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (扎馬沉穩·抱樁待機 / Rockbreaker Monk Neutral Guard)
    # Solid 2.2-head marmot monk ready stance.
    # Winding key at canonical (38.3, 28.7).
    # Fists at natural forward guard: Left at (44, 76), Right at (86, 73).
    # Ambient glint on goggles & buckteeth.
    # =========================================================================
    idle_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(38.3, 28.7), scale=1.0)
    idle_fist_l = place_fist(fist_l_crop, (46, 75), deg=0, target=(44, 76), scale=1.0)
    idle_fist_r = place_fist(fist_r_crop, (86, 75), deg=0, target=(86, 73), scale=1.0)

    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas.alpha_composite(idle_key)
    idle_canvas.alpha_composite(body_core)
    idle_canvas.alpha_composite(idle_fist_l)
    idle_canvas.alpha_composite(idle_fist_r)

    # Ambient subtle glint FX on amber goggles and forged brass teeth
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    i_draw.point((56, 42), fill=(255, 255, 255, 240))
    i_draw.point((74, 42), fill=(255, 255, 255, 240))
    i_draw.point((64, 55), fill=(255, 235, 115, 220))
    i_draw.point((88, 71), fill=(255, 208, 40, 220))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas.alpha_composite(idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (蓄力下沉·偏心空轉引勢 / Heavy Coil & Piston Drawback)
    # Body sinks down and coils back (-4, +6).
    # Head and chisel visor tuck low to protect chassis (-4, +6).
    # Key counter-winds with high spring torque (-35 deg, target=(33, 33), scale=0.96).
    # Both fists drawn back tight to ribs/chest:
    #   Right fist: target=(75, 77), deg=-24, scale=0.96.
    #   Left fist: target=(37, 79), deg=-18, scale=0.96.
    # FX: Cohesive suction tension arcs around drawn gauntlet chamber.
    # =========================================================================
    tele_offsets = {
        "cowl_top": (-4, 6), "ear_l": (-4, 6), "ear_r": (-4, 6),
        "helmet_side_l": (-4, 6), "helmet_side_r": (-4, 6),
        "head_center": (-4, 6), "optic_l": (-4, 6), "optic_r": (-4, 6),
        "buckteeth": (-4, 6), "chin_jaw": (-4, 6),
        "throat": (-4, 6), "shoulder_l": (-5, 6), "shoulder_r": (-3, 6),
        "chest_plate": (-4, 6), "arm_l": (-5, 5), "arm_r": (-6, 5),
        "harness_hem": (-4, 5),
        "curio_mount": (-4, 5), "curio_mid": (-3, 3), "curio_tip": (-2, 2),
        "pelvis": (-3, 4),
        "thigh_l": (-3, 3), "thigh_r": (1, 3),
        "knee_l": (-3, 2), "knee_r": (1, 2),
        "foot_l": (-2, 0), "foot_r": (1, 0),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele, power=2.0, epsilon=4.0)
    tele_key = place_rotated_pivot(key_src, deg=-35, pivot=KEY_PIVOT, target=(33, 33), scale=0.96)
    tele_fist_l = place_fist(fist_l_crop, (46, 75), deg=-18, target=(37, 79), scale=0.96)
    tele_fist_r = place_fist(fist_r_crop, (86, 75), deg=-24, target=(75, 77), scale=0.96)

    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Suction tension arcs around drawn gauntlet chamber
    t_draw.arc([60, 64, 90, 92], start=160, end=330, fill=(255, 160, 16, 220), width=2)
    t_draw.arc([64, 68, 86, 88], start=180, end=310, fill=(255, 208, 40, 210), width=1)
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.35))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas.alpha_composite(tele_key)
    tele_canvas.alpha_composite(warped_tele_body)
    tele_canvas.alpha_composite(tele_fist_l)
    tele_canvas.alpha_composite(tele_fist_r)
    tele_canvas.alpha_composite(tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (爆鳴直衝·廢土偏心破甲拳 / Eccentric Piston Stamping Strike)
    # Dynamic lunging punch: body surges forward (+16, +2).
    # Head and chisel teeth drive forward (+16, +2).
    # Right fist blasts forward with maximum stroke (+26 deg, target=(104, 69), scale=1.20).
    # Left fist stays at defensive chamber guard (+12, +2).
    # Key uncoils with moderate rotation (+30 deg, target=(48, 29), scale=1.02) to preserve color.
    # FX: Sweeping orange & sun-gold impact shockwave crescent and high-energy sparks at fist face.
    # =========================================================================
    atk_offsets = {
        "cowl_top": (16, 2), "ear_l": (14, 2), "ear_r": (18, 2),
        "helmet_side_l": (14, 2), "helmet_side_r": (18, 2),
        "head_center": (16, 2), "optic_l": (16, 2), "optic_r": (16, 2),
        "buckteeth": (17, 3), "chin_jaw": (17, 3),
        "throat": (15, 2), "shoulder_l": (10, 2), "shoulder_r": (18, 1),
        "chest_plate": (15, 2), "arm_l": (8, 2), "arm_r": (20, 0),
        "harness_hem": (13, 1),
        "curio_mount": (9, 0), "curio_mid": (8, 0), "curio_tip": (7, 0),
        "pelvis": (10, 1),
        "thigh_l": (6, 0), "thigh_r": (12, 0),
        "knee_l": (3, 0), "knee_r": (10, 0),
        "foot_l": (0, 0), "foot_r": (8, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk, power=2.0, epsilon=4.0)
    atk_key = place_rotated_pivot(key_src, deg=30, pivot=KEY_PIVOT, target=(48, 29), scale=1.02)
    atk_fist_l = place_fist(fist_l_crop, (46, 75), deg=-14, target=(52, 77), scale=0.96)
    atk_fist_r = place_fist(fist_r_crop, (86, 75), deg=26, target=(104, 69), scale=1.20)

    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Sweeping punch impact shockwave crescent at fist striking face
    a_draw.arc([88, 44, 123, 94], start=280, end=80, fill=(255, 160, 16, 240), width=3)
    a_draw.arc([92, 48, 119, 90], start=295, end=65, fill=(255, 208, 40, 230), width=2)
    a_draw.arc([96, 52, 115, 86], start=305, end=55, fill=(255, 253, 248, 240), width=1)
    # Punch sparks along impact anvil face
    for px, py in [(118, 62), (120, 68), (117, 75)]:
        draw_spark(a_draw, px, py)
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.35))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas.alpha_composite(atk_key)
    atk_canvas.alpha_composite(warped_atk_body)
    atk_canvas.alpha_composite(atk_fist_l)
    atk_canvas.alpha_composite(atk_fist_r)
    atk_canvas.alpha_composite(atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (旱獺崩山·雙重偏心破勢轟 / Twin Piston Overdrive Stomp & Smash)
    # Heroic elevated martial stance: body lifts upward (y=-9, x=+2).
    # Head and chisel visor held high, commanding the arena.
    # Both fists elevated and extended forward in devastating twin punch:
    #   Right fist: target=(98, 64), deg=+32, scale=1.16.
    #   Left fist: target=(68, 68), deg=+24, scale=1.12.
    # Key overclocks to max tension (+65 deg, target=(42, 22), scale=1.08).
    # FX: Clean energy shockwave arcs focused around raised twin punching fists.
    # =========================================================================
    skl_offsets = {
        "cowl_top": (2, -9), "ear_l": (2, -9), "ear_r": (2, -9),
        "helmet_side_l": (2, -9), "helmet_side_r": (2, -9),
        "head_center": (2, -9), "optic_l": (2, -8), "optic_r": (2, -8),
        "buckteeth": (2, -8), "chin_jaw": (2, -8),
        "throat": (2, -7), "shoulder_l": (0, -7), "shoulder_r": (3, -7),
        "chest_plate": (2, -6), "arm_l": (-2, -7), "arm_r": (5, -8),
        "harness_hem": (2, -5),
        "curio_mount": (1, -6), "curio_mid": (1, -5), "curio_tip": (0, -4),
        "pelvis": (2, -3),
        "thigh_l": (-1, -2), "thigh_r": (3, -2),
        "knee_l": (-1, -1), "knee_r": (3, -1),
        "foot_l": (-1, 0), "foot_r": (3, 0),
    }
    dst_skl = [(base_landmarks[k][0] + skl_offsets[k][0], base_landmarks[k][1] + skl_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skl_body = warp_image_idw(body_core, src_pts, dst_skl, power=2.0, epsilon=4.0)
    skl_key = place_rotated_pivot(key_src, deg=65, pivot=KEY_PIVOT, target=(42, 22), scale=1.08)
    skl_fist_l = place_fist(fist_l_crop, (46, 75), deg=24, target=(66, 68), scale=1.12)
    skl_fist_r = place_fist(fist_r_crop, (86, 75), deg=32, target=(98, 64), scale=1.16)

    skl_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skl_fx)
    # Energy shockwave arcs around twin fists
    s_draw.arc([56, 44, 110, 94], start=290, end=70, fill=(255, 208, 40, 230), width=2)
    s_draw.arc([84, 40, 122, 88], start=280, end=80, fill=(255, 160, 16, 230), width=2)
    for sx, sy in [(96, 36), (112, 52), (106, 68)]:
        draw_spark(s_draw, sx, sy)
    skl_fx = skl_fx.filter(ImageFilter.GaussianBlur(0.35))

    skl_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skl_canvas.alpha_composite(skl_key)
    skl_canvas.alpha_composite(warped_skl_body)
    skl_canvas.alpha_composite(skl_fist_l)
    skl_canvas.alpha_composite(skl_fist_r)
    skl_canvas.alpha_composite(skl_fx)
    poses["skill"] = enforce_ground_shadow(skl_canvas)

    # =========================================================================
    # 5. HIT (鐵壁封架·厚板受震後仰 / Iron Cross-Guard & Recoil Stagger)
    # Violent backward jolt and stagger (-14, -5).
    # Head and chisel visor thrown back sharply (-14, -5).
    # Torso jolts backward (-12, -4), pelvis (-8, -2).
    # Key knocked askew (-45 deg, target=(24, 25), scale=0.95).
    # Both fists crossed in front of chest in cross-guard (-28 deg & +28 deg).
    # FX: Collision starburst sparks on tinplate chest armor.
    # =========================================================================
    hit_offsets = {
        "cowl_top": (-14, -4), "ear_l": (-14, -4), "ear_r": (-14, -4),
        "helmet_side_l": (-14, -4), "helmet_side_r": (-14, -4),
        "head_center": (-14, -4), "optic_l": (-14, -4), "optic_r": (-14, -4),
        "buckteeth": (-14, -4), "chin_jaw": (-14, -4),
        "throat": (-12, -4), "shoulder_l": (-12, -4), "shoulder_r": (-11, -4),
        "chest_plate": (-12, -3), "arm_l": (-10, -3), "arm_r": (-7, 3),
        "harness_hem": (-10, -2),
        "curio_mount": (-9, 0), "curio_mid": (-8, 0), "curio_tip": (-8, 0),
        "pelvis": (-8, -1),
        "thigh_l": (-7, 0), "thigh_r": (-5, 0),
        "knee_l": (-5, 0), "knee_r": (-3, 0),
        "foot_l": (-3, 0), "foot_r": (-1, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit, power=2.0, epsilon=4.0)
    hit_key = place_rotated_pivot(key_src, deg=-45, pivot=KEY_PIVOT, target=(24, 25), scale=0.95)
    # Cross guard at chest center (62, 70)
    hit_fist_l = place_fist(fist_l_crop, (46, 75), deg=28, target=(54, 70), scale=0.96)
    hit_fist_r = place_fist(fist_r_crop, (86, 75), deg=-28, target=(72, 71), scale=0.96)

    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact starburst sparks on chest plate
    ix, iy = 62, 71
    for pt in [(ix - 8, iy - 6), (ix + 8, iy - 6), (ix + 10, iy + 5), (ix - 7, iy + 8), (ix + 11, iy - 1), (ix - 9, iy + 1)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    for pt in [(ix - 5, iy - 3), (ix + 5, iy + 3), (ix + 3, iy - 5), (ix - 3, iy + 5)]:
        h_draw.point(pt, fill=(255, 160, 16, 240))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.35))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas.alpha_composite(hit_key)
    hit_canvas.alpha_composite(warped_hit_body)
    hit_canvas.alpha_composite(hit_fist_l)
    hit_canvas.alpha_composite(hit_fist_r)
    hit_canvas.alpha_composite(hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (落地扎根·洩壓校準回正 / Ground Landing & Pressure Relief Brake)
    # Deep grounded landing crouch: absorbs recoil momentum (+2, +7).
    # Head and chisel visor compress down (+2, +7).
    # Legs planted wide in grounded stance (foot_l -4, foot_r +4).
    # Both fists set low and wide defensively:
    #   Right fist: target=(84, 82), deg=-14, scale=1.01.
    #   Left fist: target=(42, 83), deg=+14, scale=1.01.
    # Winding key re-engages drive (+20 deg, target=(40, 38), scale=0.98).
    # FX: Ground brake friction motes.
    # =========================================================================
    rec_offsets = {
        "cowl_top": (2, 7), "ear_l": (2, 7), "ear_r": (2, 7),
        "helmet_side_l": (2, 7), "helmet_side_r": (2, 7),
        "head_center": (2, 7), "optic_l": (2, 7), "optic_r": (2, 7),
        "buckteeth": (2, 7), "chin_jaw": (2, 7),
        "throat": (2, 6), "shoulder_l": (1, 6), "shoulder_r": (3, 6),
        "chest_plate": (2, 6), "arm_l": (-2, 6), "arm_r": (-3, 6),
        "harness_hem": (2, 5),
        "curio_mount": (1, 5), "curio_mid": (2, 5), "curio_tip": (2, 4),
        "pelvis": (2, 4),
        "thigh_l": (-4, 4), "thigh_r": (4, 4),
        "knee_l": (-4, 3), "knee_r": (4, 3),
        "foot_l": (-4, 0), "foot_r": (4, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec, power=2.0, epsilon=4.0)
    rec_key = place_rotated_pivot(key_src, deg=20, pivot=KEY_PIVOT, target=(40, 38), scale=0.98)
    rec_fist_l = place_fist(fist_l_crop, (46, 75), deg=14, target=(42, 83), scale=1.01)
    rec_fist_r = place_fist(fist_r_crop, (86, 75), deg=-14, target=(84, 82), scale=1.01)

    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for fx, fy in [(44, 114), (82, 114)]:
        draw_spark(r_draw, fx, fy, color_core=(255, 208, 40, 240), color_edge=(255, 160, 16, 200))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas.alpha_composite(rec_key)
    rec_canvas.alpha_composite(warped_rec_body)
    rec_canvas.alpha_composite(rec_fist_l)
    rec_canvas.alpha_composite(rec_fist_r)
    rec_canvas.alpha_composite(rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def main():
    print("Generating The Rockbreaker Marmot combat action poses...")
    poses = generate_poses()

    for p_name in ['idle', 'telegraph', 'attack', 'recover', 'skill', 'hit']:
        im = poses[p_name]
        path_128 = f"{OUT_DIR}/{p_name}.png"
        im.save(path_128)
        print(f"  ✓ Saved {p_name:10s} 128x128: {path_128}, bbox={im.getbbox()}")

        # 512x512 LANCZOS upscale
        im_512 = im.resize((512, 512), Image.Resampling.LANCZOS)
        path_512 = f"{OUT_DIR}/{p_name}_512.png"
        im_512.save(path_512)
        print(f"  ✓ Saved {p_name:10s} 512x512: {path_512}")

    # Official battle asset: marmot_battle.png & marmot_battle_512.png (battle == attack per review.md 4b-8-1)
    battle_128 = poses["attack"]
    battle_512 = poses["attack"].resize((512, 512), Image.Resampling.LANCZOS)
    battle_128.save(f"{PLAYER_DIR}/marmot_battle.png")
    battle_512.save(f"{PLAYER_DIR}/marmot_battle_512.png")
    print(f"  ✓ Saved {PLAYER_DIR}/marmot_battle.png & marmot_battle_512.png (battle == attack)")

    # Proof: Idle vs Battle (128 & 512)
    idle_128 = poses["idle"]
    ivb_128 = Image.new("RGBA", (256, 128), (0, 0, 0, 0))
    ivb_128.paste(idle_128, (0, 0))
    ivb_128.paste(battle_128, (128, 0))
    ivb_128.save(f"{PLAYER_DIR}/proof_marmot_idle_vs_battle.png")

    ivb_512 = Image.new("RGBA", (1024, 512), (0, 0, 0, 0))
    ivb_512.paste(poses["idle"].resize((512, 512), Image.Resampling.LANCZOS), (0, 0))
    ivb_512.paste(battle_512, (512, 0))
    ivb_512.save(f"{PLAYER_DIR}/proof_marmot_idle_vs_battle_512.png")
    print(f"  ✓ Saved proof_marmot_idle_vs_battle.png & 512")

    # Proof sheets: 768x128 Transparent & Magenta
    proof_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(['idle', 'telegraph', 'attack', 'recover', 'skill', 'hit']):
        proof_768.paste(poses[p_name], (i * 128, 0), poses[p_name])
        proof_mag.paste(poses[p_name], (i * 128, 0), poses[p_name])
    proof_768.save(f"{PLAYER_DIR}/proof_marmot_combat_poses_768.png")
    proof_mag.save(f"{PLAYER_DIR}/proof_marmot_combat_poses_magenta.png")
    print(f"  ✓ Saved proof_marmot_combat_poses_768.png & proof_marmot_combat_poses_magenta.png")

    # 8x core crop of hit pose for vision inspection
    hit_crop = poses["hit"].crop((40, 30, 88, 78))
    hit_8x = hit_crop.resize((hit_crop.width * 8, hit_crop.height * 8), Image.Resampling.NEAREST)
    hit_8x.save(f"{PLAYER_DIR}/proof_marmot_hit_core_crop_8x.png")
    print(f"  ✓ Saved proof_marmot_hit_core_crop_8x.png")

    # Ensure compatibility symlink: game/assets/sprites/player/paperdoll/marmot/poses -> ../../poses/marmot
    pd_poses = f"{BASE_DIR}/poses"
    if not os.path.exists(pd_poses):
        os.symlink("../../poses/marmot", pd_poses)
        print(f"  ✓ Created compatibility symlink: {pd_poses} -> ../../poses/marmot")

    print("\n🎉 The Rockbreaker Marmot combat action poses built successfully!")


if __name__ == "__main__":
    main()
