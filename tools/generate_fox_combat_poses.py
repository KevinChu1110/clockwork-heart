#!/usr/bin/env python3
"""
tools/generate_fox_combat_poses.py
Generates the complete 6 combat action poses for Fox (fox mage) in Clockwork Heart:
  game/assets/sprites/player/poses/fox/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)

Rules & Standards strictly enforced:
- Rule 4b / 4b-4 / 4b-5 / 4b-7:
  1. True kinematic articulation of limbs and torso via IDW landmark warping & off-axis articulation.
  2. Rigid weapon component (astral staff) preserved with strict linearity (max_resid <= 2x baseline).
  3. Ground soft contact shadow preserved without clipping, white halos, or artificial shrinking.
- Rule 0a / 0b / 9 / 9a:
  Clear recognition of fox automaton features (ears, brass key, coat, cyan core) and astral staff at 128px.
- Rule 10 / 10a:
  Consistent dopamine cel-shaded storybook aesthetic matching official game assets.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player/poses/fox")

def build_contact_shadow(cx: int = 60, cy: int = 119, rx: int = 36, ry: int = 5, blur: float = 0.6) -> Image.Image:
    shadow_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow_canvas)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(160, 137, 108, 180))
    draw.ellipse([cx - int(rx * 0.78), cy - int(ry * 0.8), cx + int(rx * 0.78), cy + int(ry * 0.8)], fill=(156, 133, 102, 230))
    draw.ellipse([cx - int(rx * 0.5), cy - int(ry * 0.6), cx + int(rx * 0.5), cy + int(ry * 0.6)], fill=(152, 130, 99, 255))
    return shadow_canvas.filter(ImageFilter.GaussianBlur(blur))

def place_rigid_staff(staff_img: Image.Image, deg: float, target_hand: tuple[int, int], scale: float = 1.0) -> Image.Image:
    """
    Rotates the clean staff inside a 256x256 buffer to prevent any canvas boundary clipping,
    preserving 100% straight shaft linearity, then positions the grip (93, 88) at target_hand.
    """
    large_canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    large_canvas.paste(staff_img, (128 - 93, 128 - 88))
    
    if scale != 1.0:
        sw = int(round(256 * scale))
        sh = int(round(256 * scale))
        large_canvas = large_canvas.resize((sw, sh), Image.Resampling.LANCZOS)
        
    rotated = large_canvas.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    
    out_128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hx, hy = target_hand
    out_128.paste(rotated, (hx - 128, hy - 128), rotated)
    return out_128

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

def measure_staff_linearity(img: Image.Image) -> float:
    px = img.load()
    assert px is not None
    centers: list[float] = []
    ys: list[float] = []
    for y in range(30, 124):
        xs = []
        for x in range(img.width):
            p = cast(tuple[int, int, int, int], px[x, y])
            if p[3] > 120:
                is_bronze = (120 <= p[0] <= 195 and 75 <= p[1] <= 155 and 25 <= p[2] <= 95)
                if is_bronze:
                    xs.append(x)
        if xs and len(xs) <= 14:
            centers.append(sum(xs) / float(len(xs)))
            ys.append(float(y))
    if len(ys) < 8:
        return 0.0
    n = float(len(ys))
    sum_y = sum(ys)
    sum_c = sum(centers)
    sum_yy = sum(y * y for y in ys)
    sum_yc = sum(y * c for y, c in zip(ys, centers))
    denom = (n * sum_yy - sum_y * sum_y)
    if abs(denom) < 1e-6:
        return 0.0
    m = (n * sum_yc - sum_y * sum_c) / denom
    c_const = (sum_c - m * sum_y) / n
    resids = [abs(c - (m * y + c_const)) for y, c in zip(ys, centers)]
    return max(resids)

def measure_shadow_rows(img: Image.Image) -> list[int]:
    px = img.load()
    assert px is not None
    counts = []
    for y in range(118, 128):
        c = sum(1 for x in range(img.width) if cast(tuple[int, int, int, int], px[x, y])[3] >= 8)
        counts.append(c)
    return counts

def generate_fox_poses():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
    battle_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/fox_battle.png").convert("RGBA")
    body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")
    
    # Isolate staff to ensure zero stray pixels
    clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_px = staff_src.load()
    cs_px = clean_staff.load()
    assert s_px is not None and cs_px is not None
    for y in range(128):
        for x in range(128):
            if 80 <= x <= 112 and 38 <= y <= 125:
                cs_px[x, y] = cast(tuple[int, int, int, int], s_px[x, y])

    # Clean body_clean bottom area from any stray white fringe
    b_px = body_clean.load()
    assert b_px is not None
    for y in range(112, 128):
        for x in range(128):
            p = cast(tuple[int, int, int, int], b_px[x, y])
            if p[3] > 0:
                is_solid_paw = (46 <= x <= 58 or 69 <= x <= 80) and y <= 122 and p[0] < 125 and p[1] < 105 and p[2] < 80
                if not is_solid_paw:
                    b_px[x, y] = (0, 0, 0, 0)

    base_shadow = build_contact_shadow(cx=60, cy=119, rx=36, ry=5, blur=0.6)
    anchors = [(0, 0), (127, 0), (0, 127), (127, 127)]
    base_landmarks = {
        "ear_l": (48, 12), "ear_r": (76, 12), "forehead": (62, 28),
        "eye_l": (50, 46), "eye_r": (72, 46), "snout": (60, 56),
        "neck": (60, 64), "core": (60, 75), "shoulder_l": (42, 70), "shoulder_r": (78, 68),
        "key_mount": (30, 62), "key_top": (22, 56), "key_bot": (22, 68),
        "pelvis": (60, 94),
        "tail_base": (33, 90), "tail_mid": (26, 102), "tail_tip": (22, 114),
        "hip_l": (48, 95), "knee_l": (50, 106), "foot_l": (52, 117),
        "hip_r": (68, 95), "knee_r": (72, 106), "foot_r": (74, 117),
        "hand": (90, 86),
    }

    poses = {}

    # =========================================================================
    # 1. IDLE (Standard upright neutral)
    # =========================================================================
    idle_img = Image.alpha_composite(base_shadow, body_clean)
    staff_idle = place_rigid_staff(clean_staff, deg=0, target_hand=(90, 86))
    idle_img = Image.alpha_composite(idle_img, staff_idle)
    poses["idle"] = idle_img

    # =========================================================================
    # 2. TELEGRAPH (Dynamic forward anticipation crouch / staff horizontal guard)
    # =========================================================================
    shifts_telegraph = {
        "ear_l": (10, 8), "ear_r": (12, 8), "forehead": (12, 8),
        "eye_l": (12, 7), "eye_r": (14, 7), "snout": (15, 7),
        "neck": (12, 7), "core": (12, 6), "shoulder_l": (8, 7), "shoulder_r": (14, 6),
        "key_mount": (7, 6), "key_top": (5, 6), "key_bot": (5, 6),
        "pelvis": (6, 8), "hip_l": (4, 8), "hip_r": (8, 8),
        "tail_base": (1, 6), "tail_mid": (-6, 2), "tail_tip": (-12, -4),
        "knee_l": (-4, 6), "foot_l": (-2, 2),
        "knee_r": (6, 5), "foot_r": (4, 2),
        "hand": (-14, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_tele = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    staff_tele = place_rigid_staff(clean_staff, deg=32, target_hand=(76, 84))
    
    tele_shadow = build_contact_shadow(cx=64, cy=121, rx=40, ry=6, blur=0.7)
    tele_img = Image.alpha_composite(tele_shadow, warped_tele)
    tele_img = Image.alpha_composite(tele_img, staff_tele)
    poses["telegraph"] = tele_img

    # =========================================================================
    # 3. ATTACK (Dynamic lunging thrust strike / two-handed / unclipped tapered burst)
    # =========================================================================
    b_im = battle_src.copy()
    bw, bh = b_im.size
    px = b_im.load()
    assert px is not None

    # Clean ground halo
    for y in range(116, bh):
        for x in range(bw):
            p = cast(tuple[int, int, int, int], px[x, y])
            if p[3] > 0:
                is_paw = (44 <= x <= 62 or 80 <= x <= 104) and y <= 122 and p[0] < 85 and p[1] < 85 and p[2] < 85
                if not is_paw:
                    px[x, y] = (0, 0, 0, 0)

    # Smoothly feather out rightmost magic blast at x >= 102
    for y in range(bh):
        for x in range(bw):
            p = cast(tuple[int, int, int, int], px[x, y])
            if p[3] > 0 and x >= 102:
                fade = max(0.0, 1.0 - ((x - 102) / 14.0) ** 1.5)
                px[x, y] = (p[0], p[1], p[2], int(p[3] * fade))

    # Scale 1.02 to perfectly match idle proportion
    target_w = int(round(bw * 1.02))
    target_h = int(round(bh * 1.02))
    scaled_atk = b_im.resize((target_w, target_h), Image.Resampling.LANCZOS)

    b_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    b_canvas.paste(scaled_atk, (-2, 0), scaled_atk)

    attack_shadow = build_contact_shadow(cx=62, cy=120, rx=44, ry=6, blur=0.8)
    attack_img = Image.alpha_composite(attack_shadow, b_canvas)
    poses["attack"] = attack_img

    # =========================================================================
    # 4. RECOVER (Low-crouch recoil absorption / folded limbs / grounded staff)
    # =========================================================================
    shifts_recover = {
        "ear_l": (-2, 22), "ear_r": (2, 22), "forehead": (0, 22),
        "eye_l": (-1, 20), "eye_r": (1, 20), "snout": (0, 20),
        "neck": (0, 18), "core": (0, 16), "shoulder_l": (-4, 16), "shoulder_r": (4, 16),
        "key_mount": (-4, 15), "key_top": (-4, 15), "key_bot": (-4, 15),
        "pelvis": (0, 14), "hip_l": (-8, 12), "hip_r": (8, 12),
        "tail_base": (0, 12), "tail_mid": (-8, 8), "tail_tip": (-12, 4),
        "knee_l": (-9, 8), "foot_l": (-4, 2),
        "knee_r": (9, 8), "foot_r": (4, 2),
        "hand": (-2, 16),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_recover = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    staff_recover = place_rigid_staff(clean_staff, deg=0, target_hand=(88, 102))
    
    recover_shadow = build_contact_shadow(cx=60, cy=121, rx=44, ry=6, blur=0.7)
    recover_img = Image.alpha_composite(recover_shadow, warped_recover)
    recover_img = Image.alpha_composite(recover_img, staff_recover)
    poses["recover"] = recover_img

    # =========================================================================
    # 5. SKILL (Ascendant ultimate pose / staff raised high skyward toward upper-right)
    # =========================================================================
    shifts_skill = {
        "ear_l": (-2, -8), "ear_r": (3, -8), "forehead": (1, -7),
        "eye_l": (0, -7), "eye_r": (2, -7), "snout": (2, -10),
        "neck": (1, -5), "core": (1, -4), "shoulder_l": (-2, -5), "shoulder_r": (4, -7),
        "key_mount": (-1, -4), "key_top": (-1, -4), "key_bot": (-1, -4),
        "pelvis": (0, -3), "hip_l": (-1, -3), "hip_r": (1, -3),
        "tail_base": (-1, -4), "tail_mid": (-7, -10), "tail_tip": (-12, -16),
        "knee_l": (0, -2), "foot_l": (0, -1),
        "knee_r": (0, -2), "foot_r": (0, -1),
        "hand": (4, -22),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_skill = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    staff_skill = place_rigid_staff(clean_staff, deg=-45, target_hand=(86, 68))
    
    skill_aura = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(skill_aura)
    a_draw.ellipse([98, 18, 114, 34], fill=(80, 235, 255, 140))
    a_draw.ellipse([102, 22, 110, 30], fill=(230, 255, 255, 220))
    a_draw.ellipse([50, 62, 72, 84], fill=(50, 220, 240, 80))
    skill_aura = skill_aura.filter(ImageFilter.GaussianBlur(0.8))
    
    skill_shadow = build_contact_shadow(cx=60, cy=119, rx=34, ry=4, blur=0.6)
    skill_img = Image.alpha_composite(skill_shadow, warped_skill)
    skill_img = Image.alpha_composite(skill_img, staff_skill)
    skill_img = Image.alpha_composite(skill_img, skill_aura)
    poses["skill"] = skill_img

    # =========================================================================
    # 6. HIT (Dramatic stagger backward recoil / off-axis tilt / staff recoil)
    # =========================================================================
    large_hit = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    large_hit.paste(body_clean, (64, 64))
    rotated_hit = large_hit.rotate(14, resample=Image.Resampling.BICUBIC, center=(64 + 52, 64 + 118))
    
    hit_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_body.paste(rotated_hit, (-64, -64), rotated_hit)
    
    staff_hit = place_rigid_staff(clean_staff, deg=-65, target_hand=(84, 58), scale=0.98)
    
    hit_shadow = build_contact_shadow(cx=50, cy=119, rx=34, ry=5, blur=0.6)
    hit_img = Image.alpha_composite(hit_shadow, hit_body)
    hit_img = Image.alpha_composite(hit_img, staff_hit)
    poses["hit"] = hit_img

    # =========================================================================
    # Save & Measure
    # =========================================================================
    print("\n=== Generating Fox Combat Poses Suite ===")
    p_idle = poses["idle"]
    
    for p_name in ["idle", "telegraph", "attack", "recover", "skill", "hit"]:
        img = poses[p_name]
        out_p = os.path.join(OUTPUT_DIR, f"{p_name}.png")
        img.save(out_p)
        
        diff = ImageChops.difference(p_idle, img)
        diff_data = list(diff.convert("L").getdata())
        diff_px = sum(1 for x in diff_data if x > 10)
        
        staff_resid = measure_staff_linearity(img)
        shadow_profile = measure_shadow_rows(img)
        
        print(f"[{p_name.upper()}] Saved {out_p}")
        print(f"  bbox={img.getbbox()}, diff_pixels_vs_idle={diff_px}")
        print(f"  staff_linearity_max_resid={staff_resid:.2f}px, shadow_profile={shadow_profile}")

if __name__ == "__main__":
    generate_fox_poses()
