#!/usr/bin/env python3
"""
tools/build_hippo_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Steamvalve Hippo (第五十六族 重閥河馬, hippo)
in Clockwork Heart:
  game/assets/sprites/player/poses/hippo/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/hippo/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7/8, Rule 4c-5/16, 0-QA34).
Features thick cast brass chassis, ballast safety valve cowl, dual pressure gauge quartz lens,
greatcog high pressure cuirass, dual valve handwheel brass key, steamvalve piston heavy lance,
and dual steam exhaust ballast tail.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/hippo"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/hippo"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_hippo_dual_valve_handwheel_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_hippo_dual_steam_exhaust_ballast_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_hippo_thick_cast_brass_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_hippo_ballast_safety_valve_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_hippo_greatcog_high_pressure_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_hippo_dual_pressure_gauge_quartz_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_hippo_steamvalve_piston_heavy_lance.png").convert("RGBA")

# Extract raw weapon and key crops
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Reference ground shadow from canonical party idle asset
ref_shadow_im = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/hippo_idle.png").convert("RGBA")
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


def place_rotated_element(elem_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places any element with smooth sub-pixel BICUBIC quality."""
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


def warp_image_idw(src_img: Image.Image, src_points: list[tuple[int, int]], dst_points: list[tuple[int, int]], power: float = 2.0, epsilon: float = 5.0) -> Image.Image:
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
                p = src_pixels[x0, y0]
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
    "cowl_top_l": (46, 20),
    "cowl_top_r": (82, 20),
    "valve_ear_l": (32, 28),
    "valve_ear_r": (96, 28),
    "optic_l": (54, 42),
    "optic_r": (74, 42),
    "snout_top": (64, 34),
    "snout_jaw_l": (40, 52),
    "snout_jaw_r": (88, 52),
    "chin_vent": (64, 58),
    "cuirass_top": (64, 62),
    "shoulder_l": (36, 68),
    "shoulder_r": (92, 68),
    "arm_hand_l": (34, 76),
    "arm_hand_r": (86, 75),
    "chest_gauge": (64, 74),
    "cuirass_flank_l": (35, 84),
    "cuirass_flank_r": (93, 84),
    "pelvis": (64, 90),
    "ballast_tail": (40, 92),
    "leg_back_l": (34, 104),
    "leg_front_l": (46, 104),
    "leg_front_r": (78, 104),
    "leg_back_r": (88, 104),
    "foot_l": (40, 114),
    "foot_r": (82, 114),
}

# Base body composite (curio + chassis + head + costume + optic)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)

