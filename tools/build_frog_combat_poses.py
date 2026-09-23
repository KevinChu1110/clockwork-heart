#!/usr/bin/env python3
"""
tools/build_frog_combat_poses.py
Generates the complete, definitive 6 combat action poses for Spring-Leg Frog (碧簧蛙, 12th Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/frog/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/frog/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/frog"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/frog"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_frog_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers
key_src = Image.open(f"{BASE_DIR}/winding_key/key_twin_wing_concentric.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_lotus_leaf_parasol.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/paint_frog_emerald.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_spring_frog_stock.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_spring_forest_courier.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/core_azure_aperture.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/wpn_lotus_cog_dart.png").convert("RGBA")

# Composite body without weapon layer
body_no_weapon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_no_weapon.alpha_composite(key_src)
body_no_weapon.alpha_composite(curio_src)
body_no_weapon.alpha_composite(chassis_src)
body_no_weapon.alpha_composite(head_src)
body_no_weapon.alpha_composite(costume_src)
body_no_weapon.alpha_composite(optic_src)

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
dart_raw = weapon_src.crop(wpn_bbox)

# Standardized ground contact shadow from baseline composite
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
assert s_px is not None and c_px is not None

for y in range(118, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p
        else:
            s_px[x, y] = (0, 0, 0, 0)

EXPECTED_SHADOW = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], s_px[x, y])[3] > 20) for y in range(118, 128)]
print(f"Benchmark ground shadow row counts (118..127): {EXPECTED_SHADOW}")

def enforce_ground_shadow(img: Image.Image) -> Image.Image:
    """Enforce exact ground contact shadow matching baseline Rule 4b-5 with zero halo/fringing."""
    out = img.copy()
    o_px = out.load()
    assert o_px is not None

    # Step 1: In ground shadow zone (118..127), strictly match baseline shadow pixels
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            o_px[x, y] = sp

    # Step 2: Clean margins strictly (L>=4, R>=4, T>=4, B>=2)
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
    return out

def place_dart(dart_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the Lotus Cog Dart with zero clipping."""
    b = dart_img.copy()
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
    "eye_l": (49, 29),
    "eye_r": (77, 29),
    "snout": (64, 42),
    "throat": (64, 52),
    "core": (63, 68),
    "shoulder_l": (36, 60),      # left shoulder (viewer's left)
    "shoulder_r": (80, 60),      # right shoulder (viewer's right)
    "arm_l": (26, 68),           # left hand holding parasol
    "arm_r": (92, 64),           # right hand holding dart
    "torso": (63, 72),
    "pelvis": (63, 84),
    "hip_l": (42, 88),
    "hip_r": (84, 88),
    "knee_l": (32, 98),
    "knee_r": (94, 98),
    "foot_l": (48, 116),
    "foot_r": (78, 116),
    "key_mount": (38, 48),
    "key_wing": (26, 25),
    "parasol_top": (18, 42),
    "parasol_mid": (17, 62),
    "parasol_bot": (16, 82),
}

