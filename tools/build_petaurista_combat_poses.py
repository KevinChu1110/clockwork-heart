#!/usr/bin/env python3
"""
tools/build_petaurista_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Stormwing Petaurista (第五十八族 嵐翼鼯鼠, petaurista)
in Clockwork Heart:
  game/assets/sprites/player/poses/petaurista/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/petaurista/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates:
  - 0-QA16 / 0-QA21 / 0-QA31 / 0-QA34
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
Features:
  - Lacquered bamboo default chassis & cold-rolled brass joints
  - Zen bamboo ninja cowl with bamboo-leaf sonar ears
  - Obsidian goggle cinnabar mask optic core
  - Folding glider wing harness with bamboo battens
  - Segmented bamboo-weave rudder tail
  - Three-leaf windchime brass winding key
  - Zen octagonal bamboo shuriken dart
"""

import math
import os
import sys
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

# Ensure clean imports
sys.path = [p for p in sys.path if not p.startswith('/tmp')]

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/petaurista"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/petaurista"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_petaurista_three_leaf_windchime_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_petaurista_bamboo_weave_rudder_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_petaurista_lacquered_bamboo_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_petaurista_zen_bamboo_ninja_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_petaurista_folding_glider_wing_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_petaurista_obsidian_goggle_cinnabar_mask.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_petaurista_zen_octagonal_bamboo_dart.png").convert("RGBA")

# Extract ground shadow master from party petaurista_idle.png
ref_shadow_im = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/petaurista_idle.png").convert("RGBA")
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

    # Sanitize dark falloff (ultra-dark pixels)
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


def warp_image_idw(src_img: Image.Image, src_points: list[tuple[int, int]], dst_points: list[tuple[int, int]], power: float = 2.0, epsilon: float = 5.0) -> Image.Image:
    """Smooth Inverse Distance Weighting (IDW) landmark warp for organic/mechanical body distortion."""
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


# Anchors ensuring edge stability
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127),
    (32, 0), (96, 0), (0, 32), (0, 96),
    (127, 32), (127, 96),
]

# Canonical landmarks on Petaurista
base_landmarks = {
    # Head / Cowl / Bamboo Ears
    "cowl_top": (64, 14),
    "ear_tip_l": (42, 8),
    "ear_tip_r": (86, 8),
    "cowl_cheek_l": (44, 34),
    "cowl_cheek_r": (84, 34),
    "visor_brow": (64, 36),
    "optic_l": (53, 43),
    "optic_r": (75, 43),
    "cinnabar_mark": (64, 43),
    "snout": (64, 50),
    "chin": (64, 56),
    # Torso & Folding Glider Wings
    "throat": (64, 58),
    "shoulder_l": (46, 64),
    "shoulder_r": (82, 64),
    "chest_harness": (64, 68),
    "wing_l": (30, 72),
    "wing_r": (92, 72),
    "hand_r": (88, 68),
    "buckle": (64, 82),
    # Tail (Segmented Bamboo Weave Rudder Tail)
    "tail_root": (50, 82),
    "tail_mid": (28, 80),
    "tail_tip": (10, 76),
    # Pelvis & Legs
    "pelvis": (64, 92),
    "hip_l": (48, 96),
    "hip_r": (80, 96),
    "knee_l": (48, 104),
    "knee_r": (80, 104),
    "foot_l": (48, 112),
    "foot_r": (80, 112),
}

src_pts = [base_landmarks[k] for k in base_landmarks] + anchors

# Canonical pivots
KEY_PIVOT = (40.5, 32.8)
WEAPON_PIVOT = (103.6, 67.6)

