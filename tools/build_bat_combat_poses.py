#!/usr/bin/env python3
"""
tools/build_bat_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Starwing Bat (第三十三族 星翼蝙蝠, bat)
in Clockwork Heart:
  game/assets/sprites/player/poses/bat/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/bat/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bat"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/bat"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_bat_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_bat_orbital_pulsar_key.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_bat_articulated_starwing_mantle.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_bat_astral_polymer_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_bat_sonar_parabolic_crest.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_bat_orbital_stealth_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_bat_dual_amber_optic_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_bat_superconducting_pulse_dart.png").convert("RGBA")

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
# Bat baseline shadow row counts: [62, 60, 57, 47, 29, 0, 0, 0, 0, 0]
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

    # Sanitize any interpolation dark falloff pixels to canon outline (46, 31, 24)
    arr = np.array(out)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    bad_dark = (alpha > 30) & (rgb[:, :, 0] < 12) & (rgb[:, :, 1] < 12) & (rgb[:, :, 2] < 12)
    if np.any(bad_dark):
        arr[bad_dark, 0] = 46
        arr[bad_dark, 1] = 31
        arr[bad_dark, 2] = 24
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
    "head_top": (64, 14),
    "ear_l": (37, 4),
    "ear_r": (85, 4),
    "ear_base_l": (44, 26),
    "ear_base_r": (82, 26),
    "eye_l": (51, 42),
    "eye_r": (77, 42),
    "snout": (64, 49),
    "throat": (64, 55),
    "core": (64, 67),
    "shoulder_l": (42, 63),
    "shoulder_r": (84, 63),
    "arm_l": (34, 71),
    "arm_r": (88, 71),
    "hand_r": (96, 69),
    "torso": (64, 75),
    "pelvis": (64, 89),
    "hip_l": (48, 97),
    "hip_r": (80, 97),
    "foot_l": (49, 116),
    "foot_r": (77, 116),
    "wing_l": (22, 61),
    "wing_r": (86, 63),
    "key_mount": (81, 35),
}

# Base body without weapon and winding key (for dynamic key & weapon animation)
# Shift canonical body_core down by 1px so ear tips land on y=4, ensuring T>=4
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)

# Shift body_core by (0, 1) to respect T>=4
body_core_shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core_shifted.paste(body_core, (0, 1), body_core)
body_core = body_core_shifted


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (星翼蝙蝠待機 / The Starwing Bat Poise)
    # Baseline stable poised ninja stance.
    # Winding key placed at center (81, 35).
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(81, 35), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(96, 69), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (暗影伏擊·聲納聚焦 / Radar Calibration & Shuriken Coil)
    # Deep ninja stealth crouch (y+6, x-2), torso leans back,
    # pulse dart pulled back into stealth throw posture (-26 deg, x-6, y-3).
    # Orbital pulsar key counter-rotates (-28 deg, x-3, y+5).
    # Parabolic sonar radar ears incline forward to track signal.
    # FX: Concentric sonar radar rings, electric pulse trajectory beam, aiming crosshair.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 6), "ear_l": (-3, 6), "ear_r": (-1, 6),
        "ear_base_l": (-2, 6), "ear_base_r": (-2, 6),
        "eye_l": (-2, 6), "eye_r": (-2, 6),
        "snout": (-2, 6), "throat": (-2, 6),
        "core": (-2, 6),
        "shoulder_l": (-1, 5), "shoulder_r": (-3, 5),
        "arm_l": (1, 5), "arm_r": (-5, 5),
        "hand_r": (-6, 3),
        "torso": (-2, 6), "pelvis": (-2, 5),
        "hip_l": (-4, 4), "hip_r": (1, 4),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "wing_l": (-3, 5), "wing_r": (-1, 5),
        "key_mount": (-3, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_tele = place_rotated_element(key_raw, deg=-28, target_center=(78, 40), scale=1.0)
    dart_tele = place_rotated_element(weapon_raw, deg=-26, target_center=(90, 66), scale=1.04)

    # Sonar radar rings & target crosshair FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Target reticle at forward locus (110, 48)
    cx, cy = 110, 48
    t_draw.arc([cx - 8, cy - 8, cx + 8, cy + 8], start=20, end=340, fill=(78, 216, 106, 230), width=1)
    t_draw.arc([cx - 4, cy - 4, cx + 4, cy + 4], start=40, end=320, fill=(56, 160, 255, 230), width=1)
    t_draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(255, 208, 40, 240), width=1)
    # Sonar pulse beam connecting shuriken to target
    t_draw.line([(90, 64), (110, 48)], fill=(78, 216, 106, 210), width=2)
    t_draw.line([(92, 63), (110, 48)], fill=(255, 255, 255, 255), width=1)
    # Concentric acoustic sonar wavefronts expanding from ears
    t_draw.arc([22, 10, 52, 40], start=210, end=330, fill=(78, 216, 106, 220), width=1)
    t_draw.arc([16, 4, 58, 46], start=210, end=330, fill=(56, 160, 255, 190), width=1)
    t_draw.arc([70, 10, 100, 40], start=210, end=330, fill=(78, 216, 106, 220), width=1)
    # Pulse sparks
    for sx, sy in [(114, 40), (120, 54), (102, 38), (84, 60), (74, 56)]:
        t_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 240))
        t_draw.point((sx, sy), fill=(78, 216, 106, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, dart_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (星紋疾斬·超導電磁鏢 / Superconducting Pulse Astral Thrust)
    # Dynamic forward lunge (+13, 0), pulse dart thrusts and spins (+36 deg, x+15, y-6)!
    # Orbital pulsar key spins rapidly (+48 deg, x+10, y-1).
    # Starwing mantle sweeps backward to channel zero-g momentum.
    # FX: Superconducting magnetic arc, cutting shockwave, plasma jet wake.
    # =========================================================================
    shifts_attack = {
        "head_top": (13, 0), "ear_l": (11, 0), "ear_r": (14, 0),
        "ear_base_l": (12, 0), "ear_base_r": (13, 0),
        "eye_l": (13, 0), "eye_r": (13, 0),
        "snout": (14, 0), "throat": (13, 0),
        "core": (12, 0),
        "shoulder_l": (14, -1), "shoulder_r": (8, 0),
        "arm_l": (15, -3), "arm_r": (-5, 2),
        "hand_r": (15, -4),
        "torso": (11, 0), "pelvis": (9, 0),
        "hip_l": (10, -1), "hip_r": (-2, 0),
        "foot_l": (7, 0), "foot_r": (-3, 0),
        "wing_l": (6, -1), "wing_r": (12, 1),
        "key_mount": (10, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=48, target_center=(91, 34), scale=1.0)
    dart_attack = place_rotated_element(weapon_raw, deg=36, target_center=(111, 63), scale=1.06)

    # Superconducting electric shock cone & cutting arcs
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Piercing pulse dart laser beam
    a_draw.line([(88, 65), (122, 58)], fill=(56, 160, 255, 245), width=2)
    a_draw.line([(96, 64), (122, 58)], fill=(255, 255, 255, 255), width=1)
    # Magnetic cutting rings around shuriken
    a_draw.arc([92, 44, 122, 74], start=300, end=60, fill=(78, 216, 106, 235), width=2)
    a_draw.arc([98, 48, 120, 70], start=310, end=50, fill=(255, 208, 40, 240), width=2)
    # Trailing plasma spark particles
    for pt in [(118, 46), (122, 56), (120, 68), (114, 76), (104, 38), (94, 76)]:
        a_draw.point(pt, fill=(56, 160, 255, 255))
        a_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, dart_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (天穹星芒·失重超導風暴 / Astral Starfall Superconducting Storm)
    # High zero-g aerial hover (y-7, x+1), starwing mantle expands into full wingspan.
    # Dart levitates in overdrive spin (-55 deg, x+2, y-16, scale 1.1).
    # Pulsar key spins in maximum overdrive (+85 deg, x+2, y-8).
    # FX: Concentric astral plasma rings, dual sonar beam geysers, luminescent starlight sparks.
    # =========================================================================
    shifts_skill = {
        "head_top": (1, -7), "ear_l": (-1, -7), "ear_r": (3, -7),
        "ear_base_l": (0, -7), "ear_base_r": (2, -7),
        "eye_l": (1, -7), "eye_r": (1, -7),
        "snout": (1, -7), "throat": (1, -7),
        "core": (1, -7),
        "shoulder_l": (-2, -7), "shoulder_r": (4, -7),
        "arm_l": (-6, -6), "arm_r": (4, -12),
        "hand_r": (2, -14),
        "torso": (1, -7), "pelvis": (1, -6),
        "hip_l": (-3, -5), "hip_r": (4, -5),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "wing_l": (-8, -6), "wing_r": (6, -6),
        "key_mount": (2, -7),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=85, target_center=(83, 27), scale=1.0)
    dart_skill = place_rotated_element(weapon_raw, deg=-55, target_center=(98, 53), scale=1.1)

    # Astral plasma storm arcs & starlight geyser FX
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    sk_draw = ImageDraw.Draw(skill_fx)
    # Astral plasma concentric aura
    sk_draw.arc([16, 14, 116, 114], start=195, end=345, fill=(56, 160, 255, 235), width=2)
    sk_draw.arc([24, 20, 108, 104], start=205, end=335, fill=(78, 216, 106, 220), width=2)
    sk_draw.arc([32, 26, 100, 94], start=215, end=325, fill=(255, 208, 40, 230), width=2)
    sk_draw.arc([40, 32, 92, 84], start=225, end=315, fill=(255, 94, 138, 220), width=1)
    # Skyward superconducting plasma beams
    sk_draw.line([(98, 51), (108, 10)], fill=(56, 160, 255, 240), width=2)
    sk_draw.line([(99, 51), (108, 10)], fill=(255, 255, 255, 255), width=1)
    sk_draw.line([(38, 52), (28, 14)], fill=(78, 216, 106, 220), width=1)
    sk_draw.line([(64, 46), (64, 8)], fill=(255, 208, 40, 220), width=1)
    # Starlight pearls / quantum sparks
    for sx, sy in [(22, 24), (106, 16), (116, 66), (18, 74), (64, 8), (112, 80)]:
        sk_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255, 240))
        sk_draw.point((sx, sy), fill=(56, 160, 255, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.4))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, dart_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊震退·夜視目鏡過載 / Impact Recoil & Sonar Glitch)
    # Recoil backward slip (x-10, y-1), head and parabolic ears tilt back (-10 deg),
    # pulse dart jarred upward (+26 deg, x-9, y+6),
    # key slips backward against gear ratchet (-32 deg, x-9, y-2), starwing folds forward (+4, -1).
    # Optic lens switches to cute dizzy/strain '> <' amber quartz LED expressions!
    # =========================================================================
    shifts_hit = {
        "head_top": (-10, -1), "ear_l": (-11, -1), "ear_r": (-8, -1),
        "ear_base_l": (-10, -1), "ear_base_r": (-9, -1),
        "eye_l": (-10, -1), "eye_r": (-10, -1),
        "snout": (-10, -1), "throat": (-9, -1),
        "core": (-8, 0),
        "shoulder_l": (-10, -1), "shoulder_r": (-7, -1),
        "arm_l": (-6, 3), "arm_r": (-9, 1),
        "hand_r": (-9, 6),
        "torso": (-8, 0), "pelvis": (-6, 0),
        "hip_l": (-6, 0), "hip_r": (-3, 0),
        "foot_l": (-3, 0), "foot_r": (2, 0),
        "wing_l": (-4, 0), "wing_r": (3, 0),
        "key_mount": (-8, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Overlay cute dizzy strain '> <' LEDs on optic eyes:
    # Left eye base: (51, 42), shifted: (51 - 10, 42 - 1) = (41, 41)
    # Right eye base: (77, 42), shifted: (77 - 10, 42 - 1) = (67, 41)
    hit_eyes = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    he_draw = ImageDraw.Draw(hit_eyes)
    # Left eye strain '>'
    lx, ly = 41, 41
    he_draw.line([(lx - 3, ly - 3), (lx + 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(lx - 3, ly + 3), (lx + 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(lx - 2, ly - 2), (lx + 1, ly)], fill=(255, 255, 255, 255), width=1)
    # Right eye strain '<'
    rx, ry = 67, 41
    he_draw.line([(rx + 3, ly - 3), (rx - 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(rx + 3, ly + 3), (rx - 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(rx + 2, ly - 2), (rx - 1, ly)], fill=(255, 255, 255, 255), width=1)

    key_hit = place_rotated_element(key_raw, deg=-32, target_center=(72, 33), scale=1.0)
    dart_hit = place_rotated_element(weapon_raw, deg=26, target_center=(87, 75), scale=1.0)

    # Impact spark burst and kinetic deflection lines
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact point at stealth polymer cuirass (56, 64)
    ix, iy = 56, 64
    h_draw.line([(ix - 12, iy - 8), (ix + 10, iy + 6)], fill=(255, 208, 40, 240), width=2)
    h_draw.line([(ix - 8, iy + 10), (ix + 8, iy - 8)], fill=(255, 94, 138, 230), width=2)
    h_draw.line([(ix - 14, iy), (ix + 12, iy)], fill=(255, 255, 255, 255), width=1)
    # Kinetic sparks
    for pt in [(ix - 14, iy - 10), (ix + 12, iy - 12), (ix + 14, iy + 8), (ix - 10, iy + 12), (ix + 18, iy - 2)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    # Slip water-skid lines at feet
    h_draw.line([(32, 116), (48, 116)], fill=(255, 255, 255, 180), width=1)
    h_draw.line([(28, 117), (46, 117)], fill=(56, 160, 255, 200), width=1)
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_eyes)
    hit_canvas = Image.alpha_composite(hit_canvas, dart_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (低空硬直·重力阻尼微調 / Gravitational Damping & Gear Re-mesh)
    # Low semi-crouch landing (y+5, x-1), body bows forward, pulse dart braces downward (-12 deg, x-1, y+5).
    # Orbital pulsar key snaps back into gear mesh (+16 deg, x+1, y+3).
    # Starwing mantle folds back to aerodynamic balance.
    # =========================================================================
    shifts_recover = {
        "head_top": (-1, 5), "ear_l": (-2, 5), "ear_r": (0, 5),
        "ear_base_l": (-1, 5), "ear_base_r": (-1, 5),
        "eye_l": (-1, 5), "eye_r": (-1, 5),
        "snout": (-1, 5), "throat": (-1, 5),
        "core": (-1, 5),
        "shoulder_l": (-2, 4), "shoulder_r": (0, 4),
        "arm_l": (1, 4), "arm_r": (-2, 4),
        "hand_r": (-1, 5),
        "torso": (-1, 5), "pelvis": (-1, 4),
        "hip_l": (-3, 3), "hip_r": (2, 3),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "wing_l": (-1, 4), "wing_r": (-1, 3),
        "key_mount": (-1, 4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=16, target_center=(82, 38), scale=1.0)
    dart_rec = place_rotated_element(weapon_raw, deg=-12, target_center=(95, 74), scale=1.0)

    # Gravitational dissipation arcs & landing ripples
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Landing shock ripple arcs at ground contact
    r_draw.arc([34, 112, 94, 122], start=190, end=350, fill=(78, 216, 106, 180), width=1)
    r_draw.arc([42, 114, 86, 120], start=200, end=340, fill=(56, 160, 255, 200), width=1)
    # Gear re-mesh spark at key mount
    r_draw.line([(78, 37), (84, 43)], fill=(255, 208, 40, 230), width=1)
    r_draw.line([(84, 37), (78, 43)], fill=(255, 255, 255, 255), width=1)
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, dart_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


# 2. Main Generation Execution
print("Generating The Starwing Bat combat action poses...")
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

proof_768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_bat_combat_poses_768.png"
proof_strip.save(proof_768_path)
print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

# 4. Generate 768x128 magenta background proof sheet for hole detection
proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
proof_magenta.paste(proof_strip, (0, 0), proof_strip)
proof_mag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_bat_combat_poses_magenta.png"
proof_magenta.save(proof_mag_path)
print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")
