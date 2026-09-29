#!/usr/bin/env python3
"""
tools/build_walrus_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Icebreaker Walrus (第六十二族 破冰海象, walrus)
in Clockwork Heart:
  game/assets/sprites/player/poses/walrus/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/walrus/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Also generates:
  game/assets/sprites/player/walrus_battle.png & walrus_battle_512.png (battle == attack per review.md 4b-8-1)
  game/assets/sprites/player/proof_walrus_idle_vs_battle.png & proof_walrus_idle_vs_battle_512.png
  game/assets/sprites/player/proof_walrus_combat_poses_768.png & proof_walrus_combat_poses_magenta.png
  game/assets/sprites/player/proof_walrus_hit_core_crop_8x.png
Follows CANON.md, art_direction.md, ICEBREAKER_WALRUS_DESIGN_PROPOSAL.md, and review.md quality gates:
  - 0-QA16 / 0-QA21 / 0-QA31 / 0-QA34
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
Features:
  - Titanium alloy pressure hull chassis with round flipper treads
  - Dual forged cold-rolled tungsten icebreaker tusks cowl & flexible sonar whiskers
  - Pressure-proof quartz dome optic core with emerald/marine luminosity
  - Abyssal navigator peacoat cuirass with brass anchor buttons & sunset orange trim
  - Dual abyssal decompression ballast tanks & anti-rust oil reservoir curio
  - Dual-fluke anchor handwheel brass winding key
  - Abyssal icebreaker cutlass (heavy single-handed broadsword for Knight class)
"""

import math
import os
import sys
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageFont
import numpy as np

# Ensure clean imports
sys.path = [p for p in sys.path if not p.startswith('/tmp')]

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/walrus"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/walrus"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PLAYER_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_walrus_anchor_handwheel_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_walrus_dual_ballast_tanks.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_walrus_icebreaker_alloy_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_walrus_tungsten_tusk_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_walrus_abyssal_peacoat_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_walrus_quartz_dome_eyes.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_walrus_abyssal_icebreaker_cutlass.png").convert("RGBA")

# Extract ground shadow master from party walrus_idle.png
ref_shadow_im = Image.open(f"{PLAYER_DIR}/party/walrus_idle.png").convert("RGBA")
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

# Canonical landmarks on Walrus (natural 128x128 space)
base_landmarks = {
    # Head & Dual Tungsten Tusks Cowl
    "cowl_top": (64, 24),
    "cowl_crest_l": (48, 28),
    "cowl_crest_r": (80, 28),
    "cowl_cheek_l": (40, 48),
    "cowl_cheek_r": (88, 48),
    "optic_l": (54, 42),
    "optic_r": (74, 42),
    "snout": (64, 48),
    "whisker_l": (44, 58),
    "whisker_r": (84, 58),
    "tusk_root_l": (52, 60),
    "tusk_root_r": (76, 60),
    "tusk_tip_l": (50, 85),
    "tusk_tip_r": (78, 85),
    # Torso & Peacoat Cuirass
    "throat": (64, 56),
    "shoulder_l": (46, 62),
    "shoulder_r": (82, 62),
    "peacoat_chest": (64, 72),
    "flipper_l": (38, 80),
    "flipper_r": (90, 82),
    "peacoat_hem": (64, 94),
    # Curio (Dual Ballast Tanks) & Chassis
    "curio_top": (35, 36),
    "curio_mid": (35, 62),
    "curio_base": (38, 82),
    "pelvis": (64, 96),
    # Legs & Flipper Feet
    "hip_l": (48, 102),
    "hip_r": (80, 102),
    "knee_l": (48, 110),
    "knee_r": (80, 110),
    "foot_l": (48, 118),
    "foot_r": (80, 118),
}

src_pts = [base_landmarks[k] for k in base_landmarks] + anchors

# Canonical pivots on original 128x128 elements
KEY_PIVOT = (42.3, 33.8)
WEAPON_PIVOT = (88.0, 84.0)

