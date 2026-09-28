#!/usr/bin/env python3
"""
tools/build_peacock_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Prism Peacock (第三十五族 稜鏡孔雀, peacock)
in Clockwork Heart:
  game/assets/sprites/player/poses/peacock/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/peacock/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/peacock"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/peacock"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_peacock_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_peacock_filigree_sunburst_key.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_peacock_articulated_kaleidoscope_fan.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_peacock_glazed_porcelain_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_peacock_baroque_diadem_prism.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_peacock_marionette_court_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_peacock_kaleidoscope_gem_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_peacock_kaleidoscope_prism_focus.png").convert("RGBA")

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
# Peacock baseline shadow row counts: [57, 57, 55, 51, 43, 27, 0, 0, 0, 0]
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

# Base body composite (curio + chassis + head + costume + optic)
body_core_raw = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core_raw.alpha_composite(curio_src)
body_core_raw.alpha_composite(chassis_src)
body_core_raw.alpha_composite(head_src)
body_core_raw.alpha_composite(costume_src)
body_core_raw.alpha_composite(optic_src)

# Smoothly compress y < 45 so y=0 maps to y=4, ensuring T>=4 while preserving ground shadow perfectly
w, h = body_core_raw.size
src_px = body_core_raw.load()
body_core = Image.new("RGBA", (w, h), (0, 0, 0, 0))
dst_px = body_core.load()
assert src_px is not None and dst_px is not None

for y in range(h):
    if y < 4:
        continue
    elif y < 45:
        src_y = (y - 4) * (45.0 / 41.0)
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

base_landmarks = {
    "head_top": (64, 5),
    "crown_l": (50, 7),
    "crown_r": (78, 7),
    "crown_base": (64, 28),
    "eye_l": (53, 39),
    "eye_r": (75, 39),
    "beak": (64, 45),
    "throat": (64, 54),
    "core": (64, 65),
    "shoulder_l": (45, 62),
    "shoulder_r": (83, 62),
    "arm_l": (38, 72),
    "arm_r": (88, 72),
    "hand_r": (96, 70),
    "torso": (64, 75),
    "pelvis": (64, 88),
    "hip_l": (50, 97),
    "hip_r": (78, 97),
    "foot_l": (48, 118),
    "foot_r": (78, 118),
    "fan_l": (24, 38),
    "fan_r": (104, 38),
    "fan_top": (64, 18),
    "key_mount": (76, 34),
}


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (稜鏡孔雀待機 / The Prism Peacock Poise)
    # Elegant poised ballet stance, feet grounded gently, crystal fan open behind in balanced poise,
    # prism focus hovering in right hand (deg=0, center=(102, 68)), sunburst winding key poised at center (77, 34).
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(77, 34), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(102, 68), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (光學校準·蓄能蓄力 / Prism Calibration & Beam Gathering)
    # Mage preparation stance: body crouches slightly and gathers power (y+4, x-2),
    # torso coils back, head and crown tilt focused, left arm raises in ritual mudra posture.
    # Prism focus pulled back closer to torso to focus optical energy (scale=1.05, deg=-22, center=(94, 63)).
    # Sunburst winding key counter-rotates under tension (deg=-30, center=(74, 38)).
    # Kaleidoscope crystal fan spreads wide and tenses backwards.
    # Optical FX: Concentric prism reticle / laser calibration lines and glowing gathering particles.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 4), "crown_l": (-3, 4), "crown_r": (-1, 4), "crown_base": (-2, 4),
        "eye_l": (-2, 4), "eye_r": (-2, 4),
        "beak": (-2, 4), "throat": (-2, 4),
        "core": (-2, 4),
        "shoulder_l": (-1, 3), "shoulder_r": (-3, 3),
        "arm_l": (1, 3), "arm_r": (-5, 3),
        "hand_r": (-6, 1),
        "torso": (-2, 4), "pelvis": (-2, 3),
        "hip_l": (-4, 2), "hip_r": (1, 2),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "fan_l": (-4, 3), "fan_r": (0, 3), "fan_top": (-2, 3),
        "key_mount": (-2, 4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tel = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_tel = place_rotated_element(key_raw, deg=-30, target_center=(74, 38), scale=1.0)
    wpn_tel = place_rotated_element(weapon_raw, deg=-22, target_center=(94, 63), scale=1.05)

    # Optical Telegraph FX: Concentric prism reticle & gathering energy rings
    tel_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tel_fx)
    cx, cy = 94, 63
    # Concentric targeting circles in Prism Sky (#38A0FF) and Kaleidoscope Mint (#4ED86A)
    t_draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], outline=(56, 160, 255, 180), width=1)
    t_draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=(78, 216, 106, 140), width=1)
    # Crosshair targeting notches
    t_draw.line([(cx - 28, cy), (cx - 18, cy)], fill=(255, 208, 40, 220), width=1)
    t_draw.line([(cx + 18, cy), (cx + 28, cy)], fill=(255, 208, 40, 220), width=1)
    t_draw.line([(cx, cy - 28), (cx, cy - 18)], fill=(255, 208, 40, 220), width=1)
    t_draw.line([(cx, cy + 18), (cx, cy + 28)], fill=(255, 208, 40, 220), width=1)
    # Gathering photons / sparks
    for pt in [(cx - 12, cy - 14), (cx + 14, cy - 12), (cx - 15, cy + 10), (cx + 11, cy + 13)]:
        t_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 255, 255, 230))
    tel_fx = tel_fx.filter(ImageFilter.GaussianBlur(0.3))

    tel_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tel_canvas = Image.alpha_composite(tel_canvas, key_tel)
    tel_canvas = Image.alpha_composite(tel_canvas, warped_tel)
    tel_canvas = Image.alpha_composite(tel_canvas, wpn_tel)
    tel_canvas = Image.alpha_composite(tel_canvas, tel_fx)
    poses["telegraph"] = enforce_ground_shadow(tel_canvas)

    # =========================================================================
    # 3. ATTACK (折光散射·晶矢迸射 / Refraction Lance & Prism Scatter)
    # Dynamic ballet lunge / optical cast attack: body leaps gracefully forward (x+5, y-2),
    # right leg lunges forward, left ballet foot sweeps back, chest expands.
    # Prism focus thrusts forward powerfully (scale=1.1, deg=28, center=(110, 62)),
    # projecting a brilliant multi-color crystal refraction beam / prism light lance.
    # Sunburst winding key spins rapidly (+48 deg, center=(81, 31)).
    # Kaleidoscope crystal fan flares forward in kinetic projection.
    # =========================================================================
    shifts_attack = {
        "head_top": (5, -1), "crown_l": (4, -1), "crown_r": (6, -1), "crown_base": (5, -1),
        "eye_l": (5, -1), "eye_r": (5, -1),
        "beak": (6, -1), "throat": (5, -1),
        "core": (5, -1),
        "shoulder_l": (3, -1), "shoulder_r": (6, -1),
        "arm_l": (1, 1), "arm_r": (8, -2),
        "hand_r": (10, -3),
        "torso": (4, -1), "pelvis": (3, 0),
        "hip_l": (1, 0), "hip_r": (5, 0),
        "foot_l": (-2, 0), "foot_r": (4, 0),
        "fan_l": (2, -1), "fan_r": (6, -1), "fan_top": (4, -1),
        "key_mount": (5, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_atk = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_atk = place_rotated_element(key_raw, deg=48, target_center=(81, 31), scale=1.0)
    wpn_atk = place_rotated_element(weapon_raw, deg=28, target_center=(107, 62), scale=1.05)

    # Attack Optical FX: Prism lance beam and refracting crystal particles
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Refraction lance beam extending from prism focus (107, 62)
    lx, ly = 107, 62
    # Tri-color prism laser rays (cyan, mint, gold, ruby) - keep within x <= 116 for natural fade
    a_draw.line([(lx - 4, ly), (116, ly - 4)], fill=(56, 160, 255, 230), width=2)
    a_draw.line([(lx - 4, ly + 1), (116, ly)], fill=(255, 255, 255, 255), width=2)
    a_draw.line([(lx - 4, ly + 2), (116, ly + 4)], fill=(78, 216, 106, 230), width=2)
    a_draw.line([(lx - 8, ly - 3), (115, ly - 8)], fill=(255, 208, 40, 180), width=1)
    a_draw.line([(lx - 8, ly + 5), (115, ly + 8)], fill=(230, 57, 70, 180), width=1)
    # Diamond crystal light sparks
    for pt in [(112, 52), (115, 58), (113, 68), (116, 62)]:
        a_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 255, 255, 240))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.3))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, wpn_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (奧義·萬花聖境光界 / Ultimate: Kaleidoscope Domain Burst)
    # Grand ultimate mage stance: character rises on tip-toes in full ballet elevation (y-3),
    # arms wide, baroque crown and chest glowing with brilliant light.
    # Kaleidoscope crystal fan expands to maximum magnificent aperture.
    # Prism focus elevated high overhead (scale=1.15, deg=-15, center=(98, 48)).
    # Sunburst winding key spins at maximum velocity (+75 deg, center=(76, 29)).
    # Optical FX: Geometric kaleidoscope prism grid, multi-wavelength refraction rings.
    # =========================================================================
    shifts_skill = {
        "head_top": (0, -2), "crown_l": (-2, -2), "crown_r": (2, -2), "crown_base": (0, -2),
        "eye_l": (-1, -2), "eye_r": (1, -2),
        "beak": (0, -2), "throat": (0, -2),
        "core": (0, -2),
        "shoulder_l": (-3, -3), "shoulder_r": (3, -3),
        "arm_l": (-4, -4), "arm_r": (4, -4),
        "hand_r": (4, -8),
        "torso": (0, -2), "pelvis": (0, -1),
        "hip_l": (-2, -1), "hip_r": (2, -1),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "fan_l": (-5, -4), "fan_r": (5, -4), "fan_top": (0, -4),
        "key_mount": (0, -3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skl = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skl = place_rotated_element(key_raw, deg=75, target_center=(76, 29), scale=1.05)
    wpn_skl = place_rotated_element(weapon_raw, deg=-15, target_center=(98, 48), scale=1.15)

    # Skill FX: Kaleidoscope geometric star domain & rainbow optical halo
    skl_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skl_fx)
    sx, sy = 98, 48
    # Multi-wavelength prism refraction rings
    s_draw.ellipse([sx - 20, sy - 20, sx + 20, sy + 20], outline=(56, 160, 255, 200), width=1)
    s_draw.ellipse([sx - 14, sy - 14, sx + 14, sy + 14], outline=(78, 216, 106, 220), width=1)
    s_draw.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], outline=(255, 208, 40, 240), width=1)
    # Hexagonal kaleidoscope symmetry lines
    angles = [0, 60, 120, 180, 240, 300]
    for ang in angles:
        rad = math.radians(ang)
        x1 = sx + int(round(10 * math.cos(rad)))
        y1 = sy + int(round(10 * math.sin(rad)))
        x2 = sx + int(round(24 * math.cos(rad)))
        y2 = sy + int(round(24 * math.sin(rad)))
        s_draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 220), width=1)
    # Surrounding brilliant diamond crystal sparkles
    sparkle_pts = [
        (sx - 18, sy - 18), (sx + 18, sy - 18), (sx - 22, sy + 14), (sx + 20, sy + 16),
        (56, 32), (72, 32), (64, 48), (44, 58)
    ]
    for sp in sparkle_pts:
        s_draw.ellipse([sp[0] - 1, sp[1] - 1, sp[0] + 1, sp[1] + 1], fill=(255, 255, 255, 240))
    skl_fx = skl_fx.filter(ImageFilter.GaussianBlur(0.3))

    skl_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skl_canvas = Image.alpha_composite(skl_canvas, key_skl)
    skl_canvas = Image.alpha_composite(skl_canvas, warped_skl)
    skl_canvas = Image.alpha_composite(skl_canvas, wpn_skl)
    skl_canvas = Image.alpha_composite(skl_canvas, skl_fx)
    poses["skill"] = enforce_ground_shadow(skl_canvas)

    # =========================================================================
    # 5. HIT (受擊震顫·鏡面偏折 / Optical Impact & Lattice Strain)
    # Hit stagger stance: body knocked backward and upward (x-8, y-1), head tilts back in recoil (-9, -2).
    # Optic eyes switch to cute dizzy/strain expression: porcelain eye lenses show strained '> <' facets!
    # Prism focus knocked adrift with wobbling angle (deg=32, center=(88, 76)).
    # Sunburst winding key slips back against ratchet tension (deg=-36, center=(68, 33)).
    # Optical FX: Impact flash, shattered crystal shard particles deflecting away.
    # =========================================================================
    shifts_hit = {
        "head_top": (-9, -1), "crown_l": (-10, -1), "crown_r": (-8, -1), "crown_base": (-9, -1),
        "eye_l": (-9, -1), "eye_r": (-9, -1),
        "beak": (-9, -1), "throat": (-8, -1),
        "core": (-7, 0),
        "shoulder_l": (-9, -1), "shoulder_r": (-6, -1),
        "arm_l": (-5, 2), "arm_r": (-8, 1),
        "hand_r": (-8, 5),
        "torso": (-7, 0), "pelvis": (-5, 0),
        "hip_l": (-5, 0), "hip_r": (-2, 0),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "fan_l": (-6, 0), "fan_r": (-2, 0), "fan_top": (-7, -1),
        "key_mount": (-7, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Overlay cute dizzy strain '> <' LEDs on optic eyes:
    # Left eye base: (53, 39), shifted: (53 - 9, 39 - 1) = (44, 38)
    # Right eye base: (75, 39), shifted: (75 - 9, 39 - 1) = (66, 38)
    hit_eyes = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    he_draw = ImageDraw.Draw(hit_eyes)
    # Left eye strain '>'
    lx, ly = 44, 38
    he_draw.line([(lx - 3, ly - 3), (lx + 2, ly)], fill=(56, 160, 255, 255), width=2)
    he_draw.line([(lx - 3, ly + 3), (lx + 2, ly)], fill=(56, 160, 255, 255), width=2)
    he_draw.line([(lx - 2, ly - 2), (lx + 1, ly)], fill=(255, 255, 255, 255), width=1)
    # Right eye strain '<'
    rx, ry = 66, 38
    he_draw.line([(rx + 3, ly - 3), (rx - 2, ly)], fill=(78, 216, 106, 255), width=2)
    he_draw.line([(rx + 3, ly + 3), (rx - 2, ly)], fill=(78, 216, 106, 255), width=2)
    he_draw.line([(rx + 2, ly - 2), (rx - 1, ly)], fill=(255, 255, 255, 255), width=1)

    key_hit = place_rotated_element(key_raw, deg=-36, target_center=(68, 33), scale=1.0)
    wpn_hit = place_rotated_element(weapon_raw, deg=32, target_center=(88, 76), scale=1.0)

    # Impact spark burst and kinetic deflection lines
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact point at court cuirass (57, 65)
    ix, iy = 57, 65
    h_draw.line([(ix - 12, iy - 8), (ix + 10, iy + 6)], fill=(255, 208, 40, 240), width=2)
    h_draw.line([(ix - 8, iy + 10), (ix + 8, iy - 8)], fill=(230, 57, 70, 230), width=2)
    h_draw.line([(ix - 14, iy), (ix + 12, iy)], fill=(255, 255, 255, 255), width=1)
    # Shattered prism crystal sparks
    for pt in [(ix - 14, iy - 10), (ix + 12, iy - 12), (ix + 14, iy + 8), (ix - 10, iy + 12), (ix + 18, iy - 2)]:
        h_draw.point(pt, fill=(56, 160, 255, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 255, 255, 230))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_eyes)
    hit_canvas = Image.alpha_composite(hit_canvas, wpn_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (芭蕾旋轉·光羽歸位 / Ballet Pirouette & Optical Reset)
    # Low ballet landing recovery (y+4, x-1), character bows courtly forward,
    # prism focus braces in protective recovery arc (scale=0.98, deg=-10, center=(99, 74)).
    # Sunburst winding key snaps smoothly into gear mesh (+18 deg, center=(78, 37)).
    # Kaleidoscope crystal fan folds gently back toward resting geometry.
    # =========================================================================
    shifts_recover = {
        "head_top": (-1, 4), "crown_l": (-2, 4), "crown_r": (0, 4), "crown_base": (-1, 4),
        "eye_l": (-1, 4), "eye_r": (-1, 4),
        "beak": (-1, 4), "throat": (-1, 4),
        "core": (-1, 4),
        "shoulder_l": (-2, 3), "shoulder_r": (0, 3),
        "arm_l": (1, 3), "arm_r": (-2, 3),
        "hand_r": (-1, 4),
        "torso": (-1, 4), "pelvis": (-1, 3),
        "hip_l": (-3, 2), "hip_r": (2, 2),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "fan_l": (-2, 3), "fan_r": (0, 3), "fan_top": (-1, 3),
        "key_mount": (-1, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=18, target_center=(78, 37), scale=1.0)
    wpn_rec = place_rotated_element(weapon_raw, deg=-10, target_center=(99, 74), scale=0.98)

    # Gravitational dissipation arcs & landing ripples
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Gear re-mesh spark at key mount
    r_draw.line([(75, 34), (81, 40)], fill=(255, 208, 40, 230), width=1)
    r_draw.line([(81, 34), (75, 40)], fill=(255, 255, 255, 255), width=1)
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, wpn_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


# 2. Main Generation Execution
print("Generating The Prism Peacock combat action poses...")
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

proof_768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_peacock_combat_poses_768.png"
proof_strip.save(proof_768_path)
print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

# 4. Generate 768x128 magenta background proof sheet for hole detection
proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
proof_magenta.paste(proof_strip, (0, 0), proof_strip)
proof_mag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_peacock_combat_poses_magenta.png"
proof_magenta.save(proof_mag_path)
print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")
