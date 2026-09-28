#!/usr/bin/env python3
"""
tools/build_stoat_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Whirling Stoat (第三十九族 旋刃伶鼬, stoat)
in Clockwork Heart:
  game/assets/sprites/player/poses/stoat/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/stoat/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
Enhanced with expressive ninja scavenger kinematics and rich mechanical articulation.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/stoat"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/stoat"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_stoat_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_stoat_whirlwind_tri_ring_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_stoat_flexible_segmented_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_stoat_ivory_tinplate_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_stoat_aerodynamic_hood_ears.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_stoat_scavenger_wind_cape.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_stoat_sapphire_crosshair_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_stoat_crescent_dagger.png").convert("RGBA")

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
    "head_top": (64, 11),
    "ears_l": (44, 18),
    "ears_r": (84, 18),
    "snout": (64, 46),
    "chin": (64, 52),
    "eye_l": (52, 40),
    "eye_r": (76, 40),
    "throat": (64, 58),
    "core": (64, 70),
    "shoulder_l": (44, 64),
    "shoulder_r": (84, 64),
    "arm_l": (38, 74),
    "arm_r": (88, 74),
    "hand_r": (98, 64),
    "torso": (64, 78),
    "pelvis": (64, 92),
    "hip_l": (48, 98),
    "hip_r": (80, 98),
    "foot_l": (48, 118),
    "foot_r": (78, 118),
    "tail_root": (46, 91),
    "tail_mid": (24, 56),
    "tail_tip": (26, 22),
    "key_mount": (84, 35),
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
    # 1. IDLE (旋刃伶鼬·荒漠拾荒架勢 / Scavenger Ninja Poise)
    # Baseline stable poised ninja stance from canonical composite.
    # Winding key placed at (84, 35).
    # Weapon placed at (102, 60) to keep R >= 4px margin.
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(84, 35), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(102, 60), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)

    # Ambient subtle sapphire lens gleam & dagger blade glimmer FX
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    # Crescent dagger curved tip glimmer at (103, 39)
    i_draw.line([(103, 36), (103, 42)], fill=(255, 253, 248, 220), width=1)
    i_draw.line([(100, 39), (106, 39)], fill=(56, 160, 255, 240), width=1)
    i_draw.point((103, 39), fill=(255, 255, 255, 255))
    # Sapphire eye lens reflection
    i_draw.point((52, 39), fill=(56, 160, 255, 230))
    i_draw.point((76, 39), fill=(56, 160, 255, 230))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (蓄勢伏地·疾風突刺預備 / Wind Scavenger Coiled Dash Windup)
    # Deep crouch: head & torso sink down and coil back (-5, +6).
    # Crescent dagger drawn back close to hip/chest in reverse tension (deg=-38, x-10, y-10).
    # Winding key counter-winds with ratchet clicks (-45 deg, x-4, y+5).
    # Flexible segmented tail coils back for spring tension.
    # FX: Sapphire targeting reticle & crosshair, golden sand tension sparks.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-5, 6), "ears_l": (-5, 6), "ears_r": (-5, 6),
        "snout": (-5, 6), "chin": (-5, 6),
        "eye_l": (-5, 6), "eye_r": (-5, 6),
        "throat": (-5, 6),
        "core": (-4, 5),
        "shoulder_l": (-5, 5), "shoulder_r": (-5, 5),
        "arm_l": (1, 5), "arm_r": (-6, 4),
        "hand_r": (-7, 4),
        "torso": (-4, 5), "pelvis": (-3, 4),
        "hip_l": (-4, 3), "hip_r": (1, 3),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_root": (-3, 3), "tail_mid": (-6, 5), "tail_tip": (-8, 6),
        "key_mount": (-4, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_tele = place_rotated_element(key_raw, deg=-45, target_center=(80, 40), scale=1.0)
    dagger_tele = place_rotated_element(weapon_raw, deg=-32, target_center=(93, 53), scale=1.03)

    # Targeting reticle & thrust trajectory FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Luminous cyan targeting trajectory line
    t_draw.line([(72, 50), (102, 58)], fill=(56, 160, 255, 210), width=1)
    t_draw.line([(102, 58), (114, 70)], fill=(255, 208, 40, 230), width=2)
    # Targeting crosshair at forward impact point (110, 72)
    cx, cy = 110, 72
    t_draw.arc([cx - 7, cy - 7, cx + 7, cy + 7], start=20, end=340, fill=(56, 160, 255, 230), width=1)
    t_draw.arc([cx - 3, cy - 3, cx + 3, cy + 3], start=40, end=320, fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx - 8, cy), (cx + 8, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 8), (cx, cy + 8)], fill=(255, 208, 40, 240), width=1)
    # Coiling sand/dust and spark particles near feet and tail
    for sx, sy in [(42, 115), (48, 114), (54, 116), (74, 115), (82, 114), (20, 28), (92, 52), (114, 42)]:
        t_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 240))
        t_draw.point((sx, sy), fill=(255, 208, 40, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, dagger_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (弧光疾閃·旋刃旋風破空斬 / Crescent Dagger Sonic Arc Slash)
    # Explosive forward ninja dash thrust (+14, +1):
    # Head & torso aggressively thrust forward, crescent dagger slashes outward (+38 deg, x-4, y+10).
    # Winding key spins forward (+60 deg, x+10, y-1).
    # Tail whips backward/upward for aerodynamic balance (-9, -4).
    # FX: Blazing sapphire-cyan & golden crescent arc slash wave, sonic shockwave rings, flying sparks.
    # =========================================================================
    shifts_attack = {
        "head_top": (14, 1), "ears_l": (13, 1), "ears_r": (15, 1),
        "snout": (15, 2), "chin": (15, 2),
        "eye_l": (14, 1), "eye_r": (14, 1),
        "throat": (14, 2),
        "core": (13, 2),
        "shoulder_l": (14, 1), "shoulder_r": (9, 2),
        "arm_l": (16, 0), "arm_r": (-2, 2),
        "hand_r": (15, 0),
        "torso": (11, 2), "pelvis": (8, 1),
        "hip_l": (8, 0), "hip_r": (-2, 0),
        "foot_l": (5, 0), "foot_r": (-3, 0),
        "tail_root": (-4, -1), "tail_mid": (-7, -3), "tail_tip": (-9, -4),
        "key_mount": (10, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_atk = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_atk = place_rotated_element(key_raw, deg=60, target_center=(94, 34), scale=1.0)
    dagger_atk = place_rotated_element(weapon_raw, deg=38, target_center=(98, 70), scale=1.05)

    # Dynamic crescent sonic arc slash FX
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Huge crescent azure-cyan and gold blade trail
    a_draw.arc([64, 18, 122, 102], start=270, end=90, fill=(56, 160, 255, 240), width=3)
    a_draw.arc([66, 20, 120, 100], start=280, end=80, fill=(255, 208, 40, 230), width=2)
    a_draw.arc([70, 24, 116, 96], start=290, end=70, fill=(255, 253, 248, 255), width=1)
    # Downward cleave impact sonic rings
    a_draw.ellipse([94, 76, 114, 92], outline=(56, 160, 255, 210), width=1)
    a_draw.ellipse([97, 79, 111, 89], outline=(255, 253, 248, 230), width=1)
    # Impact sparks & flying metallic debris
    for px, py in [(96, 68), (104, 60), (110, 50), (114, 66), (118, 78), (102, 86), (88, 83)]:
        a_draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 253, 248, 255))
        a_draw.point((px, py), fill=(255, 208, 40, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.3))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, dagger_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. RECOVER (旋影卸力·落地回架 / Shadow Drift Brake & Re-poise)
    # Hydraulic recoil: knees flexed, body lowered and braced (-4, +6).
    # Crescent dagger held low in defensive reverse parry guard (deg=18, x-5, y+8).
    # Winding key rebounds with spring damping (+18 deg, x-3, y+4).
    # Tail spreads low behind for balance.
    # FX: Soft hydraulic steam exhaust puffs, ground friction/dust skid lines, cooling sapphire optic glow.
    # =========================================================================
    shifts_recover = {
        "head_top": (-4, 6), "ears_l": (-4, 6), "ears_r": (-4, 6),
        "snout": (-4, 6), "chin": (-4, 6),
        "eye_l": (-4, 6), "eye_r": (-4, 6),
        "throat": (-4, 6),
        "core": (-4, 5),
        "shoulder_l": (-4, 5), "shoulder_r": (-4, 5),
        "arm_l": (-4, 5), "arm_r": (-4, 5),
        "hand_r": (-4, 5),
        "torso": (-3, 4), "pelvis": (-3, 3),
        "hip_l": (-3, 2), "hip_r": (-2, 2),
        "foot_l": (-1, 0), "foot_r": (0, 0),
        "tail_root": (-2, 3), "tail_mid": (-3, 4), "tail_tip": (-3, 3),
        "key_mount": (-3, 4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_rec = place_rotated_element(key_raw, deg=18, target_center=(81, 39), scale=1.0)
    dagger_rec = place_rotated_element(weapon_raw, deg=18, target_center=(97, 68), scale=1.0)

    # Steam venting & soft ground dust dissipation FX
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Steam exhaust puffs from back chassis & shoulder vents
    for (cx, cy, rad) in [(76, 52, 4), (82, 46, 5), (88, 40, 5), (38, 56, 4), (32, 50, 4)]:
        r_draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(255, 253, 248, 110), outline=(220, 235, 255, 160), width=1)
    # Soft rounded dust cloud puffs near ground contact (replaces ruler lines)
    for (dx, dy, rx, ry) in [(44, 116, 6, 3), (78, 116, 7, 3), (36, 115, 4, 2), (86, 115, 5, 2)]:
        r_draw.ellipse([dx - rx, dy - ry, dx + rx, dy + ry], fill=(255, 245, 220, 100), outline=(230, 210, 170, 140), width=1)
    # Dissipating spark specks
    for px, py in [(80, 48), (86, 42), (40, 54), (74, 114), (48, 114)]:
        r_draw.point((px, py), fill=(255, 208, 40, 200))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.4))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, dagger_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    # =========================================================================
    # 5. SKILL (旋風忍殺·超速迴旋裂空斬 / Whirlwind Ninja Overdrive Cyclone Cleave)
    # Massive torque & airborne leap: body lifts upward (+5, -7).
    # Crescent dagger in horizontal rotary spin (deg=-65, x-5, y-14).
    # Winding key spins +110 deg at high-speed overdrive.
    # Tail flares out in dynamic spiral (-8, -4).
    # FX: Overdrive cyclone gear energy rings, brilliant sapphire-gold starbursts, rotational speedlines.
    # =========================================================================
    shifts_skill = {
        "head_top": (5, -7), "ears_l": (4, -7), "ears_r": (6, -7),
        "snout": (5, -6), "chin": (5, -6),
        "eye_l": (5, -7), "eye_r": (5, -7),
        "throat": (5, -6),
        "core": (4, -5),
        "shoulder_l": (5, -5), "shoulder_r": (1, -5),
        "arm_l": (6, -5), "arm_r": (-3, -4),
        "hand_r": (5, -5),
        "torso": (4, -4), "pelvis": (3, -3),
        "hip_l": (3, -2), "hip_r": (0, -2),
        "foot_l": (2, -1), "foot_r": (-1, -1),
        "tail_root": (-4, -3), "tail_mid": (-7, -4), "tail_tip": (-9, -4),
        "key_mount": (4, -6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_skill = place_rotated_element(key_raw, deg=110, target_center=(88, 28), scale=1.06)
    dagger_skill = place_rotated_element(weapon_raw, deg=-65, target_center=(97, 46), scale=1.06)

    # Overdrive rotary clockwork & spark blast FX
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    k_draw = ImageDraw.Draw(skill_fx)
    # Double gear-teeth energy ring around chest core (68, 65)
    ox, oy = 68, 65
    k_draw.arc([ox - 22, oy - 22, ox + 22, oy + 22], start=0, end=360, fill=(56, 160, 255, 230), width=2)
    k_draw.arc([ox - 16, oy - 16, ox + 16, oy + 16], start=0, end=360, fill=(255, 208, 40, 230), width=1)
    k_draw.arc([ox - 10, oy - 10, ox + 10, oy + 10], start=0, end=360, fill=(255, 253, 248, 250), width=1)
    # Radiating gear rays
    for angle_deg in range(0, 360, 45):
        rad = math.radians(angle_deg)
        x1 = ox + int(round(18 * math.cos(rad)))
        y1 = oy + int(round(18 * math.sin(rad)))
        x2 = ox + int(round(26 * math.cos(rad)))
        y2 = oy + int(round(26 * math.sin(rad)))
        k_draw.line([(x1, y1), (x2, y2)], fill=(56, 160, 255, 240), width=2)
    # Whirling blade circular arc
    k_draw.arc([50, 18, 122, 88], start=210, end=40, fill=(255, 253, 248, 240), width=2)
    k_draw.arc([48, 16, 124, 91], start=220, end=30, fill=(255, 208, 40, 220), width=1)
    # Exploding multi-colored toy starburst particles
    for px, py, col in [
        (46, 28, (56, 160, 255)), (84, 18, (255, 253, 248)), (112, 34, (255, 94, 138)),
        (116, 58, (56, 160, 255)), (106, 78, (255, 208, 40)), (40, 58, (255, 160, 16)),
        (54, 83, (255, 253, 248)), (68, 14, (255, 208, 40))
    ]:
        k_draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col + (240,))
        k_draw.point((px, py), fill=(255, 255, 255, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.3))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, dagger_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 6. HIT (受擊震退·裝甲金屬板件火花 / Kinetic Impact & Plating Sparks)
    # Violent backward recoil: head thrown far back (-15, -4), torso arched back (-11, -2).
    # Crescent dagger jarred back and tilted (deg=-42, x-18, y-10).
    # Winding key knocked counter-clockwise (-32 deg, x-15, y-4).
    # Tail curls forward for counter-balance (+4, +2).
    # Ground shadow strictly anchored (Rule 4b-5).
    # FX: Piercing impact starburst at chest armor, brass fracture shockwave, flying sparks.
    # =========================================================================
    shifts_hit = {
        "head_top": (-15, -4), "ears_l": (-15, -4), "ears_r": (-15, -4),
        "snout": (-14, -3), "chin": (-14, -3),
        "eye_l": (-15, -4), "eye_r": (-15, -4),
        "throat": (-14, -3),
        "core": (-11, -2),
        "shoulder_l": (-12, -3), "shoulder_r": (-9, -2),
        "arm_l": (-11, -3), "arm_r": (-13, -2),
        "hand_r": (-13, -2),
        "torso": (-10, -2), "pelvis": (-7, -1),
        "hip_l": (-6, 0), "hip_r": (-4, 0),
        "foot_l": (-2, 0), "foot_r": (0, 0),
        "tail_root": (2, 1), "tail_mid": (4, 2), "tail_tip": (5, 2),
        "key_mount": (-15, -4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=3.5)
    key_hit = place_rotated_element(key_raw, deg=-32, target_center=(69, 31), scale=1.0)
    dagger_hit = place_rotated_element(weapon_raw, deg=-42, target_center=(84, 50), scale=1.02)

    # Kinetic impact flash & plating spark FX
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Violent white-cyan impact epicenter at chest armor (66, 64)
    hx, hy = 66, 64
    # 4-pointed sharp impact diamond
    h_draw.polygon([(hx, hy - 14), (hx + 4, hy - 2), (hx + 16, hy), (hx + 4, hy + 2),
                    (hx, hy + 14), (hx - 4, hy + 2), (hx - 16, hy), (hx - 4, hy - 2)],
                   fill=(255, 253, 248, 255))
    h_draw.polygon([(hx, hy - 8), (hx + 2, hy - 1), (hx + 9, hy), (hx + 2, hy + 1),
                    (hx, hy + 8), (hx - 2, hy + 1), (hx - 9, hy), (hx - 2, hy - 1)],
                   fill=(56, 160, 255, 240))
    # Shockwave ripples
    h_draw.ellipse([hx - 11, hy - 11, hx + 11, hy + 11], outline=(255, 208, 40, 230), width=1)
    h_draw.ellipse([hx - 16, hy - 16, hx + 16, hy + 16], outline=(56, 160, 255, 210), width=1)
    # Scattered sparks flying outward
    for sx, sy in [
        (hx + 12, hy - 14), (hx + 18, hy - 6), (hx + 16, hy + 12),
        (hx - 14, hy - 16), (hx - 20, hy + 4), (hx - 12, hy + 16),
        (hx + 8, hy - 20), (hx - 8, hy - 18)
    ]:
        h_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 255))
        h_draw.point((sx, sy), fill=(255, 208, 40, 255))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.3))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, dagger_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    return poses


def main():
    print("Building 6 combat action poses for The Whirling Stoat (第三十九族 旋刃伶鼬)...")
    poses = generate_poses()

    for name, img in poses.items():
        # 1. Save 128x128
        out_path = f"{OUT_DIR}/{name}.png"
        img.save(out_path)
        bbox = img.getbbox()
        print(f"✓ Saved {name:10s} (128x128) -> {out_path} (bbox={bbox})")

        # 2. Save 512x512 with LANCZOS resampling (forbidden NEAREST)
        out_512 = f"{OUT_DIR}/{name}_512.png"
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        img_512.save(out_512)
        print(f"✓ Saved {name:10s}_512 (512x512 LANCZOS) -> {out_512}")

    # 3. Create proof sheet (768x128 Transparent)
    proof_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    pose_order = ["idle", "telegraph", "attack", "recover", "skill", "hit"]
    for i, p in enumerate(pose_order):
        proof_768.paste(poses[p], (i * 128, 0), poses[p])
    proof_path_768 = f"{REPO_ROOT}/game/assets/sprites/player/proof_stoat_combat_poses_768.png"
    proof_768.save(proof_path_768)
    print(f"✓ Saved composite proof sheet -> {proof_path_768}")

    # 4. Create magenta proof sheet (768x128 Magenta #FF00FF)
    proof_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p in enumerate(pose_order):
        proof_mag.paste(poses[p], (i * 128, 0), poses[p])
    proof_path_mag = f"{REPO_ROOT}/game/assets/sprites/player/proof_stoat_combat_poses_magenta.png"
    proof_mag.save(proof_path_mag)
    print(f"✓ Saved magenta proof sheet -> {proof_path_mag}")

    print("\n🎉 ALL 6 COMBAT POSES & PROOFS BUILT SUCCESSFULLY FOR STOAT!")


if __name__ == "__main__":
    main()
