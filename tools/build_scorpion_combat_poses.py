#!/usr/bin/env python3
"""
tools/build_scorpion_combat_poses.py
Generates the complete, definitive combat action poses for The Duneshadow Scorpion (第七十族 伏影沙蠍, scorpion)
in Clockwork Heart:
  game/assets/sprites/player/poses/scorpion/{idle,telegraph,attack,recover,skill,hit,walk,defeat}.png (128x128 RGBA)
  game/assets/sprites/player/poses/scorpion/{idle,telegraph,attack,recover,skill,hit,walk,defeat}_512.png (512x512 RGBA, LANCZOS)
Also generates copies/symlinks in:
  game/assets/sprites/player/paperdoll/scorpion/{idle,telegraph,attack,recover,skill,hit,walk,defeat}.png & _512.png
Also generates:
  game/assets/sprites/player/scorpion_battle.png & scorpion_battle_512.png (battle == attack per review.md 4b-8-1)
  game/assets/sprites/player/proof_scorpion_idle_vs_battle.png & proof_scorpion_idle_vs_battle_512.png
  game/assets/sprites/player/proof_scorpion_combat_poses_768.png & proof_scorpion_combat_poses_magenta.png
  game/assets/sprites/player/proof_scorpion_hit_core_crop_8x.png
Follows CANON.md, art_direction.md, DUNESHADOW_SCORPION_DESIGN_PROPOSAL.md, and review.md quality gates:
  - 0-QA16 / 0-QA21 / 0-QA31 / 0-QA34 / 0-QA39
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
"""

import math
import os
import sys
from typing import cast
from PIL import Image, ImageDraw, ImageOps
import numpy as np

sys.path = [p for p in sys.path if not p.startswith('/tmp')]

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/scorpion"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/scorpion"
PAPERDOLL_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/scorpion"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PAPERDOLL_DIR, exist_ok=True)
os.makedirs(PLAYER_DIR, exist_ok=True)

# 1. Load canonical components (128x128 RGBA)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_scorpion_cross_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_scorpion_spring_stinger_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_scorpion_stock.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_scorpion_dune_visor.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_scorpion_scavenger_plate.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_scorpion_amber_goggles.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_scorpion_duneshadow_dart.png").convert("RGBA")

# Extract ground shadow master from party/scorpion_idle.png
ref_shadow_im = Image.open(f"{PLAYER_DIR}/party/scorpion_idle.png").convert("RGBA")
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

    # Clean stray low-alpha fringe pixels (< 20 alpha in body zone) to avoid dirty halos
    for y in range(0, 118):
        for x in range(0, 128):
            p = cast(tuple[int, int, int, int], o_px[x, y])
            if 0 < p[3] < 20:
                o_px[x, y] = (0, 0, 0, 0)

    # Sanitize dark falloff (ultra-dark pixels) to canon dark outline (#1F1A3A)
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


# Canonical pivots on original 128x128 elements for The Duneshadow Scorpion
KEY_PIVOT = (64.0, 46.0)     # Brass cross-cog key center
CURIO_PIVOT = (50.0, 76.0)   # Spring stinger tail base
HEAD_PIVOT = (64.0, 42.0)    # Dune-visor cowl dome center
TORSO_PIVOT = (64.0, 74.0)   # Tinplate chassis & cuirass center
WEAPON_PIVOT = (102.0, 68.0) # Gyro dart hub center

# Modular groups
head_group = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
head_group.alpha_composite(head_src)
head_group.alpha_composite(optic_src)

torso_group = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
torso_group.alpha_composite(chassis_src)
torso_group.alpha_composite(costume_src)


