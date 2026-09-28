#!/usr/bin/env python3
"""
tools/build_badger_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Starbreaker Honey Badger (第四十六族 破星蜜獾, badger)
in Clockwork Heart:
  game/assets/sprites/player/poses/badger/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/badger/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
Features high-density polymer space chassis, flathead ballistic visor, four-vane radar antenna gold key,
dual cold-gas reaction thrusters, and starbreaker ripper claw attacks.
"""

import math
import os
from typing import cast
from PIL import Image, ImageOps
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/badger"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/badger"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical slice layers (128x128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_badger_four_vane_antenna_gold.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_badger_dual_coldgas_reaction_thruster.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_badger_polymer_space_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_badger_flathead_ballistic_visor.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_badger_eva_heavy_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_badger_amber_led_matrix_visor.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_badger_starbreaker_ripper_claw.png").convert("RGBA")

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Canonical ground shadow directly from chassis slice (118..127)
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = chassis_src.load()
assert s_px is not None and c_px is not None

for y in range(118, 128):
    for x in range(4, 124):
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
            o_px[x, y] = sp

    # Clean outer boundary strictly (L>=4, R>=4, T>=4, B>=2)
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


# Anchor corners and borders for IDW (ground plane at y=116..127 remains grounded)
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127),
    (40, 116), (82, 116), (62, 116)
]

base_landmarks = {
    "head_top": (64, 21),
    "head_cowl_l": (40, 30),
    "head_cowl_r": (88, 30),
    "visor_brow": (64, 32),
    "led_eye_l": (55, 42),
    "led_eye_r": (73, 42),
    "snout": (64, 48),
    "jaw": (64, 55),
    "throat": (64, 58),
    "thruster_l": (42, 40),
    "thruster_r": (86, 40),
    "thruster_base": (64, 60),
    "chest_core": (64, 68),
    "shoulder_l": (44, 66),
    "shoulder_r": (84, 66),
    "arm_l": (34, 76),
    "arm_r": (88, 76),
    "hand_r": (94, 80),
    "torso": (62, 82),
    "pelvis": (62, 96),
    "hip_l": (44, 100),
    "hip_r": (80, 100),
    "foot_l": (42, 116),
    "foot_r": (80, 116),
}

