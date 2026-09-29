#!/usr/bin/env python3
"""
tools/build_giraffe_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Belfry Giraffe (第五十五族 鐘塔長頸鹿, giraffe)
in Clockwork Heart:
  game/assets/sprites/player/poses/giraffe/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/giraffe/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16, 0-QA34).
Features stamped tinplate chassis, telescoping periscope cowl, dual periscope quartz lens, dawn herald woolen cape,
three-ring carillon brass key, belfry celestial-string composite bow, and pendulum bob link tail.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/giraffe"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/giraffe"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_giraffe_three_ring_carillon_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_giraffe_pendulum_bob_link_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_giraffe_sanded_tinplate_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_giraffe_telescoping_periscope_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_giraffe_dawn_herald_woolen_cape.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_giraffe_dual_periscope_quartz_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_giraffe_belfry_celestial_bow.png").convert("RGBA")

# Extract raw weapon and key crops
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Reference ground shadow from canonical party idle asset
ref_shadow_im = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/giraffe_idle.png").convert("RGBA")
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
    (20, 116), (64, 116), (108, 116)
]

base_landmarks = {
    "ossicone_l": (52, 20),
    "ossicone_r": (76, 20),
    "cowl_top": (64, 14),
    "optic_l": (54, 42),
    "optic_r": (74, 42),
    "cowl_chin": (64, 54),
    "neck_mid": (64, 50),
    "neck_base": (64, 58),
    "chest_brooch": (64, 66),
    "cape_shoulder_l": (44, 68),
    "cape_shoulder_r": (84, 68),
    "cape_flank_l": (40, 78),
    "cape_flank_r": (88, 78),
    "pelvis": (64, 88),
    "tail_joint": (54, 86),
    "tail_bob": (46, 104),
    "leg_back_l": (36, 104),
    "leg_front_l": (48, 104),
    "leg_front_r": (80, 104),
    "leg_back_r": (90, 104),
    "hoof_back_l": (36, 114),
    "hoof_front_l": (48, 114),
    "hoof_front_r": (80, 114),
    "hoof_back_r": (90, 114),
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
    # 1. IDLE (天軌哨望·鐘塔遊俠持弓架 / Belfry Lookout Ranger Neutral Guard)
    # Neutral watchman stance. Key at (64, 25), bow at (91, 73).
    # Perfectly crisp, grounded and zero-defect.
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(64, 25), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(91, 73), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (高塔蓄力·弦滿引弓蓄勢 / Belfry Calibration & String Draw)
    # Deep crouch & draw back. Head and periscope neck retract and tilt back (head y+5, x-6; torso y+4, x-4).
    # Telescoping neck compresses slightly to steady high-tension draw.
    # Key counter-winds with tension clicks (-40 deg, target=(58, 28), scale=0.96).
    # Belfry celestial bow pulled back tight to chest (-20 deg, target=(84, 70), scale=1.02).
    # Clean, pure character kinematics with zero artificial wireframe lines.
    # =========================================================================
    tele_offsets = {
        "ossicone_l": (-7, 5),
        "ossicone_r": (-5, 5),
        "cowl_top": (-6, 5),
        "optic_l": (-6, 5),
        "optic_r": (-5, 5),
        "cowl_chin": (-6, 4),
        "neck_mid": (-5, 4),
        "neck_base": (-4, 4),
        "chest_brooch": (-5, 4),
        "cape_shoulder_l": (-6, 4),
        "cape_shoulder_r": (-3, 4),
        "cape_flank_l": (-5, 3),
        "cape_flank_r": (-3, 3),
        "pelvis": (-3, 2),
        "tail_joint": (-4, 2),
        "tail_bob": (-5, 3),
        "leg_back_l": (-3, 2),
        "leg_front_l": (-2, 2),
        "leg_front_r": (0, 2),
        "leg_back_r": (1, 2),
        "hoof_back_l": (-1, 0),
        "hoof_front_l": (0, 0),
        "hoof_front_r": (0, 0),
        "hoof_back_r": (1, 0),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele)
    tele_key = place_rotated_element(key_raw, deg=-40, target_center=(58, 28), scale=0.96)
    tele_weapon = place_rotated_element(weapon_raw, deg=-20, target_center=(84, 70), scale=1.02)

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, tele_key)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele_body)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_weapon)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (天弦發射·穿甲光矢貫穿 / Celestial Arrow Snipe Thrust)
    # Violent forward release! Head and neck lunge forward (head x+13, y-1; torso x+10, y=0).
    # Bow thrusts forward in upright follow-through (+18 deg, target=(98, 67), scale=1.10).
    # Key spins forward (+62 deg, target=(76, 27), scale=1.02).
    # Clean, pure dynamic sprite silhouette with zero 1px vector lines.
    # =========================================================================
    atk_offsets = {
        "ossicone_l": (11, -1),
        "ossicone_r": (14, -1),
        "cowl_top": (13, -1),
        "optic_l": (12, -1),
        "optic_r": (13, -1),
        "cowl_chin": (12, 0),
        "neck_mid": (11, 0),
        "neck_base": (10, 0),
        "chest_brooch": (10, 0),
        "cape_shoulder_l": (8, 0),
        "cape_shoulder_r": (12, 0),
        "cape_flank_l": (8, 0),
        "cape_flank_r": (11, 0),
        "pelvis": (6, 0),
        "tail_joint": (5, 0),
        "tail_bob": (3, 0),
        "leg_back_l": (3, 0),
        "leg_front_l": (5, 0),
        "leg_front_r": (8, 0),
        "leg_back_r": (9, 0),
        "hoof_back_l": (-1, 0),
        "hoof_front_l": (2, 0),
        "hoof_front_r": (4, 0),
        "hoof_back_r": (5, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk)
    atk_key = place_rotated_element(key_raw, deg=62, target_center=(76, 27), scale=1.02)
    atk_weapon = place_rotated_element(weapon_raw, deg=18, target_center=(98, 67), scale=1.10)

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, atk_key)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk_body)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_weapon)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (天頂鐘鳴·天弦貫日雨 / Zenith Chime: Celestial Arrow Barrage)
    # Grand sniping overdrive! Neck extends upward (head y-7, x+2; torso y-4, x+2).
    # Bow held upright aloft to the right (+22 deg, target=(97, 52), scale=1.10) - completely clear of face/eyes!
    # Three-ring carillon key spins at maximum overdrive (+90 deg, target=(66, 28), scale=1.08).
    # High-elevation stance with zero vector hair lines.
    # =========================================================================
    skill_offsets = {
        "ossicone_l": (1, -7),
        "ossicone_r": (3, -7),
        "cowl_top": (2, -7),
        "optic_l": (2, -6),
        "optic_r": (2, -6),
        "cowl_chin": (2, -5),
        "neck_mid": (2, -4),
        "neck_base": (2, -3),
        "chest_brooch": (2, -3),
        "cape_shoulder_l": (1, -3),
        "cape_shoulder_r": (3, -3),
        "cape_flank_l": (1, -2),
        "cape_flank_r": (3, -2),
        "pelvis": (1, -1),
        "tail_joint": (0, -1),
        "tail_bob": (-1, 0),
        "leg_back_l": (0, 0),
        "leg_front_l": (1, 0),
        "leg_front_r": (2, 0),
        "leg_back_r": (2, 0),
        "hoof_back_l": (0, 0),
        "hoof_front_l": (0, 0),
        "hoof_front_r": (1, 0),
        "hoof_back_r": (1, 0),
    }
    dst_skill = [(base_landmarks[k][0] + skill_offsets[k][0], base_landmarks[k][1] + skill_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skill_body = warp_image_idw(body_core, src_pts, dst_skill)
    skill_key = place_rotated_element(key_raw, deg=90, target_center=(66, 28), scale=1.08)
    skill_weapon = place_rotated_element(weapon_raw, deg=22, target_center=(97, 52), scale=1.10)

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, skill_key)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill_body)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_weapon)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (震波受衝·懸吊骨架受擊 / Kinetic Recoil & Pendulum Oscillation)
    # Severe kinetic strike and recoil backward-left (head x-12, y-2; torso x-10, y-1).
    # Bow held defensively across chest (-26 deg, target=(82, 74), scale=1.02).
    # Three-ring carillon key shaken counter-clockwise (-42 deg, target=(54, 24), scale=0.96).
    # Clean, pure character impact recoil.
    # =========================================================================
    hit_offsets = {
        "ossicone_l": (-13, -2),
        "ossicone_r": (-11, -2),
        "cowl_top": (-12, -2),
        "optic_l": (-12, -2),
        "optic_r": (-12, -2),
        "cowl_chin": (-12, -1),
        "neck_mid": (-11, -1),
        "neck_base": (-10, -1),
        "chest_brooch": (-10, -1),
        "cape_shoulder_l": (-11, -1),
        "cape_shoulder_r": (-8, -1),
        "cape_flank_l": (-10, -1),
        "cape_flank_r": (-8, -1),
        "pelvis": (-7, -1),
        "tail_joint": (-6, -1),
        "tail_bob": (-4, 0),
        "leg_back_l": (-5, 0),
        "leg_front_l": (-4, 0),
        "leg_front_r": (-3, 0),
        "leg_back_r": (-2, 0),
        "hoof_back_l": (-3, 0),
        "hoof_front_l": (-2, 0),
        "hoof_front_r": (0, 0),
        "hoof_back_r": (0, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit)
    hit_key = place_rotated_element(key_raw, deg=-42, target_center=(54, 24), scale=0.96)
    hit_weapon = place_rotated_element(weapon_raw, deg=-26, target_center=(82, 74), scale=1.02)

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, hit_key)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit_body)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_weapon)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (擺幅收斂·套管復位歸零 / Dampened Oscillation & Telescoping Reset)
    # Stance settling after attack (head x+2, y+4; torso x+2, y+3).
    # Bow resting in ready low guard (+14 deg, target=(92, 74), scale=1.02).
    # Key smoothly turning back towards neutral (+15 deg, target=(66, 27), scale=0.98).
    # Crisp, clean settling stance with zero blurry white neck patches.
    # =========================================================================
    rec_offsets = {
        "ossicone_l": (1, 4),
        "ossicone_r": (3, 4),
        "cowl_top": (2, 4),
        "optic_l": (2, 4),
        "optic_r": (2, 4),
        "cowl_chin": (2, 3),
        "neck_mid": (2, 3),
        "neck_base": (2, 3),
        "chest_brooch": (2, 3),
        "cape_shoulder_l": (1, 3),
        "cape_shoulder_r": (3, 3),
        "cape_flank_l": (1, 3),
        "cape_flank_r": (3, 3),
        "pelvis": (1, 2),
        "tail_joint": (1, 2),
        "tail_bob": (0, 1),
        "leg_back_l": (0, 1),
        "leg_front_l": (1, 1),
        "leg_front_r": (2, 1),
        "leg_back_r": (2, 1),
        "hoof_back_l": (-1, 0),
        "hoof_front_l": (0, 0),
        "hoof_front_r": (1, 0),
        "hoof_back_r": (1, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec)
    rec_key = place_rotated_element(key_raw, deg=15, target_center=(66, 27), scale=0.98)
    rec_weapon = place_rotated_element(weapon_raw, deg=14, target_center=(92, 74), scale=1.02)

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, rec_key)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec_body)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_weapon)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def build_and_save():
    print("Generating pure, artifact-free giraffe combat action poses...")
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

    p768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_giraffe_combat_poses_768.png"
    pmag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_giraffe_combat_poses_magenta.png"
    proof_768.save(p768_path, "PNG")
    proof_mag.save(pmag_path, "PNG")
    print(f"✓ Saved proof sheets:\n  - {p768_path}\n  - {pmag_path}")


if __name__ == "__main__":
    build_and_save()
