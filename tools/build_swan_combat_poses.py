#!/usr/bin/env python3
"""
tools/build_swan_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Melodic Swan (第四十三族 旋音天鵝, swan)
in Clockwork Heart:
  game/assets/sprites/player/poses/swan/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/swan/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
Enhanced with elegant ballerina knight kinematics, octave music box automaton mechanics, and rich toy articulation.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/swan"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/swan"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load individual slice layers (128x128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_swan_octave_dual_loop_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_swan_spring_steel_ballet_wings.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_swan_silver_enamel_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_swan_tiara_beak_visor.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_swan_theatre_herald_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_swan_prismatic_crystal_monocle.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_swan_octave_spiral_lance.png").convert("RGBA")

# Extract raw weapon crop & center
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Standardized ground contact shadow from cleaned baseline idle asset
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
idle_ref_path = f"{REPO_ROOT}/game/assets/sprites/player/party/swan_idle.png"
if os.path.exists(idle_ref_path):
    ref_im = Image.open(idle_ref_path).convert("RGBA")
else:
    ref_im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    shd = ImageDraw.Draw(ref_im)
    shd.ellipse([34, 108, 94, 120], fill=(31, 26, 58, 110))
    shd.ellipse([44, 110, 84, 118], fill=(31, 26, 58, 160))

s_px = shadow_master.load()
c_px = ref_im.load()
assert s_px is not None and c_px is not None

# Clean baseline shadow to guarantee Rule 4c-5 / 16 (L>=4, T>=4, R>=4, B>=2)
for y in range(118, 128):
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


def warp_image_idw(src_img: Image.Image, src_points: list[tuple[int, int]], dst_points: list[tuple[int, int]], power: float = 2.0, epsilon: float = 3.5) -> Image.Image:
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
    "tiara_top": (60, 7),
    "tiara_l": (47, 18),
    "tiara_r": (73, 18),
    "head_top": (64, 15),
    "beak_root": (74, 34),
    "beak_tip": (87, 34),
    "chin": (64, 48),
    "monocle_r": (72, 38),
    "optic_l": (54, 40),
    "throat": (64, 52),
    "core": (64, 66),
    "chest_gem": (64, 60),
    "shoulder_l": (46, 62),
    "shoulder_r": (82, 62),
    "wing_l_root": (38, 66),
    "wing_l_tip": (20, 74),
    "wing_r_root": (80, 66),
    "wing_r_tip": (92, 80),
    "arm_r": (84, 58),
    "lance_hand": (94, 58),
    "torso": (64, 76),
    "pelvis": (64, 90),
    "tasset_l": (48, 88),
    "tasset_r": (80, 88),
    "foot_l": (52, 108),
    "foot_r": (76, 108),
    "key_mount": (69, 27),
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
    # 1. IDLE (旋音天鵝·八音近衛待機 / Melodic Swan Poised Ballerina Stance)
    # Baseline stable poised ballerina knight stance from canonical composite.
    # Winding key placed at (69, 27).
    # Lance placed at (97, 58).
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(69, 27), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(97, 58), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)

    # Ambient subtle music box glint & lens glimmer FX
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    # Tiara crystal glint at (60, 10)
    i_draw.point((60, 10), fill=(255, 255, 255, 255))
    i_draw.line([(59, 10), (61, 10)], fill=(255, 253, 248, 220), width=1)
    i_draw.line([(60, 9), (60, 11)], fill=(56, 160, 255, 220), width=1)
    # Monocle lens subtle glint at (72, 38)
    i_draw.point((72, 38), fill=(56, 160, 255, 240))
    # Lance miniature music cylinder sparkle at (100, 52)
    i_draw.point((100, 52), fill=(255, 208, 40, 230))
    i_draw.point((101, 51), fill=(255, 255, 255, 255))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (沈勢八音·芭蕾蓄勁瞄準 / Ballerina Plie Windup & Lance Cock)
    # Deep ballerina plié crouch: head & torso sink down and coil back (-3, +6).
    # Lance pulled back into charging tension (deg=-24, x-7, y+6).
    # Winding key counter-winds with ratchet clicks (-35 deg, x-3, y+5).
    # Ballet wings arch back and spread gracefully.
    # FX: Octave acoustic spiral soundwave lines, cyan targeting crosshair, golden note resonance specks.
    # =========================================================================
    shifts_telegraph = {
        "tiara_top": (-3, 6), "tiara_l": (-3, 6), "tiara_r": (-3, 6),
        "head_top": (-3, 6), "beak_root": (-3, 6), "beak_tip": (-3, 6), "chin": (-3, 6),
        "monocle_r": (-3, 6), "optic_l": (-3, 6), "throat": (-3, 6),
        "core": (-2, 5), "chest_gem": (-2, 5),
        "shoulder_l": (-3, 5), "shoulder_r": (-3, 5),
        "wing_l_root": (-2, 4), "wing_l_tip": (-4, 2),
        "wing_r_root": (-3, 4), "wing_r_tip": (-1, 2),
        "lance_hand": (-5, 5), "arm_r": (-4, 5),
        "torso": (-3, 5), "pelvis": (-2, 4),
        "tasset_l": (-3, 4), "tasset_r": (-2, 4),
        "foot_l": (-1, 1), "foot_r": (1, 1),
        "key_mount": (-3, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_tele = place_rotated_element(key_raw, deg=-35, target_center=(66, 32), scale=1.0)
    lance_tele = place_rotated_element(weapon_raw, deg=-24, target_center=(90, 64), scale=1.02)

    # Targeting reticle & acoustic trajectory FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Luminous cyan targeting trajectory line
    t_draw.line([(70, 52), (98, 54)], fill=(56, 160, 255, 210), width=1)
    t_draw.line([(98, 54), (112, 56)], fill=(255, 208, 40, 230), width=2)
    # Targeting crosshair at forward impact point (110, 56)
    cx, cy = 110, 56
    t_draw.arc([cx - 7, cy - 7, cx + 7, cy + 7], start=20, end=340, fill=(56, 160, 255, 230), width=1)
    t_draw.arc([cx - 3, cy - 3, cx + 3, cy + 3], start=40, end=320, fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx - 8, cy), (cx + 8, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 8), (cx, cy + 8)], fill=(255, 208, 40, 240), width=1)
    # Concentric acoustic octave soundwave arcs around lance tip
    t_draw.arc([76, 42, 100, 66], start=120, end=240, fill=(96, 192, 255, 200), width=1)
    t_draw.arc([74, 40, 102, 68], start=130, end=230, fill=(78, 216, 106, 220), width=1)
    # Coiling musical spark particles
    for sx, sy in [(40, 114), (46, 113), (52, 115), (76, 114), (84, 113), (92, 44), (114, 48), (86, 76)]:
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
    # 3. ATTACK (螺旋突刺·大劇院穿心長槍 / Grand Jete Octave Lance Thrust)
    # Explosive forward ballerina knight lunge (+13, +1):
    # Head & torso lunges forward, octave spiral lance thrusts straight forward (+20 deg, x+3, y-2).
    # Winding key spins forward (+55 deg, x+9, y-1).
    # Wings whip backward for aerodynamic counter-balance (-6, -4).
    # Keep right margin >= 4px (weapon right edge <= 123).
    # FX: Conical supersonic acoustic shock cone, musical octave rings, golden note sparks.
    # =========================================================================
    shifts_attack = {
        "tiara_top": (12, 1), "tiara_l": (12, 1), "tiara_r": (12, 1),
        "head_top": (12, 1), "beak_root": (13, 1), "beak_tip": (13, 1), "chin": (13, 1),
        "monocle_r": (12, 1), "optic_l": (12, 1), "throat": (13, 1),
        "core": (11, 1), "chest_gem": (12, 1),
        "shoulder_l": (12, 0), "shoulder_r": (8, 1),
        "wing_l_root": (4, -1), "wing_l_tip": (-6, -4),
        "wing_r_root": (8, 0), "wing_r_tip": (2, -3),
        "lance_hand": (12, -2), "arm_r": (-1, 1),
        "torso": (9, 1), "pelvis": (6, 0),
        "tasset_l": (8, 0), "tasset_r": (5, 0),
        "foot_l": (5, 0), "foot_r": (-3, 0),
        "key_mount": (9, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_atk = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_atk = place_rotated_element(key_raw, deg=55, target_center=(78, 27), scale=1.0)
    lance_atk = place_rotated_element(weapon_raw, deg=18, target_center=(100, 56), scale=1.02)

    # Dynamic acoustic cone & octave shockwave FX
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Piercing acoustic spiral cone
    a_draw.line([(88, 54), (116, 42)], fill=(56, 160, 255, 230), width=2)
    a_draw.line([(90, 58), (118, 48)], fill=(255, 208, 40, 240), width=2)
    a_draw.line([(96, 56), (121, 46)], fill=(255, 253, 248, 255), width=1)
    # Acoustic resonance arcs
    a_draw.arc([60, 20, 118, 92], start=280, end=80, fill=(56, 160, 255, 240), width=2)
    a_draw.arc([64, 24, 114, 88], start=290, end=70, fill=(255, 208, 40, 220), width=2)
    a_draw.arc([68, 28, 110, 84], start=300, end=60, fill=(255, 253, 248, 250), width=1)
    # Impact musical note rings
    a_draw.ellipse([98, 42, 118, 62], outline=(56, 160, 255, 210), width=1)
    a_draw.ellipse([101, 45, 115, 59], outline=(255, 253, 248, 230), width=1)
    # Piercing sparks & flying musical star specks
    for px, py in [(96, 48), (104, 38), (112, 32), (116, 54), (120, 42), (102, 66), (86, 72)]:
        a_draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 253, 248, 255))
        a_draw.point((px, py), fill=(255, 208, 40, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.3))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, lance_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. RECOVER (迴旋卸力·八音近衛斂步 / Ballerina Landing Dampening & Re-poise)
    # Hydraulic recoil: knees flexed, body lowered and braced (-3, +6).
    # Lance held low in defensive reverse guard (+12 deg, x-3, y+6).
    # Winding key rebounds with spring damping (+18 deg, x-3, y+4).
    # Ballet wings tucked low behind for dampening balance.
    # FX: Soft steam puffs from robe/cuirass vents, ground dust dissipation, cooling quartz glow.
    # =========================================================================
    shifts_recover = {
        "tiara_top": (-3, 6), "tiara_l": (-3, 6), "tiara_r": (-3, 6),
        "head_top": (-3, 6), "beak_root": (-3, 6), "beak_tip": (-3, 6), "chin": (-3, 6),
        "monocle_r": (-3, 6), "optic_l": (-3, 6), "throat": (-3, 6),
        "core": (-3, 5), "chest_gem": (-3, 5),
        "shoulder_l": (-3, 5), "shoulder_r": (-3, 5),
        "wing_l_root": (-2, 4), "wing_l_tip": (-2, 3),
        "wing_r_root": (-2, 4), "wing_r_tip": (-1, 3),
        "lance_hand": (-3, 5), "arm_r": (-3, 5),
        "torso": (-2, 4), "pelvis": (-2, 3),
        "tasset_l": (-2, 4), "tasset_r": (-2, 4),
        "foot_l": (-1, 1), "foot_r": (0, 1),
        "key_mount": (-3, 4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_rec = place_rotated_element(key_raw, deg=18, target_center=(66, 31), scale=1.0)
    lance_rec = place_rotated_element(weapon_raw, deg=12, target_center=(94, 64), scale=1.0)

    # Steam venting & soft ground dust dissipation FX
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Steam exhaust puffs from back chassis & cuirass vents
    for (cx, cy, rad) in [(72, 50, 4), (78, 44, 5), (84, 38, 5), (38, 52, 4), (32, 46, 4)]:
        r_draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(255, 253, 248, 110), outline=(220, 235, 255, 160), width=1)
    # Soft rounded dust cloud puffs near ground contact
    for (dx, dy, rx, ry) in [(44, 116, 6, 3), (78, 116, 7, 3), (36, 115, 4, 2), (86, 115, 5, 2)]:
        r_draw.ellipse([dx - rx, dy - ry, dx + rx, dy + ry], fill=(255, 245, 220, 100), outline=(230, 210, 170, 140), width=1)
    # Dissipating spark specks
    for px, py in [(76, 46), (82, 40), (40, 50), (74, 114), (48, 114)]:
        r_draw.point((px, py), fill=(255, 208, 40, 200))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.4))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, lance_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    # =========================================================================
    # 5. SKILL (八音狂瀾·天鵝迴旋鳴奏 / Octave Ballet Overdrive Nova)
    # Massive torque & airborne pirouette leap: body lifts upward (+2, -6).
    # Lance held high overhead pointing skyward (deg=-48, x-5, y-14).
    # Winding key spins +105 deg at high-speed overdrive.
    # Ballet wings fully flared and extended in mechanical glory (-6, -6).
    # FX: Overdrive octave harmonic rings, brilliant multi-colored musical starbursts, radiating star rays.
    # =========================================================================
    shifts_skill = {
        "tiara_top": (2, -6), "tiara_l": (2, -6), "tiara_r": (2, -6),
        "head_top": (2, -6), "beak_root": (2, -5), "beak_tip": (2, -5), "chin": (2, -5),
        "monocle_r": (2, -6), "optic_l": (2, -6), "throat": (2, -5),
        "core": (2, -4), "chest_gem": (2, -5),
        "shoulder_l": (2, -4), "shoulder_r": (0, -4),
        "wing_l_root": (1, -4), "wing_l_tip": (-6, -6),
        "wing_r_root": (2, -4), "wing_r_tip": (4, -5),
        "lance_hand": (1, -4), "arm_r": (-2, -3),
        "torso": (1, -3), "pelvis": (1, -2),
        "tasset_l": (1, -3), "tasset_r": (0, -3),
        "foot_l": (1, -1), "foot_r": (-1, -1),
        "key_mount": (2, -5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_skill = place_rotated_element(key_raw, deg=105, target_center=(72, 22), scale=1.05)
    lance_skill = place_rotated_element(weapon_raw, deg=-48, target_center=(92, 44), scale=1.02)

    # Overdrive musical starburst & gear harmonic FX
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    k_draw = ImageDraw.Draw(skill_fx)
    # Double gear-teeth harmonic ring around chest core (66, 62)
    ox, oy = 66, 62
    k_draw.arc([ox - 22, oy - 22, ox + 22, oy + 22], start=0, end=360, fill=(56, 160, 255, 230), width=2)
    k_draw.arc([ox - 16, oy - 16, ox + 16, oy + 16], start=0, end=360, fill=(255, 208, 40, 230), width=1)
    k_draw.arc([ox - 10, oy - 10, ox + 10, oy + 10], start=0, end=360, fill=(255, 253, 248, 250), width=1)
    # Radiating musical harmonic rays
    for angle_deg in range(0, 360, 45):
        rad = math.radians(angle_deg)
        x1 = ox + int(round(18 * math.cos(rad)))
        y1 = oy + int(round(18 * math.sin(rad)))
        x2 = ox + int(round(26 * math.cos(rad)))
        y2 = oy + int(round(26 * math.sin(rad)))
        k_draw.line([(x1, y1), (x2, y2)], fill=(56, 160, 255, 240), width=2)
    # Whirling musical staff orbital arc
    k_draw.arc([46, 16, 118, 86], start=210, end=40, fill=(255, 253, 248, 240), width=2)
    k_draw.arc([44, 14, 120, 89], start=220, end=30, fill=(255, 208, 40, 220), width=1)
    # Exploding multi-colored toy starburst particles
    for px, py, col in [
        (46, 26, (56, 160, 255)), (84, 16, (255, 253, 248)), (108, 30, (255, 94, 138)),
        (114, 54, (56, 160, 255)), (104, 76, (255, 208, 40)), (38, 56, (255, 160, 16)),
        (52, 81, (255, 253, 248)), (68, 12, (255, 208, 40))
    ]:
        k_draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col + (240,))
        k_draw.point((px, py), fill=(255, 255, 255, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.3))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, lance_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 6. HIT (受擊震退·銀白琺瑯音碎星屑 / Enamel Impact & Chime Fracture)
    # Violent backward recoil: head thrown far back (-14, -3), torso arched back (-9, -1).
    # Lance jarred back and tilted (deg=-34, x-15, y-8).
    # Winding key knocked counter-clockwise (-30 deg, x-13, y-3).
    # Ballet wings fold forward defensively (+3, +2).
    # Ground shadow strictly anchored (Rule 4b-5).
    # FX: Piercing impact starburst at chest armor, clean enamel fracture shockwave, flying sparks.
    # Note: Adheres strictly to 0-QA16 and 0-QA31 (no dark rectangular patch, rich core coloration).
    # =========================================================================
    shifts_hit = {
        "tiara_top": (-14, -3), "tiara_l": (-14, -3), "tiara_r": (-14, -3),
        "head_top": (-14, -3), "beak_root": (-13, -2), "beak_tip": (-13, -2), "chin": (-13, -2),
        "monocle_r": (-14, -3), "optic_l": (-14, -3), "throat": (-13, -2),
        "core": (-9, -1), "chest_gem": (-9, -1),
        "shoulder_l": (-11, -2), "shoulder_r": (-8, -1),
        "wing_l_root": (-7, -1), "wing_l_tip": (3, 2),
        "wing_r_root": (-5, -1), "wing_r_tip": (4, 2),
        "lance_hand": (-12, -1), "arm_r": (-12, -1),
        "torso": (-9, -1), "pelvis": (-6, 0),
        "tasset_l": (-8, -1), "tasset_r": (-5, 0),
        "foot_l": (-2, 0), "foot_r": (0, 0),
        "key_mount": (-13, -3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_hit = place_rotated_element(key_raw, deg=-30, target_center=(56, 24), scale=1.0)
    lance_hit = place_rotated_element(weapon_raw, deg=-34, target_center=(82, 50), scale=1.02)

    # Kinetic impact flash & plating spark FX (0-QA31 compliant: bright epicenter, no dark mask)
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Violent white-cyan impact epicenter at chest armor (64, 62)
    hx, hy = 64, 62
    # 4-pointed sharp impact diamond
    h_draw.polygon([(hx, hy - 14), (hx + 4, hy - 2), (hx + 16, hy), (hx + 4, hy + 2),
                    (hx, hy + 14), (hx - 4, hy + 2), (hx - 16, hy), (hx - 4, hy - 2)],
                   fill=(255, 253, 248, 255))
    h_draw.polygon([(hx, hy - 8), (hx + 2, hy - 1), (hx + 9, hy), (hx + 2, hy + 1),
                    (hx, hy + 8), (hx - 2, hy + 1), (hx - 9, hy), (hx - 2, hy - 1)],
                   fill=(56, 160, 255, 255))
    # Concentric impact shock rings
    h_draw.arc([hx - 20, hy - 20, hx + 20, hy + 20], start=30, end=330, fill=(255, 208, 40, 220), width=2)
    h_draw.arc([hx - 26, hy - 26, hx + 26, hy + 26], start=45, end=315, fill=(56, 160, 255, 210), width=1)
    # Dynamic fracture sparks & flying enamel particles
    for px, py, sz in [(hx - 18, hy - 16, 2), (hx + 18, hy - 14, 2), (hx + 22, hy + 12, 1),
                       (hx - 14, hy + 18, 2), (hx + 12, hy + 22, 1), (hx - 22, hy + 6, 2),
                       (hx + 26, hy - 6, 1), (hx - 10, hy - 24, 2)]:
        h_draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=(255, 253, 248, 255))
        h_draw.point((px, py), fill=(255, 208, 40, 255))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.3))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, lance_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    return poses


def main():
    print("Generating Melodic Swan combat action poses...")
    poses = generate_poses()

    for p_name, img in poses.items():
        # Save 128x128 RGBA
        p_128 = f"{OUT_DIR}/{p_name}.png"
        img.save(p_128)

        # Save 512x512 LANCZOS RGBA
        p_512 = f"{OUT_DIR}/{p_name}_512.png"
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        img_512.save(p_512)

        print(f"  ✓ Saved {p_name:10s} (128x128 & 512x512 LANCZOS) bbox={img.getbbox()}")

    # Generate 768x128 Proof strips (transparent & magenta)
    pose_order = ["idle", "telegraph", "attack", "skill", "hit", "recover"]
    strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    for i, p_name in enumerate(pose_order):
        strip.paste(poses[p_name], (i * 128, 0))
    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_swan_combat_poses_768.png"
    strip.save(proof_strip_path)
    print(f"  ✓ Saved 768x128 proof strip: {proof_strip_path}")

    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_swan_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path)
    print(f"  ✓ Saved 768x128 magenta proof strip: {proof_magenta_path}")

    print("\nAll 6 combat poses successfully generated and saved!")


if __name__ == "__main__":
    main()
