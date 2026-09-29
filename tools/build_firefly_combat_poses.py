#!/usr/bin/env python3
"""
tools/build_firefly_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Lantern Firefly (第六十六族 靈燈飛螢, firefly)
in Clockwork Heart:
  game/assets/sprites/player/poses/firefly/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/firefly/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Also generates:
  game/assets/sprites/player/firefly_battle.png & firefly_battle_512.png (battle == attack per review.md 4b-8-1)
  game/assets/sprites/player/proof_firefly_idle_vs_battle.png & proof_firefly_idle_vs_battle_512.png
  game/assets/sprites/player/proof_firefly_combat_poses_768.png & proof_firefly_combat_poses_magenta.png
  game/assets/sprites/player/proof_firefly_hit_core_crop_8x.png
Follows CANON.md, art_direction.md, LANTERN_FIREFLY_DESIGN_PROPOSAL.md, and review.md quality gates:
  - 0-QA16 / 0-QA21 / 0-QA31 / 0-QA34
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
Features:
  - Thin stamped emerald brass sheet tinplate chassis with black rubber suction paw pads
  - Head unit with dual delicate spring brass wire antenna tuners tipped with golden polished spheres
  - Optic core: Glowing dual spherical lantern quartz lenses with concentric tungsten filament rings
  - Costume: Clockwork vine harness cuirass with dopamine sky-blue accents and brass buckles
  - Back curio: Translucent luminescent resin abdomen bulb with internal micro-gears & filigree elytra wings
  - Floral-gear four-petal brass wind-up key with central dopamine coral-pink rivet
  - Clockwork vine staff with transparent glass sap tube, miniature resin mushroom, and tuning prism
"""

import math
import os
import sys
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

sys.path = [p for p in sys.path if not p.startswith('/tmp')]

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/firefly"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/firefly"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PLAYER_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_firefly_floral_gear_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_firefly_luminescent_resin_abdomen.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_firefly_emerald_tinplate_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_firefly_brass_antenna_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_firefly_vine_harness_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_firefly_dual_lantern_quartz_eyes.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_firefly_luminescent_vine_staff.png").convert("RGBA")

# Extract ground shadow master from party/firefly_idle.png
ref_shadow_im = Image.open(f"{PLAYER_DIR}/party/firefly_idle.png").convert("RGBA")
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