# Build base body_core without weapon & key (z: curio=8, chassis=10, head=20, costume=25, optic=30)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (待機姿態)
    # Balanced ninja readiness. Exact baseline layered composite.
    # Winding key placed at (40.5, 32.8).
    # Dart placed at (103.6, 67.6).
    # =========================================================================
    idle_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(40.5, 32.8), scale=1.0)
    idle_weapon = place_rotated_pivot(weapon_src, deg=0, pivot=WEAPON_PIVOT, target=(103.6, 67.6), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas.alpha_composite(idle_key)
    idle_canvas.alpha_composite(body_core)
    idle_canvas.alpha_composite(idle_weapon)

    # Ambient subtle zen bamboo glint FX on obsidian lens and brass key
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    i_draw.point((53, 42), fill=(255, 255, 255, 230))
    i_draw.point((75, 42), fill=(255, 255, 255, 230))
    i_draw.point((40, 24), fill=(255, 208, 40, 220))
    i_draw.point((104, 68), fill=(255, 208, 40, 220))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas.alpha_composite(idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (暗忍蓄勁·竹風鎖定 / Zen Windup & Slipstream Lock)
    # Deep ninja crouch: head & torso sink down and coil back (-4, +6).
    # Winding key counter-winds with tension (-32 deg, target=(37, 39)).
    # Shuriken dart pulled back into throwing position (-28 deg, target=(96, 62)).
    # Tail arches upward (+4, -7) for aerodynamic tension.
    # FX: Wind chime resonance wave, spring tension arc, green/gold wind vortex sparks.
    # =========================================================================
    tele_offsets = {
        "cowl_top": (-4, 6), "ear_tip_l": (-4, 6), "ear_tip_r": (-4, 6),
        "cowl_cheek_l": (-4, 6), "cowl_cheek_r": (-4, 6),
        "visor_brow": (-4, 6), "optic_l": (-4, 6), "optic_r": (-4, 6),
        "cinnabar_mark": (-4, 6), "snout": (-4, 6), "chin": (-4, 6),
        "throat": (-3, 5), "shoulder_l": (-4, 5), "shoulder_r": (-3, 5),
        "chest_harness": (-3, 5), "wing_l": (-2, 5), "wing_r": (-5, 3),
        "hand_r": (-8, -4), "buckle": (-3, 4),
        "tail_root": (-2, 4), "tail_mid": (0, -3), "tail_tip": (4, -7),
        "pelvis": (-2, 4), "hip_l": (-3, 4), "hip_r": (-1, 4),
        "knee_l": (-2, 3), "knee_r": (-1, 3),
        "foot_l": (-1, 0), "foot_r": (1, 0),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele, power=2.0, epsilon=4.0)
    tele_key = place_rotated_pivot(key_src, deg=-32, pivot=KEY_PIVOT, target=(37, 39), scale=1.0)
    tele_weapon = place_rotated_pivot(weapon_src, deg=-28, pivot=WEAPON_PIVOT, target=(96, 62), scale=1.04)

    # Mechanical tension & bamboo wind vortex FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Shuriken tension arc around dart at (96, 62)
    t_draw.arc([82, 48, 110, 76], start=200, end=340, fill=(78, 216, 106, 230), width=1)
    t_draw.arc([84, 50, 108, 74], start=210, end=330, fill=(255, 208, 40, 220), width=1)
    # Windchime soundwave rings at key (37, 39)
    for sx, sy in [(35, 26), (30, 20), (42, 22), (24, 25), (46, 24)]:
        t_draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 253, 248, 200))
        t_draw.point((sx, sy), fill=(78, 216, 106, 240))
    # Bamboo spark points at right hand
    for sx, sy in [(92, 58), (98, 54), (88, 66), (94, 64)]:
        t_draw.point((sx, sy), fill=(255, 208, 40, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.35))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas.alpha_composite(tele_key)
    tele_canvas.alpha_composite(warped_tele_body)
    tele_canvas.alpha_composite(tele_weapon)
    tele_canvas.alpha_composite(tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (八卦疾旋·破空旋鏢突刺 / Bagua Shuriken Ricochet Thrust)
    # Dynamic forward lunge (+13, -1): body springs forward in agile ninja lunge.
    # Right arm thrusts forward, launching Octagonal Bamboo Dart (+45 deg, target=(106, 64), scale 1.08).
    # Three-leaf brass key spins rapidly (+52 deg, target=(53, 31)).
    # Rudder tail sweeps back (-6, +2) to counterbalance forward momentum.
    # FX: Slicing bamboo green blades, golden centrifugal blur trails, wind shockwave.
    # =========================================================================
    atk_offsets = {
        "cowl_top": (13, -1), "ear_tip_l": (12, -1), "ear_tip_r": (14, -1),
        "cowl_cheek_l": (13, -1), "cowl_cheek_r": (13, -1),
        "visor_brow": (13, -1), "optic_l": (13, -1), "optic_r": (13, -1),
        "cinnabar_mark": (13, -1), "snout": (13, -1), "chin": (13, -1),
        "throat": (13, -1), "shoulder_l": (13, -1), "shoulder_r": (11, 0),
        "chest_harness": (12, 0), "wing_l": (12, -2), "wing_r": (14, -2),
        "hand_r": (22, -5), "buckle": (11, 0),
        "tail_root": (8, 0), "tail_mid": (-1, 2), "tail_tip": (-6, 3),
        "pelvis": (9, 0), "hip_l": (9, -1), "hip_r": (0, 0),
        "knee_l": (7, -1), "knee_r": (-1, 0),
        "foot_l": (7, 0), "foot_r": (-2, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk, power=2.0, epsilon=4.0)
    atk_key = place_rotated_pivot(key_src, deg=52, pivot=KEY_PIVOT, target=(53, 31), scale=1.0)
    atk_weapon = place_rotated_pivot(weapon_src, deg=45, pivot=WEAPON_PIVOT, target=(106, 64), scale=1.08)

    # High-speed cutting arc & ricochet spark FX
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Piercing shuriken flight laser beam
    a_draw.line([(86, 66), (120, 62)], fill=(255, 208, 40, 245), width=2)
    a_draw.line([(94, 65), (120, 62)], fill=(255, 255, 255, 255), width=1)
    # Cutting vortex arcs around shuriken
    a_draw.arc([90, 48, 120, 78], start=290, end=70, fill=(78, 216, 106, 235), width=2)
    a_draw.arc([92, 50, 118, 76], start=300, end=60, fill=(255, 253, 248, 220), width=1)
    # Forward thrust wind ribbons
    for wy in [52, 60, 72]:
        a_draw.line([(70, wy), (92, wy - 3)], fill=(78, 216, 106, 180), width=1)
    # Bamboo impact particles
    for sx, sy in [(114, 56), (118, 68), (112, 72), (108, 52), (121, 62)]:
        a_draw.point((sx, sy), fill=(255, 208, 40, 255))
        a_draw.point((sx - 1, sy), fill=(255, 255, 255, 240))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.35))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas.alpha_composite(atk_key)
    atk_canvas.alpha_composite(warped_atk_body)
    atk_canvas.alpha_composite(atk_weapon)
    atk_canvas.alpha_composite(atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (奧義技能·風嵐凌空八卦刃 / Stormwing Aerial Bagua Vortex)
    # Airborne flight glide stance! Body leaps upward into storm draft (y-11).
    # Glider wings deploy laterally (airfoil expansion wing_l -9, wing_r +8).
    # Rudder tail fans wide and down (dy+5).
    # Shuriken charged and held aloft in mid-air bagua vortex (+80 deg, target=(92, 54), scale 1.15).
    # Three-leaf key overcharges in storm wind (+95 deg, target=(40, 22), scale 1.06).
    # FX: Zen octagonal bagua energy ring, swirling emerald bamboo leaves, wind chime rings.
    # =========================================================================
    skl_offsets = {
        "cowl_top": (0, -11), "ear_tip_l": (-2, -12), "ear_tip_r": (2, -12),
        "cowl_cheek_l": (-2, -11), "cowl_cheek_r": (2, -11),
        "visor_brow": (0, -11), "optic_l": (-1, -11), "optic_r": (1, -11),
        "cinnabar_mark": (0, -11), "snout": (0, -11), "chin": (0, -10),
        "throat": (0, -9), "shoulder_l": (-4, -9), "shoulder_r": (4, -9),
        "chest_harness": (0, -9), "wing_l": (-9, -8), "wing_r": (8, -8),
        "hand_r": (4, -14), "buckle": (0, -7),
        "tail_root": (0, -4), "tail_mid": (-3, 1), "tail_tip": (-5, 5),
        "pelvis": (0, -5), "hip_l": (-2, -4), "hip_r": (2, -4),
        "knee_l": (-2, -3), "knee_r": (2, -3),
        "foot_l": (-2, -2), "foot_r": (2, -2),
    }
    dst_skl = [(base_landmarks[k][0] + skl_offsets[k][0], base_landmarks[k][1] + skl_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skl_body = warp_image_idw(body_core, src_pts, dst_skl, power=2.0, epsilon=4.0)
    skl_key = place_rotated_pivot(key_src, deg=95, pivot=KEY_PIVOT, target=(40, 22), scale=1.06)
    skl_weapon = place_rotated_pivot(weapon_src, deg=80, pivot=WEAPON_PIVOT, target=(92, 54), scale=1.15)

    # Bagua sacred ring & swirling bamboo vortex FX
    skl_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skl_fx)
    # Sacred bagua octagonal energy halo around shuriken at (92, 54)
    cx, cy = 92, 54
    for r in [20, 26]:
        pts = []
        for a_step in range(8):
            ang = math.radians(a_step * 45 + 22.5)
            pts.append((int(round(cx + r * math.cos(ang))), int(round(cy + r * math.sin(ang)))))
        s_draw.polygon(pts, outline=(78, 216, 106, 210), width=1)
    # Central golden core
    s_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 253, 248, 240))
    s_draw.point((cx, cy), fill=(255, 208, 40, 255))
    # Swirling bamboo gale stream
    for sang, srad in [(30, 32), (90, 34), (150, 31), (210, 33), (270, 35), (330, 32)]:
        rad = math.radians(sang)
        bx = int(round(cx + srad * math.cos(rad)))
        by = int(round(cy + srad * math.sin(rad)))
        if 4 <= bx <= 123 and 4 <= by <= 116:
            s_draw.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=(255, 208, 40, 230))
            s_draw.point((bx, by), fill=(255, 255, 255, 255))
    skl_fx = skl_fx.filter(ImageFilter.GaussianBlur(0.35))

    skl_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skl_canvas.alpha_composite(skl_key)
    skl_canvas.alpha_composite(warped_skl_body)
    skl_canvas.alpha_composite(skl_weapon)
    skl_canvas.alpha_composite(skl_fx)
    poses["skill"] = enforce_ground_shadow(skl_canvas)

    # =========================================================================
    # 5. HIT (衝擊受創·竹甲抗震後仰 / Stormwind Impact Shock)
    # Violent impact: body snaps back and up (x-14, y-5).
    # Head and cowl snap back: dx = -14, dy = -5.
    # Winding key recoils jarred: deg = -38, target = (28, 30), scale = 0.96.
    # Weapon knocked loose / jarred: deg = -35, target = (88, 76), scale = 0.96.
    # Feet slide back: foot_l (-3, 0), foot_r (-1, 0).
    # FX: Impact sparks (white/yellow/coral), cracked barrier ripple, bamboo fragments.
    # =========================================================================
    hit_offsets = {
        "cowl_top": (-14, -5), "ear_tip_l": (-15, -5), "ear_tip_r": (-13, -5),
        "cowl_cheek_l": (-14, -5), "cowl_cheek_r": (-13, -5),
        "visor_brow": (-14, -5), "optic_l": (-14, -5), "optic_r": (-13, -5),
        "cinnabar_mark": (-14, -5), "snout": (-14, -4), "chin": (-14, -4),
        "throat": (-13, -3), "shoulder_l": (-13, -3), "shoulder_r": (-10, -3),
        "chest_harness": (-12, -3), "wing_l": (-11, -3), "wing_r": (-8, -2),
        "hand_r": (-10, 4), "buckle": (-10, -2),
        "tail_root": (-7, 0), "tail_mid": (-6, 2), "tail_tip": (-4, 4),
        "pelvis": (-8, 0), "hip_l": (-7, 0), "hip_r": (-5, 0),
        "knee_l": (-4, 0), "knee_r": (-2, 0),
        "foot_l": (-3, 0), "foot_r": (-1, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit, power=2.0, epsilon=4.0)
    hit_key = place_rotated_pivot(key_src, deg=-38, pivot=KEY_PIVOT, target=(28, 30), scale=0.96)
    hit_weapon = place_rotated_pivot(weapon_src, deg=-35, pivot=WEAPON_PIVOT, target=(88, 76), scale=0.96)

    # Impact shockwave & fragment spark FX
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact center on chest (52, 65)
    ix, iy = 52, 65
    # Cracked kinetic barrier lines
    h_draw.line([(ix - 12, iy - 8), (ix, iy), (ix + 10, iy + 6)], fill=(255, 255, 255, 240), width=1)
    h_draw.line([(ix - 4, iy + 10), (ix, iy), (ix + 12, iy - 6)], fill=(255, 94, 138, 220), width=1)
    # Impact sparks & bamboo splinters
    for pt in [(ix - 14, iy - 10), (ix + 12, iy - 12), (ix + 14, iy + 8), (ix - 10, iy + 12), (ix + 16, iy - 2)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.35))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas.alpha_composite(hit_key)
    hit_canvas.alpha_composite(warped_hit_body)
    hit_canvas.alpha_composite(hit_weapon)
    hit_canvas.alpha_composite(hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (受身復原·三點落地架勢 / Three-Point Bamboo Recovery Stance)
    # Low grounded landing crouch: body bows forward, absorbs shock (+1, +7).
    # Head and cowl sink down: dx = +1, dy = +7.
    # Torso and wings compress: dx = +1, dy = +6.
    # Winding key re-engages into main drive (+12 deg, target=(41, 41), scale 0.98).
    # Tail sweeps along the ground to arrest skid (+1, +4 root, -3, +4 mid, -6, +4 tip).
    # Weapon gathered close defensively: deg = -12, target = (96, 75), scale = 1.0.
    # Feet plant wide in deep crouch (foot_l -2, foot_r +2).
    # FX: Ground dust/steam ring, brake friction sparks on floor, bamboo stabilizing aura.
    # =========================================================================
    rec_offsets = {
        "cowl_top": (1, 7), "ear_tip_l": (1, 7), "ear_tip_r": (1, 7),
        "cowl_cheek_l": (1, 7), "cowl_cheek_r": (1, 7),
        "visor_brow": (1, 7), "optic_l": (1, 7), "optic_r": (1, 7),
        "cinnabar_mark": (1, 7), "snout": (1, 7), "chin": (1, 7),
        "throat": (1, 6), "shoulder_l": (0, 6), "shoulder_r": (2, 6),
        "chest_harness": (1, 6), "wing_l": (2, 5), "wing_r": (1, 5),
        "hand_r": (-2, 6), "buckle": (1, 5),
        "tail_root": (1, 4), "tail_mid": (-3, 4), "tail_tip": (-6, 4),
        "pelvis": (1, 4), "hip_l": (-3, 3), "hip_r": (3, 3),
        "knee_l": (-3, 2), "knee_r": (3, 2),
        "foot_l": (-2, 0), "foot_r": (2, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec, power=2.0, epsilon=4.0)
    rec_key = place_rotated_pivot(key_src, deg=12, pivot=KEY_PIVOT, target=(41, 41), scale=0.98)
    rec_weapon = place_rotated_pivot(weapon_src, deg=-12, pivot=WEAPON_PIVOT, target=(96, 75), scale=1.0)

    # Restabilizing brake sparks and steam puffs
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Steam pressure puffs at key
    for sx, sy in [(38, 28), (32, 24), (44, 22)]:
        r_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 210))
        r_draw.point((sx, sy), fill=(78, 216, 106, 240))
    # Gear re-mesh spark at key mount
    r_draw.line([(38, 35), (44, 41)], fill=(255, 208, 40, 230), width=1)
    r_draw.line([(44, 35), (38, 41)], fill=(255, 255, 255, 255), width=1)
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas.alpha_composite(rec_key)
    rec_canvas.alpha_composite(warped_rec_body)
    rec_canvas.alpha_composite(rec_weapon)
    rec_canvas.alpha_composite(rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def main():
    print("Generating The Stormwing Petaurista combat action poses...")
    poses = generate_poses()

    for p_name in ['idle', 'telegraph', 'attack', 'recover', 'skill', 'hit']:
        im = poses[p_name]
        path_128 = f"{OUT_DIR}/{p_name}.png"
        im.save(path_128)
        print(f"  ✓ Saved 128x128: {path_128}")

        # Generate 512x512 with LANCZOS
        im_512 = im.resize((512, 512), resample=Image.Resampling.LANCZOS)
        path_512 = f"{OUT_DIR}/{p_name}_512.png"
        im_512.save(path_512)
        print(f"  ✓ Saved 512x512 LANCZOS: {path_512}")

    # 3. Generate 768x128 composite proof sheet (idle, telegraph, attack, skill, hit, recover)
    proof_strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_order = ['idle', 'telegraph', 'attack', 'skill', 'hit', 'recover']
    for idx, p_name in enumerate(proof_order):
        proof_strip.paste(poses[p_name], (idx * 128, 0), poses[p_name])

    proof_768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_petaurista_combat_poses_768.png"
    proof_strip.save(proof_768_path)
    print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

    # 4. Generate 768x128 magenta background proof sheet for hole detection
    proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    proof_magenta.paste(proof_strip, (0, 0), proof_strip)
    proof_mag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_petaurista_combat_poses_magenta.png"
    proof_magenta.save(proof_mag_path)
    print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")

    # 5. Crop 8x hit core for 0-QA31
    hit_512 = poses["hit"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    core_crop = hit_512.crop((50 * 4, 55 * 4, 75 * 4, 80 * 4))
    crop_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_petaurista_hit_core_crop_8x.png"
    core_crop.save(crop_path)
    print(f"  ✓ Saved 0-QA31 core crop: {crop_path}")


if __name__ == "__main__":
    main()
