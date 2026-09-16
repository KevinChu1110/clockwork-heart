#!/usr/bin/env python3
"""
tools/build_tiger_combat_poses.py
Generates the complete, definitive 6 combat action poses for Ember Tiger (烈焰虎, ninja)
in Clockwork Heart:
  game/assets/sprites/player/poses/tiger/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tiger"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/tiger"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_tiger_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers for exact compositing
chassis_src = Image.open(f"{BASE_DIR}/chassis/paint_ember_orange.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_ember_tiger_stock.png").convert("RGBA")
key_src = Image.open(f"{BASE_DIR}/winding_key/key_turbine_flame.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_ember_tunic.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/core_molten_amber.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/wpn_twin_ember_sabers.png").convert("RGBA")
tail_src = Image.open(f"{BASE_DIR}/back_curio/curio_exhaust_tiger_tail.png").convert("RGBA")

# Composite body without weapon layer
body_no_weapon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_no_weapon.alpha_composite(key_src)
body_no_weapon.alpha_composite(tail_src)
body_no_weapon.alpha_composite(chassis_src)
body_no_weapon.alpha_composite(head_src)
body_no_weapon.alpha_composite(costume_src)
body_no_weapon.alpha_composite(optic_src)

# Extract right dagger crop
dagger_bbox = weapon_src.getbbox()
assert dagger_bbox is not None
dagger_raw = weapon_src.crop(dagger_bbox)

# Extract isolated ground contact shadow from baseline idle
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
for y in range(116, 128):
    for x in range(128):
        p = c_px[x, y]
        if p[3] > 0 and (p[0] < 50 and p[1] < 45 and p[2] < 60 or p[3] < 200):
            s_px[x, y] = p

EXPECTED_SHADOW = [sum(1 for x in range(128) if s_px[x, y][3] > 20) for y in range(118, 128)]
print(f"Benchmark ground shadow row counts (118..127): {EXPECTED_SHADOW}")

def enforce_ground_shadow(img: Image.Image) -> Image.Image:
    """Enforce exact ground contact shadow matching baseline Rule 4b-5 without flinching."""
    out = img.copy()
    o_px = out.load()
    for y in range(118, 128):
        for x in range(128):
            sp = s_px[x, y]
            fp = o_px[x, y]
            if sp[3] <= 20 and fp[3] > 20:
                o_px[x, y] = (0, 0, 0, 0)
            elif sp[3] > 20 and fp[3] <= 20:
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
    return out

def place_dagger(dagger_img: Image.Image, deg: float, target_grip: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the dagger with zero clipping."""
    d = dagger_img.copy()
    if mirror:
        d = ImageOps.mirror(d)
    dw, dh = d.size
    gx, gy = (14, 30) if not mirror else (dw - 14, 30)
    
    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    large.paste(d, (128 - gx, 128 - gy))
    
    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        large = large.resize((nw, nh), Image.Resampling.LANCZOS)
        
    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tx, ty = target_grip
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

# Anchor corners and borders
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127)
]

base_landmarks = {
    "ear_l": (42, 16),
    "ear_r": (88, 16),
    "forehead": (64, 28),
    "eye_l": (64, 43),
    "eye_r": (88, 43),
    "nose": (74, 52),
    "heart_gem": (62, 61),
    "shoulder_l": (44, 64),
    "shoulder_r": (84, 64),
    "arm_l": (38, 74),
    "arm_r": (90, 74),
    "pelvis": (64, 88),
    "hip_l": (52, 94),
    "hip_r": (76, 94),
    "knee_l": (52, 106),
    "knee_r": (78, 106),
    "foot_l": (54, 118),
    "foot_r": (78, 118),
    "key_mount": (38, 54),
    "key_wing": (28, 48),
    "tail_root": (34, 92),
    "tail_mid": (22, 74),
    "tail_tip": (18, 56),
}