def place_rotated_pivot(elem_img: Image.Image, deg: float, pivot: tuple[float, float], target: tuple[float, float], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates an element around an exact pivot point and places it at target coordinates with subpixel precision."""
    b = elem_img.copy()
    if mirror:
        b = ImageOps.mirror(b)
    px, py = pivot
    tx, ty = target

    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    paste_x = int(round(128.0 - px))
    paste_y = int(round(128.0 - py))
    large.paste(b, (paste_x, paste_y))

    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        scaled = large.resize((nw, nh), Image.Resampling.LANCZOS)
        off_x = (nw - canvas_size) // 2
        off_y = (nh - canvas_size) // 2
        large = scaled.crop((off_x, off_y, off_x + canvas_size, off_y + canvas_size))

    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    out_x = int(round(tx - 128.0))
    out_y = int(round(ty - 128.0))
    out.paste(rotated, (out_x, out_y), rotated)
    return out


def warp_image_idw(src_img: Image.Image, src_points: list[tuple[int, int]], dst_points: list[tuple[int, int]], power: float = 2.0, epsilon: float = 4.0) -> Image.Image:
    """Smooth Inverse Distance Weighting (IDW) landmark warp for mechanical body articulation."""
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


# Anchors ensuring edge stability and ground shadow preservation
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127),
    (32, 0), (96, 0), (0, 32), (0, 96),
    (127, 32), (127, 96),
    (20, 116), (64, 116), (108, 116)
]

# Canonical landmarks on Lantern Firefly
base_landmarks = {
    # Head & Dual Wire Antenna Tuners
    "antenna_tip_l": (40, 5),
    "antenna_tip_r": (88, 5),
    "antenna_mid_l": (46, 16),
    "antenna_mid_r": (82, 16),
    "cowl_top": (64, 22),
    "cowl_cheek_l": (38, 44),
    "cowl_cheek_r": (90, 44),
    "optic_l": (56, 42),
    "optic_r": (73, 42),
    "snout": (64, 48),
    "chin": (64, 56),
    # Torso & Vine Cuirass
    "throat": (64, 60),
    "shoulder_l": (44, 64),
    "shoulder_r": (84, 64),
    "chest": (64, 72),
    "hand_l": (40, 78),
    "hand_r": (88, 75),
    "cuirass_hem": (64, 92),
    # Curio (Luminescent Resin Abdomen & Stamped Wings)
    "wing_l": (22, 56),
    "abdomen_bulb": (32, 78),
    "curio_root": (42, 88),
    # Chassis Pelvis & Legs
    "pelvis": (64, 96),
    "hip_l": (50, 102),
    "hip_r": (78, 102),
    "knee_l": (48, 110),
    "knee_r": (80, 110),
    "foot_l": (50, 120),
    "foot_r": (78, 120),
}

src_pts = [base_landmarks[k] for k in base_landmarks] + anchors

# Canonical pivots
KEY_PIVOT = (38.5, 31.0)
WEAPON_PIVOT = (95.0, 68.0)

# Build base body_core (z: curio=8, chassis=10, head=20, costume=25, optic=30)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (靈光晨曦·法杖待機 / Luminescent Dawn Guard)
    # Balanced firefly mage readiness stance.
    # Winding key at canonical position (38.5, 31.0).
    # Vine staff held elegantly at (95.0, 68.0).
    # FX: Soft warm glow on lantern quartz eyes & bioluminescent spore breathing.
    # =========================================================================
    idle_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(38.5, 31.0), scale=1.0)
    idle_weapon = place_rotated_pivot(weapon_src, deg=0, pivot=WEAPON_PIVOT, target=(95.0, 68.0), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas.alpha_composite(idle_key)
    idle_canvas.alpha_composite(body_core)
    idle_canvas.alpha_composite(idle_weapon)

    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    # Eye specular highlights
    i_draw.point((56, 42), fill=(255, 255, 255, 240))
    i_draw.point((73, 42), fill=(255, 255, 255, 240))
    # Soft glowing spores around staff mushroom & abdomen
    for px, py in [(96, 32), (92, 40), (102, 36), (30, 80), (26, 86)]:
        i_draw.point((px, py), fill=(255, 208, 40, 220))
        i_draw.point((px + 1, py), fill=(78, 216, 106, 210))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas.alpha_composite(idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (晨曦蓄勢·發條預熱回聚 / Clockwork Pre-Ignition & Coil Charge)
    # Deep mage crouch: head & torso sink down and coil back (-6, +6).
    # Winding key counter-winds with high spring tension (-50 deg, target=(32.0, 37.0), scale=0.94).
    # Staff held close to chest gathering glowing spores (-30 deg, target=(88.0, 74.0), scale=0.96).
    # FX: Soft golden energy aura around abdomen bulb, spore concentration.
    # =========================================================================
    tele_offsets = {
        "antenna_tip_l": (-6, 5), "antenna_tip_r": (-6, 5),
        "antenna_mid_l": (-6, 6), "antenna_mid_r": (-6, 6),
        "cowl_top": (-6, 6), "cowl_cheek_l": (-6, 6), "cowl_cheek_r": (-6, 6),
        "optic_l": (-6, 6), "optic_r": (-6, 6), "snout": (-6, 6), "chin": (-6, 6),
        "throat": (-5, 5), "shoulder_l": (-6, 5), "shoulder_r": (-4, 5),
        "chest": (-5, 5), "hand_l": (-5, 4), "hand_r": (-7, 0),
        "cuirass_hem": (-4, 5),
        "wing_l": (-5, 4), "abdomen_bulb": (-5, 4), "curio_root": (-4, 4),
        "pelvis": (-4, 4), "hip_l": (-4, 4), "hip_r": (-2, 4),
        "knee_l": (-4, 3), "knee_r": (1, 3),
        "foot_l": (-2, 0), "foot_r": (1, 0),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele, power=2.0, epsilon=4.0)
    tele_key = place_rotated_pivot(key_src, deg=-50, pivot=KEY_PIVOT, target=(32.0, 37.0), scale=0.94)
    tele_weapon = place_rotated_pivot(weapon_src, deg=-30, pivot=WEAPON_PIVOT, target=(88.0, 74.0), scale=0.96)

    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Concentric charging pre-ignition light points around abdomen and staff crystal
    for sx, sy in [(28, 72), (24, 76), (32, 80), (22, 84), (82, 42), (90, 36), (86, 50), (80, 48), (88, 44)]:
        t_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 190))
        t_draw.point((sx, sy), fill=(255, 208, 40, 240))
        t_draw.point((sx + 1, sy), fill=(78, 216, 106, 220))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.35))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas.alpha_composite(tele_key)
    tele_canvas.alpha_composite(warped_tele_body)
    tele_canvas.alpha_composite(tele_weapon)
    tele_canvas.alpha_composite(tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (飛螢破曉·藤蔓杖芒前突射 / Dawn Blossom Vine Ray)
    # Dynamic forward casting lunge: body bursts forward (+13, 0).
    # Staff sweeps forward (+36 deg, target=(103.0, 62.0), scale=1.14).
    # Winding key spins forward (+56 deg, target=(52.0, 30.0), scale=1.05).
    # FX: Arc of Tyndall dawn light, glowing spore burst wavefront!
    # =========================================================================
    atk_offsets = {
        "antenna_tip_l": (13, 0), "antenna_tip_r": (13, 0),
        "antenna_mid_l": (13, 0), "antenna_mid_r": (13, 0),
        "cowl_top": (13, 0), "cowl_cheek_l": (13, 0), "cowl_cheek_r": (13, 0),
        "optic_l": (13, 0), "optic_r": (13, 0), "snout": (13, 0), "chin": (13, 0),
        "throat": (12, 0), "shoulder_l": (10, 0), "shoulder_r": (13, 0),
        "chest": (12, 0), "hand_l": (7, 0), "hand_r": (15, -2),
        "cuirass_hem": (9, 0),
        "wing_l": (7, 0), "abdomen_bulb": (8, 0), "curio_root": (8, 0),
        "pelvis": (8, -1), "hip_l": (6, 0), "hip_r": (9, 0),
        "knee_l": (2, 0), "knee_r": (7, 0),
        "foot_l": (1, 0), "foot_r": (6, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk, power=2.0, epsilon=4.0)
    atk_key = place_rotated_pivot(key_src, deg=56, pivot=KEY_PIVOT, target=(52.0, 30.0), scale=1.05)
    atk_weapon = place_rotated_pivot(weapon_src, deg=36, pivot=WEAPON_PIVOT, target=(103.0, 62.0), scale=1.14)

    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Piercing curved Tyndall dawn wave arc (ahead of staff tip, within safe boundary x <= 122)
    a_draw.arc([94, 38, 122, 84], start=290, end=70, fill=(78, 216, 106, 235), width=2)
    a_draw.arc([98, 42, 118, 80], start=305, end=55, fill=(255, 208, 40, 220), width=1)
    # Wavefront glowing spore particles
    for px, py in [(114, 46), (118, 56), (115, 66), (110, 72), (120, 60)]:
        a_draw.point((px, py), fill=(255, 253, 248, 255))
        a_draw.point((px + 1, py), fill=(255, 208, 40, 240))
        a_draw.point((px - 1, py), fill=(78, 216, 106, 220))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.35))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas.alpha_composite(atk_key)
    atk_canvas.alpha_composite(warped_atk_body)
    atk_canvas.alpha_composite(atk_weapon)
    atk_canvas.alpha_composite(atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (林冠靈光·萬道星屑神聖法陣 / Tyndall Aurora & Celestial Spore Overdrive)
    # Majestic elevated casting pose!
    # Head and cowl tilt high up, antennae stay within safe margin (top y >= 4).
    # Torso arches upward, wings and abdomen bulb expand aloft.
    # Staff held straight up pointing to the canopy (+66 deg, target=(96.0, 48.0), scale=1.20).
    # Winding key overclocks (+90 deg, target=(38.5, 23.0), scale=1.08).
    # FX: Golden spore halo and Tyndall dawn light rays.
    # =========================================================================
    skl_offsets = {
        "antenna_tip_l": (0, 0), "antenna_tip_r": (0, 0),
        "antenna_mid_l": (0, -2), "antenna_mid_r": (0, -2),
        "cowl_top": (0, -4), "cowl_cheek_l": (-1, -5), "cowl_cheek_r": (1, -5),
        "optic_l": (0, -6), "optic_r": (0, -6), "snout": (0, -5), "chin": (0, -5),
        "throat": (0, -6), "shoulder_l": (-1, -6), "shoulder_r": (1, -6),
        "chest": (0, -6), "hand_l": (-3, -6), "hand_r": (3, -10),
        "cuirass_hem": (0, -5),
        "wing_l": (-3, -5), "abdomen_bulb": (-2, -5), "curio_root": (-1, -5),
        "pelvis": (0, -4), "hip_l": (-2, -3), "hip_r": (2, -3),
        "knee_l": (-2, -2), "knee_r": (2, -2),
        "foot_l": (-1, 0), "foot_r": (2, 0),
    }
    dst_skl = [(base_landmarks[k][0] + skl_offsets[k][0], base_landmarks[k][1] + skl_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skl_body = warp_image_idw(body_core, src_pts, dst_skl, power=2.0, epsilon=4.0)
    skl_key = place_rotated_pivot(key_src, deg=90, pivot=KEY_PIVOT, target=(38.5, 23.0), scale=1.08)
    skl_weapon = place_rotated_pivot(weapon_src, deg=66, pivot=WEAPON_PIVOT, target=(96.0, 48.0), scale=1.20)

    skl_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skl_fx)
    # Luminous circular radiating halo around staff mushroom prism (96, 48)
    s_draw.arc([76, 28, 116, 68], start=0, end=360, fill=(255, 208, 40, 220), width=1)
    s_draw.arc([80, 32, 112, 64], start=0, end=360, fill=(78, 216, 106, 210), width=1)
    s_draw.arc([84, 36, 108, 60], start=0, end=360, fill=(255, 253, 248, 240), width=1)
    # Sparkling spore rays
    for sx, sy in [(96, 20), (114, 40), (78, 44), (110, 62), (84, 28), (96, 72)]:
        s_draw.point((sx, sy), fill=(255, 208, 40, 245))
        s_draw.point((sx + 1, sy), fill=(255, 253, 248, 255))
        s_draw.point((sx, sy + 1), fill=(78, 216, 106, 220))
    skl_fx = skl_fx.filter(ImageFilter.GaussianBlur(0.35))

    skl_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skl_canvas.alpha_composite(skl_key)
    skl_canvas.alpha_composite(warped_skl_body)
    skl_canvas.alpha_composite(skl_weapon)
    skl_canvas.alpha_composite(skl_fx)
    poses["skill"] = enforce_ground_shadow(skl_canvas)

    # =========================================================================
    # 5. HIT (金屬震撼·受擊受挫硬直 / Impact Shock & Stagger Stance)
    # Violent backward recoil and stagger (-12, 0).
    # Head and antennae snap back (-12, 0).
    # Torso jolts back (-10, 0), pelvis (-7, 0).
    # Winding key knocked askew (-44 deg, target=(28.0, 29.0), scale=0.94).
    # Staff knocked back defensively (-36 deg, target=(88.0, 78.0), scale=0.92).
    # FX: Impact starburst on chest (ix=54, iy=68) with tiny golden screw/bolt motes.
    # =========================================================================
    hit_offsets = {
        "antenna_tip_l": (-12, 0), "antenna_tip_r": (-12, 0),
        "antenna_mid_l": (-12, 0), "antenna_mid_r": (-12, 0),
        "cowl_top": (-12, 0), "cowl_cheek_l": (-12, 0), "cowl_cheek_r": (-12, 0),
        "optic_l": (-12, 0), "optic_r": (-12, 0), "snout": (-12, 0), "chin": (-12, 0),
        "throat": (-10, 0), "shoulder_l": (-10, 0), "shoulder_r": (-9, 0),
        "chest": (-10, 0), "hand_l": (-9, 0), "hand_r": (-7, 3),
        "cuirass_hem": (-8, 0),
        "wing_l": (-7, 0), "abdomen_bulb": (-7, 0), "curio_root": (-6, 0),
        "pelvis": (-7, 0), "hip_l": (-6, 0), "hip_r": (-4, 0),
        "knee_l": (-4, 0), "knee_r": (-2, 0),
        "foot_l": (-2, 0), "foot_r": (0, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit, power=2.0, epsilon=4.0)
    hit_key = place_rotated_pivot(key_src, deg=-44, pivot=KEY_PIVOT, target=(28.0, 29.0), scale=0.94)
    hit_weapon = place_rotated_pivot(weapon_src, deg=-36, pivot=WEAPON_PIVOT, target=(88.0, 78.0), scale=0.92)

    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    ix, iy = 54, 68
    for pt in [(ix - 8, iy - 7), (ix + 9, iy - 6), (ix + 10, iy + 6), (ix - 7, iy + 8), (ix + 12, iy - 1), (ix - 10, iy + 1)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.35))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas.alpha_composite(hit_key)
    hit_canvas.alpha_composite(warped_hit_body)
    hit_canvas.alpha_composite(hit_weapon)
    hit_canvas.alpha_composite(hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (柔韌接地·三點制動卸勁 / Three-Point Ground Cushion & Spore Calibrate)
    # Low grounded landing crouch: body bows forward, absorbs impact (+2, +7).
    # Head and antennae sink down (+2, +7).
    # Torso compresses down (+2, +6), pelvis (+2, +4).
    # Feet plant wide in deep crouch (foot_l -3, foot_r +3).
    # Winding key re-engages into main drive (+18 deg, target=(40.0, 38.0), scale=0.98).
    # Staff braced firmly near body (-15 deg, target=(93.0, 74.0), scale=1.02).
    # FX: Floor settling spore dust motes.
    # =========================================================================
    rec_offsets = {
        "antenna_tip_l": (2, 7), "antenna_tip_r": (2, 7),
        "antenna_mid_l": (2, 7), "antenna_mid_r": (2, 7),
        "cowl_top": (2, 7), "cowl_cheek_l": (2, 7), "cowl_cheek_r": (2, 7),
        "optic_l": (2, 7), "optic_r": (2, 7), "snout": (2, 7), "chin": (2, 7),
        "throat": (2, 6), "shoulder_l": (1, 6), "shoulder_r": (3, 6),
        "chest": (2, 6), "hand_l": (-2, 6), "hand_r": (-2, 6),
        "cuirass_hem": (2, 5),
        "wing_l": (1, 5), "abdomen_bulb": (2, 5), "curio_root": (2, 4),
        "pelvis": (2, 4), "hip_l": (-3, 3), "hip_r": (3, 3),
        "knee_l": (-3, 2), "knee_r": (3, 2),
        "foot_l": (-3, 0), "foot_r": (3, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec, power=2.0, epsilon=4.0)
    rec_key = place_rotated_pivot(key_src, deg=18, pivot=KEY_PIVOT, target=(40.0, 38.0), scale=0.98)
    rec_weapon = place_rotated_pivot(weapon_src, deg=-15, pivot=WEAPON_PIVOT, target=(93.0, 74.0), scale=1.02)

    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for sx, sy in [(36, 114), (44, 115), (78, 114), (88, 115), (40, 32), (48, 28)]:
        r_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 200))
        r_draw.point((sx, sy), fill=(78, 216, 106, 230))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas.alpha_composite(rec_key)
    rec_canvas.alpha_composite(warped_rec_body)
    rec_canvas.alpha_composite(rec_weapon)
    rec_canvas.alpha_composite(rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def main():
    print("Generating The Lantern Firefly combat action poses...")
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

    # Official Battle Sprite (battle == attack per review.md 4b-8-1)
    battle_128 = poses["attack"]
    battle_512 = battle_128.resize((512, 512), resample=Image.Resampling.LANCZOS)
    p_battle_128 = f"{PLAYER_DIR}/firefly_battle.png"
    p_battle_512 = f"{PLAYER_DIR}/firefly_battle_512.png"
    battle_128.save(p_battle_128)
    battle_512.save(p_battle_512)
    print(f"  ✓ Saved battle sprites: {p_battle_128} & {p_battle_512}")

    # Proof comparison: idle vs battle (256x128 & 1024x512)
    comp_proof = Image.new("RGBA", (256, 128), (24, 20, 36, 255))
    comp_proof.paste(poses["idle"], (0, 0), poses["idle"])
    comp_proof.paste(battle_128, (128, 0), battle_128)
    p_comp = f"{PLAYER_DIR}/proof_firefly_idle_vs_battle.png"
    comp_proof.save(p_comp)

    comp_proof_512 = Image.new("RGBA", (1024, 512), (24, 20, 36, 255))
    idle_512 = poses["idle"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    comp_proof_512.paste(idle_512, (0, 0), idle_512)
    comp_proof_512.paste(battle_512, (512, 0), battle_512)
    p_comp_512 = f"{PLAYER_DIR}/proof_firefly_idle_vs_battle_512.png"
    comp_proof_512.save(p_comp_512)
    print(f"  ✓ Saved idle vs battle proof cards: {p_comp} & {p_comp_512}")

    # Composite proof sheet (idle, telegraph, attack, skill, hit, recover)
    proof_strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_order = ['idle', 'telegraph', 'attack', 'skill', 'hit', 'recover']
    for idx, p_name in enumerate(proof_order):
        proof_strip.paste(poses[p_name], (idx * 128, 0), poses[p_name])

    proof_768_path = f"{PLAYER_DIR}/proof_firefly_combat_poses_768.png"
    proof_strip.save(proof_768_path)
    print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

    # Magenta background proof sheet for hole detection
    proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    proof_magenta.paste(proof_strip, (0, 0), proof_strip)
    proof_mag_path = f"{PLAYER_DIR}/proof_firefly_combat_poses_magenta.png"
    proof_magenta.save(proof_mag_path)
    print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")

    # Crop 8x hit core for 0-QA31
    hit_512 = poses["hit"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    core_crop = hit_512.crop((50 * 4, 55 * 4, 75 * 4, 80 * 4))
    crop_path = f"{PLAYER_DIR}/proof_firefly_hit_core_crop_8x.png"
    core_crop.save(crop_path)
    print(f"  ✓ Saved 0-QA31 core crop: {crop_path}")


if __name__ == "__main__":
    main()
