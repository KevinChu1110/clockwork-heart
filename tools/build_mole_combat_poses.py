#!/usr/bin/env python3
"""
tools/build_mole_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Asteroid Mole (第五十七族 星岩鼴鼠, mole)
in Clockwork Heart:
  game/assets/sprites/player/poses/mole/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/mole/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates:
  - 0-QA16 / 0-QA31 / 0-QA34
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
Features:
  - Milky ABS/POM polymer chassis & cold-rolled tungsten joints
  - Polycarbonate mining visor cowl & superconducting radar vane ears
  - Amber LED dot-matrix optic core with mint reticle
  - Orbital sapper dungarees with brass buckles & hazard badge
  - Cold-gas thruster cylinder tail with brass bands
  - Four-vane antenna brass winding key with coral rivet
  - Orbital plasma sledgehammer with mint plasma ring & sky-blue impact head
"""

import math
import os
import sys
from typing import cast
from PIL import Image, ImageOps
import numpy as np

# Ensure clean imports
sys.path = [p for p in sys.path if not p.startswith('/tmp')]

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/mole"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/mole"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_mole_four_vane_antenna_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_mole_cold_gas_thruster_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_mole_milky_polymer_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_mole_orbital_mining_visor_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_mole_orbital_sapper_dungarees.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_mole_amber_led_mining_visor_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_mole_orbital_plasma_sledgehammer.png").convert("RGBA")

# Extract ground shadow master from party mole_idle.png
ref_shadow_im = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/mole_idle.png").convert("RGBA")
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
                if rgba[3] < 12:
                    out_pixels[x, y] = (0, 0, 0, 0)
                else:
                    out_pixels[x, y] = tuple(rgba)
            elif 0 <= x0 < w and 0 <= y0 < h:
                p = cast(tuple[int, int, int, int], src_pixels[x0, y0])
                if p[3] < 12:
                    out_pixels[x, y] = (0, 0, 0, 0)
                else:
                    out_pixels[x, y] = p

    return out_img


# Canvas boundary anchors
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127)
]

base_landmarks = {
    "cowl_top_l": (48, 26),
    "cowl_top_r": (80, 26),
    "ear_l": (38, 28),
    "ear_r": (90, 28),
    "visor_brow": (64, 32),
    "optic_l": (54, 42),
    "optic_r": (74, 42),
    "snout": (64, 50),
    "chin_filter": (64, 55),
    "shoulder_l": (42, 60),
    "shoulder_r": (86, 60),
    "chest_badge": (64, 76),
    "bib_top": (64, 68),
    "arm_l_claw": (36, 78),
    "arm_r_hand": (88, 76),
    "curio_tail": (32, 86),
    "flank_l": (42, 82),
    "flank_r": (86, 82),
    "pelvis": (64, 92),
    "knee_l": (42, 98),
    "knee_r": (70, 98),
    "foot_l": (40, 114),
    "foot_r": (72, 114),
}

# Chassis without ground shadow for clean warping
chassis_clean = chassis_src.copy()
ch_clean_px = chassis_clean.load()
assert ch_clean_px is not None
for y in range(118, 128):
    for x in range(128):
        ch_clean_px[x, y] = (0, 0, 0, 0)

# Base body composite (curio + clean chassis + head + costume + optic)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_clean)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)

src_pts = list(base_landmarks.values()) + anchors