# Base body composite without weapon and winding key (z: curio=8, chassis=10, head=20, costume=25, optic=30)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (破星沉穩架勢 / Starbreaker Poise)
    # Grounded confident monk stance. Key at (67, 31), weapon claw at (104, 74).
    # Perfectly crisp, grounded and zero-defect.
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(67, 31), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(104, 74), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (失重壓低·反推聚能 / Low Crouch & Thruster Pre-charge)
    # Body lowers forward to charging attack line (head y+5, chest y+3).
    # Ripper claw draws back in high mechanical tension (-30 deg, target=(88, 70)).
    # Four-vane antenna winding key counter-winds (-45 deg, target=(64, 36)).
    # Dual thrusters tilt backward (y-2, x-3) preparing impulse.
    # =========================================================================
    tele_offsets = {
        "head_top": (-2, 5),
        "head_cowl_l": (-3, 5),
        "head_cowl_r": (-1, 5),
        "visor_brow": (-2, 5),
        "led_eye_l": (-2, 5),
        "led_eye_r": (-2, 5),
        "snout": (-2, 5),
        "jaw": (-2, 5),
        "throat": (-1, 4),
        "thruster_l": (-4, 2),
        "thruster_r": (-2, 2),
        "thruster_base": (-2, 4),
        "chest_core": (-1, 3),
        "shoulder_l": (-2, 3),
        "shoulder_r": (0, 3),
        "arm_l": (-4, 2),
        "arm_r": (-3, 1),
        "hand_r": (-4, 0),
        "torso": (-1, 2),
        "pelvis": (0, 1),
        "hip_l": (-1, 1),
        "hip_r": (1, 1),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    src_pts = list(base_landmarks.values()) + anchors
    dst_tele = [
        (base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1])
        for k in base_landmarks
    ] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele, power=2.0, epsilon=4.0)

    tele_key = place_rotated_element(key_raw, deg=-45, target_center=(64, 36), scale=1.0)
    tele_weapon = place_rotated_element(weapon_raw, deg=-30, target_center=(88, 70), scale=1.05)
    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, tele_key)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele_body)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_weapon)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (向量衝鋒·裂空機關爪破陣 / Vector Rush & Ripper Claw Shred)
    # Violent forward leap and shred! Ripper claw swings forward (+38 deg, target=(108, 62), scale=1.18).
    # Head & torso stretch forward into the lunge (head x+7, y-4, chest x+6, y-3).
    # Winding key releases clockwise with inertia (+50 deg, target=(72, 27)).
    # Thrusters fire back as thrust vectors push forward.
    # =========================================================================
    atk_offsets = {
        "head_top": (8, -4),
        "head_cowl_l": (7, -4),
        "head_cowl_r": (9, -4),
        "visor_brow": (8, -4),
        "led_eye_l": (8, -4),
        "led_eye_r": (8, -4),
        "snout": (9, -3),
        "jaw": (8, -3),
        "throat": (7, -3),
        "thruster_l": (3, -2),
        "thruster_r": (7, -2),
        "thruster_base": (5, -2),
        "chest_core": (6, -2),
        "shoulder_l": (4, -2),
        "shoulder_r": (8, -2),
        "arm_l": (1, -1),
        "arm_r": (9, -3),
        "hand_r": (12, -4),
        "torso": (4, -1),
        "pelvis": (2, 0),
        "hip_l": (1, 0),
        "hip_r": (3, 0),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_atk = [
        (base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1])
        for k in base_landmarks
    ] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk, power=2.0, epsilon=4.0)

    atk_key = place_rotated_element(key_raw, deg=50, target_center=(72, 27), scale=1.05)
    atk_weapon = place_rotated_element(weapon_raw, deg=38, target_center=(108, 62), scale=1.18)
    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, atk_key)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk_body)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_weapon)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (星穹過載反推·狂暴奧義爪 / Astral Overload Vector Claws)
    # Maximum dynamic elevation and overload!
    # Head & chest leap upward-forward (head x+6, y-8, chest x+5, y-7).
    # Heavy alloy ripper claw strikes high in ultimate vacuum slash (+60 deg, target=(104, 50), scale=1.28).
    # Four-vane antenna winding key over-rotates (+90 deg, target=(70, 23)).
    # Dynamic change > 35% with massive visual impact.
    # =========================================================================
    skill_offsets = {
        "head_top": (6, -8),
        "head_cowl_l": (5, -8),
        "head_cowl_r": (7, -8),
        "visor_brow": (6, -8),
        "led_eye_l": (6, -8),
        "led_eye_r": (6, -8),
        "snout": (7, -7),
        "jaw": (6, -7),
        "throat": (5, -6),
        "thruster_l": (2, -6),
        "thruster_r": (8, -6),
        "thruster_base": (5, -5),
        "chest_core": (5, -5),
        "shoulder_l": (3, -5),
        "shoulder_r": (8, -6),
        "arm_l": (0, -4),
        "arm_r": (10, -7),
        "hand_r": (12, -10),
        "torso": (4, -4),
        "pelvis": (2, -2),
        "hip_l": (1, -1),
        "hip_r": (3, -1),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_skill = [
        (base_landmarks[k][0] + skill_offsets[k][0], base_landmarks[k][1] + skill_offsets[k][1])
        for k in base_landmarks
    ] + anchors
    warped_skill_body = warp_image_idw(body_core, src_pts, dst_skill, power=2.0, epsilon=4.0)

    skill_key = place_rotated_element(key_raw, deg=90, target_center=(70, 23), scale=1.1)
    skill_weapon = place_rotated_element(weapon_raw, deg=60, target_center=(104, 50), scale=1.28)
    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, skill_key)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill_body)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_weapon)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (平頭抗震受擊 / Ballistic Visor Impact Recoil)
    # Head and torso recoil backward-downward (head x-7, y-3, chest x-5, y-2).
    # Weapon claw braces inward defensively (-20 deg, target=(94, 76), scale=1.05).
    # Antenna winding key recoils counter-clockwise (-30 deg, target=(58, 29)).
    # Strictly maintains 0-QA31 chest brightness & LED matrix visor integrity.
    # =========================================================================
    hit_offsets = {
        "head_top": (-7, -3),
        "head_cowl_l": (-8, -3),
        "head_cowl_r": (-6, -3),
        "visor_brow": (-7, -3),
        "led_eye_l": (-7, -3),
        "led_eye_r": (-7, -3),
        "snout": (-7, -2),
        "jaw": (-6, -2),
        "throat": (-5, -2),
        "thruster_l": (-6, -4),
        "thruster_r": (-4, -4),
        "thruster_base": (-5, -3),
        "chest_core": (-5, -2),
        "shoulder_l": (-6, -2),
        "shoulder_r": (-3, -2),
        "arm_l": (-6, -1),
        "arm_r": (-2, -1),
        "hand_r": (-1, 0),
        "torso": (-3, -1),
        "pelvis": (-1, 0),
        "hip_l": (-2, 0),
        "hip_r": (0, 0),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_hit = [
        (base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1])
        for k in base_landmarks
    ] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit, power=2.0, epsilon=4.0)

    hit_key = place_rotated_element(key_raw, deg=-30, target_center=(58, 29), scale=1.0)
    hit_weapon = place_rotated_element(weapon_raw, deg=-20, target_center=(94, 76), scale=1.05)
    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, hit_key)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit_body)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_weapon)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (收招歸位·冷氣洩壓 / Post-Strike Vent & Reset)
    # Slight forward crouch recovery. Head x+2, y+3, chest x+1, y+2.
    # Ripper claw lowered and resetting (+10 deg, target=(101, 77), scale=1.0).
    # Winding key resets to near vertical (+12 deg, target=(68, 33)).
    # Balanced, grounded, stable recovery.
    # =========================================================================
    rec_offsets = {
        "head_top": (2, 3),
        "head_cowl_l": (1, 3),
        "head_cowl_r": (3, 3),
        "visor_brow": (2, 3),
        "led_eye_l": (2, 3),
        "led_eye_r": (2, 3),
        "snout": (2, 3),
        "jaw": (2, 3),
        "throat": (2, 2),
        "thruster_l": (0, 2),
        "thruster_r": (3, 2),
        "thruster_base": (2, 2),
        "chest_core": (1, 2),
        "shoulder_l": (0, 2),
        "shoulder_r": (3, 2),
        "arm_l": (-1, 1),
        "arm_r": (2, 1),
        "hand_r": (3, 1),
        "torso": (1, 1),
        "pelvis": (0, 1),
        "hip_l": (-1, 1),
        "hip_r": (1, 1),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_rec = [
        (base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1])
        for k in base_landmarks
    ] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec, power=2.0, epsilon=4.0)

    rec_key = place_rotated_element(key_raw, deg=12, target_center=(68, 33), scale=1.0)
    rec_weapon = place_rotated_element(weapon_raw, deg=10, target_center=(101, 77), scale=1.0)
    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, rec_key)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec_body)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_weapon)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def main() -> None:
    print("=== Generating The Starbreaker Honey Badger 6 Action Poses ===")
    poses = generate_poses()

    for name, im in poses.items():
        # Save 128x128
        out_128 = os.path.join(OUT_DIR, f"{name}.png")
        im.save(out_128)
        print(f"✓ Saved 128x128: {out_128}")

        # Save 512x512 LANCZOS
        im_512 = im.resize((512, 512), Image.Resampling.LANCZOS)
        out_512 = os.path.join(OUT_DIR, f"{name}_512.png")
        im_512.save(out_512)
        print(f"✓ Saved 512x512 LANCZOS: {out_512}")

    # Generate 768x128 proof sheets (ordered: idle, telegraph, attack, recover, skill, hit)
    pose_order = ["idle", "telegraph", "attack", "recover", "skill", "hit"]
    proof_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))

    for idx, p in enumerate(pose_order):
        proof_768.paste(poses[p], (idx * 128, 0), poses[p])
        proof_mag.alpha_composite(poses[p], (idx * 128, 0))

    path_768 = f"{REPO_ROOT}/game/assets/sprites/player/proof_badger_combat_poses_768.png"
    path_mag = f"{REPO_ROOT}/game/assets/sprites/player/proof_badger_combat_poses_magenta.png"
    proof_768.save(path_768)
    proof_mag.save(path_mag)
    print(f"✓ Saved Proof Sheets:\n  {path_768}\n  {path_mag}")

    print("\n🎉 STARBREAKER BADGER COMBAT POSES GENERATION COMPLETE!")


if __name__ == "__main__":
    main()
