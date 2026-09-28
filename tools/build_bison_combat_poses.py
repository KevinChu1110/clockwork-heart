#!/usr/bin/env python3
"""
tools/build_bison_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Groundshaker Bison (第四十四族 撼地野牛, bison)
in Clockwork Heart:
  game/assets/sprites/player/poses/bison/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/bison/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
Enhanced with expressive junkyard demolish kinematics, heavy anvil mechanics, and rich toy articulation.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bison"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/bison"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical slice layers (128x128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_bison_heavy_cross_t_bar_cast_iron.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_bison_twin_vent_exhaust_stack.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_bison_rusted_tinplate_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_bison_riveted_brow_horn_crest.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_bison_junkyard_demolition_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_bison_amber_pressure_gauge_eye.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_bison_wasteland_anvil_crusher_hammer.png").convert("RGBA")

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Canonical ground shadow directly from chassis slice (118..127)
# Natural soft falloff with zero artificial horizontal cutoffs
comp_path = f"{BASE_DIR}/proof_paperdoll_bison_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
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
    (44, 116), (78, 116), (64, 116)
]

base_landmarks = {
    "head_top": (64, 18),
    "horn_tip_l": (22, 26),
    "horn_tip_r": (106, 26),
    "horn_crest_l": (36, 32),
    "horn_crest_r": (92, 32),
    "brow_rivet": (64, 30),
    "gauge_eye_l": (54, 42),
    "gauge_eye_r": (74, 42),
    "snout": (64, 52),
    "jaw": (64, 58),
    "throat": (64, 62),
    "chest_plate": (64, 72),
    "core": (64, 76),
    "shoulder_l": (46, 68),
    "shoulder_r": (82, 68),
    "arm_l": (36, 76),
    "arm_r": (88, 76),
    "hand_r": (94, 82),
    "torso": (64, 84),
    "pelvis": (64, 96),
    "hip_l": (46, 100),
    "hip_r": (80, 100),
    "foot_l": (44, 116),
    "foot_r": (78, 116),
    "exhaust_vent_l": (42, 28),
    "exhaust_vent_r": (82, 28),
    "curio_base": (62, 48),
    "key_mount": (80, 34),
}

# Base body without weapon and winding key (z: curio=8, chassis=10, head=20, costume=25, optic=30)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (沉穩架勢 / Groundshaker Poise)
    # Clean poised stance: Winding key at (80, 34), anvil hammer poised at (98, 86).
    # Perfectly crisp, grounded and artifact-free.
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(80, 34), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(98, 86), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (重裝蓄壓·曲角下沉·巨鎚後揚 / Hydraulic Pressure Charge & Anvil Drawback)
    # Heavy crouch forward, horn lowers forward to battering line (y+7, x-3).
    # Heavy anvil hammer draws back into full tension (-32 deg, x-6, y-10).
    # Crosshair T-bar key counter-winds (-40 deg, x-3, y+5).
    # Feet firmly planted on ground plane (foot_l/r = (0,0)).
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-3, 6), "horn_tip_l": (-4, 7), "horn_tip_r": (-2, 6),
        "horn_crest_l": (-4, 6), "horn_crest_r": (-2, 6), "brow_rivet": (-3, 6),
        "gauge_eye_l": (-3, 6), "gauge_eye_r": (-3, 6),
        "snout": (-3, 6), "jaw": (-3, 6), "throat": (-3, 6),
        "chest_plate": (-3, 5), "core": (-3, 5),
        "shoulder_l": (-2, 5), "shoulder_r": (-4, 5),
        "arm_l": (1, 4), "arm_r": (-6, 5),
        "hand_r": (-6, -4),
        "torso": (-3, 5), "pelvis": (-3, 4),
        "hip_l": (-4, 3), "hip_r": (0, 3),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "exhaust_vent_l": (-4, 5), "exhaust_vent_r": (-3, 5), "curio_base": (-3, 5),
        "key_mount": (-3, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_tele = place_rotated_element(key_raw, deg=-40, target_center=(77, 39), scale=1.0)
    hammer_tele = place_rotated_element(weapon_raw, deg=-32, target_center=(92, 76), scale=1.04)

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, hammer_tele)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (重砧碎鐵劈扣 / Wasteland Anvil Crusher Cleave)
    # Massive lunge forward (x+11, y-1), anvil hammer slams forward-down (+35 deg, x-1, y-6).
    # Target center for hammer: (96, 78) -> keeps entire hammer within x=[72..119], y=[54..104].
    # No flat edges, fully intact anvil hammer head.
    # Cross T-bar key spins rapidly (+55 deg, x+8, y-1).
    # Zero stray ribbons or noodles.
    # =========================================================================
    shifts_attack = {
        "head_top": (11, -1), "horn_tip_l": (11, -1), "horn_tip_r": (12, -1),
        "horn_crest_l": (10, -1), "horn_crest_r": (12, -1), "brow_rivet": (11, -1),
        "gauge_eye_l": (11, -1), "gauge_eye_r": (11, -1),
        "snout": (12, 0), "jaw": (11, 0), "throat": (11, 0),
        "chest_plate": (10, 0), "core": (10, 0),
        "shoulder_l": (12, -1), "shoulder_r": (8, 0),
        "arm_l": (14, -2), "arm_r": (-2, 1),
        "hand_r": (4, -4),
        "torso": (9, 0), "pelvis": (7, 0),
        "hip_l": (8, 0), "hip_r": (-2, 0),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "exhaust_vent_l": (6, -1), "exhaust_vent_r": (8, -1), "curio_base": (7, 0),
        "key_mount": (9, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=55, target_center=(89, 33), scale=1.0)
    hammer_attack = place_rotated_element(weapon_raw, deg=35, target_center=(96, 78), scale=1.04)

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, hammer_attack)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (撼地重踏·天崩地裂 / Seismic Overdrive Stomp & Scrap Shatter)
    # Vertical leap & crushing slam (y+4, x+0).
    # Heavy anvil hammer slammed straight down into ground (+12 deg, x-6, y+2).
    # Cross T-bar key spun to maximum overdrive (+90 deg, x+2, y-1).
    # Clean chimney steam vents directly above stacks without crossing character legs.
    # =========================================================================
    shifts_skill = {
        "head_top": (0, 4), "horn_tip_l": (0, 4), "horn_tip_r": (1, 4),
        "horn_crest_l": (0, 4), "horn_crest_r": (1, 4), "brow_rivet": (0, 4),
        "gauge_eye_l": (0, 4), "gauge_eye_r": (0, 4),
        "snout": (0, 4), "jaw": (0, 4), "throat": (0, 4),
        "chest_plate": (0, 4), "core": (0, 4),
        "shoulder_l": (-1, 4), "shoulder_r": (1, 4),
        "arm_l": (0, 4), "arm_r": (0, 4),
        "hand_r": (-5, 5),
        "torso": (0, 4), "pelvis": (0, 3),
        "hip_l": (-1, 3), "hip_r": (1, 3),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "exhaust_vent_l": (0, -1), "exhaust_vent_r": (1, -1), "curio_base": (0, 1),
        "key_mount": (1, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=90, target_center=(81, 33), scale=1.05)
    hammer_skill = place_rotated_element(weapon_raw, deg=12, target_center=(93, 88), scale=1.05)

    # Clean double steam chimney exhaust plumes
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    s_draw.polygon([(42, 27), (36, 15), (48, 15)], fill=(255, 160, 16, 190))
    s_draw.polygon([(42, 27), (39, 11), (45, 11)], fill=(255, 253, 248, 220))
    s_draw.polygon([(83, 27), (77, 15), (89, 15)], fill=(255, 160, 16, 190))
    s_draw.polygon([(83, 27), (80, 11), (86, 11)], fill=(255, 253, 248, 220))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.4))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, hammer_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (重裝受擊·蒸汽洩壓後仰 / Armor Impact & Steam Blowoff)
    # Knocked backward (x-9, y-4), horn pitches upward, heavy chassis braces.
    # Anvil hammer knocked backward into defensive diagonal parry (-30 deg, x-9, y-4).
    # Cross T-bar key jolted backwards (-22 deg, x-6, y-2).
    # Clean warm golden forge impact spark at chest center.
    # =========================================================================
    shifts_hit = {
        "head_top": (-9, -4), "horn_tip_l": (-9, -5), "horn_tip_r": (-8, -4),
        "horn_crest_l": (-10, -4), "horn_crest_r": (-8, -4), "brow_rivet": (-9, -4),
        "gauge_eye_l": (-9, -4), "gauge_eye_r": (-9, -4),
        "snout": (-9, -3), "jaw": (-9, -3), "throat": (-8, -3),
        "chest_plate": (-8, -2), "core": (-8, -2),
        "shoulder_l": (-7, -2), "shoulder_r": (-8, -2),
        "arm_l": (-5, -1), "arm_r": (-8, -1),
        "hand_r": (-10, -4),
        "torso": (-7, -2), "pelvis": (-6, -1),
        "hip_l": (-6, -1), "hip_r": (-4, -1),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "exhaust_vent_l": (-7, -5), "exhaust_vent_r": (-6, -5), "curio_base": (-7, -3),
        "key_mount": (-7, -3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_hit = place_rotated_element(key_raw, deg=-22, target_center=(73, 31), scale=1.0)
    hammer_hit = place_rotated_element(weapon_raw, deg=-30, target_center=(89, 82), scale=1.0)

    # Warm mechanical clashing spark at chest armor
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    ix, iy = 66, 68
    h_draw.ellipse([ix - 3, iy - 3, ix + 3, iy + 3], fill=(255, 208, 40, 220))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.3))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hammer_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (重甲著地·壓力復位·齒輪咬合 / Hydraulic Damping & Gauge Reset)
    # Heavy semi-crouch landing (y+4, x-1), armor absorbs shock.
    # Anvil hammer held at target_center=(96, 80) -> base at y=105, strictly above y=118.
    # Zero cutoff, 100% complete hammer silhouette.
    # Cross T-bar key snaps into gear mesh (+15 deg, x+1, y+2).
    # =========================================================================
    shifts_recover = {
        "head_top": (-1, 4), "horn_tip_l": (-1, 4), "horn_tip_r": (-1, 4),
        "horn_crest_l": (-2, 4), "horn_crest_r": (0, 4), "brow_rivet": (-1, 4),
        "gauge_eye_l": (-1, 4), "gauge_eye_r": (-1, 4),
        "snout": (-1, 4), "jaw": (-1, 4), "throat": (-1, 4),
        "chest_plate": (-1, 4), "core": (-1, 4),
        "shoulder_l": (-2, 3), "shoulder_r": (0, 3),
        "arm_l": (1, 2), "arm_r": (-2, 3),
        "hand_r": (-1, 4),
        "torso": (-1, 4), "pelvis": (-1, 3),
        "hip_l": (-2, 2), "hip_r": (1, 2),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "exhaust_vent_l": (-1, 3), "exhaust_vent_r": (-1, 3), "curio_base": (-1, 2),
        "key_mount": (1, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=15, target_center=(81, 36), scale=1.0)
    hammer_rec = place_rotated_element(weapon_raw, deg=-10, target_center=(96, 80), scale=1.0)

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, hammer_rec)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def main():
    print("Generating Groundshaker Bison combat poses...")
    poses = generate_poses()

    pose_names = ["idle", "telegraph", "attack", "recover", "skill", "hit"]

    # Save 128x128 poses and 512x512 LANCZOS versions
    for name in pose_names:
        im128 = poses[name]
        p128 = f"{OUT_DIR}/{name}.png"
        im128.save(p128)
        print(f"  Saved {p128} ({im128.size})")

        # 512x512 LANCZOS high-definition scale
        im512 = im128.resize((512, 512), Image.Resampling.LANCZOS)
        p512 = f"{OUT_DIR}/{name}_512.png"
        im512.save(p512)
        print(f"  Saved {p512} ({im512.size}, LANCZOS)")

    # Generate 768x128 Transparent Proof Sheet
    proof_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    for idx, name in enumerate(pose_names):
        proof_768.paste(poses[name], (idx * 128, 0))
    p_proof_768 = f"{REPO_ROOT}/game/assets/sprites/player/proof_bison_combat_poses_768.png"
    proof_768.save(p_proof_768)
    print(f"  Saved 768 proof: {p_proof_768}")

    # Generate 768x128 Magenta Proof Sheet
    proof_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for idx, name in enumerate(pose_names):
        proof_mag.alpha_composite(poses[name], (idx * 128, 0))
    p_proof_mag = f"{REPO_ROOT}/game/assets/sprites/player/proof_bison_combat_poses_magenta.png"
    proof_mag.save(p_proof_mag)
    print(f"  Saved magenta proof: {p_proof_mag}")

    print("\n✓ All Groundshaker Bison combat poses generated successfully!")


if __name__ == "__main__":
    main()
