#!/usr/bin/env python3
"""
tools/build_lemur_combat_poses.py
Generates the complete, definitive 6 combat action poses for 第六十四族 星環狐猴 (The Star-Ring Lemur, lemur)
in Clockwork Heart:
  game/assets/sprites/player/poses/lemur/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/lemur/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Also generates:
  game/assets/sprites/player/lemur_battle.png & lemur_battle_512.png (battle == attack per review.md 4b-8-1)
  game/assets/sprites/player/proof_lemur_idle_vs_battle.png & proof_lemur_idle_vs_battle_512.png
  game/assets/sprites/player/proof_lemur_combat_poses_768.png & proof_lemur_combat_poses_magenta.png
  game/assets/sprites/player/proof_lemur_hit_core_crop_8x.png
Follows CANON.md, art_direction.md, and review.md quality gates:
  - 0-QA16 / 0-QA21 / 0-QA31 / 0-QA34
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
Features:
  - Ivory high-impact polymer chassis #FFFDF8 with dopamine sky blue #38A0FF and mint #4ED86A trims
  - Orbital radar cowl head unit with sweeping antenna ears
  - Amber pulsar visors optic core
  - Astronaut stealth harness cuirass with dopamine warm orange piping
  - Neon optical fiber star-ring antenna tail (back curio)
  - Tri-ring orbit brass winding key
  - Orbital pulse twin daggers (sky blue ionized main blade + mint parrying teeth)
"""

import math
import os
import sys
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lemur"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/lemur"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PLAYER_DIR, exist_ok=True)

# 1. Load canonical components
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_lemur_neon_ring_fiber_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_lemur_orbit_polymer_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_lemur_orbit_radar_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_lemur_astro_stealth_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_lemur_amber_pulsar_visors.png").convert("RGBA")
key_src = Image.open(f"{BASE_DIR}/winding_key/key_lemur_tri_ring_orbit_brass.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_lemur_orbital_pulse_daggers.png").convert("RGBA")

# Extract ground shadow master from party lemur_idle.png
ref_shadow_im = Image.open(f"{PLAYER_DIR}/party/lemur_idle.png").convert("RGBA")
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


# Split weapon into Left Dagger (Parrying) and Right Dagger (Main Reverse Grip)
w_arr = np.array(weapon_src)
w_alpha = w_arr[:, :, 3]

left_dag_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
right_dag_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
l_px = left_dag_img.load()
r_px = right_dag_img.load()
w_px = weapon_src.load()
assert l_px is not None and r_px is not None and w_px is not None

for y in range(128):
    for x in range(128):
        if w_alpha[y, x] > 20:
            p = cast(tuple[int, int, int, int], w_px[x, y])
            if x < 64:
                l_px[x, y] = p
            else:
                r_px[x, y] = p

LEFT_DAG_PIVOT = (44.0, 76.0)
RIGHT_DAG_PIVOT = (89.0, 72.0)
KEY_PIVOT = (38.1, 28.2)

# Boundary and stabilization anchors ensuring edge stability and ground shadow preservation
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127),
    (32, 0), (96, 0), (0, 32), (0, 96),
    (127, 32), (127, 96),
    (20, 116), (64, 116), (108, 116)
]

# Canonical landmarks on Lemur
base_landmarks = {
    # Head & Radar Cowl
    "head_top": (64, 18),
    "ear_tip_l": (23, 20),
    "ear_tip_r": (105, 20),
    "ear_mid_l": (36, 30),
    "ear_mid_r": (92, 30),
    "cowl_cheek_l": (38, 48),
    "cowl_cheek_r": (90, 48),
    "optic_l": (54, 42),
    "optic_r": (74, 42),
    "optic_center": (64, 42),
    "snout_tip": (64, 52),
    "jaw_chin": (64, 58),
    # Torso & Harness
    "throat": (64, 60),
    "shoulder_l": (44, 64),
    "shoulder_r": (84, 64),
    "chest_center": (64, 72),
    "elbow_l": (40, 75),
    "elbow_r": (88, 75),
    "harness_hem": (64, 92),
    # Tail (Curio Neon Ring Fiber Tail)
    "tail_tip": (38, 23),
    "tail_bend": (22, 48),
    "tail_mid": (32, 70),
    "tail_base": (44, 95),
    # Chassis Pelvis & Legs
    "pelvis": (64, 96),
    "thigh_l": (52, 102),
    "thigh_r": (76, 102),
    "knee_l": (50, 110),
    "knee_r": (78, 110),
    "foot_l": (52, 120),
    "foot_r": (76, 120),
}

