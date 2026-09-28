#!/usr/bin/env python3
"""
tools/build_armadillo_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Crucible Armadillo (第四十九族 熔鎧犰狳, armadillo)
in Clockwork Heart:
  game/assets/sprites/player/poses/armadillo/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/armadillo/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
Features crucible iron chassis, quenched visor cowl, amber refractory lens, foundry anvil cuirass,
segmented cast iron carapace, crucible four-leaf winding key, and black iron heavy sword.
"""

import math
import os
import shutil
from typing import cast
from PIL import Image, ImageOps
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/armadillo"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/armadillo"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical slice layers (128x128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_armadillo_crucible_four_leaf_key.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_armadillo_segmented_cast_iron_carapace.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_armadillo_crucible_iron_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_armadillo_quenched_visor_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_armadillo_foundry_anvil_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_armadillo_amber_refractory_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_armadillo_black_iron_heavy_sword.png").convert("RGBA")

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
    (24, 116), (64, 116), (94, 116)
]

base_landmarks = {
    "cowl_crest": (64, 25),
    "cowl_brow": (64, 34),
    "cowl_l": (44, 38),
    "cowl_r": (84, 38),
    "optic_l": (54, 42),
    "optic_r": (74, 42),
    "snout": (64, 52),
    "throat": (64, 56),
    "shoulder_l": (42, 60),
    "shoulder_r": (86, 60),
    "carapace_top": (42, 58),
    "carapace_mid": (35, 74),
    "carapace_bot": (32, 92),
    "chest_core": (64, 70),
    "arm_l": (38, 76),
    "arm_r": (84, 76),
    "waist_belt": (64, 88),
    "pelvis": (62, 98),
    "tail_root": (40, 104),
    "tail_tip": (30, 114),
    "foot_l": (44, 114),
    "foot_r": (76, 114),
}