src_pts = list(base_landmarks.values()) + anchors


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (重閘護衛·低重心沈著防禦架勢 / Steamvalve Neutral Heavy Guard)
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(64, 21), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(93, 63), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (重閘蓄壓·活塞回縮蓄勢 / Deep Anticipation Crouch)
    # Deep, powerful crouch!
    # Head and cowl lower deeply and pull back (x-8, y+8).
    # Heavy torso coils back (x-6, y+7).
    # Pelvis drops down (x-5, y+6).
    # Knees spread wide in high-torque mechanical spring compression:
    # leg_front_l: (-5, 4), leg_front_r: (+2, 4), foot_l: (-2, 1), foot_r: (+2, 1).
    # Lance is drawn tight across the lower abdomen (-36 deg, target=(78, 72), scale=0.98).
    # Arm hand tracks spear grip to (76, 80).
    # Dual valve handwheel key counter-winds (-45 deg, target=(55, 26), scale=0.98).
    # =========================================================================
    tele_offsets = {
        "cowl_top_l": (-8, 8),
        "cowl_top_r": (-6, 8),
        "valve_ear_l": (-9, 8),
        "valve_ear_r": (-6, 8),
        "optic_l": (-8, 8),
        "optic_r": (-7, 8),
        "snout_top": (-8, 8),
        "snout_jaw_l": (-8, 8),
        "snout_jaw_r": (-6, 8),
        "chin_vent": (-7, 8),
        "cuirass_top": (-7, 7),
        "shoulder_l": (-8, 7),
        "shoulder_r": (-5, 7),
        "arm_hand_l": (-8, 7),
        "arm_hand_r": (-9, 5),
        "chest_gauge": (-7, 7),
        "cuirass_flank_l": (-7, 6),
        "cuirass_flank_r": (-4, 6),
        "pelvis": (-5, 6),
        "ballast_tail": (-7, 5),
        "leg_back_l": (-5, 4),
        "leg_front_l": (-4, 4),
        "leg_front_r": (+2, 4),
        "leg_back_r": (+3, 4),
        "foot_l": (-2, 1),
        "foot_r": (+2, 1),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele)
    tele_key = place_rotated_element(key_raw, deg=-45, target_center=(55, 26), scale=0.98)
    tele_weapon = place_rotated_element(weapon_raw, deg=-36, target_center=(78, 72), scale=0.98)

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, tele_key)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele_body)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_weapon)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (重閥活塞衝刺·高壓破陣突刺 / Full-Force Horizontal Lance Thrust Charge)
    # Violent forward charge! Head lowers and rams forward (x+17, y+2).
    # Heavy torso surges forward (x+15, y+1). Pelvis thrusts forward (x+12, y=0).
    # Front leg strides boldly forward (x+9), back leg trails back (x-3).
    # Heavy lance thrusts forward horizontally (+18 deg, target=(108, 62), scale=1.14).
    # Arm hand powers forward to (98, 68).
    # Key driven forward with maximum momentum (+55 deg, target=(80, 18), scale=1.02).
    # =========================================================================
    atk_offsets = {
        "cowl_top_l": (17, 1),
        "cowl_top_r": (19, 1),
        "valve_ear_l": (16, 1),
        "valve_ear_r": (19, 1),
        "optic_l": (17, 1),
        "optic_r": (17, 1),
        "snout_top": (18, 2),
        "snout_jaw_l": (17, 2),
        "snout_jaw_r": (19, 2),
        "chin_vent": (18, 2),
        "cuirass_top": (15, 1),
        "shoulder_l": (13, 1),
        "shoulder_r": (17, 1),
        "arm_hand_l": (11, 1),
        "arm_hand_r": (15, -2),
        "chest_gauge": (15, 1),
        "cuirass_flank_l": (12, 1),
        "cuirass_flank_r": (15, 1),
        "pelvis": (12, 0),
        "ballast_tail": (9, 0),
        "leg_back_l": (1, 0),
        "leg_front_l": (4, 0),
        "leg_front_r": (10, 0),
        "leg_back_r": (11, 0),
        "foot_l": (1, 0),
        "foot_r": (7, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk)
    atk_key = place_rotated_element(key_raw, deg=55, target_center=(80, 18), scale=1.02)
    atk_weapon = place_rotated_element(weapon_raw, deg=18, target_center=(108, 62), scale=1.14)

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, atk_key)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk_body)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_weapon)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (巨輪高壓過載·四聯安全閥大爆發 / Overpressure Relief High Bastion Stance)
    # Rearing up high! The entire body lifts skyward:
    # Head and cowl tilt high up (x=0, y-12).
    # Chest expands skyward (x=0, y-7).
    # Pelvis lifts (x=0, y-3).
    # Legs plant firmly wide: foot_l (-2, 0), foot_r (+2, 0).
    # Heavy lance held straight aloft pointing up (+68 deg, target=(94, 42), scale=1.14).
    # Arm hand raised to (86, 52).
    # Key spinning rapidly at top of back (+85 deg, target=(64, 13), scale=1.06).
    # =========================================================================
    skl_offsets = {
        "cowl_top_l": (0, -12),
        "cowl_top_r": (2, -12),
        "valve_ear_l": (-3, -13),
        "valve_ear_r": (3, -13),
        "optic_l": (0, -12),
        "optic_r": (1, -12),
        "snout_top": (0, -11),
        "snout_jaw_l": (-2, -11),
        "snout_jaw_r": (2, -11),
        "chin_vent": (0, -10),
        "cuirass_top": (0, -8),
        "shoulder_l": (-3, -8),
        "shoulder_r": (3, -8),
        "arm_hand_l": (-4, -7),
        "arm_hand_r": (+2, -12),
        "chest_gauge": (0, -8),
        "cuirass_flank_l": (-3, -6),
        "cuirass_flank_r": (3, -6),
        "pelvis": (0, -3),
        "ballast_tail": (-2, -3),
        "leg_back_l": (-2, -1),
        "leg_front_l": (-1, -1),
        "leg_front_r": (+2, -1),
        "leg_back_r": (+3, -1),
        "foot_l": (-1, 0),
        "foot_r": (+2, 0),
    }
    dst_skl = [(base_landmarks[k][0] + skl_offsets[k][0], base_landmarks[k][1] + skl_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skl_body = warp_image_idw(body_core, src_pts, dst_skl)
    skl_key = place_rotated_element(key_raw, deg=85, target_center=(64, 13), scale=1.06)
    skl_weapon = place_rotated_element(weapon_raw, deg=68, target_center=(94, 42), scale=1.14)

    skl_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skl_canvas = Image.alpha_composite(skl_canvas, skl_key)
    skl_canvas = Image.alpha_composite(skl_canvas, warped_skl_body)
    skl_canvas = Image.alpha_composite(skl_canvas, skl_weapon)
    poses["skill"] = enforce_ground_shadow(skl_canvas)

    # =========================================================================
    # 5. HIT (重裝格擋反震·裝甲抗衝擊 / Dramatic Kinetic Knockback)
    # Violent recoil! Head snaps back and up (x-16, y-5).
    # Torso thrown back (x-13, y-3).
    # Pelvis pushed back (x-9, y=0).
    # Front leg slides back (x-6), back leg braces to absorb shock (x-4).
    # Lance deflected upward in defensive shock (-35 deg, target=(76, 70), scale=0.98).
    # Arm hand recoils to (74, 78).
    # Key jolted counter-clockwise (-40 deg, target=(52, 17), scale=0.96).
    # =========================================================================
    hit_offsets = {
        "cowl_top_l": (-16, -5),
        "cowl_top_r": (-14, -5),
        "valve_ear_l": (-17, -5),
        "valve_ear_r": (-14, -5),
        "optic_l": (-16, -5),
        "optic_r": (-15, -5),
        "snout_top": (-16, -4),
        "snout_jaw_l": (-16, -4),
        "snout_jaw_r": (-13, -4),
        "chin_vent": (-15, -4),
        "cuirass_top": (-13, -3),
        "shoulder_l": (-14, -3),
        "shoulder_r": (-11, -3),
        "arm_hand_l": (-13, -2),
        "arm_hand_r": (-11, 2),
        "chest_gauge": (-13, -3),
        "cuirass_flank_l": (-12, -2),
        "cuirass_flank_r": (-10, -2),
        "pelvis": (-9, 0),
        "ballast_tail": (-10, 0),
        "leg_back_l": (-7, 0),
        "leg_front_l": (-6, 0),
        "leg_front_r": (-4, 0),
        "leg_back_r": (-3, 0),
        "foot_l": (-4, 0),
        "foot_r": (-2, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit)
    hit_key = place_rotated_element(key_raw, deg=-40, target_center=(52, 17), scale=0.96)
    hit_weapon = place_rotated_element(weapon_raw, deg=-35, target_center=(76, 70), scale=0.98)

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, hit_key)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit_body)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_weapon)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (蒸氣冷卻洩壓·活塞回位歸零 / Steam Exhaust Venting & Piston Reset)
    # Stance settling smoothly after action (head x+2, y+4; torso x+2, y+3; pelvis x+1, y+1).
    # Heavy lance resting in neutral guard angle (+10 deg, target=(93, 66), scale=1.0).
    # Dual valve handwheel key smoothly rotating back towards neutral (+10 deg, target=(65, 23), scale=0.98).
    # Arm hand resting at (88, 74).
    # =========================================================================
    rec_offsets = {
        "cowl_top_l": (2, 4),
        "cowl_top_r": (3, 4),
        "valve_ear_l": (1, 4),
        "valve_ear_r": (4, 4),
        "optic_l": (2, 4),
        "optic_r": (2, 4),
        "snout_top": (2, 4),
        "snout_jaw_l": (2, 3),
        "snout_jaw_r": (3, 3),
        "chin_vent": (2, 3),
        "cuirass_top": (2, 3),
        "shoulder_l": (2, 3),
        "shoulder_r": (3, 3),
        "arm_hand_l": (2, 3),
        "arm_hand_r": (3, 1),
        "chest_gauge": (2, 3),
        "cuirass_flank_l": (2, 2),
        "cuirass_flank_r": (3, 2),
        "pelvis": (1, 1),
        "ballast_tail": (0, 1),
        "leg_back_l": (0, 0),
        "leg_front_l": (0, 0),
        "leg_front_r": (1, 0),
        "leg_back_r": (1, 0),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec)
    rec_key = place_rotated_element(key_raw, deg=10, target_center=(65, 23), scale=0.98)
    rec_weapon = place_rotated_element(weapon_raw, deg=10, target_center=(93, 66), scale=1.0)

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, rec_key)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec_body)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_weapon)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def build_and_save():
    print("Generating hippo combat action poses...")
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

    p768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_hippo_combat_poses_768.png"
    pmag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_hippo_combat_poses_magenta.png"
    proof_768.save(p768_path, "PNG")
    proof_mag.save(pmag_path, "PNG")
    print(f"✓ Saved proof sheets:\n  - {p768_path}\n  - {pmag_path}")


if __name__ == "__main__":
    build_and_save()