def draw_clean_spark(draw: ImageDraw.ImageDraw, x: int, y: int, color_core=(255, 253, 248, 255), color_edge=(255, 208, 40, 220)):
    """Draws a crisp, anti-aliased cross-star glint without blurry halo artifacts."""
    draw.point((x, y), fill=color_core)
    draw.point((x - 1, y), fill=color_edge)
    draw.point((x + 1, y), fill=color_edge)
    draw.point((x, y - 1), fill=color_edge)
    draw.point((x, y + 1), fill=color_edge)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (伏影潛沙·低重心待機 / Duneshadow Ready Posture)
    # Neutral, poised, balanced ready posture with subtle toy breathing articulation.
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=0.4, pivot=KEY_PIVOT, target=(64.0, 46.0), scale=1.0)
    p_curio = place_rotated_pivot(curio_src, deg=-0.5, pivot=CURIO_PIVOT, target=(50.0, 76.0), scale=1.0)
    p_torso = place_rotated_pivot(torso_group, deg=0.2, pivot=TORSO_PIVOT, target=(64.0, 74.0), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=-0.3, pivot=HEAD_PIVOT, target=(64.0, 42.0), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=0.3, pivot=WEAPON_PIVOT, target=(102.0, 68.0), scale=1.0)

    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas.alpha_composite(p_key)
    idle_canvas.alpha_composite(p_curio)
    idle_canvas.alpha_composite(p_torso)
    idle_canvas.alpha_composite(p_head)
    idle_canvas.alpha_composite(p_weapon)

    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    # Eye sparkles
    draw_clean_spark(i_draw, 54, 42, color_core=(255, 255, 255, 255), color_edge=(255, 208, 40, 220))
    draw_clean_spark(i_draw, 74, 42, color_core=(255, 255, 255, 255), color_edge=(255, 208, 40, 220))
    # Key glints
    draw_clean_spark(i_draw, 64, 34, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 200))
    draw_clean_spark(i_draw, 76, 46, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 200))
    # Weapon & Stinger apex glints
    draw_clean_spark(i_draw, 102, 68, color_core=(255, 255, 255, 255), color_edge=(78, 216, 106, 220))
    draw_clean_spark(i_draw, 38, 22, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 200))
    idle_canvas.alpha_composite(idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (彈簧收攏·琉璃測距鎖定 / Spring Windup & Amber Quartz Targeting)
    # Deep draw crouch: Torso sinks down (y+5, x-3, deg=-4).
    # Head tucks low to protect chassis (y+6, x-4, deg=-6).
    # Stinger tail curves back tightly (deg=-15, target=(44, 74), scale=0.96).
    # Key counter-winds with high spring torque (-36 deg, target=(58.0, 40.0), scale=0.96).
    # Gyro dart cocked back: deg=-24, target=(92.0, 66.0), scale=1.04.
    # FX: Concentric amber & mint green targeting reticle at (106, 50).
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=-36, pivot=KEY_PIVOT, target=(58.0, 40.0), scale=0.96)
    p_curio = place_rotated_pivot(curio_src, deg=-15, pivot=CURIO_PIVOT, target=(44.0, 74.0), scale=0.96)
    p_torso = place_rotated_pivot(torso_group, deg=-4, pivot=TORSO_PIVOT, target=(61.0, 76.0), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=-6, pivot=HEAD_PIVOT, target=(60.0, 45.0), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=-24, pivot=WEAPON_PIVOT, target=(92.0, 66.0), scale=1.04)

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas.alpha_composite(p_key)
    tele_canvas.alpha_composite(p_curio)
    tele_canvas.alpha_composite(p_torso)
    tele_canvas.alpha_composite(p_head)
    tele_canvas.alpha_composite(p_weapon)

    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    cx, cy = 106, 50
    t_draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(255, 208, 40, 220), width=1)
    t_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=(78, 216, 106, 230), width=1)
    t_draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(255, 208, 40, 240), width=1)
    draw_clean_spark(t_draw, cx, cy, color_core=(255, 255, 255, 255), color_edge=(255, 208, 40, 240))
    draw_clean_spark(t_draw, 58, 40, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 220))
    tele_canvas.alpha_composite(tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK / BATTLE (疾影穿沙·甩鏢疾射 / Duneshadow Dart Throw Release)
    # Violent lunge forward-right: Torso leans aggressively forward (deg=+10, target=(74.0, 73.0)).
    # Head thrusts forward with visor aim (deg=+12, target=(76.0, 41.0)).
    # Stinger tail arches high to counter balance (deg=+20, target=(60.0, 72.0), scale=1.06).
    # Gyro dart released forward with high velocity: deg=+28, target=(104.0, 62.0), scale=1.06.
    # Winding key spins forward (+45 deg, target=(68.0, 36.0), scale=1.04).
    # Aerodynamic thrust trail & tungsten tip projectile!
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=45, pivot=KEY_PIVOT, target=(68.0, 36.0), scale=1.04)
    p_curio = place_rotated_pivot(curio_src, deg=20, pivot=CURIO_PIVOT, target=(60.0, 72.0), scale=1.06)
    p_torso = place_rotated_pivot(torso_group, deg=10, pivot=TORSO_PIVOT, target=(74.0, 73.0), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=12, pivot=HEAD_PIVOT, target=(76.0, 41.0), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=28, pivot=WEAPON_PIVOT, target=(104.0, 62.0), scale=1.06)

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas.alpha_composite(p_key)
    atk_canvas.alpha_composite(p_curio)
    atk_canvas.alpha_composite(p_torso)
    atk_canvas.alpha_composite(p_head)
    atk_canvas.alpha_composite(p_weapon)

    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Dart speed trajectory line
    a_draw.line([(80, 62), (120, 62)], fill=(255, 160, 16, 245), width=3)
    a_draw.line([(88, 62), (122, 62)], fill=(255, 255, 255, 255), width=1)
    # Tungsten piercing tip wedge polygon
    a_draw.polygon([(122, 62), (114, 57), (116, 62), (114, 67)], fill=(255, 208, 40, 255))
    # Muzzle / release flash sparks
    draw_clean_spark(a_draw, 122, 62, color_core=(255, 255, 255, 255), color_edge=(255, 208, 40, 240))
    draw_clean_spark(a_draw, 68, 36, color_core=(255, 255, 255, 255), color_edge=(255, 94, 138, 220))
    draw_clean_spark(a_draw, 82, 62, color_core=(255, 255, 255, 255), color_edge=(78, 216, 106, 240))
    atk_canvas.alpha_composite(atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. RECOVER (落沙減震·流體緩衝接地 / Shock Absorption Brake & Cushion Landing)
    # Low grounded landing crouch: body absorbs recoil (+1, +4, deg=+2).
    # Head and cowl sink down (+1, +6).
    # Tail drops low to brace against dust (deg=-8, target=(48.0, 78.0), scale=1.02).
    # Key re-engages into main drive (+16 deg, target=(64.0, 44.0), scale=0.98).
    # Gyro dart lowered into ready hold: deg=-16, target=(96.0, 75.0), scale=1.0.
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=16, pivot=KEY_PIVOT, target=(64.0, 44.0), scale=0.98)
    p_curio = place_rotated_pivot(curio_src, deg=-8, pivot=CURIO_PIVOT, target=(48.0, 78.0), scale=1.02)
    p_torso = place_rotated_pivot(torso_group, deg=2, pivot=TORSO_PIVOT, target=(64.0, 78.0), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=3, pivot=HEAD_PIVOT, target=(65.0, 48.0), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=-16, pivot=WEAPON_PIVOT, target=(96.0, 75.0), scale=1.0)

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas.alpha_composite(p_key)
    rec_canvas.alpha_composite(p_curio)
    rec_canvas.alpha_composite(p_torso)
    rec_canvas.alpha_composite(p_head)
    rec_canvas.alpha_composite(p_weapon)

    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    draw_clean_spark(r_draw, 64, 44, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 210))
    rec_canvas.alpha_composite(rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    # =========================================================================
    # 5. SKILL (奧義·沙暴萬鏢齊射·齒輪過載 / Dune Maelstrom Overdrive Barrage)
    # Majestic upward surge: Torso lifts up (deg=0, target=(64.0, 68.0)).
    # Head looks skyward with martial focus (deg=-10, target=(64.0, 34.0)).
    # Stinger tail spreads wide with full rail extension (deg=0, target=(52.0, 66.0), scale=1.16)!
    # Gyro dart raised overhead (-48 deg, target=(102.0, 48.0), scale=1.14).
    # Winding key reaches supercharged torque (+72 deg, target=(64.0, 30.0), scale=1.10).
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=72, pivot=KEY_PIVOT, target=(64.0, 30.0), scale=1.10)
    p_curio = place_rotated_pivot(curio_src, deg=0, pivot=CURIO_PIVOT, target=(52.0, 66.0), scale=1.16)
    p_torso = place_rotated_pivot(torso_group, deg=0, pivot=TORSO_PIVOT, target=(64.0, 68.0), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=-10, pivot=HEAD_PIVOT, target=(64.0, 34.0), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=-48, pivot=WEAPON_PIVOT, target=(102.0, 48.0), scale=1.14)

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas.alpha_composite(p_key)
    skill_canvas.alpha_composite(p_curio)
    skill_canvas.alpha_composite(p_torso)
    skill_canvas.alpha_composite(p_head)
    skill_canvas.alpha_composite(p_weapon)

    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    draw_clean_spark(s_draw, 64, 30, color_core=(255, 255, 255, 255), color_edge=(255, 94, 138, 220))
    draw_clean_spark(s_draw, 50, 16, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 220))
    draw_clean_spark(s_draw, 78, 16, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 220))
    draw_clean_spark(s_draw, 102, 42, color_core=(255, 255, 255, 255), color_edge=(56, 160, 255, 240))
    draw_clean_spark(s_draw, 36, 42, color_core=(255, 253, 248, 255), color_edge=(78, 216, 106, 230))
    skill_canvas.alpha_composite(skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 6. HIT (金屬震退·雙鉗護體格擋 / Kinetic Deflection & Shock Recoil)
    # Violent backward displacement: Torso knocked back-left (deg=-10, target=(54.0, 76.0)).
    # Head snapped hard back-left (deg=-18, target=(52.0, 38.0)).
    # Tail folded forward to protect back key (deg=-24, target=(46.0, 72.0), scale=0.94).
    # Key disengages violently (-45 deg, target=(50.0, 36.0), scale=0.92).
    # Gyro dart held defensively across torso: deg=+36, target=(84.0, 68.0), scale=0.98).
    # FX: Clean deflection cross-star spark on armor plate.
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=-45, pivot=KEY_PIVOT, target=(50.0, 36.0), scale=0.92)
    p_curio = place_rotated_pivot(curio_src, deg=-24, pivot=CURIO_PIVOT, target=(46.0, 72.0), scale=0.94)
    p_torso = place_rotated_pivot(torso_group, deg=-10, pivot=TORSO_PIVOT, target=(54.0, 76.0), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=-18, pivot=HEAD_PIVOT, target=(52.0, 38.0), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=36, pivot=WEAPON_PIVOT, target=(84.0, 68.0), scale=0.98)

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas.alpha_composite(p_key)
    hit_canvas.alpha_composite(p_curio)
    hit_canvas.alpha_composite(p_torso)
    hit_canvas.alpha_composite(p_head)
    hit_canvas.alpha_composite(p_weapon)

    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 68, 68
    h_draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx - 6, cy - 6), (cx + 6, cy + 6)], fill=(78, 216, 106, 220), width=1)
    h_draw.line([(cx - 6, cy + 6), (cx + 6, cy - 6)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255, 255))
    draw_clean_spark(h_draw, 50, 36, color_core=(255, 250, 185, 240), color_edge=(255, 94, 138, 220))
    hit_canvas.alpha_composite(hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 7. WALK (沙丘疾馳·六足踏步 / Sand Dunes Sprint Walk Cycle)
    # Streamlined crawl: Torso leans slightly forward (deg=+6, target=(68.0, 74.0)).
    # Head low and focused (deg=+6, target=(69.0, 42.0)).
    # Stinger tail aligns with torso streamline (deg=+8, target=(54.0, 75.0), scale=1.02).
    # Key rotates steadily (deg=+20, target=(66.0, 42.0), scale=1.0).
    # Dart balanced in front: deg=+10, target=(100.0, 67.0), scale=1.0.
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=20, pivot=KEY_PIVOT, target=(66.0, 42.0), scale=1.0)
    p_curio = place_rotated_pivot(curio_src, deg=8, pivot=CURIO_PIVOT, target=(54.0, 75.0), scale=1.02)
    p_torso = place_rotated_pivot(torso_group, deg=6, pivot=TORSO_PIVOT, target=(68.0, 74.0), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=6, pivot=HEAD_PIVOT, target=(69.0, 42.0), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=10, pivot=WEAPON_PIVOT, target=(100.0, 67.0), scale=1.0)

    walk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    walk_canvas.alpha_composite(p_key)
    walk_canvas.alpha_composite(p_curio)
    walk_canvas.alpha_composite(p_torso)
    walk_canvas.alpha_composite(p_head)
    walk_canvas.alpha_composite(p_weapon)

    walk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    w_draw = ImageDraw.Draw(walk_fx)
    draw_clean_spark(w_draw, 56, 42, color_core=(255, 255, 255, 255), color_edge=(255, 208, 40, 220))
    walk_canvas.alpha_composite(walk_fx)
    poses["walk"] = enforce_ground_shadow(walk_canvas)

    # =========================================================================
    # 8. DEFEAT (發條停拍·休眠鎖定 / Winding Key Lockdown Sleeping Posture)
    # Slumped sideways: Torso tilts back-down (deg=-14, target=(56.0, 80.0), scale=0.96).
    # Head drops down (deg=-22, target=(54.0, 52.0), scale=0.96).
    # Tail lies limp on ground (deg=-35, target=(42.0, 78.0), scale=0.92).
    # Key disengages & locks: deg=0, target=(52.0, 48.0), scale=0.92.
    # Dart rests quietly on ground: deg=+45, target=(90.0, 84.0), scale=0.96.
    # Zero gore, 100% sleeping clockwork toy.
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(52.0, 48.0), scale=0.92)
    p_curio = place_rotated_pivot(curio_src, deg=-35, pivot=CURIO_PIVOT, target=(42.0, 78.0), scale=0.92)
    p_torso = place_rotated_pivot(torso_group, deg=-14, pivot=TORSO_PIVOT, target=(56.0, 80.0), scale=0.96)
    p_head = place_rotated_pivot(head_group, deg=-22, pivot=HEAD_PIVOT, target=(54.0, 52.0), scale=0.96)
    p_weapon = place_rotated_pivot(weapon_src, deg=45, pivot=WEAPON_PIVOT, target=(90.0, 84.0), scale=0.96)

    def_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    def_canvas.alpha_composite(p_key)
    def_canvas.alpha_composite(p_curio)
    def_canvas.alpha_composite(p_torso)
    def_canvas.alpha_composite(p_head)
    def_canvas.alpha_composite(p_weapon)
    poses["defeat"] = enforce_ground_shadow(def_canvas)

    return poses