src_pts = [base_landmarks[k] for k in base_landmarks] + anchors

# Build base body_core (z: curio=8, chassis=10, head=15, costume=25, optic=30)
raw_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
raw_body.alpha_composite(curio_src)
raw_body.alpha_composite(chassis_src)
raw_body.alpha_composite(head_src)
raw_body.alpha_composite(costume_src)
raw_body.alpha_composite(optic_src)

body_core = raw_body.copy()


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (靈狐潛巡·星軌常備 / Star-Ring Orbit Stealth Readiness Stance)
    # Balanced 2.2-head agile lemur ninja toy automaton stance.
    # Winding key at natural (38.1, 28.2).
    # Twin daggers held at ready (left at 44, 76; right at 89, 72).
    # Neon tail arched elegantly on the left.
    # =========================================================================
    idle_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(38.1, 28.2), scale=1.0)
    idle_l_dag = place_rotated_pivot(left_dag_img, deg=0, pivot=LEFT_DAG_PIVOT, target=(44.0, 76.0), scale=1.0)
    idle_r_dag = place_rotated_pivot(right_dag_img, deg=0, pivot=RIGHT_DAG_PIVOT, target=(89.0, 72.0), scale=1.0)

    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas.alpha_composite(idle_key)
    idle_canvas.alpha_composite(body_core)
    idle_canvas.alpha_composite(idle_l_dag)
    idle_canvas.alpha_composite(idle_r_dag)

    # Ambient subtle glint FX on amber visors and ionization grooves
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    i_draw.point((54, 42), fill=(255, 255, 255, 240))
    i_draw.point((74, 42), fill=(255, 255, 255, 240))
    i_draw.point((82, 80), fill=(205, 238, 255, 230))
    i_draw.point((48, 86), fill=(195, 255, 215, 220))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas.alpha_composite(idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (星環蓄勢·伏地十字引刃 / Orbital Low-Crouch Cross-Dagger Telegraph)
    # Deep stealth crouch & windup: body coils backward & down (-5, +6).
    # Head & ears lower, amber visors lock onto target (-5, +6).
    # Tail coils tightly inward to store potential energy (-6, +4).
    # Winding key counter-winds with high spring torque (-48 deg, target=(30, 34), scale=0.94).
    # Daggers cross in front of chest into defensive/offensive X-stance:
    # Left dagger raises across chest (+42 deg, target=(49, 70), scale=0.98).
    # Right dagger lowers across chest (-38 deg, target=(79, 74), scale=0.98).
    # FX: Concentric mint-green #4ED86A and sky-blue #38A0FF tension pulse arcs at cross point.
    # =========================================================================
    tele_offsets = {
        "head_top": (-5, 6),
        "ear_tip_l": (-5, 6), "ear_tip_r": (-5, 6),
        "ear_mid_l": (-5, 6), "ear_mid_r": (-5, 6),
        "cowl_cheek_l": (-5, 6), "cowl_cheek_r": (-5, 6),
        "optic_l": (-5, 6), "optic_r": (-5, 6), "optic_center": (-5, 6),
        "snout_tip": (-5, 6), "jaw_chin": (-5, 6),
        "throat": (-5, 6), "shoulder_l": (-6, 6), "shoulder_r": (-4, 6),
        "chest_center": (-5, 6), "elbow_l": (-5, 5), "elbow_r": (-7, 5),
        "harness_hem": (-5, 5),
        "tail_tip": (-7, 5), "tail_bend": (-6, 5), "tail_mid": (-5, 4), "tail_base": (-4, 3),
        "pelvis": (-4, 4),
        "thigh_l": (-4, 4), "thigh_r": (-1, 4),
        "knee_l": (-4, 3), "knee_r": (0, 3),
        "foot_l": (-2, 0), "foot_r": (1, 0),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele, power=2.0, epsilon=4.0)

    tele_key = place_rotated_pivot(key_src, deg=-48, pivot=KEY_PIVOT, target=(30, 34), scale=0.94)
    tele_l_dag = place_rotated_pivot(left_dag_img, deg=42, pivot=LEFT_DAG_PIVOT, target=(49, 70), scale=0.98)
    tele_r_dag = place_rotated_pivot(right_dag_img, deg=-38, pivot=RIGHT_DAG_PIVOT, target=(79, 74), scale=0.98)

    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Suction power arcs around crossed daggers intersection (64, 72)
    cx, cy = 64, 72
    t_draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=30, end=210, fill=(56, 160, 255, 230), width=2)
    t_draw.arc([cx - 12, cy - 12, cx + 12, cy + 12], start=150, end=330, fill=(78, 216, 106, 230), width=2)
    t_draw.arc([cx - 8, cy - 8, cx + 8, cy + 8], start=0, end=360, fill=(255, 208, 40, 200), width=1)
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.35))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas.alpha_composite(tele_key)
    tele_canvas.alpha_composite(warped_tele_body)
    tele_canvas.alpha_composite(tele_l_dag)
    tele_canvas.alpha_composite(tele_r_dag)
    tele_canvas.alpha_composite(tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (星芒疾空·雙刃交錯破空突刺 / Orbital Flash Cross-Dagger Cleave)
    # Explosive forward lunging sprint & dual dagger cross cleave:
    # Body drives forward with intense kinetic inertia.
    # Head & snout thrust forward (+20, +3), radar ears stream back in aerodynamic slipstream (+12, +5).
    # Chest surges forward (+18, +2), pelvis at (+10, +1).
    # Rear right leg braces firmly behind to kick off ground (foot_r at 0, 0, thigh_r at +2, +1).
    # Front left leg lunges far forward into dynamic lunge (thigh_l +16, knee_l +18, foot_l +16).
    # Neon tail whips backward-upward like a dynamic balancing antenna (tail_tip -4, -8; tail_bend 0, -4).
    # Right main dagger thrusts forward with full reach (+20, -5, deg=+35, target=(104, 66), scale=1.04).
    # Left parrying dagger slashes low across the flank (-45 deg, target=(52, 78), scale=1.0).
    # Winding key uncoils with full spring release (+68 deg, target=(56, 26), scale=1.06).
    # FX: Continuous bold sweeping cross-slash crescents of celestial sky blue #38A0FF and brass gold #FFD028,
    # with clean aerodynamic energy trails (zero stray noise dots).
    # =========================================================================
    atk_offsets = {
        "head_top": (18, 3),
        "ear_tip_l": (12, 5), "ear_tip_r": (10, 5),
        "ear_mid_l": (14, 4), "ear_mid_r": (12, 4),
        "cowl_cheek_l": (17, 3), "cowl_cheek_r": (16, 3),
        "optic_l": (19, 3), "optic_r": (19, 3), "optic_center": (19, 3),
        "snout_tip": (21, 4), "jaw_chin": (20, 4),
        "throat": (18, 3), "shoulder_l": (16, 2), "shoulder_r": (18, 2),
        "chest_center": (18, 2), "elbow_l": (14, 1), "elbow_r": (18, 1),
        "harness_hem": (16, 2),
        "tail_tip": (-4, -8), "tail_bend": (0, -4), "tail_mid": (4, -2), "tail_base": (8, 0),
        "pelvis": (10, 1),
        "thigh_l": (16, 0), "thigh_r": (2, 1),
        "knee_l": (18, 0), "knee_r": (2, 1),
        "foot_l": (16, 0), "foot_r": (0, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk, power=2.0, epsilon=4.0)

    atk_key = place_rotated_pivot(key_src, deg=68, pivot=KEY_PIVOT, target=(56, 26), scale=1.06)
    atk_l_dag = place_rotated_pivot(left_dag_img, deg=-45, pivot=LEFT_DAG_PIVOT, target=(52, 78), scale=1.0)
    atk_r_dag = place_rotated_pivot(right_dag_img, deg=35, pivot=RIGHT_DAG_PIVOT, target=(104, 66), scale=1.04)

    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Continuous bold curved crescent slashes
    # 1. Primary forward sky-blue slash arc sweeping from (74, 46) to (122, 86)
    a_draw.arc([70, 44, 122, 90], start=285, end=65, fill=(56, 160, 255, 240), width=3)
    a_draw.arc([72, 46, 120, 88], start=295, end=60, fill=(205, 238, 255, 255), width=1)
    # 2. Secondary gold parrying arc cutting back from (40, 68) to (78, 96)
    a_draw.arc([42, 66, 80, 98], start=140, end=260, fill=(255, 208, 40, 230), width=2)
    # 3. Aerodynamic motion streak lines under thrusting blade
    a_draw.line([(88, 62), (108, 62)], fill=(205, 238, 255, 180), width=1)
    a_draw.line([(92, 70), (116, 70)], fill=(56, 160, 255, 200), width=2)
    a_draw.line([(96, 76), (114, 76)], fill=(78, 216, 106, 180), width=1)
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.35))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas.alpha_composite(atk_key)
    atk_canvas.alpha_composite(warped_atk_body)
    atk_canvas.alpha_composite(atk_l_dag)
    atk_canvas.alpha_composite(atk_r_dag)
    atk_canvas.alpha_composite(atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. RECOVER (疾影折躍·落地緩衝回勢 / Agile Rebound & Stealth Recovery)
    # Spring rebound & grounded recoil brake: body steps back (-8, +4).
    # Head & radar ears tilt alertly (-8, +4).
    # Tail arches high in S-curve for stability (-10, -2).
    # Left dagger held horizontally across lower chest (-45 deg, target=(46, 73), scale=0.98).
    # Right dagger held defensively point-down (+30 deg, target=(85, 76), scale=0.98).
    # Winding key re-engages damper (+18 deg, target=(34, 32), scale=0.98).
    # FX: Mint cold-gas exhaust dissipation motes & amber radar sweep lines.
    # =========================================================================
    rec_offsets = {
        "head_top": (-8, 4),
        "ear_tip_l": (-8, 4), "ear_tip_r": (-8, 4),
        "ear_mid_l": (-8, 4), "ear_mid_r": (-8, 4),
        "cowl_cheek_l": (-8, 4), "cowl_cheek_r": (-8, 4),
        "optic_l": (-8, 4), "optic_r": (-8, 4), "optic_center": (-8, 4),
        "snout_tip": (-8, 4), "jaw_chin": (-8, 4),
        "throat": (-8, 4), "shoulder_l": (-9, 4), "shoulder_r": (-7, 4),
        "chest_center": (-8, 4), "elbow_l": (-9, 4), "elbow_r": (-6, 4),
        "harness_hem": (-7, 3),
        "tail_tip": (-10, -2), "tail_bend": (-10, 0), "tail_mid": (-9, 2), "tail_base": (-7, 3),
        "pelvis": (-6, 3),
        "thigh_l": (-6, 3), "thigh_r": (-2, 3),
        "knee_l": (-6, 2), "knee_r": (-1, 2),
        "foot_l": (-4, 0), "foot_r": (0, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec, power=2.0, epsilon=4.0)

    rec_key = place_rotated_pivot(key_src, deg=18, pivot=KEY_PIVOT, target=(34, 32), scale=0.98)
    rec_l_dag = place_rotated_pivot(left_dag_img, deg=-45, pivot=LEFT_DAG_PIVOT, target=(46, 73), scale=0.98)
    rec_r_dag = place_rotated_pivot(right_dag_img, deg=30, pivot=RIGHT_DAG_PIVOT, target=(85, 76), scale=0.98)

    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Cooling exhaust vapor particles
    for fx, fy in [(40, 114), (46, 115), (74, 115), (80, 114)]:
        r_draw.point((fx, fy), fill=(78, 216, 106, 230))
        r_draw.point((fx, fy - 1), fill=(195, 255, 215, 240))
    r_draw.line([(54, 46), (82, 46)], fill=(255, 160, 16, 160), width=1)
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas.alpha_composite(rec_key)
    rec_canvas.alpha_composite(warped_rec_body)
    rec_canvas.alpha_composite(rec_l_dag)
    rec_canvas.alpha_composite(rec_r_dag)
    rec_canvas.alpha_composite(rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    # =========================================================================
    # 5. SKILL (天體星環·軌道脈衝天頂爆發 / Astral Ring Orbit Burst Ultimate)
    # High mid-air leap & orbital ring release: body elevates upward (y - 10).
    # Spine extends, ears spread wide (ear_l -6, ear_r +6, y - 10).
    # Legs airborne, kicking symmetrically outward (knee_l -6, knee_r +6, y - 6).
    # Neon tail coils fully into glowing celestial halo around upper body (tail_tip +6, y - 8).
    # Daggers spread outward wide like celestial binary stars:
    # Left dagger raised to upper left (-65 deg, target=(32, 64), scale=1.04).
    # Right dagger raised to upper right (+55 deg, target=(98, 62), scale=1.04).
    # Winding key spins at turbine speed (+125 deg, target=(38, 16), scale=1.08).
    # FX: Multi-ring dopamine nebula burst (Sky Blue #38A0FF, Brass Gold #FFD028, Mint Green #4ED86A, Coral Pink #FF5E8A).
    # =========================================================================
    skill_offsets = {
        "head_top": (0, -10),
        "ear_tip_l": (-4, -10), "ear_tip_r": (4, -10),
        "ear_mid_l": (-3, -10), "ear_mid_r": (3, -10),
        "cowl_cheek_l": (-2, -10), "cowl_cheek_r": (2, -10),
        "optic_l": (-1, -10), "optic_r": (1, -10), "optic_center": (0, -10),
        "snout_tip": (0, -10), "jaw_chin": (0, -10),
        "throat": (0, -10), "shoulder_l": (-3, -10), "shoulder_r": (3, -10),
        "chest_center": (0, -10), "elbow_l": (-5, -9), "elbow_r": (5, -9),
        "harness_hem": (0, -9),
        "tail_tip": (8, -8), "tail_bend": (4, -9), "tail_mid": (2, -8), "tail_base": (0, -8),
        "pelvis": (0, -8),
        "thigh_l": (-4, -7), "thigh_r": (4, -7),
        "knee_l": (-6, -6), "knee_r": (6, -6),
        "foot_l": (-6, -4), "foot_r": (6, -4),
    }
    dst_skill = [(base_landmarks[k][0] + skill_offsets[k][0], base_landmarks[k][1] + skill_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skill_body = warp_image_idw(body_core, src_pts, dst_skill, power=2.0, epsilon=4.0)

    skill_key = place_rotated_pivot(key_src, deg=125, pivot=KEY_PIVOT, target=(38, 16), scale=1.08)
    skill_l_dag = place_rotated_pivot(left_dag_img, deg=-65, pivot=LEFT_DAG_PIVOT, target=(32, 64), scale=1.04)
    skill_r_dag = place_rotated_pivot(right_dag_img, deg=55, pivot=RIGHT_DAG_PIVOT, target=(98, 62), scale=1.04)

    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    # Giant concentric astral orbit rings centered at (64, 46)
    k_cx, k_cy = 64, 46
    s_draw.ellipse([k_cx - 40, k_cy - 28, k_cx + 40, k_cy + 28], outline=(56, 160, 255, 230), width=2)
    s_draw.ellipse([k_cx - 30, k_cy - 20, k_cx + 30, k_cy + 20], outline=(255, 208, 40, 230), width=1)
    s_draw.ellipse([k_cx - 18, k_cy - 12, k_cx + 18, k_cy + 12], outline=(78, 216, 106, 240), width=1)
    # Energy starburst rays
    for ray in [(k_cx - 48, k_cy), (k_cx + 48, k_cy), (k_cx, k_cy - 34), (k_cx, k_cy + 34)]:
        s_draw.line([(k_cx, k_cy), ray], fill=(255, 255, 255, 200), width=1)
    # Coral pink core spark
    s_draw.ellipse([k_cx - 3, k_cy - 3, k_cx + 3, k_cy + 3], fill=(255, 94, 138, 240), outline=(255, 255, 255, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.35))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas.alpha_composite(skill_key)
    skill_canvas.alpha_composite(warped_skill_body)
    skill_canvas.alpha_composite(skill_l_dag)
    skill_canvas.alpha_composite(skill_r_dag)
    skill_canvas.alpha_composite(skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 6. HIT (震盪過載·金屬裝甲格擋後挫 / Kinetic Shock & Stagger Defend)
    # Severe recoil & armor impact stagger: body jolts backward & tilts (-12, +2).
    # Head snaps backward (-14, -3).
    # Tail flings upward in alarmed tension (-14, -6).
    # Daggers knocked outward during impact parry:
    # Left dagger knocked downward (+50 deg, target=(34, 80), scale=0.94).
    # Right dagger knocked upward (-45 deg, target=(80, 68), scale=0.94).
    # Winding key jolted backward (-35 deg, target=(26, 26), scale=0.94).
    # FX: Kinetic impact sparks on chestplate & visor overload warning.
    # =========================================================================
    hit_offsets = {
        "head_top": (-14, -3),
        "ear_tip_l": (-14, -3), "ear_tip_r": (-14, -3),
        "ear_mid_l": (-14, -3), "ear_mid_r": (-14, -3),
        "cowl_cheek_l": (-14, -3), "cowl_cheek_r": (-14, -3),
        "optic_l": (-14, -3), "optic_r": (-14, -3), "optic_center": (-14, -3),
        "snout_tip": (-14, -3), "jaw_chin": (-14, -3),
        "throat": (-12, 0), "shoulder_l": (-13, 0), "shoulder_r": (-11, 0),
        "chest_center": (-12, 2), "elbow_l": (-12, 2), "elbow_r": (-9, 2),
        "harness_hem": (-10, 2),
        "tail_tip": (-14, -6), "tail_bend": (-14, -5), "tail_mid": (-12, -3), "tail_base": (-9, 0),
        "pelvis": (-8, 1),
        "thigh_l": (-8, 1), "thigh_r": (-4, 1),
        "knee_l": (-8, 1), "knee_r": (-3, 1),
        "foot_l": (-6, 0), "foot_r": (-2, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit, power=2.0, epsilon=4.0)

    hit_key = place_rotated_pivot(key_src, deg=-35, pivot=KEY_PIVOT, target=(26, 26), scale=0.94)
    hit_l_dag = place_rotated_pivot(left_dag_img, deg=50, pivot=LEFT_DAG_PIVOT, target=(34, 80), scale=0.94)
    hit_r_dag = place_rotated_pivot(right_dag_img, deg=-45, pivot=RIGHT_DAG_PIVOT, target=(80, 68), scale=0.94)

    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact sparks centered on chest armor (52, 74)
    ix, iy = 52, 74
    for pt in [(ix - 8, iy - 6), (ix + 8, iy - 6), (ix + 10, iy + 5), (ix - 7, iy + 8), (ix + 11, iy - 1), (ix - 9, iy + 1)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    for pt in [(ix - 5, iy - 3), (ix + 5, iy + 3), (ix + 3, iy - 5), (ix - 3, iy + 5)]:
        h_draw.point(pt, fill=(56, 160, 255, 240))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.35))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas.alpha_composite(hit_key)
    hit_canvas.alpha_composite(warped_hit_body)
    hit_canvas.alpha_composite(hit_l_dag)
    hit_canvas.alpha_composite(hit_r_dag)
    hit_canvas.alpha_composite(hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    return poses


def create_godot_import(png_path: str):
    """Creates standard Godot 4.x .import file for 2D pixel art sprite."""
    import_path = f"{png_path}.import"
    content = f"""[remap]

importer="texture"
type="CompressedTexture2D"
uid="uid://{abs(hash(png_path)):012x}"
path="res://.godot/imported/{os.path.basename(png_path)}-{abs(hash(png_path)):08x}.ctex"
metadata={{
"vram_texture": false
}}

[deps]

source_file="res://{os.path.relpath(png_path, f'{REPO_ROOT}/game')}"
dest_files=["res://.godot/imported/{os.path.basename(png_path)}-{abs(hash(png_path)):08x}.ctex"]

[params]

compress/mode=0
compress/high_quality=false
compress/lossy_quality=0.7
compress/hdr_compression=1
compress/normal_map=0
compress/channel_pack=0
mipmaps/generate=false
mipmaps/limit=-1
roughness/mode=0
roughness/src_normal=""
process/fix_alpha_border=true
process/premult_alpha=false
process/normal_map_invert_y=false
process/hdr_as_srgb=false
process/hdr_clamp_exposure=false
process/size_limit=0
detect_3d/compress_to=1
"""
    with open(import_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")


def main():
    print("Generating The Star-Ring Lemur combat action poses...")
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

    # Official battle asset: lemur_battle.png & lemur_battle_512.png (battle == attack per review.md 4b-8-1)
    battle_128 = poses["attack"]
    battle_512 = poses["attack"].resize((512, 512), Image.Resampling.LANCZOS)
    battle_path_128 = f"{PLAYER_DIR}/lemur_battle.png"
    battle_path_512 = f"{PLAYER_DIR}/lemur_battle_512.png"
    battle_128.save(battle_path_128)
    battle_512.save(battle_path_512)
    print(f"  ✓ Saved {PLAYER_DIR}/lemur_battle.png & lemur_battle_512.png (battle == attack)")

    # Proof: Idle vs Battle (128 & 512)
    idle_128 = poses["idle"]
    ivb_128 = Image.new("RGBA", (256, 128), (0, 0, 0, 0))
    ivb_128.paste(idle_128, (0, 0))
    ivb_128.paste(battle_128, (128, 0))
    ivb_path_128 = f"{PLAYER_DIR}/proof_lemur_idle_vs_battle.png"
    ivb_128.save(ivb_path_128)

    ivb_512 = Image.new("RGBA", (1024, 512), (0, 0, 0, 0))
    ivb_512.paste(poses["idle"].resize((512, 512), Image.Resampling.LANCZOS), (0, 0))
    ivb_512.paste(battle_512, (512, 0))
    ivb_path_512 = f"{PLAYER_DIR}/proof_lemur_idle_vs_battle_512.png"
    ivb_512.save(ivb_path_512)

    # Proof: 768x128 Transparent & Magenta contact sheets
    proof_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(['idle', 'telegraph', 'attack', 'recover', 'skill', 'hit']):
        proof_768.paste(poses[p_name], (i * 128, 0))
        proof_mag.alpha_composite(poses[p_name], (i * 128, 0))

    p768_path = f"{PLAYER_DIR}/proof_lemur_combat_poses_768.png"
    pmag_path = f"{PLAYER_DIR}/proof_lemur_combat_poses_magenta.png"
    proof_768.save(p768_path)
    proof_mag.save(pmag_path)
    print(f"  ✓ Saved {p768_path} & {pmag_path}")

    # Proof: 0-QA31 Hit Optic Core 8x Crop (crop around amber visors in hit stance)
    hit_arr = np.array(poses["hit"])
    # Visor in hit stance is around (50, 40)
    hit_crop = poses["hit"].crop((34, 28, 74, 56))
    hit_crop_8x = hit_crop.resize((hit_crop.width * 8, hit_crop.height * 8), Image.Resampling.NEAREST)
    hc_path = f"{PLAYER_DIR}/proof_lemur_hit_core_crop_8x.png"
    hit_crop_8x.save(hc_path)
    print(f"  ✓ Saved {hc_path} (8x Nearest neighbor crop for 0-QA31)")

    print("\nAll 6 combat poses, battle立繪, and proof assets generated successfully!")


if __name__ == "__main__":
    main()