def generate_poses():
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (Baseline stable poise, dart in left hand, parasol at right)
    # =========================================================================
    idle_canvas = body_no_weapon.copy()
    dart_idle = place_dart(dart_raw, deg=0, target_center=(94, 64), scale=1.0, mirror=False)
    idle_canvas = Image.alpha_composite(idle_canvas, dart_idle)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (碧簧蓄勁·極限彈簧深蹲 High-Tension Coiled Crouch)
    # Distinct frog silhouette: body drops y+12, knees flare far wide (x-12, x+12),
    # feet locked to ground (no tearing), dart pulled back to high shoulder
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-4, 12), "eye_l": (-4, 12), "eye_r": (-4, 12),
        "snout": (-4, 12), "throat": (-3, 12), "core": (-3, 12),
        "shoulder_l": (6, 10), "arm_l": (10, 6),       # Parasol hugs body
        "shoulder_r": (-9, 11), "arm_r": (-16, 4),     # Dart drawn back high
        "torso": (-3, 12), "pelvis": (-3, 12),
        "hip_l": (-8, 10), "hip_r": (6, 10),
        "knee_l": (-13, 8), "knee_r": (11, 8),         # Wide splayed frog crouch knees
        "foot_l": (-3, 0), "foot_r": (2, 0),           # Foot grounding locked
        "key_mount": (-4, 11), "key_wing": (-6, 8),
        "parasol_top": (9, 2), "parasol_mid": (10, 6), "parasol_bot": (8, 8),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Dart cocked back high near shoulder
    dart_tele = place_dart(dart_raw, deg=45, target_center=(76, 68), scale=1.05, mirror=False)

    # Concentric charging rings & spark lines around cocked dart (confined to y<=110)
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    t_draw.arc([58, 50, 94, 86], start=30, end=320, fill=(255, 208, 40, 230), width=2)
    t_draw.arc([54, 46, 98, 90], start=50, end=300, fill=(78, 216, 106, 210), width=2)
    t_draw.arc([62, 54, 90, 82], start=10, end=340, fill=(56, 160, 255, 220), width=1)
    # High-tension spring compression spark points
    t_draw.point([(76, 52), (80, 82), (64, 68), (88, 68), (60, 56), (92, 76), (68, 80), (84, 54)], fill=(255, 255, 255, 255))
    t_draw.line([(76, 52), (92, 76)], fill=(255, 208, 40, 160), width=1)
    t_draw.line([(60, 56), (84, 54)], fill=(78, 216, 106, 180), width=1)
    # Twin-wing winding key rapid spin aura
    t_draw.arc([12, 18, 36, 42], start=15, end=345, fill=(255, 208, 40, 210), width=2)
    t_draw.arc([8, 14, 40, 46], start=45, end=315, fill=(56, 160, 255, 180), width=1)
    # Azure aperture core intense cyan pulse
    t_draw.ellipse([54, 76, 68, 90], fill=(56, 160, 255, 190))
    t_draw.ellipse([57, 79, 65, 87], fill=(255, 255, 255, 220))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.6))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, dart_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (簧力疾躍·蓮齒飛擲 Explosive Forward Leap & Dart Throw)
    # Distinct dynamic silhouette: full body lunges forward x+15,
    # rear leg extends back, arm throws dart forward-right (margins safe <=124)
    # =========================================================================
    shifts_attack = {
        "head_top": (14, -2), "eye_l": (15, -2), "eye_r": (15, -2),
        "snout": (17, -1), "throat": (16, -1), "core": (15, -1),
        "shoulder_l": (-8, 1), "arm_l": (-15, 3),      # Parasol swings back for counterweight
        "shoulder_r": (16, -2), "arm_r": (22, -3),     # Dart arm fully extended
        "torso": (13, -1), "pelvis": (10, -1),
        "hip_l": (-8, 0), "hip_r": (14, -1),
        "knee_l": (-14, 0), "knee_r": (16, -2),        # Rear leg stretches back, lead leg forward
        "foot_l": (-9, 0), "foot_r": (9, 0),
        "key_mount": (10, -1), "key_wing": (8, -2),
        "parasol_top": (-12, -3), "parasol_mid": (-10, 1), "parasol_bot": (-8, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Dart launched forward-right (margins: right edge strictly <= 123)
    dart_attack = place_dart(dart_raw, deg=-32, target_center=(105, 59), scale=1.03, mirror=False)

    # Piercing emerald/cyan supersonic shockwave & kinetic streaks (confined y<=110)
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Supersonic propulsion trail
    a_draw.line([(94, 59), (122, 57)], fill=(78, 216, 106, 240), width=3)
    a_draw.line([(96, 59), (123, 57)], fill=(255, 255, 255, 255), width=1)
    # Expanding kinetic pressure cone in front of dart
    a_draw.arc([102, 45, 122, 73], start=275, end=85, fill=(56, 160, 255, 220), width=2)
    a_draw.arc([106, 43, 122, 75], start=280, end=80, fill=(255, 208, 40, 230), width=2)
    # Spring recoil back-blast wind lines
    a_draw.line([(32, 72), (12, 76)], fill=(135, 240, 160, 180), width=2)
    a_draw.line([(28, 76), (10, 82)], fill=(56, 160, 255, 160), width=2)
    # Friction sparks
    a_draw.ellipse([98, 55, 106, 63], fill=(255, 255, 220, 255))
    a_draw.point([(108, 51), (105, 67), (114, 53), (109, 63), (118, 51)], fill=(255, 208, 40, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.5))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, dart_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (九曲蓮簧·騰空天樞陣 High-Ascendant Lotus Channelling)
    # Distinct aerial silhouette: full body lifts y-10, legs tuck in airborne frog pose,
    # arms spread wide holding dart & parasol high, elegant circular mandala (no ground cutoff)
    # =========================================================================
    shifts_skill = {
        "head_top": (0, -10), "eye_l": (0, -10), "eye_r": (0, -10),
        "snout": (0, -9), "throat": (0, -8), "core": (0, -7),
        "shoulder_l": (-11, -8), "arm_l": (-17, -11), # Left arm & parasol flared high left
        "shoulder_r": (12, -8), "arm_r": (18, -10),   # Dart hand held high overhead
        "torso": (0, -7), "pelvis": (0, -6),
        "hip_l": (-5, -5), "hip_r": (5, -5),
        "knee_l": (-7, -6), "knee_r": (7, -6),         # Legs tucked up in midair hop
        "foot_l": (-4, -6), "foot_r": (4, -6),
        "key_mount": (-1, -5), "key_wing": (-2, -7),
        "parasol_top": (-12, -12), "parasol_mid": (-13, -8), "parasol_bot": (-9, -4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Dart channeled high-right overhead
    dart_skill = place_dart(dart_raw, deg=48, target_center=(98, 41), scale=1.06, mirror=False)

    # Lotus Wheel array & floating petal runes (kept strictly y: 16..108, completely above ground!)
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    # Concentric celestial lotus orbit rings (safely contained inside canvas)
    s_draw.arc([18, 18, 118, 96], start=140, end=350, fill=(78, 216, 106, 220), width=3)
    s_draw.arc([24, 22, 112, 90], start=150, end=330, fill=(56, 160, 255, 230), width=2)
    s_draw.arc([32, 26, 104, 84], start=160, end=310, fill=(255, 208, 40, 240), width=1)
    # Floating lotus gear petal runes
    s_draw.polygon([(110, 28), (118, 24), (112, 32)], fill=(255, 255, 255, 255))
    s_draw.polygon([(20, 58), (12, 64), (22, 66)], fill=(78, 216, 106, 230))
    s_draw.polygon([(90, 16), (98, 12), (92, 20)], fill=(56, 160, 255, 230))
    s_draw.polygon([(18, 34), (26, 28), (24, 38)], fill=(255, 208, 40, 240))
    # Airborne energy shimmer lines (y <= 108)
    s_draw.line([(44, 98), (84, 98)], fill=(135, 240, 160, 180), width=2)
    s_draw.line([(50, 103), (78, 103)], fill=(56, 160, 255, 160), width=1)
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.7))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, dart_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (金屬重擊·大幅後仰失衡 Heavy Impact Stagger & Shield Parry)
    # Distinct recoil silhouette: head/torso pitches far back x-16, y-3,
    # body tilts off-balance, dart parries defensively across chest,
    # crisp spark flashes & relief vent steam lines (no weird white circles)
    # =========================================================================
    shifts_hit = {
        "head_top": (-16, -3), "eye_l": (-16, -3), "eye_r": (-16, -3),
        "snout": (-15, -1), "throat": (-14, -1), "core": (-13, 0),
        "shoulder_l": (-12, 1), "arm_l": (-8, 3),       # Parasol flails back
        "shoulder_r": (-11, 0), "arm_r": (-12, 0),      # Dart arm pulled defensively across chest
        "torso": (-11, 1), "pelvis": (-9, 1),
        "hip_l": (-11, 1), "hip_r": (-6, 1),
        "knee_l": (-12, 0), "knee_r": (-6, 0),
        "foot_l": (-8, 0), "foot_r": (-4, 0),
        "key_mount": (-13, 0), "key_wing": (-13, -2),
        "parasol_top": (-15, 6), "parasol_mid": (-13, 5), "parasol_bot": (-9, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Dart held across chest in emergency parry posture
    dart_hit = place_dart(dart_raw, deg=40, target_center=(68, 64), scale=0.96, mirror=False)

    # Crisp metallic deflection spark flashes & directional steam exhaust lines (no blob circles)
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Sharp cross-star impact flash at parry center
    cx, cy = 68, 64
    h_draw.line([(cx - 14, cy), (cx + 14, cy)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx, cy - 14), (cx, cy + 14)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx - 8, cy - 8), (cx + 8, cy + 8)], fill=(255, 208, 40, 220), width=1)
    h_draw.line([(cx - 8, cy + 8), (cx + 8, cy - 8)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255, 255))
    h_draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=0, end=360, fill=(255, 208, 40, 180), width=2)
    # Kinetic spark points
    h_draw.point([(cx - 12, cy - 10), (cx + 14, cy - 8), (cx + 12, cy + 12), (cx - 10, cy + 14)], fill=(255, 255, 220, 255))
    # Linear steam exhaust venting jets from back joints (crisp lines, not circular patches)
    h_draw.line([(32, 38), (18, 30)], fill=(240, 248, 255, 200), width=2)
    h_draw.line([(30, 42), (14, 38)], fill=(220, 235, 250, 170), width=1)
    h_draw.line([(34, 46), (20, 48)], fill=(220, 235, 250, 160), width=1)
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.5))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, dart_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (定神復位·單側沉著回穩 Solid Grounded Restabilization)
    # Distinct grounded silhouette: torso sinks into solid low stance (y+7),
    # parasol firmly planted on left for balance, dart at waist ready position
    # =========================================================================
    shifts_recover = {
        "head_top": (4, 7), "eye_l": (4, 7), "eye_r": (4, 7),
        "snout": (4, 8), "throat": (4, 8), "core": (4, 8),
        "shoulder_l": (-6, 7), "arm_l": (-10, 8),      # Parasol grounded firmly
        "shoulder_r": (7, 7), "arm_r": (9, 8),
        "torso": (4, 8), "pelvis": (4, 8),
        "hip_l": (-7, 7), "hip_r": (8, 7),
        "knee_l": (-9, 6), "knee_r": (9, 6),
        "foot_l": (-5, 0), "foot_r": (7, 0),           # Feet locked to ground
        "key_mount": (4, 7), "key_wing": (4, 6),
        "parasol_top": (6, 5), "parasol_mid": (6, 6), "parasol_bot": (6, 6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_recover = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Dart held firmly at side waist
    dart_recover = place_dart(dart_raw, deg=-20, target_center=(92, 76), scale=0.98, mirror=False)

    # Ground settling shimmer lines & calming optic core pulse (confined y<=110)
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Ground settling ripples (y <= 110)
    r_draw.arc([36, 96, 92, 110], start=15, end=165, fill=(78, 216, 106, 180), width=2)
    r_draw.arc([42, 100, 86, 110], start=25, end=155, fill=(56, 160, 255, 160), width=1)
    # Linear steam dissipating jets
    r_draw.line([(24, 46), (14, 42)], fill=(220, 235, 250, 160), width=1)
    r_draw.line([(84, 76), (96, 72)], fill=(220, 235, 250, 150), width=1)
    # Calming cyan/yellow pulse at optic core
    r_draw.ellipse([58, 71, 70, 83], fill=(56, 160, 255, 160))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.6))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, warped_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, dart_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING SPRING FROG 6 COMBAT ACTION POSES ===")
    poses = generate_poses()

    for p_name, img in poses.items():
        dst_128 = os.path.join(OUT_DIR, f"{p_name}.png")
        img.save(dst_128, format="PNG")

        # 512 LANCZOS upscale
        dst_512 = os.path.join(OUT_DIR, f"{p_name}_512.png")
        img_512 = img.resize((512, 512), resample=Image.Resampling.LANCZOS)
        img_512.save(dst_512, format="PNG")

        bbox = img.getbbox()
        print(f"✓ Saved {p_name:10s} -> {dst_128} (128x128, bbox={bbox}) and {dst_512} (512x512)")

    # Generate proof sheets
    # 1. 768-wide strip (all 6 poses in a row: 128 x 6 = 768)
    pose_order = ["idle", "telegraph", "attack", "skill", "hit", "recover"]
    strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    for i, p_name in enumerate(pose_order):
        strip.paste(poses[p_name], (i * 128, 0))

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_frog_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    # 2. Magenta background proof sheet
    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_frog_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
    print("\nAll 6 frog combat poses successfully generated and saved!")