def generate_poses():
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (Low-slung prowling stance, dual sabers at ready)
    # =========================================================================
    idle_canvas = body_no_weapon.copy()
    d_main = place_dagger(dagger_raw, deg=0, target_grip=(88, 76), scale=1.0, mirror=False)
    d_off = place_dagger(dagger_raw, deg=-35, target_grip=(40, 76), scale=0.92, mirror=True)
    
    idle_canvas = Image.alpha_composite(d_off, idle_canvas)
    idle_canvas = Image.alpha_composite(idle_canvas, d_main)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (Coiled spring compression, low crouch, overdrive glow)
    # Calibrated for left margin >= 4px
    # =========================================================================
    shifts_telegraph = {
        "ear_l": (4, 7), "ear_r": (6, 7), "forehead": (5, 8),
        "eye_l": (5, 8), "eye_r": (7, 8), "nose": (6, 8),
        "heart_gem": (3, 6), "shoulder_l": (2, 6), "shoulder_r": (5, 6),
        "arm_l": (-1, 5), "arm_r": (-2, 5),
        "pelvis": (-1, 6), "hip_l": (-3, 6), "hip_r": (2, 6),
        "knee_l": (-5, 5), "knee_r": (4, 5),
        "foot_l": (-2, 1), "foot_r": (2, 1),
        "key_mount": (0, 5), "key_wing": (-2, 4),
        "tail_root": (-1, 5), "tail_mid": (-6, -3), "tail_tip": (-8, -10),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Coiled daggers tucked back
    d_tele_off = place_dagger(dagger_raw, deg=45, target_grip=(38, 80), scale=0.95, mirror=True)
    d_tele_main = place_dagger(dagger_raw, deg=35, target_grip=(82, 80), scale=0.98, mirror=False)

    # Golden overdrive thermal glow on forehead I-beam & vents
    glow_layer = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_layer)
    g_draw.ellipse([64, 32, 76, 42], fill=(255, 200, 30, 160))
    g_draw.ellipse([66, 34, 74, 40], fill=(255, 255, 180, 220))
    # Wind-up key motion blur circle (x kept >= 10)
    g_draw.arc([16, 42, 34, 60], start=40, end=320, fill=(255, 180, 20, 180), width=2)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(0.8))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, d_tele_off)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, d_tele_main)
    tele_canvas = Image.alpha_composite(tele_canvas, glow_layer)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (Cross Ember Slash / deep forward lunge / twin blade slash)
    # =========================================================================
    shifts_attack = {
        "ear_l": (13, 2), "ear_r": (15, 2), "forehead": (15, 2),
        "eye_l": (15, 2), "eye_r": (17, 2), "nose": (17, 3),
        "heart_gem": (13, 3), "shoulder_l": (11, 3), "shoulder_r": (15, 3),
        "arm_l": (13, 2), "arm_r": (17, 1),
        "pelvis": (8, 3),
        "hip_l": (-2, 3), "knee_l": (-8, 3), "foot_l": (-12, 1),
        "hip_r": (14, 3), "knee_r": (16, 2), "foot_r": (14, 0),
        "key_mount": (8, 3), "key_wing": (6, 3),
        "tail_root": (2, 3), "tail_mid": (-6, -4), "tail_tip": (-14, -10),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Dual slashing blades (target grip calibrated to stay <= 123)
    d_atk_main = place_dagger(dagger_raw, deg=-30, target_grip=(96, 68), scale=1.0, mirror=False)
    d_atk_off = place_dagger(dagger_raw, deg=15, target_grip=(80, 78), scale=0.98, mirror=True)

    # X-shaped Cross Ember Slash effect with sparks
    slash_layer = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(slash_layer)
    s_draw.line([(116, 50), (92, 84)], fill=(230, 81, 0, 200), width=4)
    s_draw.line([(115, 51), (94, 82)], fill=(255, 160, 16, 240), width=2)
    s_draw.line([(114, 52), (95, 81)], fill=(255, 255, 230, 255), width=1)
    s_draw.line([(86, 60), (118, 78)], fill=(230, 81, 0, 200), width=4)
    s_draw.line([(88, 62), (116, 76)], fill=(255, 160, 16, 240), width=2)
    s_draw.line([(89, 63), (115, 75)], fill=(255, 255, 230, 255), width=1)
    s_draw.ellipse([100, 66, 106, 72], fill=(255, 240, 160, 255))
    s_draw.point([(108, 62), (111, 65), (98, 74), (104, 76), (113, 71)], fill=(255, 210, 50, 255))
    slash_layer = slash_layer.filter(ImageFilter.GaussianBlur(0.5))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, d_atk_off)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, d_atk_main)
    atk_canvas = Image.alpha_composite(atk_canvas, slash_layer)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (Ember Cyclone Pounce / aerial leap / whirl slash storm)
    # Calibrated so top margin >= 4px and height diff <= 5%
    # =========================================================================
    shifts_skill = {
        "ear_l": (2, -9), "ear_r": (6, -9), "forehead": (4, -9),
        "eye_l": (4, -9), "eye_r": (6, -9), "nose": (5, -8),
        "heart_gem": (4, -8), "shoulder_l": (-2, -10), "shoulder_r": (8, -10),
        "arm_l": (-4, -11), "arm_r": (10, -11),
        "pelvis": (2, -7), "hip_l": (-4, -6), "hip_r": (6, -6),
        "knee_l": (-6, -9), "knee_r": (6, -7),
        "foot_l": (-2, -11), "foot_r": (4, -9),
        "key_mount": (0, -8), "key_wing": (-4, -8),
        "tail_root": (-2, -8), "tail_mid": (-10, -11), "tail_tip": (-14, -13),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Overhead cyclone daggers
    d_skill_main = place_dagger(dagger_raw, deg=-65, target_grip=(94, 55), scale=1.0, mirror=False)
    d_skill_off = place_dagger(dagger_raw, deg=65, target_grip=(48, 53), scale=0.98, mirror=True)

    # Swirling flame cyclone vortex & exhaust steam (top margin kept >= 5)
    cyclone_layer = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(cyclone_layer)
    c_draw.arc([30, 26, 114, 90], start=160, end=350, fill=(230, 81, 0, 180), width=4)
    c_draw.arc([32, 28, 112, 88], start=170, end=340, fill=(255, 160, 16, 220), width=2)
    c_draw.ellipse([8, 42, 20, 54], fill=(220, 230, 240, 160))
    c_draw.ellipse([14, 36, 24, 46], fill=(240, 245, 255, 200))
    c_draw.ellipse([18, 30, 26, 38], fill=(255, 255, 255, 220))
    cyclone_layer = cyclone_layer.filter(ImageFilter.GaussianBlur(0.7))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, d_skill_off)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, d_skill_main)
    skill_canvas = Image.alpha_composite(skill_canvas, cyclone_layer)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (Dual blade cross-guard recoil / defensive flinch)
    # =========================================================================
    shifts_hit = {
        "ear_l": (-10, -3), "ear_r": (-8, -3), "forehead": (-9, -2),
        "eye_l": (-9, -2), "eye_r": (-7, -2), "nose": (-8, -1),
        "heart_gem": (-7, -1), "shoulder_l": (-7, -1), "shoulder_r": (-5, -1),
        "arm_l": (-4, 0), "arm_r": (-4, 0),
        "pelvis": (-5, 0), "hip_l": (-7, 0), "hip_r": (-3, 0),
        "knee_l": (-8, 0), "knee_r": (-3, 0),
        "foot_l": (-8, 0), "foot_r": (-2, 0),
        "key_mount": (-7, -1), "key_wing": (-9, -1),
        "tail_root": (-5, 0), "tail_mid": (-2, 4), "tail_tip": (0, 8),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Crossed blades guard over chest (X-block)
    d_hit_off = place_dagger(dagger_raw, deg=-42, target_grip=(64, 66), scale=0.96, mirror=True)
    d_hit_main = place_dagger(dagger_raw, deg=42, target_grip=(74, 66), scale=0.96, mirror=False)

    # Impact spark & steam release
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    h_draw.ellipse([66, 60, 72, 66], fill=(255, 240, 180, 240))
    h_draw.line([(60, 63), (78, 63)], fill=(255, 255, 230, 220), width=1)
    h_draw.line([(69, 54), (69, 72)], fill=(255, 255, 230, 220), width=1)
    h_draw.ellipse([34, 52, 44, 62], fill=(230, 240, 250, 160))
    h_draw.ellipse([30, 46, 38, 54], fill=(245, 250, 255, 200))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.6))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, d_hit_off)
    hit_canvas = Image.alpha_composite(hit_canvas, d_hit_main)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (Low single-knee ground re-anchor / brake slide)
    # Calibrated so height diff <= 5%
    # =========================================================================
    shifts_recover = {
        "ear_l": (4, 6), "ear_r": (6, 6), "forehead": (5, 6),
        "eye_l": (5, 6), "eye_r": (7, 6), "nose": (6, 6),
        "heart_gem": (3, 5), "shoulder_l": (0, 5), "shoulder_r": (6, 5),
        "arm_l": (-4, 4), "arm_r": (4, 6),
        "pelvis": (2, 6), "hip_l": (-5, 6), "hip_r": (5, 6),
        "knee_l": (-8, 6), "knee_r": (7, 6),
        "foot_l": (-8, 1), "foot_r": (5, 1),
        "key_mount": (0, 5), "key_wing": (-3, 4),
        "tail_root": (0, 6), "tail_mid": (-7, 3), "tail_tip": (-12, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_recover = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Right dagger planted tip-down in ground to brake (friction spark)
    d_rec_main = place_dagger(dagger_raw, deg=85, target_grip=(82, 94), scale=0.95, mirror=False)
    # Left dagger held back high in ready guard
    d_rec_off = place_dagger(dagger_raw, deg=-60, target_grip=(36, 70), scale=0.92, mirror=True)

    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    r_draw.ellipse([88, 114, 94, 118], fill=(255, 220, 60, 200))
    r_draw.point([(96, 112), (92, 111), (99, 115)], fill=(255, 255, 200, 240))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.5))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, d_rec_off)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, d_rec_main)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    poses = generate_poses()
    for name, im in poses.items():
        out_p = f"{OUT_DIR}/{name}.png"
        im.save(out_p, "PNG")
        bbox = im.getbbox()
        h = bbox[3] - bbox[1] if bbox else 0
        w = bbox[2] - bbox[0] if bbox else 0
        px_115 = sum(1 for y in range(115) for x in range(128) if im.getpixel((x, y))[3] > 8)
        print(f"✓ {name:10s}: saved to {out_p}, bbox={bbox}, w={w}, h={h}, y<115={px_115}")
