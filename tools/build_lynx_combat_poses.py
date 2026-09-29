#!/usr/bin/env python3
"""
tools/build_lynx_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Marionette Lynx (第五十九族 提線猞猁, lynx)
in Clockwork Heart:
  game/assets/sprites/player/poses/lynx/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/lynx/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Also generates:
  game/assets/sprites/player/lynx_battle.png & lynx_battle_512.png (battle == attack per review.md 4b-8-1)
  game/assets/sprites/player/proof_lynx_idle_vs_battle.png & proof_lynx_idle_vs_battle_512.png
  game/assets/sprites/player/proof_lynx_combat_poses_768.png & proof_lynx_combat_poses_magenta.png
  game/assets/sprites/player/proof_lynx_hit_core_crop_8x.png
Follows CANON.md, art_direction.md, and review.md quality gates:
  - 0-QA16 / 0-QA21 / 0-QA31 / 0-QA34
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
Features:
  - Polished walnut marionette chassis & brass ball joints
  - White porcelain faceplate with dual upright brass wire resonance ear tufts
  - Emerald quartz eyemask optic core with warm orange accents
  - Dawn marionette acrobat workwear vest with mint green straps
  - Twin-segment pendulum bobtail balance back curio
  - Twin-ring chime brass winding key
  - Dawn marionette five-blade tungsten steel claws
"""

import math
import os
import sys
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

# Ensure clean imports
sys.path = [p for p in sys.path if not p.startswith('/tmp')]

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lynx"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/lynx"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PLAYER_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_lynx_twin_ring_chime_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_lynx_pendulum_bobtail_balance.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_lynx_marionette_walnut_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_lynx_bazaar_marionette_tufted_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_lynx_marionette_acrobat_vest.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_lynx_emerald_quartz_eyemask.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_lynx_dawn_marionette_steel_claws.png").convert("RGBA")

# Extract ground shadow master from party lynx_idle.png
ref_shadow_im = Image.open(f"{PLAYER_DIR}/party/lynx_idle.png").convert("RGBA")
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

# Canonical landmarks on Lynx (base +3 vertical shift applied to satisfy T>=4 margin)
base_landmarks = {
    # Head & Dual Upright Ear Tufts
    "cowl_top": (64, 25),
    "ear_tip_l": (36, 7),
    "ear_tip_r": (92, 7),
    "ear_base_l": (46, 29),
    "ear_base_r": (82, 29),
    "cowl_cheek_l": (44, 45),
    "cowl_cheek_r": (84, 45),
    "visor_brow": (64, 39),
    "optic_l": (54, 45),
    "optic_r": (74, 45),
    "snout": (64, 51),
    "chin": (64, 59),
    # Torso & Acrobat Vest
    "throat": (64, 61),
    "shoulder_l": (48, 67),
    "shoulder_r": (80, 67),
    "chest_vest": (64, 75),
    "hand_l": (38, 77),
    "hand_r": (88, 73),
    "waist": (64, 87),
    # Pendulum Bobtail & Pelvis
    "tail_root": (46, 91),
    "tail_mid": (37, 88),
    "tail_sphere": (20, 81),
    "pelvis": (64, 91),
    # Legs & Feet
    "hip_l": (48, 97),
    "hip_r": (80, 97),
    "knee_l": (48, 105),
    "knee_r": (80, 105),
    "foot_l": (48, 115),
    "foot_r": (80, 115),
}

src_pts = [base_landmarks[k] for k in base_landmarks] + anchors

# Canonical pivots on original 128x128 elements (before vertical base shift)
KEY_PIVOT = (40.0, 30.0)
WEAPON_PIVOT = (97.0, 72.0)

# Build base body_core with +3 vertical shift (z: curio=8, chassis=10, head=20, costume=25, optic=30)
raw_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
raw_body.alpha_composite(curio_src)
raw_body.alpha_composite(chassis_src)
raw_body.alpha_composite(head_src)
raw_body.alpha_composite(costume_src)
raw_body.alpha_composite(optic_src)

