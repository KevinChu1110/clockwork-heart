#!/usr/bin/env python3
"""
tools/build_scarab_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Obsidian Scarab (第六十族 黑曜金龜, scarab)
in Clockwork Heart:
  game/assets/sprites/player/poses/scarab/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/scarab/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Also generates:
  game/assets/sprites/player/scarab_battle.png & scarab_battle_512.png (battle == attack per review.md 4b-8-1)
  game/assets/sprites/player/proof_scarab_idle_vs_battle.png & proof_scarab_idle_vs_battle_512.png
  game/assets/sprites/player/proof_scarab_combat_poses_768.png & proof_scarab_combat_poses_magenta.png
  game/assets/sprites/player/proof_scarab_hit_core_crop_8x.png
Follows CANON.md, art_direction.md, and review.md quality gates:
  - 0-QA16 / 0-QA21 / 0-QA31 / 0-QA34
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
Features:
  - Quenched obsidian chassis & brass ball joints
  - Quenched obsidian cowl with cute twin-forked brass mechanical tuning horn antennae
  - Amber crystal visor optic core with warm golden/molten luminescence
  - Crucible artisan heat-resistant apron with mint green trim and brass rivets
  - Deployable obsidian elytra & twin micro-vent high-pressure exhaust tail
  - Four-leaf forge cross-fire brass winding key
  - Crucible obsidian focus crystal with glowing concentric runic aura
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
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/scarab"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/scarab"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PLAYER_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_scarab_crucible_cross_fire_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_scarab_twin_vent_exhaust_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_scarab_obsidian_forge_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_scarab_quenched_obsidian_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_scarab_crucible_artisan_apron.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_scarab_amber_crystal_visor.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_scarab_crucible_obsidian_focus.png").convert("RGBA")

# Extract ground shadow master from party scarab_idle.png
ref_shadow_im = Image.open(f"{PLAYER_DIR}/party/scarab_idle.png").convert("RGBA")
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

# Canonical landmarks on Scarab (base +2 vertical shift applied to satisfy T>=4 margin)
base_landmarks = {
    # Head & Dual Horn Antennae
    "cowl_top": (64, 5),
    "horn_tip_l": (52, 5),
    "horn_tip_r": (76, 5),
    "horn_base_l": (58, 24),
    "horn_base_r": (70, 24),
    "cowl_cheek_l": (46, 40),
    "cowl_cheek_r": (82, 40),
    "visor_brow": (64, 38),
    "optic_l": (55, 44),
    "optic_r": (73, 44),
    "snout": (64, 52),
    "chin": (64, 62),
    # Torso & Artisan Apron
    "throat": (64, 66),
    "shoulder_l": (46, 70),
    "shoulder_r": (82, 70),
    "chest_apron": (64, 76),
    "hand_l": (38, 80),
    "hand_r": (90, 78),
    "apron_hem": (64, 94),
    # Curio (Twin Vent Exhaust Tail) & Chassis
    "vent_l": (22, 72),
    "vent_r": (36, 76),
    "curio_root": (40, 88),
    "pelvis": (64, 96),
    # Legs & Feet
    "hip_l": (46, 102),
    "hip_r": (82, 102),
    "knee_l": (46, 110),
    "knee_r": (82, 110),
    "foot_l": (46, 118),
    "foot_r": (82, 118),
}

src_pts = [base_landmarks[k] for k in base_landmarks] + anchors

# Canonical pivots on original 128x128 elements (before vertical base shift)
KEY_PIVOT = (40.0, 30.5)
WEAPON_PIVOT = (102.0, 68.0)

# Build base body_core with +2 vertical shift (z: curio=8, chassis=10, head=20, costume=25, optic=30)
raw_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
raw_body.alpha_composite(curio_src)
raw_body.alpha_composite(chassis_src)
raw_body.alpha_composite(head_src)
raw_body.alpha_composite(costume_src)
raw_body.alpha_composite(optic_src)

body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.paste(raw_body, (0, 2), raw_body)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (赤焰黑曜·熔爐法師待機護體 / Crucible Obsidian Neutral Guard)
    # Balanced scarab mage readiness stance.
    # Key placed at (40.0, 32.5).
    # Focus crystal levitating at (100.0, 70.0).
    # =========================================================================
    idle_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(40.0, 32.5), scale=1.0)
    idle_weapon = place_rotated_pivot(weapon_src, deg=0, pivot=WEAPON_PIVOT, target=(100.0, 70.0), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas.alpha_composite(idle_key)
    idle_canvas.alpha_composite(body_core)
    idle_canvas.alpha_composite(idle_weapon)

    # Ambient subtle glint FX on amber crystal visor and molten gold brass accents
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    i_draw.point((55, 44), fill=(255, 255, 255, 240))
    i_draw.point((73, 44), fill=(255, 255, 255, 240))
    i_draw.point((100, 64), fill=(255, 208, 40, 220))
    i_draw.point((100, 76), fill=(255, 160, 16, 230))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas.alpha_composite(idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (熔爐蓄聚·晶核回旋充能 / Molten Crucible Calibration & Core Charge)
    # Deep mage crouch: head & torso sink down and coil back (-7, +8).
    # Winding key counter-winds with high spring tension (-52 deg, target=(32, 42), scale=0.92).
    # Obsidian focus drawn close to chest in defensive charge (-38 deg, target=(84, 76), scale=0.95).
    # FX: Soft golden charging glow circle around focus, gentle steam puffs from vents.
    # =========================================================================
    tele_offsets = {
        "cowl_top": (-7, 8), "horn_tip_l": (-7, 8), "horn_tip_r": (-7, 8),
        "horn_base_l": (-7, 8), "horn_base_r": (-7, 8),
        "cowl_cheek_l": (-7, 8), "cowl_cheek_r": (-7, 8),
        "visor_brow": (-7, 8), "optic_l": (-7, 8), "optic_r": (-7, 8),
        "snout": (-7, 8), "chin": (-7, 8),
        "throat": (-6, 7), "shoulder_l": (-7, 7), "shoulder_r": (-5, 7),
        "chest_apron": (-6, 7), "hand_l": (-6, 6), "hand_r": (-9, -2),
        "apron_hem": (-5, 6),
        "vent_l": (-6, 6), "vent_r": (-5, 6), "curio_root": (-5, 5),
        "pelvis": (-5, 5), "hip_l": (-5, 5), "hip_r": (-2, 5),
        "knee_l": (-5, 4), "knee_r": (1, 4),
        "foot_l": (-2, 0), "foot_r": (1, 0),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele, power=2.0, epsilon=4.0)
    tele_key = place_rotated_pivot(key_src, deg=-52, pivot=KEY_PIVOT, target=(32, 42), scale=0.92)
    tele_weapon = place_rotated_pivot(weapon_src, deg=-38, pivot=WEAPON_PIVOT, target=(84, 76), scale=0.95)

    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Soft golden charging aura around focus at (84, 76)
    t_draw.arc([68, 60, 100, 92], start=160, end=350, fill=(255, 160, 16, 220), width=2)
    t_draw.arc([72, 64, 96, 88], start=180, end=330, fill=(255, 208, 40, 210), width=1)
    # Steam puff motes from rear exhaust vents
    for sx, sy in [(20, 66), (16, 60), (26, 62)]:
        t_draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 253, 248, 170))
        t_draw.point((sx, sy), fill=(255, 208, 40, 230))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.35))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas.alpha_composite(tele_key)
    tele_canvas.alpha_composite(warped_tele_body)
    tele_canvas.alpha_composite(tele_weapon)
    tele_canvas.alpha_composite(tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (織盾成刃·黑曜晶芒前突射 / Obsidian Shard Blade Blast)
    # Dynamic forward lunge: body bursts forward (+16, 0).
    # Focus crystal projects forward (+44 deg, target=(106, 64), scale=1.16).
    # Winding key spins rapidly clockwise (+62 deg, target=(56, 30), scale=1.05).
    # FX: Blazing molten energy arc and crystal particle spray.
    # =========================================================================
    atk_offsets = {
        "cowl_top": (16, 0), "horn_tip_l": (16, 0), "horn_tip_r": (16, 0),
        "horn_base_l": (16, 0), "horn_base_r": (16, 0),
        "cowl_cheek_l": (16, 0), "cowl_cheek_r": (16, 0),
        "visor_brow": (16, 0), "optic_l": (16, 0), "optic_r": (16, 0),
        "snout": (16, 0), "chin": (16, 0),
        "throat": (14, 0), "shoulder_l": (12, 0), "shoulder_r": (15, 0),
        "chest_apron": (14, 0), "hand_l": (9, 0), "hand_r": (17, -2),
        "apron_hem": (11, 0),
        "vent_l": (9, 0), "vent_r": (10, 0), "curio_root": (10, 0),
        "pelvis": (10, -1), "hip_l": (7, 0), "hip_r": (11, 0),
        "knee_l": (3, 0), "knee_r": (9, 0),
        "foot_l": (1, 0), "foot_r": (8, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk, power=2.0, epsilon=4.0)
    atk_key = place_rotated_pivot(key_src, deg=62, pivot=KEY_PIVOT, target=(56, 30), scale=1.05)
    atk_weapon = place_rotated_pivot(weapon_src, deg=44, pivot=WEAPON_PIVOT, target=(106, 64), scale=1.16)

    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Piercing curved molten refraction wave
    a_draw.arc([74, 30, 122, 94], start=280, end=80, fill=(255, 160, 16, 235), width=2)
    a_draw.arc([78, 34, 118, 90], start=295, end=65, fill=(255, 208, 40, 220), width=1)
    # Wavefront concentric soft glow
    a_draw.ellipse([98, 56, 118, 76], outline=(255, 208, 40, 210), width=1)
    for px, py in [(114, 52), (118, 62), (115, 72), (110, 76), (120, 66)]:
        a_draw.point((px, py), fill=(255, 253, 248, 255))
        a_draw.point((px + 1, py), fill=(255, 208, 40, 240))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.35))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas.alpha_composite(atk_key)
    atk_canvas.alpha_composite(warped_atk_body)
    atk_canvas.alpha_composite(atk_weapon)
    atk_canvas.alpha_composite(atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (赤焰熔爐·黑曜護體靈晶法陣 / Molten Crucible Aegis & Crystal Barrier)
    # Majestic elevated casting pose!
    # Head and cowl tilt high up (x=0, y-12).
    # Torso elevates upward (x=0, y-8), pelvis lifts (x=0, y-4).
    # Winding key overclocks (+90 deg, target=(40, 20), scale=1.08).
    # Obsidian focus expands aloft (+72 deg, target=(94, 46), scale=1.22).
    # FX: Luminous circular radiating halo around focus, steam geysers from vents.
    # =========================================================================
    skl_offsets = {
        "cowl_top": (0, -12), "horn_tip_l": (0, -12), "horn_tip_r": (0, -12),
        "horn_base_l": (0, -12), "horn_base_r": (0, -12),
        "cowl_cheek_l": (0, -11), "cowl_cheek_r": (0, -11),
        "visor_brow": (0, -11), "optic_l": (0, -11), "optic_r": (0, -11),
        "snout": (0, -10), "chin": (0, -10),
        "throat": (0, -8), "shoulder_l": (-1, -8), "shoulder_r": (1, -8),
        "chest_apron": (0, -8), "hand_l": (-4, -7), "hand_r": (4, -12),
        "apron_hem": (0, -6),
        "vent_l": (-2, -7), "vent_r": (0, -7), "curio_root": (0, -6),
        "pelvis": (0, -4), "hip_l": (-2, -3), "hip_r": (2, -3),
        "knee_l": (-2, -2), "knee_r": (2, -2),
        "foot_l": (-1, 0), "foot_r": (2, 0),
    }
    dst_skl = [(base_landmarks[k][0] + skl_offsets[k][0], base_landmarks[k][1] + skl_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skl_body = warp_image_idw(body_core, src_pts, dst_skl, power=2.0, epsilon=4.0)
    skl_key = place_rotated_pivot(key_src, deg=90, pivot=KEY_PIVOT, target=(40, 20), scale=1.08)
    skl_weapon = place_rotated_pivot(weapon_src, deg=72, pivot=WEAPON_PIVOT, target=(94, 46), scale=1.22)

    skl_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skl_fx)
    # Luminous circular radiating halo around elevated focus (94, 46)
    s_draw.arc([76, 28, 112, 64], start=0, end=360, fill=(255, 208, 40, 220), width=1)
    s_draw.arc([80, 32, 108, 60], start=0, end=360, fill=(255, 160, 16, 200), width=1)
    s_draw.arc([84, 36, 104, 56], start=0, end=360, fill=(255, 253, 248, 240), width=1)

    # Vent high pressure steam puffs upward
    for vy in range(32, 60, 6):
        s_draw.ellipse([20, vy - 2, 26, vy + 2], fill=(255, 253, 248, 140))
        s_draw.ellipse([34, vy, 40, vy + 4], fill=(255, 253, 248, 140))

    # Sparkle points
    for sx, sy in [(94, 24), (112, 42), (80, 46), (106, 62), (84, 32)]:
        s_draw.point((sx, sy), fill=(255, 208, 40, 240))
        s_draw.point((sx + 1, sy), fill=(255, 253, 248, 255))
    skl_fx = skl_fx.filter(ImageFilter.GaussianBlur(0.35))

    skl_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skl_canvas.alpha_composite(skl_key)
    skl_canvas.alpha_composite(warped_skl_body)
    skl_canvas.alpha_composite(skl_weapon)
    skl_canvas.alpha_composite(skl_fx)
    poses["skill"] = enforce_ground_shadow(skl_canvas)

    # =========================================================================
    # 5. HIT (金屬震撼·受擊受挫硬直 / Impact Shock & Stagger Stance)
    # Violent backward recoil and stagger (-14, -5).
    # Head snaps back (-14, -5).
    # Torso jolts back (-12, -3), pelvis jolts back (-8, -1).
    # Winding key knocked askew (-48 deg, target=(26, 28), scale=0.94).
    # Weapon knocked askew (-42 deg, target=(92, 80), scale=0.92).
    # FX: Starburst impact sparks on chest (ix=52, iy=68), pink & gold particle debris.
    # =========================================================================
    hit_offsets = {
        "cowl_top": (-14, -5), "horn_tip_l": (-14, -5), "horn_tip_r": (-14, -5),
        "horn_base_l": (-14, -5), "horn_base_r": (-14, -5),
        "cowl_cheek_l": (-14, -5), "cowl_cheek_r": (-14, -5),
        "visor_brow": (-14, -5), "optic_l": (-14, -5), "optic_r": (-14, -5),
        "snout": (-14, -5), "chin": (-14, -5),
        "throat": (-12, -4), "shoulder_l": (-12, -4), "shoulder_r": (-11, -4),
        "chest_apron": (-12, -3), "hand_l": (-10, -3), "hand_r": (-8, 4),
        "apron_hem": (-10, -2),
        "vent_l": (-8, 0), "vent_r": (-7, 0), "curio_root": (-7, 0),
        "pelvis": (-8, -1), "hip_l": (-7, 0), "hip_r": (-5, 0),
        "knee_l": (-5, 0), "knee_r": (-3, 0),
        "foot_l": (-3, 0), "foot_r": (-1, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit, power=2.0, epsilon=4.0)
    hit_key = place_rotated_pivot(key_src, deg=-48, pivot=KEY_PIVOT, target=(26, 28), scale=0.94)
    hit_weapon = place_rotated_pivot(weapon_src, deg=-42, pivot=WEAPON_PIVOT, target=(92, 80), scale=0.92)

    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact starburst on chest (52, 68)
    ix, iy = 52, 68
    for pt in [(ix - 10, iy - 8), (ix + 10, iy - 8), (ix + 12, iy + 6), (ix - 8, iy + 10), (ix + 14, iy - 2), (ix - 12, iy + 2)]:
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
    # 6. RECOVER (重裝接地·三點制動卸勁 / Three-Point Shock Absorption Stance)
    # Low grounded landing crouch: body bows forward, absorbs impact (+2, +8).
    # Head and cowl sink down (+2, +8).
    # Torso compresses down (+2, +7), pelvis (+2, +5).
    # Feet plant wide in deep crouch (foot_l -4, foot_r +4).
    # Winding key re-engages into main drive (+20 deg, target=(42, 42), scale=0.98).
    # Weapon gathered close defensively (-18 deg, target=(92, 76), scale=1.04).
    # FX: Brake friction sparks on floor, steam puff rings.
    # =========================================================================
    rec_offsets = {
        "cowl_top": (2, 8), "horn_tip_l": (2, 8), "horn_tip_r": (2, 8),
        "horn_base_l": (2, 8), "horn_base_r": (2, 8),
        "cowl_cheek_l": (2, 8), "cowl_cheek_r": (2, 8),
        "visor_brow": (2, 8), "optic_l": (2, 8), "optic_r": (2, 8),
        "snout": (2, 8), "chin": (2, 8),
        "throat": (2, 7), "shoulder_l": (1, 7), "shoulder_r": (3, 7),
        "chest_apron": (2, 7), "hand_l": (-2, 7), "hand_r": (-3, 7),
        "apron_hem": (2, 6),
        "vent_l": (1, 6), "vent_r": (2, 6), "curio_root": (2, 5),
        "pelvis": (2, 5), "hip_l": (-4, 4), "hip_r": (4, 4),
        "knee_l": (-4, 3), "knee_r": (4, 3),
        "foot_l": (-4, 0), "foot_r": (4, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec, power=2.0, epsilon=4.0)
    rec_key = place_rotated_pivot(key_src, deg=20, pivot=KEY_PIVOT, target=(42, 42), scale=0.98)
    rec_weapon = place_rotated_pivot(weapon_src, deg=-18, pivot=WEAPON_PIVOT, target=(92, 76), scale=1.04)

    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for sx, sy in [(38, 28), (32, 24), (44, 22)]:
        r_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 210))
        r_draw.point((sx, sy), fill=(255, 208, 40, 240))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas.alpha_composite(rec_key)
    rec_canvas.alpha_composite(warped_rec_body)
    rec_canvas.alpha_composite(rec_weapon)
    rec_canvas.alpha_composite(rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def main():
    print("Generating The Obsidian Scarab combat action poses...")
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
    p_battle_128 = f"{PLAYER_DIR}/scarab_battle.png"
    p_battle_512 = f"{PLAYER_DIR}/scarab_battle_512.png"
    battle_128.save(p_battle_128)
    battle_512.save(p_battle_512)
    print(f"  ✓ Saved battle sprites: {p_battle_128} & {p_battle_512}")

    # Proof comparison: idle vs battle (256x128 & 1024x512)
    comp_proof = Image.new("RGBA", (256, 128), (24, 20, 36, 255))
    comp_proof.paste(poses["idle"], (0, 0), poses["idle"])
    comp_proof.paste(battle_128, (128, 0), battle_128)
    p_comp = f"{PLAYER_DIR}/proof_scarab_idle_vs_battle.png"
    comp_proof.save(p_comp)

    comp_proof_512 = Image.new("RGBA", (1024, 512), (24, 20, 36, 255))
    idle_512 = poses["idle"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    comp_proof_512.paste(idle_512, (0, 0), idle_512)
    comp_proof_512.paste(battle_512, (512, 0), battle_512)
    p_comp_512 = f"{PLAYER_DIR}/proof_scarab_idle_vs_battle_512.png"
    comp_proof_512.save(p_comp_512)
    print(f"  ✓ Saved idle vs battle proof cards: {p_comp} & {p_comp_512}")

    # Composite proof sheet (idle, telegraph, attack, skill, hit, recover)
    proof_strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_order = ['idle', 'telegraph', 'attack', 'skill', 'hit', 'recover']
    for idx, p_name in enumerate(proof_order):
        proof_strip.paste(poses[p_name], (idx * 128, 0), poses[p_name])

    proof_768_path = f"{PLAYER_DIR}/proof_scarab_combat_poses_768.png"
    proof_strip.save(proof_768_path)
    print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

    # Magenta background proof sheet for hole detection
    proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    proof_magenta.paste(proof_strip, (0, 0), proof_strip)
    proof_mag_path = f"{PLAYER_DIR}/proof_scarab_combat_poses_magenta.png"
    proof_magenta.save(proof_mag_path)
    print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")

    # Crop 8x hit core for 0-QA31
    hit_512 = poses["hit"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    core_crop = hit_512.crop((50 * 4, 55 * 4, 75 * 4, 80 * 4))
    crop_path = f"{PLAYER_DIR}/proof_scarab_hit_core_crop_8x.png"
    core_crop.save(crop_path)
    print(f"  ✓ Saved 0-QA31 core crop: {crop_path}")


if __name__ == "__main__":
    main()
