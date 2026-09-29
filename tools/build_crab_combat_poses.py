#!/usr/bin/env python3
"""
tools/build_crab_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Anvil Crab (第五十二族 熔砧石蟹, crab)
in Clockwork Heart:
  game/assets/sprites/player/poses/crab/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/crab/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16, 0-QA34).
Features molten iron crucible chassis, periscope visor cowl, dual gauge convex optic lens, furnace sapper cuirass,
pneumatic exhaust chimney back curio, quad-flue crucible t-bar winding key, and obsidian stamping fist.
"""

import math
import os
from typing import cast
from PIL import Image, ImageOps
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crab"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/crab"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_crab_quad_flue_crucible_t_bar.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_crab_pneumatic_exhaust_chimney.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_crab_molten_iron_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_crab_periscope_visor_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_crab_furnace_sapper_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_crab_dual_gauge_convex_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_crab_obsidian_stamping_fist.png").convert("RGBA")

# Extract raw weapon and key crops
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Reference ground shadow from canonical party idle asset
ref_shadow_im = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/crab_idle.png").convert("RGBA")
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
    """Rotates and places any element with sub-pixel quality."""
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
    "periscope_top": (64, 18),
    "periscope_horn_l": (44, 24),
    "periscope_horn_r": (84, 24),
    "optic_l": (54, 42),
    "optic_r": (74, 42),
    "brow_cowl": (64, 52),
    "chimney_l": (38, 36),
    "chimney_r": (90, 36),
    "shoulder_l": (34, 60),
    "shoulder_r": (92, 60),
    "chest_cuirass": (64, 72),
    "apron_mid": (64, 88),
    "arm_guard_l": (36, 72),
    "arm_hinge_r": (84, 74),
    "pelvis": (64, 94),
    "knee_l": (48, 100),
    "knee_r": (73, 100),
    "roller_l": (34, 108),
    "roller_r": (86, 108),
    "foot_l": (44, 114),
    "foot_r": (76, 114),
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
    # 1. IDLE (熔爐磐石·武僧守架 / Molten Furnace Stance - monk neutral guard)
    # Neutral vanguard monk poise. Key at (64, 33), fist at (89, 74).
    # Perfectly crisp, grounded and zero-defect.
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(64, 33), scale=0.98)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(89, 74), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (熔岩積蓄·重衝壓後蓄 / Molten Pressure Charge & Stamping Drawback)
    # Heavy crouch & draw back. Head and torso sink down (head y+5, torso y+4).
    # Stepper rollers and feet brace low against stone ground.
    # Obsidian stamping fist drawn tight to furnace chest (-25 deg, target=(81, 72), scale=1.02).
    # Quad-flue crucible key counter-winds (-40 deg, target=(62, 37), scale=0.96).
    # =========================================================================
    tele_offsets = {
        "periscope_top": (1, 5),
        "periscope_horn_l": (-1, 5),
        "periscope_horn_r": (2, 5),
        "optic_l": (0, 5),
        "optic_r": (2, 5),
        "brow_cowl": (1, 4),
        "chimney_l": (-1, 5),
        "chimney_r": (2, 5),
        "shoulder_l": (-2, 4),
        "shoulder_r": (2, 4),
        "chest_cuirass": (1, 4),
        "apron_mid": (0, 3),
        "arm_guard_l": (1, 3),
        "arm_hinge_r": (-3, 2),
        "pelvis": (0, 2),
        "knee_l": (-2, 1),
        "knee_r": (2, 1),
        "roller_l": (-3, 0),
        "roller_r": (3, 0),
        "foot_l": (-1, 0),
        "foot_r": (1, 0),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele)
    tele_key = place_rotated_element(key_raw, deg=-40, target_center=(62, 37), scale=0.96)
    tele_weapon = place_rotated_element(weapon_raw, deg=-25, target_center=(81, 72), scale=1.02)
    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, tele_key)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele_body)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_weapon)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (黑曜衝壓·鐵砧破甲重拳 / Obsidian Anvil Stamping Punch)
    # Violent forward lunge! Head and torso shift forward (head x+7, y-1; torso x+6, y=0).
    # Stepper rollers push off dynamically.
    # Obsidian stamping fist slams forward (+32 deg, target=(101, 70), scale=1.18).
    # Crucible key spins forward (+52 deg, target=(71, 30), scale=1.0).
    # =========================================================================
    atk_offsets = {
        "periscope_top": (7, -1),
        "periscope_horn_l": (5, -1),
        "periscope_horn_r": (8, -1),
        "optic_l": (7, -1),
        "optic_r": (7, -1),
        "brow_cowl": (7, 0),
        "chimney_l": (4, -1),
        "chimney_r": (8, -1),
        "shoulder_l": (4, 0),
        "shoulder_r": (8, -1),
        "chest_cuirass": (6, 0),
        "apron_mid": (4, 0),
        "arm_guard_l": (3, 1),
        "arm_hinge_r": (8, -1),
        "pelvis": (3, 0),
        "knee_l": (2, 0),
        "knee_r": (4, 0),
        "roller_l": (-2, 0),
        "roller_r": (4, 0),
        "foot_l": (-1, 0),
        "foot_r": (3, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk)
    atk_key = place_rotated_element(key_raw, deg=52, target_center=(71, 30), scale=1.0)
    atk_weapon = place_rotated_element(weapon_raw, deg=32, target_center=(101, 70), scale=1.18)
    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, atk_key)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk_body)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_weapon)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (熔爐過載·四聯排煙地煞碎地拳 / Furnace Overdrive & Quake Strike)
    # Airborne surge / high strike (head y-5, x+3; torso y-4, x+3).
    # Legs flare and lift off ground in hydraulic stamping pulse.
    # Stamping fist raised high overhead in devastating smash stance (+68 deg, target=(96, 52), scale=1.22).
    # Quad-flue crucible key revs to maximum overdrive (+90 deg, target=(67, 26), scale=1.05).
    # =========================================================================
    skill_offsets = {
        "periscope_top": (3, -5),
        "periscope_horn_l": (1, -5),
        "periscope_horn_r": (5, -5),
        "optic_l": (3, -5),
        "optic_r": (3, -5),
        "brow_cowl": (3, -4),
        "chimney_l": (2, -5),
        "chimney_r": (5, -5),
        "shoulder_l": (1, -4),
        "shoulder_r": (5, -4),
        "chest_cuirass": (3, -3),
        "apron_mid": (2, -2),
        "arm_guard_l": (1, -3),
        "arm_hinge_r": (4, -5),
        "pelvis": (1, -2),
        "knee_l": (0, -2),
        "knee_r": (2, -2),
        "roller_l": (-1, -1),
        "roller_r": (2, -1),
        "foot_l": (0, -1),
        "foot_r": (1, -1),
    }
    dst_skill = [(base_landmarks[k][0] + skill_offsets[k][0], base_landmarks[k][1] + skill_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skill_body = warp_image_idw(body_core, src_pts, dst_skill)
    skill_key = place_rotated_element(key_raw, deg=90, target_center=(67, 26), scale=1.05)
    skill_weapon = place_rotated_element(weapon_raw, deg=68, target_center=(96, 52), scale=1.22)
    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, skill_key)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill_body)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_weapon)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (鑄鐵受衝·外殼巨震受擊 / Carapace Kinetic Shock & Stagger)
    # Recoil backward-left from severe kinetic strike (head x-6, y-1; torso x-4).
    # Stamping fist parries reflexively (-20 deg, target=(81, 76), scale=1.02).
    # Crucible key shaken counter-clockwise (-30 deg, target=(58, 31), scale=0.96).
    # =========================================================================
    hit_offsets = {
        "periscope_top": (-6, -1),
        "periscope_horn_l": (-7, -1),
        "periscope_horn_r": (-5, -1),
        "optic_l": (-6, -1),
        "optic_r": (-6, -1),
        "brow_cowl": (-6, 0),
        "chimney_l": (-6, -1),
        "chimney_r": (-3, -1),
        "shoulder_l": (-5, 0),
        "shoulder_r": (-3, 0),
        "chest_cuirass": (-4, 0),
        "apron_mid": (-3, 0),
        "arm_guard_l": (-5, 0),
        "arm_hinge_r": (-3, 0),
        "pelvis": (-2, 0),
        "knee_l": (-2, 0),
        "knee_r": (-1, 0),
        "roller_l": (-2, 0),
        "roller_r": (0, 0),
        "foot_l": (-1, 0),
        "foot_r": (0, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit)
    hit_key = place_rotated_element(key_raw, deg=-30, target_center=(58, 31), scale=0.96)
    hit_weapon = place_rotated_element(weapon_raw, deg=-20, target_center=(81, 76), scale=1.02)
    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, hit_key)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit_body)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_weapon)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (氣閥排氣·重壓冷卻復位 / Pneumatic Vent Release & Reset)
    # Stance settling after heavy punch (head x+2, y+4; torso x+2, y+3).
    # Stamping fist resting in neutral angle (+14 deg, target=(87, 77), scale=1.02).
    # Crucible key settling back upright (+15 deg, target=(66, 36), scale=0.98).
    # =========================================================================
    rec_offsets = {
        "periscope_top": (2, 4),
        "periscope_horn_l": (1, 4),
        "periscope_horn_r": (3, 4),
        "optic_l": (2, 4),
        "optic_r": (2, 4),
        "brow_cowl": (2, 3),
        "chimney_l": (1, 4),
        "chimney_r": (3, 4),
        "shoulder_l": (1, 3),
        "shoulder_r": (3, 3),
        "chest_cuirass": (2, 3),
        "apron_mid": (1, 2),
        "arm_guard_l": (2, 3),
        "arm_hinge_r": (2, 3),
        "pelvis": (0, 2),
        "knee_l": (-1, 2),
        "knee_r": (2, 2),
        "roller_l": (-2, 0),
        "roller_r": (2, 0),
        "foot_l": (-1, 0),
        "foot_r": (1, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec)
    rec_key = place_rotated_element(key_raw, deg=15, target_center=(66, 36), scale=0.98)
    rec_weapon = place_rotated_element(weapon_raw, deg=14, target_center=(87, 77), scale=1.02)
    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, rec_key)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec_body)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_weapon)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def build_and_save():
    print("Generating crab combat action poses...")
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

    p768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_crab_combat_poses_768.png"
    pmag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_crab_combat_poses_magenta.png"
    proof_768.save(p768_path, "PNG")
    proof_mag.save(pmag_path, "PNG")
    print(f"✓ Saved proof sheets:\n  - {p768_path}\n  - {pmag_path}")


if __name__ == "__main__":
    build_and_save()
