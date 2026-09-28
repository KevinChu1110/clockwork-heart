#!/usr/bin/env python3
"""
tools/build_rhino_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Heavyhorn Rhino (第三十二族 重角犀牛, rhino)
in Clockwork Heart:
  game/assets/sprites/player/poses/rhino/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/rhino/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rhino"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/rhino"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_rhino_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_rhino_crucible_crosshair_key.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_rhino_steam_furnace_exhaust.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_rhino_molten_iron_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_rhino_crucible_battering_crest.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_rhino_crucible_smith_plate.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_rhino_dual_amber_pyro_optic.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_rhino_crucible_breaker_axe.png").convert("RGBA")

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
# Rhino baseline shadow row counts: [64, 63, 62, 59, 49, 29, 0, 0, 0, 0]
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
    "head_top": (64, 10),
    "horn_tip": (66, 6),
    "horn_base": (64, 25),
    "crest_l": (44, 20),
    "crest_r": (84, 20),
    "eye_l": (52, 44),
    "eye_r": (76, 44),
    "snout": (64, 48),
    "throat": (64, 56),
    "core": (62, 68),
    "shoulder_l": (42, 64),
    "shoulder_r": (82, 64),
    "arm_l": (34, 72),
    "arm_r": (86, 72),
    "hand_r": (91, 63),
    "torso": (62, 76),
    "pelvis": (62, 90),
    "hip_l": (46, 96),
    "hip_r": (78, 96),
    "foot_l": (46, 115),
    "foot_r": (76, 115),
    "curio_vent": (45, 18),
    "curio_base": (40, 55),
    "key_mount": (82, 35),
}

# Base body without weapon and winding key (for dynamic key & weapon animation)
body_core_raw = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core_raw.alpha_composite(curio_src)
body_core_raw.alpha_composite(chassis_src)
body_core_raw.alpha_composite(head_src)
body_core_raw.alpha_composite(costume_src)
body_core_raw.alpha_composite(optic_src)

# Smoothly compress y < 35 such that y=0 maps to y=4, ensuring T>=4 while preserving ground shadow perfectly
w, h = body_core_raw.size
src_px = body_core_raw.load()
body_core = Image.new("RGBA", (w, h), (0, 0, 0, 0))
dst_px = body_core.load()
assert src_px is not None and dst_px is not None

for y in range(h):
    if y < 4:
        continue
    elif y < 35:
        src_y = (y - 4) * (35.0 / 31.0)
    else:
        src_y = float(y)
    y0 = int(src_y)
    y1 = min(h - 1, y0 + 1)
    fy = src_y - y0
    for x in range(w):
        p0 = cast(tuple[int, int, int, int], src_px[x, y0])
        p1 = cast(tuple[int, int, int, int], src_px[x, y1])
        rgba = tuple(int(round(p0[c] * (1 - fy) + p1[c] * fy)) for c in range(4))
        dst_px[x, y] = rgba


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (重角犀牛·沉穩架勢 / Crucible Poise)
    # Baseline stable poised stance from canonical composite.
    # Winding key placed at center (82, 35).
    # Breaker axe held poised at (91, 63).
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(82, 35), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(91, 63), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)

    # Ambient subtle heat glimmer
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    # Gentle steam wisps from exhaust vent (45, 14)
    i_draw.line([(45, 14), (43, 8)], fill=(255, 253, 248, 160), width=1)
    i_draw.line([(43, 8), (41, 5)], fill=(255, 160, 16, 140), width=1)
    i_draw.point((41, 5), fill=(255, 208, 40, 180))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (熔爐蓄壓·重角衝撞預備 / Furnace Pressure Charge & Horn Lowering)
    # Heavy crouch forward, horn lowers forward to battering ram line (y+6, x-2).
    # Steam exhaust overcharges with valve pressure (x-3, y+5).
    # Breaker axe draws back into full swing tension (-24 deg, x-3, y-4).
    # Crosshair key counter-winds (-32 deg, x-2, y+5).
    # FX: Battering reticle, superheated exhaust flames, aiming beam.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 6), "horn_tip": (-3, 6), "horn_base": (-2, 6),
        "crest_l": (-3, 6), "crest_r": (-1, 6),
        "eye_l": (-2, 6), "eye_r": (-2, 6),
        "snout": (-2, 6), "throat": (-2, 6),
        "core": (-2, 5),
        "shoulder_l": (-1, 5), "shoulder_r": (-3, 5),
        "arm_l": (1, 4), "arm_r": (-5, 5),
        "hand_r": (-3, 4),
        "torso": (-2, 5), "pelvis": (-2, 4),
        "hip_l": (-3, 3), "hip_r": (1, 3),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "curio_vent": (-3, 5), "curio_base": (-2, 5),
        "key_mount": (-2, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_tele = place_rotated_element(key_raw, deg=-32, target_center=(80, 40), scale=1.0)
    axe_tele = place_rotated_element(weapon_raw, deg=-24, target_center=(88, 59), scale=1.04)

    # Aiming crosshairs & superheated steam jet FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Battering ram trajectory line
    t_draw.line([(64, 52), (96, 48)], fill=(255, 160, 16, 210), width=1)
    t_draw.line([(96, 48), (120, 44)], fill=(255, 208, 40, 230), width=2)
    # Crosshair targeting reticle at forward target (112, 45)
    cx, cy = 112, 45
    t_draw.arc([cx - 7, cy - 7, cx + 7, cy + 7], start=20, end=340, fill=(255, 94, 138, 220), width=1)
    t_draw.arc([cx - 3, cy - 3, cx + 3, cy + 3], start=40, end=320, fill=(255, 208, 40, 230), width=1)
    t_draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(255, 208, 40, 240), width=1)
    # Superheated exhaust steam jet venting backwards from chimney (42, 23)
    t_draw.line([(42, 23), (32, 16)], fill=(255, 160, 16, 220), width=2)
    t_draw.line([(32, 16), (20, 11)], fill=(255, 253, 248, 190), width=1)
    t_draw.ellipse([18, 9, 24, 15], fill=(255, 208, 40, 200))
    # Heat embers
    for sx, sy in [(116, 38), (122, 50), (98, 42), (36, 12), (28, 18), (88, 54)]:
        t_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 240))
        t_draw.point((sx, sy), fill=(255, 94, 138, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, axe_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (熔爐破壞劈砍 / Crucible Breaker Axe Cleave)
    # Massive lunge forward (x+12, y-2), heavy axe cleaves downward (+35 deg, x+12, y-1).
    # Horn thrusts forward to shatter defenses.
    # Crosshair key spins rapidly (+45 deg, x+10, y-1).
    # FX: Blazing molten cleave arc, forge sparks, impact shock wave.
    # =========================================================================
    shifts_attack = {
        "head_top": (12, -2), "horn_tip": (13, -2), "horn_base": (12, -2),
        "crest_l": (11, -2), "crest_r": (13, -2),
        "eye_l": (12, -2), "eye_r": (12, -2),
        "snout": (13, -1), "throat": (12, -1),
        "core": (11, -1),
        "shoulder_l": (13, -2), "shoulder_r": (8, -1),
        "arm_l": (15, -4), "arm_r": (-5, 1),
        "hand_r": (12, -1),
        "torso": (10, -1), "pelvis": (8, 0),
        "hip_l": (9, -1), "hip_r": (-2, 0),
        "foot_l": (6, 0), "foot_r": (-3, 0),
        "curio_vent": (6, -2), "curio_base": (7, -1),
        "key_mount": (10, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=45, target_center=(92, 34), scale=1.0)
    axe_attack = place_rotated_element(weapon_raw, deg=35, target_center=(103, 62), scale=1.06)

    # Blazing molten cleave arc & forge sparks FX
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Fiery cleave crescent (kept in upper-right so it doesn't enclose lower void)
    a_draw.arc([80, 26, 122, 76], start=290, end=65, fill=(255, 94, 138, 230), width=2)
    a_draw.arc([86, 30, 120, 72], start=300, end=55, fill=(255, 208, 40, 240), width=2)
    a_draw.arc([92, 34, 118, 68], start=310, end=45, fill=(255, 255, 255, 255), width=1)
    # Forward horn thrust sonic burst
    a_draw.line([(88, 38), (116, 34)], fill=(255, 160, 16, 210), width=2)
    a_draw.line([(96, 37), (120, 33)], fill=(255, 253, 248, 255), width=1)
    # Molten anvil sparks
    for sp in [(116, 40), (122, 54), (114, 76), (108, 92), (98, 26), (104, 18), (120, 68), (112, 84)]:
        a_draw.line([(sp[0], sp[1]), (sp[0] + 3, sp[1] + 1)], fill=(255, 208, 40, 240), width=1)
        a_draw.point(sp, fill=(255, 255, 255, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.3))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, axe_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (赤焰熔爐·過載蒸汽重踏天崩 / Overdrive Furnace Stomp & Magma Slam)
    # Vertical leap & crushing slam (y+2, x+3).
    # Breaker axe slammed down into ground center (+8 deg, x-6, y+13).
    # Exhaust chimney roaring wide open, spewing double plume of superheated steam.
    # Crosshair key spun to redline (+85 deg, x+2, y-1).
    # FX: Expanding fiery magma ground shockwave, molten cracks, fiery geysers.
    # =========================================================================
    shifts_skill = {
        "head_top": (3, 2), "horn_tip": (3, 2), "horn_base": (3, 2),
        "crest_l": (2, 2), "crest_r": (4, 2),
        "eye_l": (3, 2), "eye_r": (3, 2),
        "snout": (3, 2), "throat": (3, 2),
        "core": (2, 3),
        "shoulder_l": (1, 2), "shoulder_r": (3, 2),
        "arm_l": (2, 2), "arm_r": (2, 2),
        "hand_r": (-6, 13),
        "torso": (2, 3), "pelvis": (2, 2),
        "hip_l": (1, 2), "hip_r": (3, 2),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "curio_vent": (1, -1), "curio_base": (2, 1),
        "key_mount": (2, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=85, target_center=(84, 34), scale=1.05)
    axe_skill = place_rotated_element(weapon_raw, deg=8, target_center=(85, 76), scale=1.08)

    # Fiery magma ground shockwave & exhaust eruption FX
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    # Steam chimney twin exhaust eruption plume (46, 17)
    s_draw.polygon([(46, 17), (36, 6), (56, 6)], fill=(255, 160, 16, 210))
    s_draw.polygon([(46, 17), (40, 4), (52, 4)], fill=(255, 253, 248, 230))
    # Concentric ground magma slam shockwave rings
    s_draw.ellipse([18, 108, 110, 124], outline=(255, 94, 138, 230), width=2)
    s_draw.ellipse([26, 110, 102, 122], outline=(255, 208, 40, 240), width=2)
    s_draw.ellipse([34, 112, 94, 120], outline=(255, 255, 255, 255), width=1)
    # Radial magma cracks
    s_draw.line([(64, 116), (22, 114)], fill=(255, 208, 40, 220), width=1)
    s_draw.line([(64, 116), (106, 114)], fill=(255, 208, 40, 220), width=1)
    s_draw.line([(64, 116), (36, 120)], fill=(255, 94, 138, 230), width=1)
    s_draw.line([(64, 116), (92, 120)], fill=(255, 94, 138, 230), width=1)
    # Erupting embers & lava droplets
    for ep in [(24, 102), (32, 96), (96, 98), (104, 104), (64, 100), (48, 106), (80, 106), (44, 4), (54, 5)]:
        s_draw.ellipse([ep[0] - 1, ep[1] - 1, ep[0] + 1, ep[1] + 1], fill=(255, 253, 248, 255))
        s_draw.point(ep, fill=(255, 208, 40, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.3))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, axe_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (裝甲受擊·蒸汽洩壓後仰 / Armor Impact & Steam Venting Knockback)
    # Knocked backward (x-9, y-3), horn pitches upward, heavy chassis braces.
    # Breaker axe knocked backward into defensive parry (-32 deg, x-7, y+3).
    # Crosshair key jolted backwards (-18 deg, x-6, y-2).
    # Optic eyes flicker with impact reticle shock.
    # FX: Clashing metal impact sparks, safety valve steam blowoff.
    # =========================================================================
    shifts_hit = {
        "head_top": (-8, -3), "horn_tip": (-7, -4), "horn_base": (-8, -3),
        "crest_l": (-9, -3), "crest_r": (-7, -3),
        "eye_l": (-9, -3), "eye_r": (-8, -3),
        "snout": (-9, -2), "throat": (-8, -2),
        "core": (-7, -1),
        "shoulder_l": (-6, -1), "shoulder_r": (-7, -1),
        "arm_l": (-4, 0), "arm_r": (-7, 0),
        "hand_r": (-7, 3),
        "torso": (-6, -1), "pelvis": (-5, 0),
        "hip_l": (-5, 0), "hip_r": (-4, 0),
        "foot_l": (-3, 0), "foot_r": (-2, 0),
        "curio_vent": (-5, -4), "curio_base": (-6, -2),
        "key_mount": (-6, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_hit = place_rotated_element(key_raw, deg=-18, target_center=(76, 33), scale=1.0)
    axe_hit = place_rotated_element(weapon_raw, deg=-32, target_center=(84, 66), scale=1.0)

    # Optic eyes impact flicker overlay
    hit_eyes = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    he_draw = ImageDraw.Draw(hit_eyes)
    # Impact cross bursts on amber optic eyes (adjusted for hit head shift)
    for eye_pos in [(52 - 9, 44 - 3), (76 - 8, 44 - 3)]:
        he_draw.line([(eye_pos[0] - 3, eye_pos[1]), (eye_pos[0] + 3, eye_pos[1])], fill=(255, 255, 255, 255), width=1)
        he_draw.line([(eye_pos[0], eye_pos[1] - 3), (eye_pos[0], eye_pos[1] + 3)], fill=(255, 208, 40, 240), width=1)
        he_draw.point(eye_pos, fill=(255, 94, 138, 255))

    # Armor impact spark burst & steam venting FX
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Metal impact point at front chest armor (68, 64)
    ix, iy = 68, 64
    h_draw.line([(ix - 12, iy - 6), (ix + 12, iy + 6)], fill=(255, 255, 255, 255), width=2)
    h_draw.line([(ix - 6, iy + 12), (ix + 6, iy - 12)], fill=(255, 208, 40, 240), width=2)
    h_draw.line([(ix - 10, iy), (ix + 10, iy)], fill=(255, 94, 138, 220), width=1)
    # Emergency safety valve blowoff steam jet
    h_draw.line([(40, 19), (28, 14)], fill=(255, 253, 248, 220), width=2)
    h_draw.line([(28, 14), (16, 10)], fill=(255, 253, 248, 180), width=1)
    h_draw.ellipse([14, 8, 20, 14], fill=(255, 253, 248, 190))
    # Flying metal sparks
    for pt in [(ix - 14, iy - 8), (ix + 14, iy - 8), (ix + 10, iy + 14), (ix - 8, iy + 12), (ix + 16, iy), (ix - 14, iy + 4)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_eyes)
    hit_canvas = Image.alpha_composite(hit_canvas, axe_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (重甲著地·機芯回轉咬合 / Hydraulic Damping & Crucible Reset)
    # Heavy semi-crouch landing (y+5, x-1), armor absorbs shock.
    # Breaker axe plants into ground as stabilizing anchor (-10 deg, x+2, y+5).
    # Crosshair key snaps into gear mesh (+12 deg, x+1, y+2).
    # Exhaust chimney vents smooth idle warmth.
    # FX: Landing shock ripples, gear re-mesh spark.
    # =========================================================================
    shifts_recover = {
        "head_top": (-1, 5), "horn_tip": (-1, 5), "horn_base": (-1, 5),
        "crest_l": (-2, 5), "crest_r": (0, 5),
        "eye_l": (-1, 5), "eye_r": (-1, 5),
        "snout": (-1, 5), "throat": (-1, 5),
        "core": (-1, 5),
        "shoulder_l": (-2, 4), "shoulder_r": (0, 4),
        "arm_l": (1, 3), "arm_r": (-2, 4),
        "hand_r": (2, 5),
        "torso": (-1, 5), "pelvis": (-1, 4),
        "hip_l": (-2, 3), "hip_r": (1, 3),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "curio_vent": (-1, 4), "curio_base": (-1, 3),
        "key_mount": (1, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=12, target_center=(83, 37), scale=1.0)
    axe_rec = place_rotated_element(weapon_raw, deg=-10, target_center=(93, 68), scale=1.0)

    # Hydraulic damping ripples & re-mesh spark FX
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Cooling steam wisp from chimney (44, 18)
    r_draw.line([(44, 18), (42, 11)], fill=(255, 253, 248, 180), width=1)
    r_draw.line([(42, 11), (39, 7)], fill=(255, 208, 40, 150), width=1)
    # Gear re-mesh spark at key mount (83, 37)
    r_draw.line([(80, 34), (86, 40)], fill=(255, 208, 40, 230), width=1)
    r_draw.line([(86, 34), (80, 40)], fill=(255, 255, 255, 255), width=1)
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, axe_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


# 2. Main Generation Execution
print("Generating Heavyhorn Rhino combat action poses...")
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

proof_768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_rhino_combat_poses_768.png"
proof_strip.save(proof_768_path)
print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

# 4. Generate 768x128 magenta background proof sheet for hole detection
proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
proof_magenta.paste(proof_strip, (0, 0), proof_strip)
proof_mag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_rhino_combat_poses_magenta.png"
proof_magenta.save(proof_mag_path)
print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")

print("\nAll 6 Heavyhorn Rhino combat action poses successfully generated and exported!")
