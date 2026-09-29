#!/usr/bin/env python3
"""
tools/build_camel_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Sundial Camel (第五十三族 日晷駱駝, camel)
in Clockwork Heart:
  game/assets/sprites/player/poses/camel/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/camel/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16, 0-QA34).
Features sanded tinplate chassis, sundial gnomon cowl, dual spectroscope quartz lens, scavenger astronomer robe,
armillary dial brass winding key, wasteland sundial refraction rod, and twin condenser oil humps.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/camel"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/camel"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_camel_armillary_dial_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_camel_twin_condenser_humps.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_camel_sanded_tinplate_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_camel_sundial_gnomon_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_camel_scavenger_astronomer_robe.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_camel_dual_spectroscope_quartz_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_camel_sundial_refraction_rod.png").convert("RGBA")

# Extract raw weapon and key crops
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Reference ground shadow from canonical party idle asset
ref_shadow_im = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/camel_idle.png").convert("RGBA")
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
    "gnomon_tip": (64, 16),
    "cowl_top_l": (46, 26),
    "cowl_top_r": (82, 26),
    "bell_l": (36, 42),
    "bell_r": (92, 42),
    "optic_l": (55, 42),
    "optic_r": (73, 42),
    "cowl_chin": (64, 54),
    "hump_l": (44, 46),
    "hump_r": (84, 46),
    "hump_valve_l": (40, 56),
    "hump_valve_r": (88, 56),
    "chest_pin": (64, 66),
    "robe_flank_l": (38, 72),
    "robe_flank_r": (90, 72),
    "pelvis": (64, 88),
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
    # 1. IDLE (荒漠巡曆·日晷觀星持架 / Desert Astrologer Neutral Guard)
    # Neutral caravan astronomer stance. Key at (64, 37), wand at (96, 66).
    # Perfectly crisp, grounded and zero-defect.
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(64, 37), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(96, 66), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)

    # Subtle ambient quartz gleam FX
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    i_draw.point((96, 46), fill=(255, 255, 255, 240))
    i_draw.point((56, 42), fill=(133, 255, 160, 220))
    i_draw.point((72, 42), fill=(120, 205, 255, 220))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (風沙蓄力·晷針校準蓄勢 / Sandstorm Calibration & Gnomon Charge)
    # Deep crouch & draw back. Head and torso sink down and coil backward (head y+6, x-6; torso y+5, x-4).
    # Gnomon needle tilts downward as if measuring the acute sun angle across the dunes.
    # Robe folds tighten, hooves brace on ground.
    # Key counter-winds with tension clicks (-45 deg, target=(60, 42), scale=0.96).
    # Wasteland Sundial Refraction Rod drawn tight to chest/hip (-36 deg, target=(84, 70), scale=1.02).
    # =========================================================================
    tele_offsets = {
        "gnomon_tip": (-7, 6),
        "cowl_top_l": (-7, 6),
        "cowl_top_r": (-5, 6),
        "bell_l": (-7, 6),
        "bell_r": (-4, 6),
        "optic_l": (-6, 6),
        "optic_r": (-5, 6),
        "cowl_chin": (-6, 5),
        "hump_l": (-6, 5),
        "hump_r": (-4, 5),
        "hump_valve_l": (-6, 5),
        "hump_valve_r": (-4, 5),
        "chest_pin": (-5, 5),
        "robe_flank_l": (-5, 4),
        "robe_flank_r": (-3, 4),
        "pelvis": (-3, 3),
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
    tele_key = place_rotated_element(key_raw, deg=-45, target_center=(60, 42), scale=0.96)
    tele_weapon = place_rotated_element(weapon_raw, deg=-36, target_center=(84, 70), scale=1.02)

    # Solar calibration trajectory lines & targeting reticle FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Golden solar trajectory angle ray
    t_draw.line([(64, 42), (94, 58)], fill=(255, 208, 40, 200), width=1)
    t_draw.line([(94, 58), (112, 68)], fill=(255, 160, 16, 220), width=2)
    # Sundial targeting reticle crosshair at (110, 70)
    tcx, tcy = 110, 70
    t_draw.arc([tcx - 6, tcy - 6, tcx + 6, tcy + 6], start=30, end=330, fill=(255, 208, 40, 230), width=1)
    t_draw.line([(tcx - 7, tcy), (tcx + 7, tcy)], fill=(255, 208, 40, 220), width=1)
    t_draw.line([(tcx, tcy - 7), (tcx, tcy + 7)], fill=(255, 208, 40, 220), width=1)
    # Fine sand motes rising
    for sx, sy in [(38, 112), (44, 110), (52, 114), (76, 112), (84, 110), (92, 114), (86, 52), (102, 48)]:
        t_draw.point((sx, sy), fill=(255, 208, 40, 240))
        t_draw.point((sx + 1, sy), fill=(255, 253, 248, 220))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.3))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, tele_key)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele_body)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_weapon)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (日冕折光·日晷長槍光束 / Coronal Refraction Ray Thrust)
    # Violent forward thrust! Head and torso surge forward (head x+13, y-1; torso x+11, y=0).
    # Gnomon needle points forward directly at enemy core.
    # Sundial refraction rod thrusts straight forward (+34 deg, target=(102, 63), scale=1.14).
    # Key spins forward (+65 deg, target=(76, 33), scale=1.0).
    # Blazing golden-orange Tyndall solar ray & shockwave sparks.
    # =========================================================================
    atk_offsets = {
        "gnomon_tip": (13, -1),
        "cowl_top_l": (11, -1),
        "cowl_top_r": (14, -1),
        "bell_l": (10, -1),
        "bell_r": (14, -1),
        "optic_l": (12, -1),
        "optic_r": (12, -1),
        "cowl_chin": (12, 0),
        "hump_l": (9, -1),
        "hump_r": (13, -1),
        "hump_valve_l": (9, -1),
        "hump_valve_r": (13, -1),
        "chest_pin": (11, 0),
        "robe_flank_l": (8, 0),
        "robe_flank_r": (12, 0),
        "pelvis": (7, 0),
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
    atk_key = place_rotated_element(key_raw, deg=65, target_center=(76, 33), scale=1.0)
    atk_weapon = place_rotated_element(weapon_raw, deg=34, target_center=(102, 63), scale=1.14)

    # Solar beam thrust FX
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Piercing golden-orange refraction beam
    a_draw.arc([68, 26, 120, 96], start=280, end=80, fill=(255, 160, 16, 240), width=3)
    a_draw.arc([70, 28, 118, 94], start=290, end=70, fill=(255, 208, 40, 230), width=2)
    a_draw.arc([74, 32, 114, 90], start=300, end=60, fill=(255, 253, 248, 255), width=1)
    # Solar wavefront concentric rings
    a_draw.ellipse([96, 68, 116, 84], outline=(255, 208, 40, 220), width=1)
    a_draw.ellipse([99, 71, 113, 81], outline=(255, 253, 248, 240), width=1)
    # Prismatic spark particles
    for px, py in [(98, 58), (106, 50), (112, 44), (116, 62), (118, 74), (104, 78), (92, 74)]:
        a_draw.point((px, py), fill=(255, 253, 248, 255))
        a_draw.point((px + 1, py), fill=(255, 208, 40, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.3))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, atk_key)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk_body)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_weapon)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (天頂日冕·超時空聚光折射烈陽爆 / Zenith Coronal Overdrive & Solar Flare)
    # Grand casting stance! Surge upward into high elevation (head y-6, x+2; torso y-4, x+2).
    # Sundial Refraction Rod raised high overhead towards noon sun (+72 deg, target=(96, 50), scale=1.20).
    # Armillary dial brass key spins at maximum overdrive (+90 deg, target=(66, 28), scale=1.06).
    # Blazing solar corona mandala & steam release from twin condenser humps.
    # =========================================================================
    skill_offsets = {
        "gnomon_tip": (2, -6),
        "cowl_top_l": (1, -6),
        "cowl_top_r": (3, -6),
        "bell_l": (0, -6),
        "bell_r": (4, -6),
        "optic_l": (2, -6),
        "optic_r": (2, -6),
        "cowl_chin": (2, -5),
        "hump_l": (1, -5),
        "hump_r": (4, -5),
        "hump_valve_l": (1, -5),
        "hump_valve_r": (4, -5),
        "chest_pin": (2, -4),
        "robe_flank_l": (1, -3),
        "robe_flank_r": (3, -3),
        "pelvis": (1, -2),
        "leg_back_l": (0, -1),
        "leg_front_l": (1, -1),
        "leg_front_r": (2, -1),
        "leg_back_r": (2, -1),
        "hoof_back_l": (0, 0),
        "hoof_front_l": (0, 0),
        "hoof_front_r": (1, 0),
        "hoof_back_r": (1, 0),
    }
    dst_skill = [(base_landmarks[k][0] + skill_offsets[k][0], base_landmarks[k][1] + skill_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skill_body = warp_image_idw(body_core, src_pts, dst_skill)
    skill_key = place_rotated_element(key_raw, deg=90, target_center=(66, 28), scale=1.06)
    skill_weapon = place_rotated_element(weapon_raw, deg=72, target_center=(96, 50), scale=1.20)

    # Zenith solar mandala & steam plume FX
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    # Golden coronal radiating rings
    s_draw.arc([76, 12, 116, 52], start=0, end=360, fill=(255, 208, 40, 230), width=1)
    s_draw.arc([80, 16, 112, 48], start=0, end=360, fill=(255, 160, 16, 220), width=1)
    s_draw.arc([84, 20, 108, 44], start=0, end=360, fill=(255, 253, 248, 255), width=2)
    # Steam puffs from condenser hump relief valves
    s_draw.ellipse([34, 46, 42, 54], fill=(255, 253, 248, 180))
    s_draw.ellipse([32, 40, 42, 48], fill=(232, 236, 242, 160))
    s_draw.ellipse([86, 46, 94, 54], fill=(255, 253, 248, 180))
    s_draw.ellipse([86, 40, 96, 48], fill=(232, 236, 242, 160))
    # Radiating celestial star rays
    for rx, ry in [(96, 10), (118, 32), (96, 54), (74, 32), (81, 17), (111, 17), (111, 47), (81, 47)]:
        s_draw.line([(96, 32), (rx, ry)], fill=(255, 208, 40, 210), width=1)
        s_draw.point((rx, ry), fill=(255, 253, 248, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.3))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, skill_key)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill_body)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_weapon)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (重砂受衝·外殼震盪受擊 / Sand-Impact Shock & Recoil)
    # Severe kinetic strike and recoil backward-left (head x-12, y-2; torso x-10, y-1).
    # Sundial Refraction Rod raised reflexively in front of chest (-28 deg, target=(82, 72), scale=1.02).
    # Armillary dial brass key shaken counter-clockwise (-40 deg, target=(55, 33), scale=0.96).
    # =========================================================================
    hit_offsets = {
        "gnomon_tip": (-12, -2),
        "cowl_top_l": (-13, -2),
        "cowl_top_r": (-11, -2),
        "bell_l": (-13, -2),
        "bell_r": (-10, -2),
        "optic_l": (-12, -2),
        "optic_r": (-12, -2),
        "cowl_chin": (-12, -1),
        "hump_l": (-11, -2),
        "hump_r": (-9, -2),
        "hump_valve_l": (-11, -2),
        "hump_valve_r": (-9, -2),
        "chest_pin": (-10, -1),
        "robe_flank_l": (-10, -1),
        "robe_flank_r": (-8, -1),
        "pelvis": (-7, -1),
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
    hit_key = place_rotated_element(key_raw, deg=-40, target_center=(55, 33), scale=0.96)
    hit_weapon = place_rotated_element(weapon_raw, deg=-28, target_center=(82, 72), scale=1.02)

    # Impact shock FX
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Deflection sparks at impact center (64, 68)
    for hx, hy in [(62, 60), (56, 68), (68, 74), (72, 62), (58, 76)]:
        h_draw.line([(64, 68), (hx, hy)], fill=(255, 208, 40, 220), width=1)
        h_draw.point((hx, hy), fill=(255, 253, 248, 255))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.3))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, hit_key)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit_body)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_weapon)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (散熱冷凝·走時復歸歸零 / Thermal Condenser Vent & Reset)
    # Stance settling after attack (head x+2, y+4; torso x+2, y+3).
    # Sundial Refraction Rod resting in neutral angle (+16 deg, target=(93, 72), scale=1.02).
    # Armillary key smoothly rotating back towards neutral (+15 deg, target=(66, 39), scale=0.98).
    # =========================================================================
    rec_offsets = {
        "gnomon_tip": (2, 4),
        "cowl_top_l": (1, 4),
        "cowl_top_r": (3, 4),
        "bell_l": (1, 4),
        "bell_r": (3, 4),
        "optic_l": (2, 4),
        "optic_r": (2, 4),
        "cowl_chin": (2, 3),
        "hump_l": (1, 4),
        "hump_r": (3, 4),
        "hump_valve_l": (1, 4),
        "hump_valve_r": (3, 4),
        "chest_pin": (2, 3),
        "robe_flank_l": (1, 3),
        "robe_flank_r": (3, 3),
        "pelvis": (1, 2),
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
    rec_key = place_rotated_element(key_raw, deg=15, target_center=(66, 39), scale=0.98)
    rec_weapon = place_rotated_element(weapon_raw, deg=16, target_center=(93, 72), scale=1.02)

    # Condenser cooling vapor FX
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    r_draw.ellipse([38, 48, 46, 56], fill=(255, 253, 248, 140))
    r_draw.ellipse([82, 48, 90, 56], fill=(255, 253, 248, 140))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.4))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, rec_key)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec_body)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_weapon)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def build_and_save():
    print("Generating camel combat action poses...")
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

    p768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_camel_combat_poses_768.png"
    pmag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_camel_combat_poses_magenta.png"
    proof_768.save(p768_path, "PNG")
    proof_mag.save(pmag_path, "PNG")
    print(f"✓ Saved proof sheets:\n  - {p768_path}\n  - {pmag_path}")


if __name__ == "__main__":
    build_and_save()
