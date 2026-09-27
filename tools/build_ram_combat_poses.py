#!/usr/bin/env python3
"""
tools/build_ram_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Astral Ram (第二十九族 星盤靈羊, ram)
in Clockwork Heart:
  game/assets/sprites/player/poses/ram/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/ram/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/ram"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/ram"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_ram_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_ram_astrolabe_tri_star.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_ram_gravity_orbit_rings.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_ram_astral_polymer_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_ram_spiral_balance_horns.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_ram_gravity_starlight_robe.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_ram_starlight_amber_optic.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_ram_astral_spiral_staff.png").convert("RGBA")

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
    "head_top": (64, 20),
    "horn_tip_l": (20, 36),
    "horn_tip_r": (108, 36),
    "horn_spiral_l": (30, 42),
    "horn_spiral_r": (98, 42),
    "ear_l": (36, 44),
    "ear_r": (92, 44),
    "eye_l": (54, 42),
    "eye_r": (74, 42),
    "snout": (64, 48),
    "throat": (64, 54),
    "core": (64, 62),
    "shoulder_l": (46, 62),
    "shoulder_r": (82, 62),
    "arm_l": (38, 72),
    "arm_r": (90, 72),
    "torso": (64, 76),
    "pelvis": (64, 88),
    "hip_l": (50, 96),
    "hip_r": (78, 96),
    "foot_l": (50, 116),
    "foot_r": (76, 116),
    "curio_mount": (64, 60),
    "key_mount": (86, 34),
    "staff_hand": (92, 54),
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
    # 1. IDLE (星階巡禮法師待機 / Astral Pilgrim Stance)
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (出招蓄勁 / 天體引力充能 Astrolabe Calibration & Tension Coil)
    # Body crouches (y+6, x-2), key counter-rotates (-26 deg),
    # staff recoils slightly (-16 deg, x-5, y+2).
    # Orbit rings compress slightly, astral calibration reticle in mint (#4ED86A) and amber (#FFD028).
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 6), "horn_tip_l": (-3, 5), "horn_tip_r": (-1, 5),
        "horn_spiral_l": (-3, 6), "horn_spiral_r": (-1, 6),
        "ear_l": (-3, 6), "ear_r": (-1, 6),
        "eye_l": (-2, 6), "eye_r": (-2, 6),
        "snout": (-2, 6), "throat": (-2, 6),
        "core": (-2, 6),
        "shoulder_l": (-3, 5), "shoulder_r": (-2, 5),
        "arm_l": (-1, 5), "arm_r": (-5, 4),
        "torso": (-2, 6), "pelvis": (-2, 5),
        "hip_l": (-4, 4), "hip_r": (1, 4),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "curio_mount": (-2, 5), "key_mount": (-2, 5), "staff_hand": (-5, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_tele = place_rotated_element(key_raw, deg=-26, target_center=(84, 39), scale=1.0)
    staff_tele = place_rotated_element(weapon_raw, deg=-16, target_center=(87, 56), scale=1.02)

    # Calibration reticle and astral flux FX (open arcs, not closed loops)
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Starlight trajectory lines
    t_draw.line([(88, 48), (116, 42)], fill=(255, 208, 40, 220), width=1)
    t_draw.line([(94, 46), (118, 40)], fill=(78, 216, 106, 230), width=2)
    t_draw.line([(100, 44), (120, 39)], fill=(255, 255, 255, 255), width=1)
    # Calibration reticle crosshair around target focus point (106, 40)
    cx, cy = 106, 40
    t_draw.arc([cx - 8, cy - 8, cx + 8, cy + 8], start=30, end=330, fill=(78, 216, 106, 220), width=1)
    t_draw.arc([cx - 4, cy - 4, cx + 4, cy + 4], start=45, end=315, fill=(255, 208, 40, 230), width=1)
    t_draw.line([(cx - 11, cy), (cx + 11, cy)], fill=(78, 216, 106, 240), width=1)
    t_draw.line([(cx, cy - 11), (cx, cy + 11)], fill=(78, 216, 106, 240), width=1)
    # Balance spring tension arcs around horns & key
    t_draw.arc([74, 22, 102, 50], start=180, end=350, fill=(255, 208, 40, 220), width=2)
    t_draw.arc([78, 26, 98, 46], start=200, end=330, fill=(56, 160, 255, 200), width=1)
    # Micro starlight flux particles
    for sx, sy in [(114, 32), (118, 48), (100, 28), (92, 22)]:
        t_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 240))
        t_draw.point((sx, sy), fill=(255, 208, 40, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, staff_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (普攻出手 / 星軌引力脈衝轟擊 Astral Orbital Pulse Burst)
    # Forward leap & thrust (+11, -1), right staff swings forward violently (+28 deg, x+14, y-3)!
    # Astrolabe key spins rapidly forward (+38 deg).
    # Sonic/astral orbital beam cone with starlight sparks and concentric gravity wave arcs.
    # =========================================================================
    shifts_attack = {
        "head_top": (11, -1), "horn_tip_l": (9, -2), "horn_tip_r": (12, -1),
        "horn_spiral_l": (10, -1), "horn_spiral_r": (12, -1),
        "ear_l": (10, -1), "ear_r": (12, -1),
        "eye_l": (11, -1), "eye_r": (11, -1),
        "snout": (12, 0), "throat": (11, 0),
        "core": (10, 0),
        "shoulder_l": (11, 0), "shoulder_r": (6, 0),
        "arm_l": (12, -1), "arm_r": (14, -3),
        "torso": (9, 0), "pelvis": (7, 0),
        "hip_l": (8, -1), "hip_r": (-4, 0),
        "foot_l": (5, 0), "foot_r": (-5, 0),
        "curio_mount": (7, 0), "key_mount": (8, 0), "staff_hand": (14, -3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=38, target_center=(94, 34), scale=1.0)
    staff_attack = place_rotated_element(weapon_raw, deg=28, target_center=(106, 51), scale=1.06)

    # Explosive astral pulse blast cone and starlight rings
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Starlight thrust beam
    a_draw.line([(88, 52), (122, 48)], fill=(56, 160, 255, 245), width=2)
    a_draw.line([(96, 51), (122, 47)], fill=(255, 255, 255, 255), width=1)
    # Concentric orbital shockwave arcs
    a_draw.arc([80, 26, 122, 74], start=290, end=70, fill=(255, 94, 138, 230), width=2)
    a_draw.arc([86, 30, 120, 70], start=300, end=60, fill=(255, 208, 40, 240), width=2)
    a_draw.arc([92, 34, 118, 66], start=310, end=50, fill=(78, 216, 106, 255), width=1)
    # Astral stardust sparks
    for pt in [(116, 32), (122, 44), (120, 62), (114, 72), (106, 26), (98, 22)]:
        a_draw.point(pt, fill=(255, 208, 40, 255))
        a_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 253, 248, 220))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, staff_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (怒氣大招 / 天穹星盤超載共鳴 Celestial Resonance Overdrive)
    # Airborne levitation (y-9, x+1), staff aimed directly skyward (-48 deg, x+6, y-11),
    # astrolabe tri-star key in extreme overdrive (+82 deg).
    # Open celestial orbital arcs and radial starlight rays (avoiding closed hollow loops).
    # =========================================================================
    shifts_skill = {
        "head_top": (1, -9), "horn_tip_l": (-2, -10), "horn_tip_r": (4, -9),
        "horn_spiral_l": (-1, -9), "horn_spiral_r": (3, -9),
        "ear_l": (-1, -9), "ear_r": (3, -9),
        "eye_l": (1, -9), "eye_r": (1, -9),
        "snout": (1, -8), "throat": (1, -8),
        "core": (1, -8),
        "shoulder_l": (-2, -8), "shoulder_r": (4, -8),
        "arm_l": (-5, -6), "arm_r": (6, -11),
        "torso": (1, -8), "pelvis": (1, -7),
        "hip_l": (-3, -6), "hip_r": (4, -6),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "curio_mount": (1, -8), "key_mount": (2, -8), "staff_hand": (6, -11),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=82, target_center=(88, 26), scale=1.0)
    staff_skill = place_rotated_element(weapon_raw, deg=-48, target_center=(98, 43), scale=1.08)

    # Celestial resonance open arcs, zenith beam, and orbital stardust rays
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    sk_draw = ImageDraw.Draw(skill_fx)
    # Open rotating celestial orbital arcs (skyward zenith, no loop enclosing body/legs)
    sk_draw.arc([18, 12, 114, 108], start=195, end=345, fill=(56, 160, 255, 235), width=2)
    sk_draw.arc([28, 18, 104, 94], start=205, end=335, fill=(255, 208, 40, 220), width=2)
    sk_draw.arc([36, 24, 96, 84], start=215, end=325, fill=(78, 216, 106, 230), width=2)
    # Overhead celestial zenith beam
    sk_draw.line([(96, 42), (108, 8)], fill=(255, 208, 40, 240), width=2)
    sk_draw.line([(97, 42), (108, 8)], fill=(255, 255, 255, 255), width=1)
    # Radial orbital energy ray bursts (radiating outward, unconnected)
    for rad_angle in [205, 235, 270, 305, 335]:
        rad = math.radians(rad_angle)
        x1 = 64 + int(round(36 * math.cos(rad)))
        y1 = 48 + int(round(28 * math.sin(rad)))
        x2 = 64 + int(round(56 * math.cos(rad)))
        y2 = 48 + int(round(44 * math.sin(rad)))
        x2 = max(6, min(121, x2))
        y2 = max(6, min(121, y2))
        sk_draw.line([(x1, y1), (x2, y2)], fill=(255, 94, 138, 180), width=1)
    # Floating starlight motes
    for star_x, star_y in [(24, 28), (104, 16), (116, 68), (18, 74), (64, 12), (110, 84)]:
        sk_draw.ellipse([star_x - 1, star_y - 1, star_x + 1, star_y + 1], fill=(255, 255, 255, 240))
        sk_draw.point((star_x, star_y), fill=(255, 208, 40, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.4))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, staff_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊後仰 / 失重震退衝擊 Gravity Slip & Recoil Impact)
    # Violent backward slip (x-11, y-2), head & horns tilt back (-12 deg),
    # staff recoils and flings upward (+22 deg, x+5, y+4),
    # winding key recoils against ratchets (-32 deg), enamel chest shield sparks.
    # Optics show charming "> <" dizzy / strain LEDs!
    # =========================================================================
    shifts_hit = {
        "head_top": (-11, -2), "horn_tip_l": (-13, -3), "horn_tip_r": (-9, -2),
        "horn_spiral_l": (-12, -2), "horn_spiral_r": (-9, -2),
        "ear_l": (-12, -2), "ear_r": (-9, -2),
        "eye_l": (-11, -2), "eye_r": (-11, -2),
        "snout": (-11, -2), "throat": (-10, -2),
        "core": (-9, -1),
        "shoulder_l": (-11, -2), "shoulder_r": (-8, -2),
        "arm_l": (-12, 0), "arm_r": (-4, 3),
        "torso": (-9, -1), "pelvis": (-7, 0),
        "hip_l": (-7, -1), "hip_r": (-4, 0),
        "foot_l": (-3, 0), "foot_r": (2, 0),
        "curio_mount": (-10, -2), "key_mount": (-10, -2), "staff_hand": (-4, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    # Base body for hit (without optic, so we can draw custom "> <" eyes)
    body_hit_base = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    body_hit_base.alpha_composite(curio_src)
    body_hit_base.alpha_composite(chassis_src)
    body_hit_base.alpha_composite(head_src)
    body_hit_base.alpha_composite(costume_src)
    body_hit_base.alpha_composite(optic_src)

    warped_hit = warp_image_idw(body_hit_base, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Overlay cute "> <" optic indicators at shifted eye positions:
    # Eye left base=(54, 42) -> shifted to (43, 40)
    # Eye right base=(74, 42) -> shifted to (63, 40)
    hit_eyes = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    he_draw = ImageDraw.Draw(hit_eyes)
    # Left eye ">"
    lx, ly = 43, 40
    he_draw.line([(lx - 3, ly - 3), (lx + 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(lx - 3, ly + 3), (lx + 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(lx - 2, ly - 2), (lx + 1, ly)], fill=(255, 255, 255, 255), width=1)
    # Right eye "<"
    rx, ry = 63, 40
    he_draw.line([(rx + 3, ly - 3), (rx - 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(rx + 3, ly + 3), (rx - 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(rx + 2, ly - 2), (rx - 1, ly)], fill=(255, 255, 255, 255), width=1)

    key_hit = place_rotated_element(key_raw, deg=-32, target_center=(76, 32), scale=1.0)
    staff_hit = place_rotated_element(weapon_raw, deg=22, target_center=(97, 58), scale=1.0)

    # Impact spark burst and kinetic deflection lines
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact point at enamel chest plate (55, 60)
    ix, iy = 55, 60
    h_draw.line([(ix - 12, iy - 8), (ix + 10, iy + 6)], fill=(255, 208, 40, 240), width=2)
    h_draw.line([(ix - 8, iy + 10), (ix + 8, iy - 8)], fill=(255, 94, 138, 230), width=2)
    h_draw.line([(ix - 14, iy), (ix + 12, iy)], fill=(255, 255, 255, 255), width=1)
    # Kinetic deflection impact stars
    for pt in [(ix - 14, iy - 10), (ix + 12, iy - 12), (ix + 14, iy + 8), (ix - 10, iy + 12), (ix + 18, iy - 2)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 253, 248, 220))
    # Slip lines near rear hooves
    h_draw.line([(34, 115), (46, 115)], fill=(255, 255, 255, 180), width=1)
    h_draw.line([(30, 117), (44, 117)], fill=(56, 160, 255, 200), width=1)
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_eyes)
    hit_canvas = Image.alpha_composite(hit_canvas, staff_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (受擊硬直重整復位 / Gyro Stabilization & Ground Re-anchoring)
    # Low semi-crouch landing (y+6, x-1), body bows forward, horns dip slightly,
    # staff braces forward-downward (-8 deg, x+2, y+5),
    # key snaps back into gear mesh (+12 deg), stabilizer orbit rings recalibrate.
    # =========================================================================
    shifts_recover = {
        "head_top": (-1, 6), "horn_tip_l": (-2, 5), "horn_tip_r": (0, 5),
        "horn_spiral_l": (-2, 6), "horn_spiral_r": (0, 6),
        "ear_l": (-2, 6), "ear_r": (0, 6),
        "eye_l": (-1, 6), "eye_r": (-1, 6),
        "snout": (-1, 6), "throat": (-1, 6),
        "core": (-1, 6),
        "shoulder_l": (-2, 5), "shoulder_r": (0, 5),
        "arm_l": (-1, 5), "arm_r": (2, 5),
        "torso": (-1, 6), "pelvis": (-1, 5),
        "hip_l": (-3, 4), "hip_r": (2, 4),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "curio_mount": (-1, 5), "key_mount": (-1, 5), "staff_hand": (2, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=12, target_center=(85, 39), scale=1.0)
    staff_rec = place_rotated_element(weapon_raw, deg=-8, target_center=(94, 59), scale=1.0)

    # Ground impact dissipation arcs & stabilization curves (open arcs, not closed loops)
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Landing dust/shock dissipation arcs at ground contact
    r_draw.arc([34, 112, 94, 122], start=190, end=350, fill=(56, 160, 255, 180), width=1)
    r_draw.arc([42, 114, 86, 120], start=200, end=340, fill=(255, 208, 40, 200), width=1)
    # Gear re-mesh spark at key base
    r_draw.line([(82, 36), (88, 42)], fill=(255, 208, 40, 230), width=1)
    r_draw.line([(88, 36), (82, 42)], fill=(255, 255, 255, 255), width=1)
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, staff_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


# 2. Main Generation Execution
print("Generating Astral Ram combat action poses...")
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

proof_768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_ram_combat_poses_768.png"
proof_strip.save(proof_768_path)
print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

# 4. Generate 768x128 magenta background proof sheet for hole detection
proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
proof_magenta.paste(proof_strip, (0, 0), proof_strip)
proof_mag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_ram_combat_poses_magenta.png"
proof_magenta.save(proof_mag_path)
print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")

print("\nAll 6 Astral Ram combat action poses successfully generated and exported!")
