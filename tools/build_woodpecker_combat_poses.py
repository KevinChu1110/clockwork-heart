#!/usr/bin/env python3
"""
tools/build_woodpecker_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Resonance Woodpecker (第四十八族 振律啄木鳥, woodpecker)
in Clockwork Heart:
  game/assets/sprites/player/poses/woodpecker/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/woodpecker/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
Features riveted tinplate brass chassis, scarlet stepped crest cowl, precision gauge monocle,
skyspire inspector harness, prop tail, percussion key, and resonance pneumatic heavy gun.
"""

import math
import os
import shutil
from typing import cast
from PIL import Image, ImageOps
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/woodpecker"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/woodpecker"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical slice layers (128x128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_woodpecker_high_frequency_percussion_key.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_woodpecker_riveted_tinplate_prop_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_woodpecker_tinplate_brass_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_woodpecker_scarlet_crest_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_woodpecker_skyspire_inspector_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_woodpecker_precision_gauge_monocle.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_woodpecker_resonance_pneumatic_heavy_gun.png").convert("RGBA")

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
    (30, 116), (64, 116), (90, 116)
]

base_landmarks = {
    "crest_apex": (64, 12),
    "crest_mid": (64, 22),
    "cowl_brow": (64, 30),
    "cowl_l": (45, 36),
    "cowl_r": (83, 36),
    "optic_l": (54, 42),
    "optic_r": (74, 42),
    "beak": (64, 52),
    "throat": (64, 56),
    "shoulder_l": (44, 62),
    "shoulder_r": (84, 62),
    "chest_dial": (64, 72),
    "arm_l": (46, 76),
    "hand_r": (84, 78),
    "waist_belt": (64, 88),
    "pelvis": (62, 94),
    "tail_base": (48, 96),
    "tail_tip": (32, 115),
    "foot_l": (46, 115),
    "foot_r": (76, 115)
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
    # 1. IDLE (常態巡檢架勢 / Resonance Sentry Poise)
    # Grounded confident ranger poise. Key at (66, 35), weapon gun at (81, 76).
    # Perfectly crisp, grounded and zero-defect.
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(66, 35), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(81, 76), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (高壓蓄能·俯身測距 / High-Pressure Pre-Charge & Sight Alignment)
    # Body lowers forward to charging attack line (head y+5, x+3; chest y+3, x+2).
    # Pneumatic gun draws back close to chest (-18 deg, target=(75, 76), scale=1.02).
    # High-frequency percussion key counter-winds (-45 deg, target=(63, 39)).
    # Prop tail braces against ground to absorb recoil.
    # =========================================================================
    tele_offsets = {
        "crest_apex": (3, 5),
        "crest_mid": (3, 5),
        "cowl_brow": (3, 5),
        "cowl_l": (2, 5),
        "cowl_r": (4, 5),
        "optic_l": (3, 5),
        "optic_r": (3, 5),
        "beak": (4, 5),
        "throat": (3, 4),
        "shoulder_l": (1, 3),
        "shoulder_r": (3, 3),
        "chest_dial": (2, 3),
        "arm_l": (-2, 2),
        "hand_r": (-1, 2),
        "waist_belt": (1, 1),
        "pelvis": (0, 0),
        "tail_base": (-2, 1),
        "tail_tip": (-1, 0),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    src_pts = list(base_landmarks.values()) + anchors
    dst_tele = [
        (base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1])
        for k in base_landmarks
    ] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele, power=2.0, epsilon=4.0)

    tele_key = place_rotated_element(key_raw, deg=-45, target_center=(63, 39), scale=1.0)
    tele_weapon = place_rotated_element(weapon_raw, deg=-18, target_center=(75, 76), scale=1.02)
    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, tele_key)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele_body)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_weapon)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (高頻氣動爆鳴·平射穿刺 / Pneumatic Rapid Percussion Blast)
    # Violent forward thrust & muzzle blast! Heavy gun lunges forward (+12 deg, target=(82, 73), scale=1.05).
    # Head & torso stretch forward into the lunge (head x+7, y-3; chest x+6, y-1).
    # Percussion key releases clockwise with inertia (+55 deg, target=(72, 31)).
    # Prop tail digs into ground against high pneumatic thrust.
    # =========================================================================
    attack_offsets = {
        "crest_apex": (7, -3),
        "crest_mid": (7, -3),
        "cowl_brow": (7, -3),
        "cowl_l": (6, -3),
        "cowl_r": (8, -3),
        "optic_l": (7, -3),
        "optic_r": (7, -3),
        "beak": (9, -3),
        "throat": (7, -2),
        "shoulder_l": (5, -1),
        "shoulder_r": (7, -1),
        "chest_dial": (6, -1),
        "arm_l": (4, 0),
        "hand_r": (6, 0),
        "waist_belt": (3, 0),
        "pelvis": (1, 0),
        "tail_base": (-1, 0),
        "tail_tip": (-1, 0),
        "foot_l": (0, 0),
        "foot_r": (1, 0),
    }
    dst_attack = [
        (base_landmarks[k][0] + attack_offsets[k][0], base_landmarks[k][1] + attack_offsets[k][1])
        for k in base_landmarks
    ] + anchors
    warped_attack_body = warp_image_idw(body_core, src_pts, dst_attack, power=2.0, epsilon=4.0)

    attack_key = place_rotated_element(key_raw, deg=55, target_center=(72, 31), scale=1.0)
    attack_weapon = place_rotated_element(weapon_raw, deg=12, target_center=(82, 73), scale=1.05)
    attack_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    attack_canvas = Image.alpha_composite(attack_canvas, attack_key)
    attack_canvas = Image.alpha_composite(attack_canvas, warped_attack_body)
    attack_canvas = Image.alpha_composite(attack_canvas, attack_weapon)
    poses["attack"] = enforce_ground_shadow(attack_canvas)

    # =========================================================================
    # 4. RECOVER (氣閥洩壓·冷卻回正 / Vent Exhaust Reset & Thermal Cooldown)
    # Gun vents steam downward (-32 deg, target=(75, 82), scale=1.0).
    # Head & torso lean back in post-shot decompression (head x-5, y+3; chest x-3, y+2).
    # Percussion key spins to rest (+15 deg, target=(63, 38)).
    # =========================================================================
    recov_offsets = {
        "crest_apex": (-5, 3),
        "crest_mid": (-5, 3),
        "cowl_brow": (-5, 3),
        "cowl_l": (-5, 3),
        "cowl_r": (-4, 3),
        "optic_l": (-5, 3),
        "optic_r": (-4, 3),
        "beak": (-5, 3),
        "throat": (-4, 2),
        "shoulder_l": (-3, 2),
        "shoulder_r": (-3, 2),
        "chest_dial": (-3, 2),
        "arm_l": (-3, 3),
        "hand_r": (-3, 3),
        "waist_belt": (-2, 1),
        "pelvis": (-1, 0),
        "tail_base": (-1, 1),
        "tail_tip": (0, 0),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_recov = [
        (base_landmarks[k][0] + recov_offsets[k][0], base_landmarks[k][1] + recov_offsets[k][1])
        for k in base_landmarks
    ] + anchors
    warped_recov_body = warp_image_idw(body_core, src_pts, dst_recov, power=2.0, epsilon=4.0)

    recov_key = place_rotated_element(key_raw, deg=15, target_center=(63, 38), scale=0.98)
    recov_weapon = place_rotated_element(weapon_raw, deg=-32, target_center=(75, 82), scale=1.0)
    recov_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    recov_canvas = Image.alpha_composite(recov_canvas, recov_key)
    recov_canvas = Image.alpha_composite(recov_canvas, warped_recov_body)
    recov_canvas = Image.alpha_composite(recov_canvas, recov_weapon)
    poses["recover"] = enforce_ground_shadow(recov_canvas)

    # =========================================================================
    # 5. SKILL (天穹共振·超頻音錐貫穿 / Skyspire Sonic Resonance Penetration)
    # Ultimate resonance piercing blast! Heavy gun raised at 42 deg (target=(78, 64), scale=1.12).
    # Crest flairs up, core gauge needles red-line (head y-4..-6, x+3).
    # Percussion key spins violently (-85 deg, target=(68, 30)).
    # High mechanical articulation and stance change.
    # =========================================================================
    skill_offsets = {
        "crest_apex": (3, -6),
        "crest_mid": (3, -5),
        "cowl_brow": (3, -4),
        "cowl_l": (2, -4),
        "cowl_r": (4, -4),
        "optic_l": (3, -4),
        "optic_r": (3, -4),
        "beak": (4, -4),
        "throat": (3, -3),
        "shoulder_l": (2, -2),
        "shoulder_r": (4, -2),
        "chest_dial": (3, -2),
        "arm_l": (1, -2),
        "hand_r": (3, -2),
        "waist_belt": (1, -1),
        "pelvis": (0, 0),
        "tail_base": (-2, 0),
        "tail_tip": (-2, 0),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_skill = [
        (base_landmarks[k][0] + skill_offsets[k][0], base_landmarks[k][1] + skill_offsets[k][1])
        for k in base_landmarks
    ] + anchors
    warped_skill_body = warp_image_idw(body_core, src_pts, dst_skill, power=2.0, epsilon=4.0)

    skill_key = place_rotated_element(key_raw, deg=-85, target_center=(68, 30), scale=1.05)
    skill_weapon = place_rotated_element(weapon_raw, deg=42, target_center=(78, 64), scale=1.12)
    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, skill_key)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill_body)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_weapon)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 6. HIT (受創過載·衝擊震退 / Recoil Blowback & Impact Shock)
    # Violent blowback! Head & torso violently tilt backward (head x-8, y-2; chest x-6).
    # Heavy gun recoils upward in staggering recoil (+36 deg, target=(74, 71), scale=1.02).
    # Percussion key rattled askew (-65 deg, target=(58, 33)).
    # =========================================================================
    hit_offsets = {
        "crest_apex": (-8, -2),
        "crest_mid": (-8, -2),
        "cowl_brow": (-8, -2),
        "cowl_l": (-8, -2),
        "cowl_r": (-7, -2),
        "optic_l": (-8, -2),
        "optic_r": (-7, -2),
        "beak": (-9, -2),
        "throat": (-7, -1),
        "shoulder_l": (-6, 0),
        "shoulder_r": (-5, 0),
        "chest_dial": (-6, 0),
        "arm_l": (-6, 1),
        "hand_r": (-5, 1),
        "waist_belt": (-3, 0),
        "pelvis": (-2, 0),
        "tail_base": (-3, 0),
        "tail_tip": (-1, 0),
        "foot_l": (0, 0),
        "foot_r": (-1, 0),
    }
    dst_hit = [
        (base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1])
        for k in base_landmarks
    ] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit, power=2.0, epsilon=4.0)

    hit_key = place_rotated_element(key_raw, deg=-65, target_center=(58, 33), scale=1.0)
    hit_weapon = place_rotated_element(weapon_raw, deg=36, target_center=(74, 71), scale=1.02)
    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, hit_key)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit_body)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_weapon)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    return poses


def build_and_save():
    print("Generating woodpecker combat action poses...")
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

    p768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_woodpecker_combat_poses_768.png"
    pmag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_woodpecker_combat_poses_magenta.png"
    proof_768.save(p768_path, "PNG")
    proof_mag.save(pmag_path, "PNG")
    print(f"✓ Saved proof sheets:\n  - {p768_path}\n  - {pmag_path}")


if __name__ == "__main__":
    build_and_save()