KEY_PIVOT = (64.0, 44.0)
WEAPON_PIVOT = (90.0, 78.0)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (星岩沉穩·低重心採礦架勢 / Asteroid Vanguard Mining Neutral Poise)
    # Low-center-of-gravity stout stance. Plasma hammer held in right hand (88, 78).
    # Four-vane antenna key standing upright at (64, 46.5).
    # =========================================================================
    idle_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(64, 46.5), scale=1.0)
    idle_weapon = place_rotated_pivot(weapon_src, deg=0, pivot=WEAPON_PIVOT, target=(88, 78), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (等離子蓄能·重鎚下壓深蹲聚勢 / Deep Sledgehammer Compression & Coil)
    # Heavy sapper crouch!
    # Head and cowl lower deeply and tuck back (x-7, y+8).
    # Dungarees and torso coil back (x-5, y+7).
    # Pelvis drops down (x-4, y+6).
    # Knees widen in spring compression (knee_l x-4 y+4, knee_r +2 y+4).
    # Sledgehammer drawn back across flank (-36 deg, pivot=(90, 78), target=(78, 80), scale=1.02).
    # Four-vane antenna key counter-winds (-45 deg, pivot=(64, 44), target=(57, 49), scale=0.98).
    # =========================================================================
    tele_offsets = {
        "cowl_top_l": (-7, 8),
        "cowl_top_r": (-5, 8),
        "ear_l": (-8, 8),
        "ear_r": (-5, 8),
        "visor_brow": (-6, 8),
        "optic_l": (-7, 8),
        "optic_r": (-6, 8),
        "snout": (-6, 7),
        "chin_filter": (-6, 7),
        "shoulder_l": (-7, 7),
        "shoulder_r": (-4, 7),
        "chest_badge": (-6, 7),
        "bib_top": (-6, 7),
        "arm_l_claw": (-7, 6),
        "arm_r_hand": (-8, 6),
        "curio_tail": (-6, 5),
        "flank_l": (-6, 6),
        "flank_r": (-3, 6),
        "pelvis": (-4, 6),
        "knee_l": (-4, 4),
        "knee_r": (+2, 4),
        "foot_l": (-2, 1),
        "foot_r": (+2, 1),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele)
    tele_key = place_rotated_pivot(key_src, deg=-45, pivot=KEY_PIVOT, target=(57, 49), scale=0.98)
    tele_weapon = place_rotated_pivot(weapon_src, deg=-36, pivot=WEAPON_PIVOT, target=(78, 80), scale=1.02)

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, tele_key)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele_body)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_weapon)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (軌道破岩擊·等離子重鎚怒砸衝刺 / Full-Force Plasma Sledgehammer Slam)
    # Violent forward charge and overhead slam!
    # Head and cowl thrust forward (x+16, y+1).
    # Torso lunges forward (x+14, y+1), pelvis drives forward (x+11, y=0).
    # Front foot steps forward boldly (x+6), back foot trails (x+1).
    # Sledgehammer swung forward and downward in devastating slam (+34 deg, pivot=(90, 78), target=(98, 72), scale=1.12).
    # Four-vane antenna key whips forward with momentum (+55 deg, pivot=(64, 44), target=(78, 45), scale=1.02).
    # =========================================================================
    atk_offsets = {
        "cowl_top_l": (15, 1),
        "cowl_top_r": (17, 1),
        "ear_l": (14, 1),
        "ear_r": (18, 1),
        "visor_brow": (16, 1),
        "optic_l": (16, 1),
        "optic_r": (16, 1),
        "snout": (17, 2),
        "chin_filter": (17, 2),
        "shoulder_l": (12, 1),
        "shoulder_r": (16, 1),
        "chest_badge": (14, 1),
        "bib_top": (14, 1),
        "arm_l_claw": (10, 1),
        "arm_r_hand": (14, -2),
        "curio_tail": (8, 0),
        "flank_l": (11, 1),
        "flank_r": (14, 1),
        "pelvis": (11, 0),
        "knee_l": (2, 0),
        "knee_r": (8, 0),
        "foot_l": (1, 0),
        "foot_r": (6, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk)
    atk_key = place_rotated_pivot(key_src, deg=55, pivot=KEY_PIVOT, target=(78, 45), scale=1.02)
    atk_weapon = place_rotated_pivot(weapon_src, deg=34, pivot=WEAPON_PIVOT, target=(98, 72), scale=1.12)

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, atk_key)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk_body)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_weapon)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (星穹共振·軌道電漿天基超載 / Orbital Plasma Sky-Breaker Stance)
    # Mighty rearing up! Sledgehammer raised straight to the sky to channel orbital resonance.
    # Head and cowl tilt high up (x=0, y-12).
    # Torso and dungarees expand skyward (x=0, y-8).
    # Pelvis lifts (x=0, y-3).
    # Legs plant wide: foot_l (-1, 0), foot_r (+2, 0).
    # Sledgehammer held aloft vertically (+72 deg, pivot=(90, 78), target=(88, 52), scale=1.14).
    # Four-vane antenna key overclocks and spins rapidly (+85 deg, pivot=(64, 44), target=(64, 35), scale=1.05).
    # =========================================================================
    skl_offsets = {
        "cowl_top_l": (0, -12),
        "cowl_top_r": (2, -12),
        "ear_l": (-3, -13),
        "ear_r": (3, -13),
        "visor_brow": (1, -12),
        "optic_l": (0, -12),
        "optic_r": (1, -12),
        "snout": (1, -11),
        "chin_filter": (1, -10),
        "shoulder_l": (-3, -8),
        "shoulder_r": (3, -8),
        "chest_badge": (0, -8),
        "bib_top": (0, -8),
        "arm_l_claw": (-4, -7),
        "arm_r_hand": (+2, -12),
        "curio_tail": (-2, -3),
        "flank_l": (-3, -6),
        "flank_r": (3, -6),
        "pelvis": (0, -3),
        "knee_l": (-1, -1),
        "knee_r": (+2, -1),
        "foot_l": (-1, 0),
        "foot_r": (+2, 0),
    }
    dst_skl = [(base_landmarks[k][0] + skl_offsets[k][0], base_landmarks[k][1] + skl_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skl_body = warp_image_idw(body_core, src_pts, dst_skl)
    skl_key = place_rotated_pivot(key_src, deg=85, pivot=KEY_PIVOT, target=(64, 35), scale=1.05)
    skl_weapon = place_rotated_pivot(weapon_src, deg=72, pivot=WEAPON_PIVOT, target=(88, 52), scale=1.14)

    skl_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skl_canvas = Image.alpha_composite(skl_canvas, skl_key)
    skl_canvas = Image.alpha_composite(skl_canvas, warped_skl_body)
    skl_canvas = Image.alpha_composite(skl_canvas, skl_weapon)
    poses["skill"] = enforce_ground_shadow(skl_canvas)

    # =========================================================================
    # 5. HIT (衝擊格擋·裝甲抗震受創反沖 / Heavy Kinetic Impact Recoil)
    # Violent kinetic shock!
    # Head and cowl snap back and up (x-15, y-5).
    # Torso thrown back (x-13, y-3), pelvis shoved back (x-9, y=0).
    # Legs slide back to brace (knee_l -5, knee_r -3, foot_l -3, foot_r -1).
    # Sledgehammer jolted up defensively in shock (-32 deg, pivot=(90, 78), target=(76, 74), scale=0.98).
    # Four-vane antenna key recoils counter-clockwise (-40 deg, pivot=(64, 44), target=(52, 42), scale=0.96).
    # =========================================================================
    hit_offsets = {
        "cowl_top_l": (-15, -5),
        "cowl_top_r": (-13, -5),
        "ear_l": (-16, -5),
        "ear_r": (-13, -5),
        "visor_brow": (-14, -5),
        "optic_l": (-15, -5),
        "optic_r": (-14, -5),
        "snout": (-15, -4),
        "chin_filter": (-14, -4),
        "shoulder_l": (-13, -3),
        "shoulder_r": (-10, -3),
        "chest_badge": (-12, -3),
        "bib_top": (-12, -3),
        "arm_l_claw": (-12, -2),
        "arm_r_hand": (-10, 2),
        "curio_tail": (-9, 0),
        "flank_l": (-11, -2),
        "flank_r": (-9, -2),
        "pelvis": (-9, 0),
        "knee_l": (-5, 0),
        "knee_r": (-3, 0),
        "foot_l": (-3, 0),
        "foot_r": (-1, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit)
    hit_key = place_rotated_pivot(key_src, deg=-40, pivot=KEY_PIVOT, target=(52, 42), scale=0.96)
    hit_weapon = place_rotated_pivot(weapon_src, deg=-32, pivot=WEAPON_PIVOT, target=(76, 74), scale=0.98)

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, hit_key)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit_body)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_weapon)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (冷氣洩壓·反推回位歸零 / Cold Gas Venting & Hammer Restabilization)
    # Stance settles smoothly after action:
    # Head and cowl slight breathing breath (x+2, y+4).
    # Torso settles smoothly (x+2, y+3), pelvis (x+1, y+1).
    # Sledgehammer resting in steady restabilization angle (+10 deg, pivot=(90, 78), target=(89, 80), scale=1.0).
    # Four-vane antenna key smoothly returning to neutral (+10 deg, pivot=(64, 44), target=(65, 48), scale=0.98).
    # =========================================================================
    rec_offsets = {
        "cowl_top_l": (2, 4),
        "cowl_top_r": (3, 4),
        "ear_l": (1, 4),
        "ear_r": (4, 4),
        "visor_brow": (2, 4),
        "optic_l": (2, 4),
        "optic_r": (2, 4),
        "snout": (2, 4),
        "chin_filter": (2, 3),
        "shoulder_l": (2, 3),
        "shoulder_r": (3, 3),
        "chest_badge": (2, 3),
        "bib_top": (2, 3),
        "arm_l_claw": (2, 3),
        "arm_r_hand": (3, 1),
        "curio_tail": (0, 1),
        "flank_l": (2, 2),
        "flank_r": (3, 2),
        "pelvis": (1, 1),
        "knee_l": (0, 0),
        "knee_r": (1, 0),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec)
    rec_key = place_rotated_pivot(key_src, deg=10, pivot=KEY_PIVOT, target=(65, 48), scale=0.98)
    rec_weapon = place_rotated_pivot(weapon_src, deg=10, pivot=WEAPON_PIVOT, target=(89, 80), scale=1.0)

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, rec_key)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec_body)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_weapon)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def build_and_save():
    print("Generating Asteroid Mole combat action poses...")
    poses = generate_poses()

    for name, img in poses.items():
        # Save 128x128
        out_128 = os.path.join(OUT_DIR, f"{name}.png")
        img.save(out_128, "PNG")

        # Save 512x512 LANCZOS
        out_512 = os.path.join(OUT_DIR, f"{name}_512.png")
        img_512 = img.resize((512, 512), resample=Image.Resampling.LANCZOS)
        img_512.save(out_512, "PNG")

        print(f"✓ Saved {name}.png (128x128) and {name}_512.png (512x512 LANCZOS)")

    # Generate 6-pose comparison proof sheets (768x128)
    order = ["idle", "telegraph", "attack", "recover", "skill", "hit"]
    proof_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))

    for i, p_name in enumerate(order):
        p_img = poses[p_name]
        proof_768.paste(p_img, (i * 128, 0), p_img)
        proof_mag.alpha_composite(p_img, (i * 128, 0))

    p768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_mole_combat_poses_768.png"
    pmag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_mole_combat_poses_magenta.png"
    proof_768.save(p768_path, "PNG")
    proof_mag.save(pmag_path, "PNG")
    print(f"✓ Saved proof sheets:\n  - {p768_path}\n  - {pmag_path}")


if __name__ == "__main__":
    build_and_save()