body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.paste(raw_body, (0, 3), raw_body)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (武道沉穩·待機防架)
    # Balanced marionette monk readiness stance.
    # Key placed at (40.0, 33.0).
    # Claws placed at (93.0, 74.0) to strictly comply with R>=4 margin (x<=123).
    # =========================================================================
    idle_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(40.0, 33.0), scale=1.0)
    idle_weapon = place_rotated_pivot(weapon_src, deg=0, pivot=WEAPON_PIVOT, target=(93.0, 74.0), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas.alpha_composite(idle_key)
    idle_canvas.alpha_composite(body_core)
    idle_canvas.alpha_composite(idle_weapon)

    # Ambient subtle glint FX on emerald quartz lenses and golden brass rivets
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    i_draw.point((54, 45), fill=(255, 255, 255, 240))
    i_draw.point((74, 45), fill=(255, 255, 255, 240))
    i_draw.point((40, 25), fill=(255, 208, 40, 220))
    i_draw.point((94, 71), fill=(255, 208, 40, 230))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas.alpha_composite(idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (沉身蓄勁·提線崩緊 / Low Crouch & Spring Tension Lock)
    # Deep monk crouch: head & torso sink down and coil back (-5, +6).
    # Winding key counter-winds with high tension (-35 deg, target=(35, 40)).
    # Steel claws pulled back into chambered striking posture (-28 deg, target=(84, 68)).
    # Pendulum bobtail arches upward (+4, -6) for aerodynamic tension.
    # FX: Brass pull-cords, golden tension arc, warm orange (#FFA010) & mint (#4ED86A) sparks.
    # =========================================================================
    tele_offsets = {
        "cowl_top": (-5, 6), "ear_tip_l": (-5, 6), "ear_tip_r": (-5, 6),
        "ear_base_l": (-5, 6), "ear_base_r": (-5, 6),
        "cowl_cheek_l": (-5, 6), "cowl_cheek_r": (-5, 6),
        "visor_brow": (-5, 6), "optic_l": (-5, 6), "optic_r": (-5, 6),
        "snout": (-5, 6), "chin": (-5, 6),
        "throat": (-4, 5), "shoulder_l": (-5, 5), "shoulder_r": (-4, 5),
        "chest_vest": (-4, 5), "hand_l": (-4, 5), "hand_r": (-8, -4),
        "waist": (-3, 4),
        "tail_root": (-2, 4), "tail_mid": (0, -2), "tail_sphere": (4, -6),
        "pelvis": (-3, 4), "hip_l": (-4, 4), "hip_r": (-2, 4),
        "knee_l": (-3, 3), "knee_r": (-1, 3),
        "foot_l": (-2, 0), "foot_r": (1, 0),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele, power=2.0, epsilon=4.0)
    tele_key = place_rotated_pivot(key_src, deg=-35, pivot=KEY_PIVOT, target=(35, 40), scale=1.02)
    tele_weapon = place_rotated_pivot(weapon_src, deg=-28, pivot=WEAPON_PIVOT, target=(84, 68), scale=1.05)

    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Tension arc around claws at (84, 68)
    t_draw.arc([68, 52, 98, 82], start=190, end=350, fill=(255, 160, 16, 235), width=2)
    t_draw.arc([70, 54, 96, 80], start=200, end=340, fill=(255, 208, 40, 220), width=1)
    # Windchime soundwave rings at key (35, 40)
    for sx, sy in [(33, 27), (28, 21), (40, 23), (22, 26), (44, 25)]:
        t_draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 253, 248, 200))
        t_draw.point((sx, sy), fill=(78, 216, 106, 240))
    # Marionette pull-cord lines from ear tufts & claw wrist
    t_draw.line([(31, 13), (25, 4)], fill=(255, 208, 40, 160), width=1)
    t_draw.line([(87, 13), (93, 4)], fill=(255, 208, 40, 160), width=1)
    t_draw.line([(84, 68), (84, 40)], fill=(78, 216, 106, 170), width=1)
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.35))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas.alpha_composite(tele_key)
    tele_canvas.alpha_composite(warped_tele_body)
    tele_canvas.alpha_composite(tele_weapon)
    tele_canvas.alpha_composite(tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (裂空瞬步·五聯鋼爪前突刺 / Five-Blade Marionette Claw Lunge)
    # Dynamic forward monk lunge: body bursts forward (+12, -2).
    # Right arm thrusts forward, unleashing five-blade steel claw (+38 deg, target=(98, 66), scale=1.08).
    # Winding key spins rapidly clockwise (+55 deg, target=(52, 33)).
    # Pendulum bobtail sweeps back (-6, +2) to counterbalance forward momentum.
    # FX: Five razor claw slash trails (warm orange #FFA010, mint green #4ED86A, ivory white #FFFDF8).
    # =========================================================================
    atk_offsets = {
        "cowl_top": (12, -2), "ear_tip_l": (11, -2), "ear_tip_r": (13, -2),
        "ear_base_l": (12, -2), "ear_base_r": (12, -2),
        "cowl_cheek_l": (12, -2), "cowl_cheek_r": (12, -2),
        "visor_brow": (12, -2), "optic_l": (12, -2), "optic_r": (12, -2),
        "snout": (12, -2), "chin": (12, -2),
        "throat": (12, -2), "shoulder_l": (12, -2), "shoulder_r": (10, -1),
        "chest_vest": (11, -1), "hand_l": (6, -1), "hand_r": (18, -4),
        "waist": (10, -1),
        "tail_root": (7, 0), "tail_mid": (-1, 2), "tail_sphere": (-6, 3),
        "pelvis": (8, 0), "hip_l": (8, -1), "hip_r": (0, 0),
        "knee_l": (6, -1), "knee_r": (-1, 0),
        "foot_l": (6, 0), "foot_r": (-2, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk, power=2.0, epsilon=4.0)
    atk_key = place_rotated_pivot(key_src, deg=55, pivot=KEY_PIVOT, target=(52, 33), scale=1.05)
    atk_weapon = place_rotated_pivot(weapon_src, deg=36, pivot=WEAPON_PIVOT, target=(98, 66), scale=1.06)

    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Five sweeping claw trails cutting through air
    claw_trails = [
        ((88, 54), (105, 50), (121, 52)),
        ((90, 59), (108, 56), (122, 58)),
        ((92, 65), (111, 62), (123, 65)),
        ((90, 71), (108, 69), (122, 73)),
        ((88, 77), (104, 76), (119, 80)),
    ]
    for p1, p2, p3 in claw_trails:
        a_draw.line([p1, p2, p3], fill=(255, 160, 16, 240), width=2)
        a_draw.line([p1, p2, p3], fill=(255, 255, 255, 255), width=1)
    # Slicing shockwave curve
    a_draw.arc([92, 46, 122, 84], start=280, end=80, fill=(78, 216, 106, 235), width=2)
    # Thrust speed ribbons
    for wy in [50, 62, 74]:
        a_draw.line([(68, wy), (88, wy - 3)], fill=(255, 208, 40, 180), width=1)
    # Impact spark points
    for sx, sy in [(118, 51), (122, 59), (123, 65), (121, 74), (117, 81), (110, 60)]:
        a_draw.point((sx, sy), fill=(255, 208, 40, 255))
        a_draw.point((sx - 1, sy), fill=(255, 255, 255, 240))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.35))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas.alpha_composite(atk_key)
    atk_canvas.alpha_composite(warped_atk_body)
    atk_canvas.alpha_composite(atk_weapon)
    atk_canvas.alpha_composite(atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (奧義·提線疾風百裂爪 / Marionette Gale Claw Flurry Vortex)
    # Leaping acrobatic aerial claw vortex!
    # Body leaps into mid-air (y-11), legs tuck into aerial martial strike.
    # Steel claws raised high in 360-degree slashing spiral (+78 deg, target=(91, 52), scale=1.14).
    # Twin-ring chime brass key overcharges (+90 deg, target=(40, 22), scale=1.06).
    # Pendulum bobtail flares wide for centrifugal stability (-5, +5).
    # FX: Double concentric cutting halos, golden and mint swirling energy ribbons.
    # =========================================================================
    skl_offsets = {
        "cowl_top": (0, -11), "ear_tip_l": (-2, -12), "ear_tip_r": (2, -12),
        "ear_base_l": (-1, -11), "ear_base_r": (1, -11),
        "cowl_cheek_l": (-2, -11), "cowl_cheek_r": (2, -11),
        "visor_brow": (0, -11), "optic_l": (-1, -11), "optic_r": (1, -11),
        "snout": (0, -11), "chin": (0, -10),
        "throat": (0, -9), "shoulder_l": (-4, -9), "shoulder_r": (4, -9),
        "chest_vest": (0, -9), "hand_l": (-6, -10), "hand_r": (4, -14),
        "waist": (0, -7),
        "tail_root": (0, -4), "tail_mid": (-3, 1), "tail_sphere": (-5, 5),
        "pelvis": (0, -5), "hip_l": (-2, -4), "hip_r": (2, -4),
        "knee_l": (-2, -3), "knee_r": (2, -3),
        "foot_l": (-2, -2), "foot_r": (2, -2),
    }
    dst_skl = [(base_landmarks[k][0] + skl_offsets[k][0], base_landmarks[k][1] + skl_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skl_body = warp_image_idw(body_core, src_pts, dst_skl, power=2.0, epsilon=4.0)
    skl_key = place_rotated_pivot(key_src, deg=90, pivot=KEY_PIVOT, target=(40, 22), scale=1.06)
    skl_weapon = place_rotated_pivot(weapon_src, deg=78, pivot=WEAPON_PIVOT, target=(91, 52), scale=1.12)

    skl_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skl_fx)
    # Concentric slashing vortex circles around claw at (91, 52)
    cx, cy = 91, 52
    for r in [20, 26]:
        pts = []
        for a_step in range(12):
            ang = math.radians(a_step * 30 + 15)
            pts.append((int(round(cx + r * math.cos(ang))), int(round(cy + r * math.sin(ang)))))
        s_draw.polygon(pts, outline=(255, 160, 16, 210), width=1)
    # Golden and mint claw streaks
    for sang, srad in [(20, 30), (80, 32), (140, 29), (200, 31), (260, 33), (320, 30)]:
        rad = math.radians(sang)
        bx = int(round(cx + srad * math.cos(rad)))
        by = int(round(cy + srad * math.sin(rad)))
        if 4 <= bx <= 123 and 4 <= by <= 116:
            s_draw.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=(255, 208, 40, 230))
            s_draw.point((bx, by), fill=(255, 255, 255, 255))
    skl_fx = skl_fx.filter(ImageFilter.GaussianBlur(0.35))

    skl_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skl_canvas.alpha_composite(skl_key)
    skl_canvas.alpha_composite(warped_skl_body)
    skl_canvas.alpha_composite(skl_weapon)
    skl_canvas.alpha_composite(skl_fx)
    poses["skill"] = enforce_ground_shadow(skl_canvas)

    # =========================================================================
    # 5. HIT (受創震退·齒輪卡滯後仰 / Impact Shock & Gear Brake Recoil)
    # Violent impact: body snaps back and up (x-12, y-4).
    # Head and cowl snap back: dx = -12, dy = -4.
    # Winding key recoils jarred: deg = -36, target = (29, 31), scale = 0.96.
    # Weapon claw knocked loose / jarred: deg = -32, target = (88, 76), scale = 0.96.
    # Pendulum bobtail tucks inward (+1, +3) to avoid clipping left boundary.
    # Feet slide back: foot_l (-3, 0), foot_r (-1, 0).
    # FX: Impact kinetic barrier lines, coral pink (#FF5E8A) and gold (#FFD028) spark fragments.
    # =========================================================================
    hit_offsets = {
        "cowl_top": (-12, -4), "ear_tip_l": (-12, -4), "ear_tip_r": (-11, -4),
        "ear_base_l": (-12, -4), "ear_base_r": (-11, -4),
        "cowl_cheek_l": (-12, -4), "cowl_cheek_r": (-11, -4),
        "visor_brow": (-12, -4), "optic_l": (-12, -4), "optic_r": (-11, -4),
        "snout": (-12, -4), "chin": (-12, -3),
        "throat": (-11, -3), "shoulder_l": (-11, -3), "shoulder_r": (-9, -3),
        "chest_vest": (-10, -3), "hand_l": (-9, -2), "hand_r": (-8, 4),
        "waist": (-9, -2),
        "tail_root": (-6, 0), "tail_mid": (-3, 2), "tail_sphere": (1, 3),
        "pelvis": (-7, 0), "hip_l": (-6, 0), "hip_r": (-4, 0),
        "knee_l": (-4, 0), "knee_r": (-2, 0),
        "foot_l": (-3, 0), "foot_r": (-1, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit, power=2.0, epsilon=4.0)
    hit_key = place_rotated_pivot(key_src, deg=-36, pivot=KEY_PIVOT, target=(29, 31), scale=0.96)
    hit_weapon = place_rotated_pivot(weapon_src, deg=-32, pivot=WEAPON_PIVOT, target=(88, 76), scale=0.96)

    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact center on chest (54, 66)
    ix, iy = 54, 66
    h_draw.line([(ix - 12, iy - 8), (ix, iy), (ix + 10, iy + 6)], fill=(255, 255, 255, 240), width=1)
    h_draw.line([(ix - 4, iy + 10), (ix, iy), (ix + 12, iy - 6)], fill=(255, 94, 138, 220), width=1)
    for pt in [(ix - 14, iy - 10), (ix + 12, iy - 12), (ix + 14, iy + 8), (ix - 10, iy + 12), (ix + 16, iy - 2)]:
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
    # 6. RECOVER (受身復原·三點著地卸勁 / Three-Point Shock Absorption Stance)
    # Low grounded landing crouch: body bows forward, absorbs impact (+1, +7).
    # Head and cowl sink down: dx = +1, dy = +7.
    # Torso compresses down: dx = +1, dy = +6.
    # Winding key re-engages into main drive (+14 deg, target=(41, 42), scale=0.98).
    # Tail sweeps along ground to arrest skid (+1, +4 root, -3, +4 mid, -6, +4 sphere).
    # Weapon gathered close defensively: deg = -14, target = (93, 76), scale = 1.02.
    # Feet plant wide in deep crouch (foot_l -3, foot_r +3).
    # FX: Brake friction sparks on floor, steam puff rings.
    # =========================================================================
    rec_offsets = {
        "cowl_top": (1, 7), "ear_tip_l": (1, 7), "ear_tip_r": (1, 7),
        "ear_base_l": (1, 7), "ear_base_r": (1, 7),
        "cowl_cheek_l": (1, 7), "cowl_cheek_r": (1, 7),
        "visor_brow": (1, 7), "optic_l": (1, 7), "optic_r": (1, 7),
        "snout": (1, 7), "chin": (1, 7),
        "throat": (1, 6), "shoulder_l": (0, 6), "shoulder_r": (2, 6),
        "chest_vest": (1, 6), "hand_l": (-2, 6), "hand_r": (-3, 6),
        "waist": (1, 5),
        "tail_root": (1, 4), "tail_mid": (-3, 4), "tail_sphere": (-6, 4),
        "pelvis": (1, 4), "hip_l": (-3, 3), "hip_r": (3, 3),
        "knee_l": (-3, 2), "knee_r": (3, 2),
        "foot_l": (-3, 0), "foot_r": (3, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec, power=2.0, epsilon=4.0)
    rec_key = place_rotated_pivot(key_src, deg=14, pivot=KEY_PIVOT, target=(41, 42), scale=0.98)
    rec_weapon = place_rotated_pivot(weapon_src, deg=-14, pivot=WEAPON_PIVOT, target=(93, 76), scale=1.02)

    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for sx, sy in [(38, 28), (32, 24), (44, 22)]:
        r_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 210))
        r_draw.point((sx, sy), fill=(78, 216, 106, 240))
    r_draw.line([(38, 36), (44, 42)], fill=(255, 208, 40, 230), width=1)
    r_draw.line([(44, 36), (38, 42)], fill=(255, 255, 255, 255), width=1)
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas.alpha_composite(rec_key)
    rec_canvas.alpha_composite(warped_rec_body)
    rec_canvas.alpha_composite(rec_weapon)
    rec_canvas.alpha_composite(rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def main():
    print("Generating The Marionette Lynx combat action poses...")
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
    p_battle_128 = f"{PLAYER_DIR}/lynx_battle.png"
    p_battle_512 = f"{PLAYER_DIR}/lynx_battle_512.png"
    battle_128.save(p_battle_128)
    battle_512.save(p_battle_512)
    print(f"  ✓ Saved battle sprites: {p_battle_128} & {p_battle_512}")

    # Proof comparison: idle vs battle (256x128 & 1024x512)
    comp_proof = Image.new("RGBA", (256, 128), (24, 20, 36, 255))
    comp_proof.paste(poses["idle"], (0, 0), poses["idle"])
    comp_proof.paste(battle_128, (128, 0), battle_128)
    p_comp = f"{PLAYER_DIR}/proof_lynx_idle_vs_battle.png"
    comp_proof.save(p_comp)

    comp_proof_512 = Image.new("RGBA", (1024, 512), (24, 20, 36, 255))
    idle_512 = poses["idle"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    comp_proof_512.paste(idle_512, (0, 0), idle_512)
    comp_proof_512.paste(battle_512, (512, 0), battle_512)
    p_comp_512 = f"{PLAYER_DIR}/proof_lynx_idle_vs_battle_512.png"
    comp_proof_512.save(p_comp_512)
    print(f"  ✓ Saved idle vs battle proof cards: {p_comp} & {p_comp_512}")

    # Composite proof sheet (idle, telegraph, attack, skill, hit, recover)
    proof_strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_order = ['idle', 'telegraph', 'attack', 'skill', 'hit', 'recover']
    for idx, p_name in enumerate(proof_order):
        proof_strip.paste(poses[p_name], (idx * 128, 0), poses[p_name])

    proof_768_path = f"{PLAYER_DIR}/proof_lynx_combat_poses_768.png"
    proof_strip.save(proof_768_path)
    print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

    # Magenta background proof sheet for hole detection
    proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    proof_magenta.paste(proof_strip, (0, 0), proof_strip)
    proof_mag_path = f"{PLAYER_DIR}/proof_lynx_combat_poses_magenta.png"
    proof_magenta.save(proof_mag_path)
    print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")

    # Crop 8x hit core for 0-QA31
    hit_512 = poses["hit"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    core_crop = hit_512.crop((50 * 4, 55 * 4, 75 * 4, 80 * 4))
    crop_path = f"{PLAYER_DIR}/proof_lynx_hit_core_crop_8x.png"
    core_crop.save(crop_path)
    print(f"  ✓ Saved 0-QA31 core crop: {crop_path}")


if __name__ == "__main__":
    main()