# Base body composite without weapon and winding key (z: curio, chassis, head, costume, optic)
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
    # 1. IDLE (熔爐堅守·重步巡哨 / Crucible Bastion Poise)
    # Grounded confident vanguard stance. Key at (65, 35), weapon sword at (88, 57).
    # Perfectly crisp, grounded and zero-defect.
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(65, 35), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(88, 57), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (熔鎧蓄壓·抱頭聚勢 / Crucible Compression & Greatsword Drawback)
    # Low vanguard crouch, head and torso tuck into cast-iron carapace (head y+6, x+1; chest y+4, x+1).
    # Heavy sword draws back close to shoulder (-30 deg, target=(78, 53), scale=1.04).
    # Four-leaf key counter-winds (-45 deg, target=(62, 40)).
    # =========================================================================
    tele_offsets = {
        "cowl_crest": (1, 6),
        "cowl_brow": (1, 6),
        "cowl_l": (-1, 6),
        "cowl_r": (2, 6),
        "optic_l": (0, 6),
        "optic_r": (2, 6),
        "snout": (1, 5),
        "throat": (1, 5),
        "shoulder_l": (-1, 4),
        "shoulder_r": (2, 4),
        "carapace_top": (-2, 4),
        "carapace_mid": (-2, 3),
        "carapace_bot": (-2, 2),
        "chest_core": (1, 4),
        "arm_l": (-2, 3),
        "arm_r": (0, 3),
        "waist_belt": (0, 2),
        "pelvis": (0, 1),
        "tail_root": (-1, 1),
        "tail_tip": (-1, 0),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele)
    tele_key = place_rotated_element(key_raw, deg=-45, target_center=(62, 40), scale=1.0)
    tele_weapon = place_rotated_element(weapon_raw, deg=-30, target_center=(78, 53), scale=1.04)
    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, tele_key)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele_body)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_weapon)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (黑鐵重斬·踏地裂地擊 / Black Iron Cleave & Groundbreaker Lunge)
    # Violent forward leap and ground-cleaving strike (head x+7, y-2; chest x+6, y-1).
    # Heavy sword swings down-forward (+42 deg, target=(100, 68), scale=1.18).
    # Four-leaf winding key releases with inertia (+50 deg, target=(72, 28), scale=1.05).
    # =========================================================================
    atk_offsets = {
        "cowl_crest": (7, -2),
        "cowl_brow": (7, -2),
        "cowl_l": (6, -2),
        "cowl_r": (8, -2),
        "optic_l": (7, -2),
        "optic_r": (7, -2),
        "snout": (8, -1),
        "throat": (7, -1),
        "shoulder_l": (4, -1),
        "shoulder_r": (8, -1),
        "carapace_top": (3, -1),
        "carapace_mid": (2, 0),
        "carapace_bot": (1, 0),
        "chest_core": (6, -1),
        "arm_l": (2, 0),
        "arm_r": (9, -2),
        "waist_belt": (3, 0),
        "pelvis": (2, 0),
        "tail_root": (1, 0),
        "tail_tip": (0, 0),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk)
    atk_key = place_rotated_element(key_raw, deg=50, target_center=(72, 28), scale=1.05)
    atk_weapon = place_rotated_element(weapon_raw, deg=42, target_center=(100, 68), scale=1.18)
    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, atk_key)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk_body)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_weapon)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (熔火全開·旋輪鋼甲崩山破 / Molten Overdrive · Carapace Wheel Sunder)
    # Upward-surging two-handed overhead greatsword smash (head x+4, y-6; chest x+4, y-4).
    # Heavy sword raised high in earth-shattering stance (+65 deg, target=(96, 44), scale=1.22).
    # Winding key over-winds with torque (+90 deg, target=(68, 24), scale=1.08).
    # =========================================================================
    skill_offsets = {
        "cowl_crest": (4, -6),
        "cowl_brow": (4, -6),
        "cowl_l": (3, -6),
        "cowl_r": (5, -6),
        "optic_l": (4, -6),
        "optic_r": (4, -6),
        "snout": (5, -5),
        "throat": (4, -5),
        "shoulder_l": (3, -4),
        "shoulder_r": (6, -4),
        "carapace_top": (2, -3),
        "carapace_mid": (1, -2),
        "carapace_bot": (0, -1),
        "chest_core": (4, -4),
        "arm_l": (1, -3),
        "arm_r": (8, -5),
        "waist_belt": (2, -2),
        "pelvis": (1, -1),
        "tail_root": (0, 0),
        "tail_tip": (0, 0),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_skill = [(base_landmarks[k][0] + skill_offsets[k][0], base_landmarks[k][1] + skill_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skill_body = warp_image_idw(body_core, src_pts, dst_skill)
    skill_key = place_rotated_element(key_raw, deg=90, target_center=(68, 24), scale=1.08)
    skill_weapon = place_rotated_element(weapon_raw, deg=65, target_center=(96, 44), scale=1.22)
    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, skill_key)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill_body)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_weapon)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (鑄鐵甲震·硬直受挫 / Quenched Carapace Shock Absorber)
    # Absorbing blow! Recoil backward-left (head x-6, y-2; chest x-4, y-1).
    # Heavy sword knocked back in defensive guard (-22 deg, target=(82, 65), scale=1.04).
    # Four-leaf key shaken counter-clockwise (-30 deg, target=(58, 30), scale=1.0).
    # =========================================================================
    hit_offsets = {
        "cowl_crest": (-6, -2),
        "cowl_brow": (-6, -2),
        "cowl_l": (-7, -2),
        "cowl_r": (-5, -2),
        "optic_l": (-6, -2),
        "optic_r": (-6, -2),
        "snout": (-6, -1),
        "throat": (-5, -1),
        "shoulder_l": (-5, -1),
        "shoulder_r": (-3, -1),
        "carapace_top": (-5, -1),
        "carapace_mid": (-4, 0),
        "carapace_bot": (-3, 0),
        "chest_core": (-4, -1),
        "arm_l": (-5, 0),
        "arm_r": (-2, 0),
        "waist_belt": (-2, 0),
        "pelvis": (-1, 0),
        "tail_root": (-2, 0),
        "tail_tip": (-1, 0),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit)
    hit_key = place_rotated_element(key_raw, deg=-30, target_center=(58, 30), scale=1.0)
    hit_weapon = place_rotated_element(weapon_raw, deg=-22, target_center=(82, 65), scale=1.04)
    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, hit_key)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit_body)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_weapon)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (爐火冷卻·回氣卸力 / Forge Vent & Stance Reset)
    # Stance settling back after cleave (head x+2, y+3; chest x+1, y+2).
    # Heavy sword lowering to ground (+12 deg, target=(88, 64), scale=1.0).
    # Winding key resets towards upright (+12 deg, target=(66, 36), scale=1.0).
    # =========================================================================
    rec_offsets = {
        "cowl_crest": (2, 3),
        "cowl_brow": (2, 3),
        "cowl_l": (1, 3),
        "cowl_r": (3, 3),
        "optic_l": (2, 3),
        "optic_r": (2, 3),
        "snout": (2, 3),
        "throat": (2, 2),
        "shoulder_l": (1, 2),
        "shoulder_r": (2, 2),
        "carapace_top": (0, 2),
        "carapace_mid": (0, 1),
        "carapace_bot": (0, 1),
        "chest_core": (1, 2),
        "arm_l": (0, 1),
        "arm_r": (2, 1),
        "waist_belt": (1, 1),
        "pelvis": (0, 0),
        "tail_root": (0, 0),
        "tail_tip": (0, 0),
        "foot_l": (0, 0),
        "foot_r": (0, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec)
    rec_key = place_rotated_element(key_raw, deg=12, target_center=(66, 36), scale=1.0)
    rec_weapon = place_rotated_element(weapon_raw, deg=12, target_center=(88, 64), scale=1.0)
    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, rec_key)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec_body)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_weapon)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def build_and_save():
    print("Generating armadillo combat action poses...")
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

    p768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_armadillo_combat_poses_768.png"
    pmag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_armadillo_combat_poses_magenta.png"
    proof_768.save(p768_path, "PNG")
    proof_mag.save(pmag_path, "PNG")
    print(f"✓ Saved proof sheets:\n  - {p768_path}\n  - {pmag_path}")


if __name__ == "__main__":
    build_and_save()