# Build base body_core (z: curio=8, chassis=10, head=20, costume=25, optic=30)
# Note: key and weapon are articulated separately
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
    # 1. IDLE (深淵破冰·耐壓騎士待機站姿 / Abyssal Neutral Knight Readiness)
    # Balanced 2.2-head walrus knight stance.
    # Key placed at (42.3, 33.8).
    # Cutlass ready at (88.0, 84.0).
    # =========================================================================
    idle_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(42.3, 33.8), scale=1.0)
    idle_weapon = place_rotated_pivot(weapon_src, deg=0, pivot=WEAPON_PIVOT, target=(88.0, 84.0), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas.alpha_composite(idle_key)
    idle_canvas.alpha_composite(body_core)
    idle_canvas.alpha_composite(idle_weapon)

    # Ambient subtle glint FX on quartz dome eye and cutlass blade edge
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    i_draw.point((54, 42), fill=(255, 255, 255, 240))
    i_draw.point((74, 42), fill=(255, 255, 255, 240))
    i_draw.point((96, 44), fill=(255, 253, 248, 250))
    i_draw.point((92, 54), fill=(56, 160, 255, 220))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas.alpha_composite(idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (壓載增壓·破冰蓄勢預備姿態 / Pressure Coiling & Blade Charge)
    # Low knight coil: body drops and coils backward (-8, +8).
    # Head and tusks tuck in defensively.
    # Winding key counter-winds with high spring torque (-46 deg, target=(32, 44), scale=0.92).
    # Cutlass drawn back close to hip (-36 deg, target=(76, 80), scale=0.96).
    # FX: Soft turquoise pressure ripple arcs, steam micro-bubbles from ballast vents.
    # =========================================================================
    tele_offsets = {
        "cowl_top": (-8, 8), "cowl_crest_l": (-8, 8), "cowl_crest_r": (-8, 8),
        "cowl_cheek_l": (-8, 8), "cowl_cheek_r": (-8, 8),
        "optic_l": (-8, 8), "optic_r": (-8, 8),
        "snout": (-8, 8), "whisker_l": (-8, 7), "whisker_r": (-8, 7),
        "tusk_root_l": (-8, 8), "tusk_root_r": (-8, 8),
        "tusk_tip_l": (-7, 8), "tusk_tip_r": (-7, 8),
        "throat": (-7, 7), "shoulder_l": (-8, 7), "shoulder_r": (-6, 7),
        "peacoat_chest": (-7, 7), "flipper_l": (-7, 6), "flipper_r": (-9, 2),
        "peacoat_hem": (-6, 6),
        "curio_top": (-7, 7), "curio_mid": (-6, 6), "curio_base": (-6, 5),
        "pelvis": (-5, 5), "hip_l": (-5, 5), "hip_r": (-2, 5),
        "knee_l": (-5, 4), "knee_r": (1, 4),
        "foot_l": (-2, 0), "foot_r": (1, 0),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele, power=2.0, epsilon=4.0)
    tele_key = place_rotated_pivot(key_src, deg=-46, pivot=KEY_PIVOT, target=(32, 44), scale=0.92)
    tele_weapon = place_rotated_pivot(weapon_src, deg=-36, pivot=WEAPON_PIVOT, target=(76, 80), scale=0.96)

    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Pressure concentric arcs around drawn back blade
    t_draw.arc([60, 60, 94, 94], start=150, end=340, fill=(56, 160, 255, 220), width=2)
    t_draw.arc([64, 64, 90, 90], start=170, end=320, fill=(78, 216, 106, 210), width=1)
    # Micro-bubbles motes from ballast vent (top of curio)
    for bx, by in [(24, 40), (20, 34), (28, 30), (18, 44)]:
        t_draw.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=(255, 253, 248, 180))
        t_draw.point((bx, by), fill=(56, 160, 255, 240))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.35))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas.alpha_composite(tele_key)
    tele_canvas.alpha_composite(warped_tele_body)
    tele_canvas.alpha_composite(tele_weapon)
    tele_canvas.alpha_composite(tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (破冰重劈·厚刃海軍短闊劍突斬 / Abyssal Cutlass Breaker Cleave)
    # Heavy knight forward lunging cleave: body surges forward (+15, -1).
    # Cutlass sweeps forward with high impact momentum (+48 deg, target=(100, 72), scale=1.18).
    # Winding key spins clockwise releasing torque (+64 deg, target=(56, 32), scale=1.06).
    # FX: Sweeping cyan/gold hydrodynamic cleave wake & tusk resonance sparks.
    # =========================================================================
    atk_offsets = {
        "cowl_top": (15, -1), "cowl_crest_l": (15, -1), "cowl_crest_r": (15, -1),
        "cowl_cheek_l": (15, -1), "cowl_cheek_r": (15, -1),
        "optic_l": (15, -1), "optic_r": (15, -1),
        "snout": (15, -1), "whisker_l": (15, -1), "whisker_r": (15, -1),
        "tusk_root_l": (15, -1), "tusk_root_r": (15, -1),
        "tusk_tip_l": (16, 0), "tusk_tip_r": (16, 0),
        "throat": (14, -1), "shoulder_l": (12, -1), "shoulder_r": (15, -1),
        "peacoat_chest": (14, -1), "flipper_l": (9, 0), "flipper_r": (16, -2),
        "peacoat_hem": (12, 0),
        "curio_top": (10, -1), "curio_mid": (10, 0), "curio_base": (10, 0),
        "pelvis": (10, -1), "hip_l": (7, 0), "hip_r": (12, 0),
        "knee_l": (3, 0), "knee_r": (10, 0),
        "foot_l": (1, 0), "foot_r": (9, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk, power=2.0, epsilon=4.0)
    atk_key = place_rotated_pivot(key_src, deg=64, pivot=KEY_PIVOT, target=(56, 32), scale=1.06)
    atk_weapon = place_rotated_pivot(weapon_src, deg=48, pivot=WEAPON_PIVOT, target=(100, 72), scale=1.18)

    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Piercing sweeping cyan-orange cleave arc
    a_draw.arc([68, 26, 122, 98], start=280, end=85, fill=(56, 160, 255, 235), width=2)
    a_draw.arc([72, 30, 118, 94], start=295, end=70, fill=(255, 160, 16, 220), width=1)
    a_draw.arc([76, 34, 114, 90], start=305, end=60, fill=(255, 208, 40, 210), width=1)
    # Impact glint points at blade tip and tusk edge
    for px, py in [(114, 48), (120, 58), (116, 68), (110, 76), (118, 62)]:
        a_draw.point((px, py), fill=(255, 253, 248, 255))
        a_draw.point((px + 1, py), fill=(56, 160, 255, 240))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.35))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas.alpha_composite(atk_key)
    atk_canvas.alpha_composite(warped_atk_body)
    atk_canvas.alpha_composite(atk_weapon)
    atk_canvas.alpha_composite(atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (深淵鎮海·壓載全開破冰屏障 / Abyssal Aegis & Hydrodynamic Barrier)
    # Heroic elevated knight skill stance!
    # Head and tusks tilt high up (x=0, y=-12).
    # Torso elevates proudly (x=0, y=-8), pelvis lifts (x=0, y=-4).
    # Cutlass raised vertically overhead (+74 deg, target=(86, 52), scale=1.20).
    # Winding key overclocks (+90 deg, target=(42, 22), scale=1.08).
    # FX: Concentric hydrodynamic barrier halo, ballast vent bubble geysers.
    # =========================================================================
    skl_offsets = {
        "cowl_top": (0, -12), "cowl_crest_l": (0, -12), "cowl_crest_r": (0, -12),
        "cowl_cheek_l": (0, -11), "cowl_cheek_r": (0, -11),
        "optic_l": (0, -11), "optic_r": (0, -11),
        "snout": (0, -10), "whisker_l": (0, -10), "whisker_r": (0, -10),
        "tusk_root_l": (0, -10), "tusk_root_r": (0, -10),
        "tusk_tip_l": (0, -9), "tusk_tip_r": (0, -9),
        "throat": (0, -8), "shoulder_l": (-1, -8), "shoulder_r": (1, -8),
        "peacoat_chest": (0, -8), "flipper_l": (-4, -7), "flipper_r": (4, -12),
        "peacoat_hem": (0, -6),
        "curio_top": (-2, -8), "curio_mid": (0, -7), "curio_base": (0, -6),
        "pelvis": (0, -4), "hip_l": (-2, -3), "hip_r": (2, -3),
        "knee_l": (-2, -2), "knee_r": (2, -2),
        "foot_l": (-1, 0), "foot_r": (2, 0),
    }
    dst_skl = [(base_landmarks[k][0] + skl_offsets[k][0], base_landmarks[k][1] + skl_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skl_body = warp_image_idw(body_core, src_pts, dst_skl, power=2.0, epsilon=4.0)
    skl_key = place_rotated_pivot(key_src, deg=90, pivot=KEY_PIVOT, target=(42, 22), scale=1.08)
    skl_weapon = place_rotated_pivot(weapon_src, deg=74, pivot=WEAPON_PIVOT, target=(86, 52), scale=1.20)

    skl_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skl_fx)
    # Luminous circular barrier aura around elevated cutlass at (86, 52)
    s_draw.arc([66, 32, 106, 72], start=0, end=360, fill=(56, 160, 255, 220), width=1)
    s_draw.arc([70, 36, 102, 68], start=0, end=360, fill=(78, 216, 106, 200), width=1)
    s_draw.arc([74, 40, 98, 64], start=0, end=360, fill=(255, 253, 248, 240), width=1)

    # Vent high pressure ballast bubbles upward
    for vy in range(24, 56, 6):
        s_draw.ellipse([24, vy - 2, 30, vy + 2], fill=(255, 253, 248, 160))
        s_draw.ellipse([34, vy, 40, vy + 4], fill=(56, 160, 255, 150))

    # Sparkle points
    for sx, sy in [(86, 26), (106, 46), (72, 48), (98, 68), (78, 36)]:
        s_draw.point((sx, sy), fill=(255, 208, 40, 240))
        s_draw.point((sx + 1, sy), fill=(255, 253, 248, 255))
    skl_fx = skl_fx.filter(ImageFilter.GaussianBlur(0.35))

    skl_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skl_canvas.alpha_composite(skl_key)
    skl_canvas.alpha_composite(warped_skl_body)
    skl_canvas.alpha_composite(skl_weapon)
    skl_canvas.alpha_composite(skl_fx)
    poses["skill"] = enforce_ground_shadow(skl_canvas)

    # =========================================================================
    # 5. HIT (金屬震撼·受擊受挫硬直 / Impact Shock & Recoil Stagger)
    # Violent backward jolt and recoil (-14, -5).
    # Head and tusks thrown back violently (-14, -5).
    # Torso jolts backward (-12, -3), pelvis (-8, -1).
    # Winding key knocked askew (-48 deg, target=(28, 30), scale=0.94).
    # Cutlass knocked off balance (-42 deg, target=(84, 88), scale=0.92).
    # FX: Starburst impact sparks on peacoat chest (56, 70), golden & marine blue fragments.
    # =========================================================================
    hit_offsets = {
        "cowl_top": (-14, -5), "cowl_crest_l": (-14, -5), "cowl_crest_r": (-14, -5),
        "cowl_cheek_l": (-14, -5), "cowl_cheek_r": (-14, -5),
        "optic_l": (-14, -5), "optic_r": (-14, -5),
        "snout": (-14, -5), "whisker_l": (-14, -5), "whisker_r": (-14, -5),
        "tusk_root_l": (-14, -5), "tusk_root_r": (-14, -5),
        "tusk_tip_l": (-13, -5), "tusk_tip_r": (-13, -5),
        "throat": (-12, -4), "shoulder_l": (-12, -4), "shoulder_r": (-11, -4),
        "peacoat_chest": (-12, -3), "flipper_l": (-10, -3), "flipper_r": (-7, 4),
        "peacoat_hem": (-10, -2),
        "curio_top": (-9, 0), "curio_mid": (-8, 0), "curio_base": (-8, 0),
        "pelvis": (-8, -1), "hip_l": (-7, 0), "hip_r": (-5, 0),
        "knee_l": (-5, 0), "knee_r": (-3, 0),
        "foot_l": (-3, 0), "foot_r": (-1, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit, power=2.0, epsilon=4.0)
    hit_key = place_rotated_pivot(key_src, deg=-48, pivot=KEY_PIVOT, target=(28, 30), scale=0.94)
    hit_weapon = place_rotated_pivot(weapon_src, deg=-42, pivot=WEAPON_PIVOT, target=(84, 88), scale=0.92)

    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact starburst on chest (56, 70)
    ix, iy = 56, 70
    for pt in [(ix - 10, iy - 8), (ix + 10, iy - 8), (ix + 12, iy + 6), (ix - 8, iy + 10), (ix + 14, iy - 2), (ix - 12, iy + 2)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    for pt in [(ix - 6, iy - 4), (ix + 6, iy + 4), (ix + 4, iy - 6), (ix - 4, iy + 6)]:
        h_draw.point(pt, fill=(56, 160, 255, 240))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.35))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas.alpha_composite(hit_key)
    hit_canvas.alpha_composite(warped_hit_body)
    hit_canvas.alpha_composite(hit_weapon)
    hit_canvas.alpha_composite(hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (重裝接地·三點制動卸勁 / Grounded Impact Absorption Stance)
    # Deep grounded landing crouch: body bows forward, absorbs momentum (+2, +8).
    # Head and tusks compress down (+2, +8).
    # Torso compresses down (+2, +7), pelvis (+2, +5).
    # Feet planted wide in grounded brake stance (foot_l -4, foot_r +4).
    # Cutlass tucked close defensively (-18 deg, target=(86, 82), scale=1.04).
    # Winding key re-engages drive (+20 deg, target=(44, 42), scale=0.98).
    # FX: Deck brake friction sparks, pressure release micro-bubbles.
    # =========================================================================
    rec_offsets = {
        "cowl_top": (2, 8), "cowl_crest_l": (2, 8), "cowl_crest_r": (2, 8),
        "cowl_cheek_l": (2, 8), "cowl_cheek_r": (2, 8),
        "optic_l": (2, 8), "optic_r": (2, 8),
        "snout": (2, 8), "whisker_l": (2, 8), "whisker_r": (2, 8),
        "tusk_root_l": (2, 8), "tusk_root_r": (2, 8),
        "tusk_tip_l": (2, 8), "tusk_tip_r": (2, 8),
        "throat": (2, 7), "shoulder_l": (1, 7), "shoulder_r": (3, 7),
        "peacoat_chest": (2, 7), "flipper_l": (-2, 7), "flipper_r": (-3, 7),
        "peacoat_hem": (2, 6),
        "curio_top": (1, 6), "curio_mid": (2, 6), "curio_base": (2, 5),
        "pelvis": (2, 5), "hip_l": (-4, 4), "hip_r": (4, 4),
        "knee_l": (-4, 3), "knee_r": (4, 3),
        "foot_l": (-4, 0), "foot_r": (4, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec, power=2.0, epsilon=4.0)
    rec_key = place_rotated_pivot(key_src, deg=20, pivot=KEY_PIVOT, target=(44, 42), scale=0.98)
    rec_weapon = place_rotated_pivot(weapon_src, deg=-18, pivot=WEAPON_PIVOT, target=(86, 82), scale=1.04)

    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for bx, by in [(40, 32), (34, 28), (46, 26)]:
        r_draw.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=(255, 253, 248, 210))
        r_draw.point((bx, by), fill=(56, 160, 255, 240))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas.alpha_composite(rec_key)
    rec_canvas.alpha_composite(warped_rec_body)
    rec_canvas.alpha_composite(rec_weapon)
    rec_canvas.alpha_composite(rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def main():
    print("Generating The Icebreaker Walrus combat action poses...")
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

    # Official Battle Sprite (battle == attack per review.md 4b-8-1)
    battle_128 = poses["attack"]
    battle_512 = battle_128.resize((512, 512), resample=Image.Resampling.LANCZOS)
    p_battle_128 = f"{PLAYER_DIR}/walrus_battle.png"
    p_battle_512 = f"{PLAYER_DIR}/walrus_battle_512.png"
    battle_128.save(p_battle_128)
    battle_512.save(p_battle_512)
    print(f"  ✓ Saved battle sprites: {p_battle_128} & {p_battle_512}")

    # Proof comparison: idle vs battle (256x128 & 1024x512)
    comp_proof = Image.new("RGBA", (256, 128), (24, 20, 36, 255))
    comp_proof.paste(poses["idle"], (0, 0), poses["idle"])
    comp_proof.paste(battle_128, (128, 0), battle_128)
    p_comp = f"{PLAYER_DIR}/proof_walrus_idle_vs_battle.png"
    comp_proof.save(p_comp)

    comp_proof_512 = Image.new("RGBA", (1024, 512), (24, 20, 36, 255))
    idle_512 = poses["idle"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    comp_proof_512.paste(idle_512, (0, 0), idle_512)
    comp_proof_512.paste(battle_512, (512, 0), battle_512)
    p_comp_512 = f"{PLAYER_DIR}/proof_walrus_idle_vs_battle_512.png"
    comp_proof_512.save(p_comp_512)
    print(f"  ✓ Saved idle vs battle proof cards: {p_comp} & {p_comp_512}")

    # Composite proof sheet (idle, telegraph, attack, skill, hit, recover)
    proof_strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_order = ['idle', 'telegraph', 'attack', 'skill', 'hit', 'recover']
    for idx, p_name in enumerate(proof_order):
        proof_strip.paste(poses[p_name], (idx * 128, 0), poses[p_name])

    proof_768_path = f"{PLAYER_DIR}/proof_walrus_combat_poses_768.png"
    proof_strip.save(proof_768_path)
    print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

    # Magenta background proof sheet for hole detection
    proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    proof_magenta.paste(proof_strip, (0, 0), proof_strip)
    proof_mag_path = f"{PLAYER_DIR}/proof_walrus_combat_poses_magenta.png"
    proof_magenta.save(proof_mag_path)
    print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")

    # Crop 8x hit core for 0-QA31
    hit_512 = poses["hit"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    core_crop = hit_512.crop((50 * 4, 55 * 4, 75 * 4, 80 * 4))
    crop_path = f"{PLAYER_DIR}/proof_walrus_hit_core_crop_8x.png"
    core_crop.save(crop_path)
    print(f"  ✓ Saved 0-QA31 core crop: {crop_path}")


if __name__ == "__main__":
    main()
