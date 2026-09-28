#!/usr/bin/env python3
"""
tools/build_courser_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Ironhoof Courser (第三十七族 鐵蹄駿駒, courser)
in Clockwork Heart:
  game/assets/sprites/player/poses/courser/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/courser/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/courser"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/courser"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_courser_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_courser_baroque_trefoil_gold.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_courser_articulated_spring_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_courser_cream_gold_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_courser_brass_chanfron_mane.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_courser_dawn_patrol_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_courser_sapphire_optic_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_courser_cavalry_saber.png").convert("RGBA")

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Extract raw curio crop
curio_bbox = curio_src.getbbox()
assert curio_bbox is not None
curio_raw = curio_src.crop(curio_bbox)

# Standardized ground contact shadow from cleaned baseline composite
# Courser baseline shadow row counts: [34, 34, 34, 34, 0, 0, 0, 0, 0, 0]
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
assert s_px is not None and c_px is not None

# Clean baseline shadow to guarantee Rule 4c-5 / 16 (L>=4, T>=4, R>=4, B>=2)
for y in range(118, 126):  # up to 125, y=126 and 127 are 0
    for x in range(4, 124):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p
        else:
            s_px[x, y] = (0, 0, 0, 0)

EXPECTED_SHADOW = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], s_px[x, y])[3] > 20) for y in range(118, 128)]
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

    # Clean margins strictly (L>=4, R>=4, T>=4, B>=2)
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


# Anchor corners and borders for IDW
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127)
]

base_landmarks = {
    "head_top": (64, 8),
    "ears_l": (50, 10),
    "ears_r": (78, 10),
    "mane_top": (64, 15),
    "crest_l": (46, 20),
    "crest_r": (82, 20),
    "eye_l": (52, 40),
    "eye_r": (76, 40),
    "snout": (64, 46),
    "throat": (64, 55),
    "core": (64, 68),
    "shoulder_l": (44, 65),
    "shoulder_r": (84, 65),
    "arm_l": (36, 74),
    "arm_r": (88, 74),
    "hand_r": (96, 53),
    "torso": (64, 76),
    "pelvis": (64, 90),
    "hip_l": (48, 96),
    "hip_r": (80, 96),
    "foot_l": (48, 116),
    "foot_r": (78, 116),
    "curio_tail_top": (36, 80),
    "curio_tail_mid": (30, 95),
    "curio_tail_tip": (22, 114),
    "key_mount": (87, 27),
}

# Base body without weapon and winding key (for dynamic key & weapon animation)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (鐵蹄駿駒·晨曦威儀 / Dawn Poise)
    # Baseline stable poised stance from canonical composite.
    # Winding key placed at center (87, 27).
    # Cavalry saber held poised at (97, 50).
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(87, 27), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(97, 50), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)

    # Ambient subtle brass and sapphire gleam FX
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    # Gilded saber tip glimmer at (96, 20)
    i_draw.line([(96, 17), (96, 23)], fill=(255, 253, 248, 220), width=1)
    i_draw.line([(93, 20), (99, 20)], fill=(255, 208, 40, 240), width=1)
    i_draw.point((96, 20), fill=(255, 255, 255, 255))
    # Sapphire eye lens reflection
    i_draw.point((52, 39), fill=(56, 160, 255, 220))
    i_draw.point((76, 39), fill=(56, 160, 255, 220))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (蓄勢踏步·鐵蹄突刺預備 / Ironhoof Pre-thrust Charge)
    # Heavy crouch forward, mane and chanfron lower forward (y+5, x-2).
    # Cavalry saber draws back into upper thrust tension (deg=-26, x-5, y-6).
    # Baroque trefoil key counter-winds (-35 deg, x-2, y+4).
    # Spring tail compresses slightly (+2, +2).
    # FX: Gold & cyan targeting reticle, kinetic steam/ember trails, ground hoof tension.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 5), "ears_l": (-2, 5), "ears_r": (-2, 5),
        "mane_top": (-2, 5), "crest_l": (-3, 5), "crest_r": (-1, 5),
        "eye_l": (-2, 5), "eye_r": (-2, 5),
        "snout": (-2, 5), "throat": (-2, 5),
        "core": (-2, 4),
        "shoulder_l": (-2, 4), "shoulder_r": (-3, 4),
        "arm_l": (1, 4), "arm_r": (-4, 4),
        "hand_r": (-4, 4),
        "torso": (-2, 4), "pelvis": (-2, 3),
        "hip_l": (-3, 2), "hip_r": (1, 2),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "curio_tail_top": (1, 3), "curio_tail_mid": (2, 2), "curio_tail_tip": (3, 1),
        "key_mount": (-2, 4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_tele = place_rotated_element(key_raw, deg=-35, target_center=(85, 31), scale=1.0)
    saber_tele = place_rotated_element(weapon_raw, deg=-26, target_center=(92, 44), scale=1.04)

    # Targeting reticle & thrust trajectory FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Cavalry thrust trajectory line towards forward target
    t_draw.line([(70, 50), (105, 45)], fill=(255, 160, 16, 210), width=1)
    t_draw.line([(105, 45), (122, 42)], fill=(255, 208, 40, 230), width=2)
    # Baroque crosshair targeting reticle at forward target (114, 43)
    cx, cy = 114, 43
    t_draw.arc([cx - 7, cy - 7, cx + 7, cy + 7], start=20, end=340, fill=(255, 94, 138, 220), width=1)
    t_draw.arc([cx - 3, cy - 3, cx + 3, cy + 3], start=40, end=320, fill=(255, 208, 40, 230), width=1)
    t_draw.line([(cx - 9, cy), (cx + 9, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 9), (cx, cy + 9)], fill=(255, 208, 40, 240), width=1)
    # Ground hoof scraping spark particles
    for sx, sy in [(42, 115), (46, 114), (52, 116), (74, 115), (82, 114), (96, 48), (118, 38)]:
        t_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 240))
        t_draw.point((sx, sy), fill=(255, 208, 40, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, saber_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (晨曦斬擊·皇家騎兵刀突進 / Dawn Cavalry Saber Slash & Lunge)
    # Fierce lunge forward (+12, -1), saber slashes forward with curved arc (+26 deg, x+11, y-2).
    # Trefoil key spins forward (+48 deg, x+10, y-1).
    # Tail whips backward with momentum (x-3, y-2).
    # FX: Brilliant golden-cyan arc slash wave, sonic burst ring, dynamic sparks.
    # =========================================================================
    shifts_attack = {
        "head_top": (12, -1), "ears_l": (11, -1), "ears_r": (13, -1),
        "mane_top": (12, -1), "crest_l": (10, -1), "crest_r": (13, -1),
        "eye_l": (12, -1), "eye_r": (12, -1),
        "snout": (13, 0), "throat": (12, 0),
        "core": (11, 0),
        "shoulder_l": (13, -1), "shoulder_r": (8, 0),
        "arm_l": (14, -3), "arm_r": (-5, 1),
        "hand_r": (14, -3),
        "torso": (10, 0), "pelvis": (8, 0),
        "hip_l": (9, -1), "hip_r": (-2, 0),
        "foot_l": (7, 0), "foot_r": (-3, 0),
        "curio_tail_top": (-3, -1), "curio_tail_mid": (-4, -2), "curio_tail_tip": (-5, -2),
        "key_mount": (10, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=48, target_center=(97, 26), scale=1.0)
    saber_attack = place_rotated_element(weapon_raw, deg=26, target_center=(108, 48), scale=1.06)

    # Curved cavalry saber slash wave & wind shockwaves
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Dynamic golden crescent slash arc
    a_draw.arc([68, 14, 122, 92], start=295, end=65, fill=(255, 208, 40, 245), width=2)
    a_draw.arc([74, 18, 120, 88], start=305, end=55, fill=(56, 160, 255, 235), width=2)
    a_draw.arc([80, 22, 118, 84], start=315, end=45, fill=(255, 255, 255, 255), width=1)
    # Secondary inner energy ribbon
    a_draw.arc([86, 26, 114, 80], start=325, end=35, fill=(255, 94, 138, 220), width=1)
    # Sonic burst wind trails and sparks
    for pt in [(116, 28), (122, 42), (121, 60), (115, 74), (102, 18), (92, 14)]:
        a_draw.point(pt, fill=(255, 208, 40, 255))
        a_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, saber_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (天際破陣·萬馬奔騰鐵蹄踐踏 / Grand Cavalry Charge & Celestial Trample)
    # Airborne leap pose (y-8, x+1), dual hooves poised to trample,
    # saber held high to channel dawn lightning (-52 deg, x+1, y-18).
    # Baroque trefoil key overclocks to +88 deg (x+2, y-7).
    # Tail sweeps upwards (x-2, y-7).
    # FX: Golden-cyan shock rings, celestial trample stars, ascending energy beams.
    # =========================================================================
    shifts_skill = {
        "head_top": (1, -8), "ears_l": (-1, -8), "ears_r": (3, -8),
        "mane_top": (1, -8), "crest_l": (-1, -8), "crest_r": (3, -8),
        "eye_l": (1, -8), "eye_r": (1, -8),
        "snout": (1, -8), "throat": (1, -8),
        "core": (1, -8),
        "shoulder_l": (-2, -8), "shoulder_r": (4, -8),
        "arm_l": (8, -16), "arm_r": (-4, -6),
        "hand_r": (8, -16),
        "torso": (1, -8), "pelvis": (1, -7),
        "hip_l": (-3, -6), "hip_r": (4, -6),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "curio_tail_top": (-2, -7), "curio_tail_mid": (-2, -6), "curio_tail_tip": (-1, -5),
        "key_mount": (2, -7),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=88, target_center=(89, 20), scale=1.0)
    saber_skill = place_rotated_element(weapon_raw, deg=-52, target_center=(98, 32), scale=1.08)

    # Celestial trample shock rings & ascending rays
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    sk_draw = ImageDraw.Draw(skill_fx)
    # Radiating golden shockwave rings
    sk_draw.arc([16, 12, 116, 112], start=195, end=345, fill=(255, 208, 40, 235), width=2)
    sk_draw.arc([24, 18, 108, 102], start=205, end=335, fill=(56, 160, 255, 220), width=2)
    sk_draw.arc([32, 24, 100, 92], start=215, end=325, fill=(78, 216, 106, 230), width=2)
    sk_draw.arc([40, 30, 92, 82], start=225, end=315, fill=(255, 94, 138, 220), width=1)
    # Ascending celestial beam rays from saber tip (98, 14)
    sk_draw.line([(98, 20), (106, 6)], fill=(255, 208, 40, 240), width=2)
    sk_draw.line([(98, 20), (106, 6)], fill=(255, 255, 255, 255), width=1)
    sk_draw.line([(94, 22), (80, 8)], fill=(56, 160, 255, 220), width=1)
    sk_draw.line([(102, 22), (120, 10)], fill=(78, 216, 106, 220), width=1)
    # Celestial ironhoof stars and glints
    for star_x, star_y in [(22, 24), (108, 16), (116, 66), (18, 74), (64, 8), (112, 82)]:
        sk_draw.ellipse([star_x - 1, star_y - 1, star_x + 1, star_y + 1], fill=(255, 255, 255, 240))
        sk_draw.point((star_x, star_y), fill=(255, 208, 40, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.4))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, saber_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊後挫·裝甲震盪偏斜 / Impact Recoil & Armor Deflection)
    # Backward slip (x-10, y-2), head and chanfron tilt back (-8 deg),
    # saber deflected and knocked askew (+22 deg, x-7, y+6),
    # key slips backward against gear ratchet (-28 deg, x-9, y-2), tail flares forward (+3, -1).
    # Optic eyes display strain/overload cute '> <' LED indicators!
    # FX: Kinetic impact sparks, armor stress lines, ground skid marks.
    # =========================================================================
    shifts_hit = {
        "head_top": (-10, -2), "ears_l": (-11, -2), "ears_r": (-9, -2),
        "mane_top": (-10, -2), "crest_l": (-11, -2), "crest_r": (-8, -2),
        "eye_l": (-10, -2), "eye_r": (-10, -2),
        "snout": (-10, -2), "throat": (-9, -2),
        "core": (-8, -1),
        "shoulder_l": (-10, -2), "shoulder_r": (-7, -2),
        "arm_l": (-6, 3), "arm_r": (-9, 0),
        "hand_r": (-6, 3),
        "torso": (-8, -1), "pelvis": (-6, 0),
        "hip_l": (-6, -1), "hip_r": (-3, 0),
        "foot_l": (-3, 0), "foot_r": (2, 0),
        "curio_tail_top": (3, -1), "curio_tail_mid": (4, -1), "curio_tail_tip": (5, 0),
        "key_mount": (-9, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Overlay cute dizzy strain '> <' LEDs on optic eyes:
    # Left eye base: (52, 40) -> shifted: (42, 38)
    # Right eye base: (76, 40) -> shifted: (66, 38)
    hit_eyes = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    he_draw = ImageDraw.Draw(hit_eyes)
    # Left eye strain '>'
    lx, ly = 42, 38
    he_draw.line([(lx - 3, ly - 3), (lx + 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(lx - 3, ly + 3), (lx + 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(lx - 2, ly - 2), (lx + 1, ly)], fill=(255, 255, 255, 255), width=1)
    # Right eye strain '<'
    rx, ry = 66, 38
    he_draw.line([(rx + 3, ly - 3), (rx - 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(rx + 3, ly + 3), (rx - 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(rx + 2, ly - 2), (rx - 1, ly)], fill=(255, 255, 255, 255), width=1)

    key_hit = place_rotated_element(key_raw, deg=-28, target_center=(78, 25), scale=1.0)
    saber_hit = place_rotated_element(weapon_raw, deg=22, target_center=(90, 56), scale=1.0)

    # Impact spark burst & deflection rays
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact center at dawn patrol cuirass (56, 64)
    ix, iy = 56, 64
    h_draw.line([(ix - 12, iy - 8), (ix + 10, iy + 6)], fill=(255, 208, 40, 240), width=2)
    h_draw.line([(ix - 8, iy + 10), (ix + 8, iy - 8)], fill=(255, 94, 138, 230), width=2)
    h_draw.line([(ix - 14, iy), (ix + 12, iy)], fill=(255, 255, 255, 255), width=1)
    # Kinetic sparks
    for pt in [(ix - 14, iy - 10), (ix + 12, iy - 12), (ix + 14, iy + 8), (ix - 10, iy + 12), (ix + 18, iy - 2)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    # Skid lines on ground
    h_draw.line([(34, 115), (50, 115)], fill=(255, 255, 255, 180), width=1)
    h_draw.line([(30, 117), (48, 117)], fill=(255, 208, 40, 200), width=1)
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_eyes)
    hit_canvas = Image.alpha_composite(hit_canvas, saber_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (踏地止退·重組防禦架式 / Hoof Grounding & Saber Guard)
    # Low semi-crouch landing (y+5, x-1), torso bows slightly,
    # saber braced across body guarding chest (-16 deg, x-3, y+5).
    # Trefoil key snaps back into gear mesh (+15 deg, x-1, y+5).
    # Tail folds down naturally for balance.
    # FX: Hoof impact dust ripples, gear re-mesh spark glint.
    # =========================================================================
    shifts_recover = {
        "head_top": (-1, 5), "ears_l": (-2, 5), "ears_r": (0, 5),
        "mane_top": (-1, 5), "crest_l": (-2, 5), "crest_r": (0, 5),
        "eye_l": (-1, 5), "eye_r": (-1, 5),
        "snout": (-1, 5), "throat": (-1, 5),
        "core": (-1, 5),
        "shoulder_l": (-2, 4), "shoulder_r": (0, 4),
        "arm_l": (1, 4), "arm_r": (-2, 4),
        "hand_r": (1, 4),
        "torso": (-1, 5), "pelvis": (-1, 4),
        "hip_l": (-3, 3), "hip_r": (2, 3),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "curio_tail_top": (-1, 4), "curio_tail_mid": (-1, 3), "curio_tail_tip": (0, 2),
        "key_mount": (-1, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=15, target_center=(86, 32), scale=1.0)
    saber_rec = place_rotated_element(weapon_raw, deg=-16, target_center=(94, 55), scale=1.0)

    # Hoof impact ground shock & gear re-mesh spark FX
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Ground hoof landing ripples
    r_draw.arc([36, 112, 92, 122], start=190, end=350, fill=(255, 208, 40, 180), width=1)
    r_draw.arc([44, 114, 84, 120], start=200, end=340, fill=(56, 160, 255, 200), width=1)
    # Gear re-mesh spark at key mount (86, 32)
    r_draw.line([(83, 29), (89, 35)], fill=(255, 208, 40, 230), width=1)
    r_draw.line([(89, 29), (83, 35)], fill=(255, 255, 255, 255), width=1)
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, saber_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


# 2. Main Generation Execution
print("Generating The Ironhoof Courser combat action poses...")
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

proof_768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_courser_combat_poses_768.png"
proof_strip.save(proof_768_path)
print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

# 4. Generate 768x128 magenta background proof sheet for hole detection
proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
proof_magenta.paste(proof_strip, (0, 0), proof_strip)
proof_mag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_courser_combat_poses_magenta.png"
proof_magenta.save(proof_mag_path)
print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")

print("\nAll 6 Ironhoof Courser combat action poses successfully generated and exported!")