def main():
    print("Generating The Duneshadow Scorpion combat action poses...")
    poses = generate_poses()

    all_poses = ['idle', 'telegraph', 'attack', 'recover', 'skill', 'hit', 'walk', 'defeat']
    for p_name in all_poses:
        im = poses[p_name]
        # In poses/scorpion/
        path_128 = f"{OUT_DIR}/{p_name}.png"
        im.save(path_128)
        print(f"  ✓ Saved 128x128: {path_128}")

        # In paperdoll/scorpion/ (per task prompt)
        path_pd_128 = f"{PAPERDOLL_DIR}/{p_name}.png"
        im.save(path_pd_128)

        # Generate 512x512 with LANCZOS
        im_512 = im.resize((512, 512), resample=Image.Resampling.LANCZOS)
        path_512 = f"{OUT_DIR}/{p_name}_512.png"
        im_512.save(path_512)
        print(f"  ✓ Saved 512x512 LANCZOS: {path_512}")

        path_pd_512 = f"{PAPERDOLL_DIR}/{p_name}_512.png"
        im_512.save(path_pd_512)

    # Official Battle Sprite (battle == attack per review.md 4b-8-1)
    battle_128 = poses["attack"]
    battle_512 = battle_128.resize((512, 512), resample=Image.Resampling.LANCZOS)
    p_battle_128 = f"{PLAYER_DIR}/scorpion_battle.png"
    p_battle_512 = f"{PLAYER_DIR}/scorpion_battle_512.png"
    battle_128.save(p_battle_128)
    battle_512.save(p_battle_512)
    print(f"  ✓ Saved battle sprites: {p_battle_128} & {p_battle_512}")

    # Proof comparison: idle vs battle (256x128 & 1024x512)
    comp_proof = Image.new("RGBA", (256, 128), (24, 20, 36, 255))
    comp_proof.paste(poses["idle"], (0, 0), poses["idle"])
    comp_proof.paste(battle_128, (128, 0), battle_128)
    p_comp = f"{PLAYER_DIR}/proof_scorpion_idle_vs_battle.png"
    comp_proof.save(p_comp)

    comp_proof_512 = Image.new("RGBA", (1024, 512), (24, 20, 36, 255))
    idle_512 = poses["idle"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    comp_proof_512.paste(idle_512, (0, 0), idle_512)
    comp_proof_512.paste(battle_512, (512, 0), battle_512)
    p_comp_512 = f"{PLAYER_DIR}/proof_scorpion_idle_vs_battle_512.png"
    comp_proof_512.save(p_comp_512)
    print(f"  ✓ Saved idle vs battle proof cards: {p_comp} & {p_comp_512}")

    # Composite proof sheet (idle, telegraph, attack, skill, hit, recover)
    proof_strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_order = ['idle', 'telegraph', 'attack', 'skill', 'hit', 'recover']
    for idx, p_name in enumerate(proof_order):
        proof_strip.paste(poses[p_name], (idx * 128, 0), poses[p_name])

    proof_768_path = f"{PLAYER_DIR}/proof_scorpion_combat_poses_768.png"
    proof_strip.save(proof_768_path)
    print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

    # Magenta background proof sheet for hole detection
    proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    proof_magenta.paste(proof_strip, (0, 0), proof_strip)
    proof_mag_path = f"{PLAYER_DIR}/proof_scorpion_combat_poses_magenta.png"
    proof_magenta.save(proof_mag_path)
    print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")

    # Crop 8x hit core for 0-QA31
    hit_512 = poses["hit"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    core_crop = hit_512.crop((50 * 4, 55 * 4, 75 * 4, 80 * 4))
    crop_path = f"{PLAYER_DIR}/proof_scorpion_hit_core_crop_8x.png"
    core_crop.save(crop_path)
    print(f"  ✓ Saved 0-QA31 core crop: {crop_path}")


if __name__ == "__main__":
    main()
