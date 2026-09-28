#!/usr/bin/env python3
"""
tools/build_sailfish_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Hydrofoil Sailfish (第三十一族 破浪旗魚, sailfish)
in Clockwork Heart:
  game/assets/sprites/player/poses/sailfish/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/sailfish/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/sailfish"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/sailfish"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_sailfish_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_sailfish_abyssal_helm_trident.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_sailfish_clockwork_sailfin_mantle.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_sailfish_abyssal_titanium_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_sailfish_hydrofoil_visor_crest.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_sailfish_abyssal_knight_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_sailfish_dual_abyssal_optic_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_sailfish_hydrofoil_lance.png").convert("RGBA")

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
    "head_top": (62, 12),
    "crest_top": (62, 11),
    "visor_l": (46, 28),
    "visor_r": (80, 28),
    "eye_l": (51, 41),
    "eye_r": (77, 41),
    "snout": (62, 48),
    "throat": (62, 54),
    "core": (62, 64),
    "shoulder_l": (44, 62),
    "shoulder_r": (82, 62),
    "arm_l": (36, 70),
    "arm_r": (86, 70),
    "lance_hand": (34, 70),
    "torso": (62, 74),
    "pelvis": (62, 86),
    "hip_l": (48, 94),
    "hip_r": (78, 94),
    "foot_l": (48, 114),
    "foot_r": (76, 114),
    "fin_base": (42, 42),
    "fin_top": (36, 18),
    "key_mount": (85, 30),
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
    # 1. IDLE (破浪旗魚待機 / The Hydrofoil Sailfish Poise)
    # Baseline stable poise from canonical composite.
    # Winding key placed at center (85, 31) ensuring top >= 4 (Rule 4c-5 / 16).
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(85, 31), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(33, 69), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (深海蓄勢·破浪瞄準 / Hydro-Cavitation Tension & Lance Draw)
    # Deep hydrofoil crouch (y+7, x-2), torso leans slightly back (-2 deg),
    # hydrofoil lance pulled back into firing stance (-18 deg, x+2, y-3).
    # Trident helm key counter-rotates (-28 deg, x-2, y+5).
    # Mantle sailfin arches tense and ready.
    # FX: Hydro cavitation spiral vortex, aiming reticle, sonic bubbles.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 7), "crest_top": (-2, 7),
        "visor_l": (-3, 7), "visor_r": (-1, 7),
        "eye_l": (-2, 7), "eye_r": (-2, 7),
        "snout": (-2, 7), "throat": (-2, 7),
        "core": (-2, 7),
        "shoulder_l": (-1, 6), "shoulder_r": (-3, 6),
        "arm_l": (1, 5), "arm_r": (-5, 6),
        "lance_hand": (1, 5),
        "torso": (-2, 7), "pelvis": (-2, 6),
        "hip_l": (-4, 5), "hip_r": (1, 5),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "fin_base": (-2, 6), "fin_top": (-3, 4),
        "key_mount": (-2, 6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_tele = place_rotated_element(key_raw, deg=-28, target_center=(83, 36), scale=1.0)
    lance_tele = place_rotated_element(weapon_raw, deg=-18, target_center=(35, 66), scale=1.04)

    # Hydro-cavitation vortex & targeting reticle FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Hydro cavitation trajectory beam
    t_draw.line([(36, 64), (78, 54)], fill=(56, 160, 255, 210), width=1)
    t_draw.line([(78, 54), (118, 44)], fill=(78, 216, 106, 230), width=2)
    t_draw.line([(92, 51), (122, 43)], fill=(255, 255, 255, 255), width=1)
    # Abyssal hydrofoil crosshair reticle at target forward (108, 46)
    cx, cy = 108, 46
    t_draw.arc([cx - 8, cy - 8, cx + 8, cy + 8], start=25, end=335, fill=(56, 160, 255, 220), width=1)
    t_draw.arc([cx - 4, cy - 4, cx + 4, cy + 4], start=45, end=315, fill=(255, 208, 40, 230), width=1)
    t_draw.line([(cx - 11, cy), (cx + 11, cy)], fill=(78, 216, 106, 240), width=1)
    t_draw.line([(cx, cy - 11), (cx, cy + 11)], fill=(78, 216, 106, 240), width=1)
    # Cavitation water rings around lance tip
    t_draw.arc([22, 54, 48, 78], start=120, end=300, fill=(56, 160, 255, 220), width=2)
    t_draw.arc([26, 57, 44, 75], start=140, end=280, fill=(255, 253, 248, 200), width=1)
    # Bubbles / cavitation sparks
    for sx, sy in [(114, 38), (120, 52), (98, 36), (88, 28), (28, 50), (46, 76)]:
        t_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 240))
        t_draw.point((sx, sy), fill=(56, 160, 255, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, lance_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (破浪穿刺·超空泡騎槍突擊 / Supercavitating Hydrofoil Thrust)
    # Fierce lunge forward-right (+13, -1), lance thrusts straight forward (+20 deg, x+14, y-5)!
    # Trident key spins rapidly (+42 deg, x+8, y-1).
    # Sailfin mantle flares back to channel oceanic thrust.
    # FX: Supersonic conical water cavitation shock cone, hydro-jet wake trails.
    # =========================================================================
    shifts_attack = {
        "head_top": (13, -1), "crest_top": (13, -1),
        "visor_l": (11, -1), "visor_r": (14, -1),
        "eye_l": (13, -1), "eye_r": (13, -1),
        "snout": (14, 0), "throat": (13, 0),
        "core": (12, 0),
        "shoulder_l": (14, -1), "shoulder_r": (7, 0),
        "arm_l": (16, -4), "arm_r": (-7, 2),
        "lance_hand": (16, -4),
        "torso": (11, 0), "pelvis": (9, 0),
        "hip_l": (10, -1), "hip_r": (-3, 0),
        "foot_l": (7, 0), "foot_r": (-4, 0),
        "fin_base": (8, 0), "fin_top": (6, -2),
        "key_mount": (10, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=42, target_center=(95, 30), scale=1.0)
    lance_attack = place_rotated_element(weapon_raw, deg=20, target_center=(47, 64), scale=1.06)

    # Supercavitating shock cone & water-jet trails
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Piercing cavitation lance beam
    a_draw.line([(48, 63), (122, 54)], fill=(56, 160, 255, 245), width=2)
    a_draw.line([(58, 62), (122, 53)], fill=(255, 255, 255, 255), width=1)
    # Conical cavitation shockwave arcs
    a_draw.arc([76, 38, 122, 80], start=305, end=55, fill=(78, 216, 106, 230), width=2)
    a_draw.arc([82, 42, 120, 76], start=315, end=45, fill=(255, 208, 40, 240), width=2)
    a_draw.arc([88, 46, 118, 72], start=325, end=35, fill=(56, 160, 255, 255), width=1)
    # Spray & cavitation bubbles
    for pt in [(118, 40), (122, 52), (120, 66), (114, 76), (106, 34), (98, 28)]:
        a_draw.point(pt, fill=(56, 160, 255, 255))
        a_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, lance_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (蒼洋裂波·天頂水翼狂潮 / Oceanic Hydrofoil Deluge)
    # Airborne leap pose (y-8, x+1), lance raised skyward (-50 deg, x+10, y-17).
    # Trident key in maximum overdrive (+82 deg, x+2, y-9).
    # Sailfin mantle expands into full wave-splitting hydrodynamic hydrofoil.
    # FX: Ascending tidal rings, spiraling water geyser, radiant starlight pearls.
    # =========================================================================
    shifts_skill = {
        "head_top": (1, -8), "crest_top": (1, -8),
        "visor_l": (-1, -8), "visor_r": (3, -8),
        "eye_l": (1, -8), "eye_r": (1, -8),
        "snout": (1, -8), "throat": (1, -8),
        "core": (1, -8),
        "shoulder_l": (-2, -8), "shoulder_r": (4, -8),
        "arm_l": (10, -17), "arm_r": (-5, -6),
        "lance_hand": (10, -17),
        "torso": (1, -8), "pelvis": (1, -7),
        "hip_l": (-3, -6), "hip_r": (4, -6),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "fin_base": (0, -7), "fin_top": (-2, -6),
        "key_mount": (2, -8),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=82, target_center=(87, 23), scale=1.0)
    lance_skill = place_rotated_element(weapon_raw, deg=-50, target_center=(43, 52), scale=1.08)

    # Tidal hydrofoil deluge rings & geyser beams
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    sk_draw = ImageDraw.Draw(skill_fx)
    # Spiral water deluge arcs
    sk_draw.arc([16, 12, 116, 112], start=195, end=345, fill=(56, 160, 255, 235), width=2)
    sk_draw.arc([24, 18, 108, 102], start=205, end=335, fill=(78, 216, 106, 220), width=2)
    sk_draw.arc([32, 24, 100, 92], start=215, end=325, fill=(255, 208, 40, 230), width=2)
    sk_draw.arc([40, 30, 92, 82], start=225, end=315, fill=(255, 94, 138, 220), width=1)
    # Skyward cavitation water geyser rays
    sk_draw.line([(44, 50), (56, 8)], fill=(56, 160, 255, 240), width=2)
    sk_draw.line([(45, 50), (56, 8)], fill=(255, 255, 255, 255), width=1)
    sk_draw.line([(40, 53), (32, 12)], fill=(78, 216, 106, 220), width=1)
    sk_draw.line([(48, 53), (76, 10)], fill=(255, 208, 40, 220), width=1)
    # Oceanic luminescent pearls / bubbles
    for star_x, star_y in [(22, 24), (106, 16), (116, 66), (18, 74), (64, 8), (112, 80)]:
        sk_draw.ellipse([star_x - 1, star_y - 1, star_x + 1, star_y + 1], fill=(255, 255, 255, 240))
        sk_draw.point((star_x, star_y), fill=(56, 160, 255, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.4))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, lance_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊震退·深海面甲過載 / Impact Recoil & Hydro-Armor Glitch)
    # Violent backward slip (x-11, y-2), head and hydrofoil crest tilt back (-10 deg),
    # lance jarred upward (+24 deg, x-7, y+5),
    # key slips backward against gear ratchet (-30 deg, x-8, y-3), mantle collapses forward (+4, -1).
    # Optic turret indicators show dizzy/strain '> <' cute LED eyes!
    # =========================================================================
    shifts_hit = {
        "head_top": (-11, -2), "crest_top": (-11, -2),
        "visor_l": (-12, -2), "visor_r": (-9, -2),
        "eye_l": (-11, -2), "eye_r": (-11, -2),
        "snout": (-11, -2), "throat": (-10, -2),
        "core": (-9, -1),
        "shoulder_l": (-11, -2), "shoulder_r": (-8, -2),
        "arm_l": (-7, 4), "arm_r": (-10, 0),
        "lance_hand": (-7, 4),
        "torso": (-9, -1), "pelvis": (-7, 0),
        "hip_l": (-7, -1), "hip_r": (-4, 0),
        "foot_l": (-3, 0), "foot_r": (2, 0),
        "fin_base": (-6, -1), "fin_top": (4, -1),
        "key_mount": (-9, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    # Warped body for hit
    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Overlay cute dizzy strain '> <' LEDs on optic eyes:
    # Left eye shifted: (51 - 11, 41 - 2) = (40, 39)
    # Right eye shifted: (77 - 11, 41 - 2) = (66, 39)
    hit_eyes = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    he_draw = ImageDraw.Draw(hit_eyes)
    # Left eye strain '>'
    lx, ly = 40, 39
    he_draw.line([(lx - 3, ly - 3), (lx + 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(lx - 3, ly + 3), (lx + 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(lx - 2, ly - 2), (lx + 1, ly)], fill=(255, 255, 255, 255), width=1)
    # Right eye strain '<'
    rx, ry = 66, 39
    he_draw.line([(rx + 3, ly - 3), (rx - 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(rx + 3, ly + 3), (rx - 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(rx + 2, ly - 2), (rx - 1, ly)], fill=(255, 255, 255, 255), width=1)

    key_hit = place_rotated_element(key_raw, deg=-30, target_center=(77, 28), scale=1.0)
    lance_hit = place_rotated_element(weapon_raw, deg=24, target_center=(26, 74), scale=1.0)

    # Impact spark burst and kinetic deflection lines
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact point at titanium abyssal cuirass (54, 62)
    ix, iy = 54, 62
    h_draw.line([(ix - 12, iy - 8), (ix + 10, iy + 6)], fill=(255, 208, 40, 240), width=2)
    h_draw.line([(ix - 8, iy + 10), (ix + 8, iy - 8)], fill=(255, 94, 138, 230), width=2)
    h_draw.line([(ix - 14, iy), (ix + 12, iy)], fill=(255, 255, 255, 255), width=1)
    # Kinetic sparks
    for pt in [(ix - 14, iy - 10), (ix + 12, iy - 12), (ix + 14, iy + 8), (ix - 10, iy + 12), (ix + 18, iy - 2)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    # Slip water-skid lines at feet
    h_draw.line([(30, 115), (46, 115)], fill=(255, 255, 255, 180), width=1)
    h_draw.line([(26, 117), (44, 117)], fill=(56, 160, 255, 200), width=1)
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_eyes)
    hit_canvas = Image.alpha_composite(hit_canvas, lance_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (低空硬直·深海舵輪咬合 / Hydrodynamic Damping & Gear Re-mesh)
    # Low semi-crouch landing (y+6, x-1), body bows forward, hydrofoil lance braces downward (-10 deg, x+1, y+5).
    # Trident helm key snaps back into gear mesh (+15 deg, x+1, y+3).
    # Sailfin mantle folds back to hydrodynamic balance (x-1, y+3).
    # =========================================================================
    shifts_recover = {
        "head_top": (-1, 6), "crest_top": (-1, 6),
        "visor_l": (-2, 6), "visor_r": (0, 6),
        "eye_l": (-1, 6), "eye_r": (-1, 6),
        "snout": (-1, 6), "throat": (-1, 6),
        "core": (-1, 6),
        "shoulder_l": (-2, 5), "shoulder_r": (0, 5),
        "arm_l": (1, 4), "arm_r": (-2, 5),
        "lance_hand": (1, 4),
        "torso": (-1, 6), "pelvis": (-1, 5),
        "hip_l": (-3, 4), "hip_r": (2, 4),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "fin_base": (-1, 5), "fin_top": (-1, 3),
        "key_mount": (-1, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=15, target_center=(86, 34), scale=1.0)
    lance_rec = place_rotated_element(weapon_raw, deg=-10, target_center=(34, 74), scale=1.0)

    # Hydrodynamic dissipation arcs & landing ripples
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Landing water ripple / dissipation arcs at ground contact
    r_draw.arc([34, 112, 94, 122], start=190, end=350, fill=(56, 160, 255, 180), width=1)
    r_draw.arc([42, 114, 86, 120], start=200, end=340, fill=(78, 216, 106, 200), width=1)
    # Gear re-mesh spark at key mount
    r_draw.line([(82, 35), (88, 41)], fill=(255, 208, 40, 230), width=1)
    r_draw.line([(88, 35), (82, 41)], fill=(255, 255, 255, 255), width=1)
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, lance_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


# 2. Main Generation Execution
print("Generating Hydrofoil Sailfish combat action poses...")
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

proof_768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_sailfish_combat_poses_768.png"
proof_strip.save(proof_768_path)
print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

# 4. Generate 768x128 magenta background proof sheet for hole detection
proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
proof_magenta.paste(proof_strip, (0, 0), proof_strip)
proof_mag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_sailfish_combat_poses_magenta.png"
proof_magenta.save(proof_mag_path)
print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")

print("\nAll 6 Hydrofoil Sailfish combat action poses successfully generated and exported!")
