#!/usr/bin/env python3
"""
tools/build_gecko_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Conduit Gecko (第四十五族 巡管守宮, gecko)
in Clockwork Heart:
  game/assets/sprites/player/poses/gecko/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/gecko/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
Features conduit agile wall-runner kinematics, micro-suction pads, dual-ring relief valve key,
segmented gear balance tail, and brass ratchet polygon conduit shuriken attacks.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/gecko"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/gecko"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load individual slice layers (128x128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_gecko_dual_ring_relief_valve_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_gecko_segmented_gear_balance_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_gecko_brass_patina_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_gecko_conduit_scout_crest_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_gecko_highpressure_stealth_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_gecko_dual_slit_aperture_quartz_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_gecko_conduit_ratchet_dart.png").convert("RGBA")

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Standardized ground contact shadow from cleaned baseline idle asset
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
idle_ref_path = f"{REPO_ROOT}/game/assets/sprites/player/party/gecko_idle.png"
if os.path.exists(idle_ref_path):
    ref_im = Image.open(idle_ref_path).convert("RGBA")
else:
    ref_im = Image.open(f"{BASE_DIR}/proof_paperdoll_gecko_composite.png").convert("RGBA")

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
    "cowl_top": (63, 22),
    "cowl_l": (46, 28),
    "cowl_r": (80, 28),
    "snout": (64, 48),
    "chin": (64, 56),
    "eye_l": (53, 40),
    "eye_r": (75, 41),
    "throat": (64, 56),
    "core": (64, 66),
    "shoulder_l": (46, 62),
    "shoulder_r": (82, 62),
    "arm_l": (38, 72),
    "hand_r": (82, 70),
    "buckle": (64, 76),
    "pelvis": (64, 88),
    "hip_l": (48, 96),
    "hip_r": (80, 96),
    "foot_l": (50, 116),
    "foot_r": (76, 116),
    "tail_root": (59, 84),
    "tail_mid": (35, 78),
    "tail_tip": (14, 67),
    "key_mount": (70, 33),
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
    # 1. IDLE (巡管守宮·暗忍待機 / Conduit Scout Alert Stance)
    # Baseline stable poised ninja stealth stance from canonical composite.
    # Winding key placed at (70, 33).
    # Dart placed at (82, 70).
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(70, 33), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(82, 70), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)

    # Ambient subtle conduit optical glint & ratchet sparkle FX
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    # Dual-slit quartz lens glimmers
    i_draw.point((53, 40), fill=(255, 208, 40, 240))
    i_draw.point((75, 41), fill=(255, 208, 40, 240))
    i_draw.line([(52, 40), (54, 40)], fill=(255, 255, 255, 220), width=1)
    i_draw.line([(74, 41), (76, 41)], fill=(255, 255, 255, 220), width=1)
    # Shuriken bearing brass highlight
    i_draw.point((82, 70), fill=(255, 253, 248, 230))
    i_draw.point((83, 69), fill=(255, 208, 40, 220))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (暗忍蓄勁·裂隙瞄準鎖定 / Ratchet Shuriken Windup & Slit Aim)
    # Deep conduit ninja crouch: head & torso sink down and coil back (-3, +6).
    # Ratchet shuriken pulled back into throwing tension (deg=-28, target_center=(74, 65)).
    # Dual-ring relief valve key counter-winds with ratchet clicks (-32 deg, target_center=(67, 39)).
    # Tail curls upward and arches (+3, -4) to counterbalance rearward tension.
    # FX: Cyan & gold trajectory beam, target reticle, steam pressure relief particles.
    # =========================================================================
    shifts_telegraph = {
        "cowl_top": (-3, 6), "cowl_l": (-3, 6), "cowl_r": (-3, 6),
        "snout": (-3, 6), "chin": (-3, 6),
        "eye_l": (-3, 6), "eye_r": (-3, 6),
        "throat": (-3, 6), "core": (-2, 5),
        "shoulder_l": (-3, 5), "shoulder_r": (-3, 5),
        "arm_l": (-1, 5), "hand_r": (-8, -5),
        "buckle": (-2, 5), "pelvis": (-2, 4),
        "hip_l": (-3, 4), "hip_r": (-1, 4),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_root": (-2, 4), "tail_mid": (0, -2), "tail_tip": (3, -6),
        "key_mount": (-3, 6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_tele = place_rotated_element(key_raw, deg=-32, target_center=(67, 39), scale=1.0)
    dart_tele = place_rotated_element(weapon_raw, deg=-28, target_center=(74, 65), scale=1.04)

    # Mechanical winding tension & valve steam venting FX (directly tied to weapon & valve)
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Shuriken tension ratchet arc around dart at (74, 65)
    t_draw.arc([60, 51, 88, 79], start=210, end=330, fill=(255, 208, 40, 230), width=1)
    t_draw.arc([62, 53, 86, 77], start=220, end=320, fill=(255, 253, 248, 220), width=1)
    # Steam pressure venting puffs at relief valve key (67, 39)
    for sx, sy in [(65, 30), (58, 24), (72, 22), (54, 28), (76, 26)]:
        t_draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 253, 248, 200))
        t_draw.point((sx, sy), fill=(56, 160, 255, 240))
    # Ratchet mechanical click sparks at right hand
    for sx, sy in [(78, 62), (84, 58), (70, 72), (82, 70)]:
        t_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255, 240))
        t_draw.point((sx, sy), fill=(255, 208, 40, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.35))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, dart_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (棘輪急射·管網跳彈疾刺 / Ratchet Shuriken Ricochet Thrust)
    # Dynamic forward lunge (+12, -1): body springs forward in agile ninja lunge.
    # Ratchet shuriken thrusts forward with high-speed rotation (+38 deg, (108, 64), scale 1.06).
    # Dual-ring key spins rapidly (+52 deg, (82, 32)).
    # Segmented tail sweeps horizontally backward (-6, +2) to counterbalance momentum.
    # FX: Cutting polygon shockwave, brass sparks, ricochet trajectory lines.
    # =========================================================================
    shifts_attack = {
        "cowl_top": (12, -1), "cowl_l": (11, -1), "cowl_r": (13, -1),
        "snout": (13, -1), "chin": (13, -1),
        "eye_l": (13, -1), "eye_r": (13, -1),
        "throat": (13, -1), "core": (12, 0),
        "shoulder_l": (13, -1), "shoulder_r": (9, 0),
        "arm_l": (13, -2), "hand_r": (26, -6),
        "buckle": (11, 0), "pelvis": (9, 0),
        "hip_l": (9, -1), "hip_r": (0, 0),
        "foot_l": (7, 0), "foot_r": (-2, 0),
        "tail_root": (8, 0), "tail_mid": (-1, 1), "tail_tip": (-6, 2),
        "key_mount": (12, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_attack = place_rotated_element(key_raw, deg=52, target_center=(82, 32), scale=1.0)
    dart_attack = place_rotated_element(weapon_raw, deg=38, target_center=(108, 64), scale=1.06)

    # High-speed cutting arc & ricochet spark FX
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Piercing shuriken flight laser beam
    a_draw.line([(88, 66), (122, 60)], fill=(255, 208, 40, 245), width=2)
    a_draw.line([(96, 65), (122, 60)], fill=(255, 255, 255, 255), width=1)
    # Cutting vortex arcs around shuriken
    a_draw.arc([92, 46, 122, 76], start=290, end=70, fill=(78, 216, 106, 235), width=2)
    a_draw.arc([98, 50, 120, 72], start=300, end=60, fill=(56, 160, 255, 240), width=1)
    # Trailing sparks
    for pt in [(120, 48), (122, 58), (118, 70), (112, 76), (102, 42), (92, 74)]:
        a_draw.point(pt, fill=(255, 208, 40, 255))
        a_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.35))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, dart_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (奧義·暴風鏢陣·高壓洩壓全功率 / Steam Conduit Overdrive & Shuriken Typhoon)
    # Acrobatic pipe leap / wall-spring launch: body leaps upward into suspension (y-7, x+1).
    # Maintains strict 1:1 head scale (no horizontal stretching).
    # Dual-ring key in rapid spin overdrive (+24 deg, (72, 28)), clearly visible above cowl.
    # Shuriken hyper-spin (-58 deg, (96, 54), scale 1.12).
    # Segmented gear tail lashes upward (-5, -8) to adjust aerial orientation.
    # FX: Concentric cutting vortex arcs, dual steam jets, radiant golden & cyan sparks.
    # =========================================================================
    shifts_skill = {
        "cowl_top": (1, -7), "cowl_l": (1, -7), "cowl_r": (1, -7),
        "snout": (1, -7), "chin": (1, -7),
        "eye_l": (1, -7), "eye_r": (1, -7),
        "throat": (1, -7), "core": (1, -7),
        "shoulder_l": (0, -7), "shoulder_r": (2, -7),
        "arm_l": (-4, -6), "hand_r": (14, -16),
        "buckle": (1, -7), "pelvis": (1, -6),
        "hip_l": (-2, -5), "hip_r": (2, -5),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_root": (0, -6), "tail_mid": (-3, -8), "tail_tip": (-5, -8),
        "key_mount": (2, -7),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_skill = place_rotated_element(key_raw, deg=24, target_center=(72, 28), scale=1.0)
    dart_skill = place_rotated_element(weapon_raw, deg=-58, target_center=(96, 54), scale=1.12)

    # Concentric steam vortex & polygon typhoon FX around shuriken & core
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    sk_draw = ImageDraw.Draw(skill_fx)
    # Shuriken spinning cutting vortex rings centered at (96, 54)
    ox, oy = 96, 54
    sk_draw.arc([ox - 22, oy - 22, ox + 22, oy + 22], start=280, end=110, fill=(56, 160, 255, 230), width=2)
    sk_draw.arc([ox - 16, oy - 16, ox + 16, oy + 16], start=290, end=90, fill=(78, 216, 106, 220), width=2)
    sk_draw.arc([ox - 10, oy - 10, ox + 10, oy + 10], start=300, end=70, fill=(255, 208, 40, 235), width=2)
    # Steam conduit exhaust angled bursts radiating from shuriken (96, 54)
    sk_draw.line([(96, 51), (114, 22)], fill=(56, 160, 255, 240), width=2)
    sk_draw.line([(97, 51), (114, 22)], fill=(255, 255, 255, 255), width=1)
    sk_draw.line([(88, 48), (68, 26)], fill=(78, 216, 106, 220), width=1)
    sk_draw.line([(104, 58), (120, 44)], fill=(255, 208, 40, 220), width=1)
    # High-pressure steam sparks
    for sx, sy in [(114, 24), (118, 50), (108, 76), (82, 36), (42, 36), (72, 12), (104, 30)]:
        sk_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255, 240))
        sk_draw.point((sx, sy), fill=(255, 208, 40, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.35))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, dart_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊震退·洩壓閥過載硬直 / Kinetic Impact Recoil & Pressure Vent Glitch)
    # Recoil backward slip (x-9, y-2), head and cowl tilt backward.
    # Shuriken jarred upward (+24 deg, (74, 76)).
    # Key knocked backward (-34 deg, (61, 31)).
    # Tail whipped forward and curled protectively (-4, -2).
    # Optic slits express cute strain '> <' yellow quartz overload indicators.
    # FX: Kinetic impact sparks, steam pop burst. (Clean shadow zone, 0 skid artifacts).
    # =========================================================================
    shifts_hit = {
        "cowl_top": (-9, -2), "cowl_l": (-10, -2), "cowl_r": (-8, -2),
        "snout": (-9, -2), "chin": (-9, -2),
        "eye_l": (-9, -2), "eye_r": (-9, -2),
        "throat": (-8, -1), "core": (-7, -1),
        "shoulder_l": (-9, -1), "shoulder_r": (-6, -1),
        "arm_l": (-5, 2), "hand_r": (-8, 6),
        "buckle": (-7, -1), "pelvis": (-5, 0),
        "hip_l": (-5, 0), "hip_r": (-2, 0),
        "foot_l": (-3, 0), "foot_r": (2, 0),
        "tail_root": (-5, 0), "tail_mid": (-4, -2), "tail_tip": (-2, -3),
        "key_mount": (-9, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)

    # Overlay cute dizzy strain '> <' LEDs on optic eyes:
    # Left eye base: (53, 40), shifted: (53 - 9, 40 - 2) = (44, 38)
    # Right eye base: (75, 41), shifted: (75 - 9, 41 - 2) = (66, 39)
    hit_eyes = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    he_draw = ImageDraw.Draw(hit_eyes)
    # Left eye strain '>'
    lx, ly = 44, 38
    he_draw.line([(lx - 3, ly - 3), (lx + 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(lx - 3, ly + 3), (lx + 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(lx - 2, ly - 2), (lx + 1, ly)], fill=(255, 255, 255, 255), width=1)
    # Right eye strain '<'
    rx, ry = 66, 39
    he_draw.line([(rx + 3, ry - 3), (rx - 2, ry)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(rx + 3, ry + 3), (rx - 2, ry)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(rx + 2, ry - 2), (rx - 1, ry)], fill=(255, 255, 255, 255), width=1)

    key_hit = place_rotated_element(key_raw, deg=-34, target_center=(61, 31), scale=1.0)
    dart_hit = place_rotated_element(weapon_raw, deg=24, target_center=(74, 76), scale=1.0)

    # Impact spark burst and kinetic deflection lines
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    ix, iy = 58, 64
    h_draw.line([(ix - 12, iy - 8), (ix + 10, iy + 6)], fill=(255, 208, 40, 240), width=2)
    h_draw.line([(ix - 8, iy + 10), (ix + 8, iy - 8)], fill=(255, 94, 138, 230), width=2)
    h_draw.line([(ix - 14, iy), (ix + 12, iy)], fill=(255, 255, 255, 255), width=1)
    for pt in [(ix - 14, iy - 10), (ix + 12, iy - 12), (ix + 14, iy + 8), (ix - 10, iy + 12), (ix + 18, iy - 2)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.35))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_eyes)
    hit_canvas = Image.alpha_composite(hit_canvas, dart_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (翻滾著地·吸盤急停阻尼收勢 / Suction Pad Braking & Gyro Dampening)
    # Low-profile landing crouch (y+5, x-1), body bows forward, absorbs shock.
    # Winding key re-engages into main drive (+14 deg, (71, 37)).
    # Tail lowers to touch down (+2, +4).
    # Shuriken gathered close to body (-14 deg, (80, 75)).
    # FX: Residual pressure vent puffs, gear re-mesh spark. (Clean shadow zone, 0 ground arc lines).
    # =========================================================================
    shifts_recover = {
        "cowl_top": (-1, 5), "cowl_l": (-1, 5), "cowl_r": (-1, 5),
        "snout": (-1, 5), "chin": (-1, 5),
        "eye_l": (-1, 5), "eye_r": (-1, 5),
        "throat": (-1, 5), "core": (-1, 5),
        "shoulder_l": (-2, 4), "shoulder_r": (0, 4),
        "arm_l": (1, 4), "hand_r": (-2, 5),
        "buckle": (-1, 5), "pelvis": (-1, 4),
        "hip_l": (-3, 3), "hip_r": (1, 3),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_root": (-1, 4), "tail_mid": (1, 4), "tail_tip": (2, 4),
        "key_mount": (1, 4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_rec = place_rotated_element(key_raw, deg=14, target_center=(71, 37), scale=1.0)
    dart_rec = place_rotated_element(weapon_raw, deg=-14, target_center=(80, 75), scale=1.0)

    # Residual pressure vent puffs & re-mesh spark
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Steam pressure puffs at valve
    for sx, sy in [(68, 28), (62, 24), (74, 22)]:
        r_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 210))
        r_draw.point((sx, sy), fill=(56, 160, 255, 240))
    # Gear re-mesh spark at key mount
    r_draw.line([(68, 35), (74, 41)], fill=(255, 208, 40, 230), width=1)
    r_draw.line([(74, 35), (68, 41)], fill=(255, 255, 255, 255), width=1)
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, dart_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def main():
    print("Generating The Conduit Gecko combat action poses...")
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

    proof_768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_gecko_combat_poses_768.png"
    proof_strip.save(proof_768_path)
    print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

    # 4. Generate 768x128 magenta background proof sheet for hole detection
    proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    proof_magenta.paste(proof_strip, (0, 0), proof_strip)
    proof_mag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_gecko_combat_poses_magenta.png"
    proof_magenta.save(proof_mag_path)
    print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")

    # 5. Crop 8x hit core for 0-QA31
    hit_512 = poses["hit"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    core_crop = hit_512.crop((50 * 4, 55 * 4, 75 * 4, 80 * 4))
    crop_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_gecko_hit_core_crop_8x.png"
    core_crop.save(crop_path)
    print(f"  ✓ Saved 0-QA31 core crop: {crop_path}")


if __name__ == "__main__":
    main()
