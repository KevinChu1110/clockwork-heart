#!/usr/bin/env python3
"""
tools/test_kinematic_fox.py
Precision kinematic generator for Fox Mage 6 combat action poses.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player/poses/fox")

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

def build_contact_shadow(cx: int = 60, cy: int = 119, rx: int = 36, ry: int = 5, blur: float = 0.6) -> Image.Image:
    shadow_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow_canvas)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(160, 137, 108, 180))
    draw.ellipse([cx - int(rx * 0.78), cy - int(ry * 0.8), cx + int(rx * 0.78), cy + int(ry * 0.8)], fill=(156, 133, 102, 230))
    draw.ellipse([cx - int(rx * 0.5), cy - int(ry * 0.6), cx + int(rx * 0.5), cy + int(ry * 0.6)], fill=(152, 130, 99, 255))
    return shadow_canvas.filter(ImageFilter.GaussianBlur(blur))

def measure_staff_linearity(img: Image.Image) -> float:
    px = img.load()
    assert px is not None
    centers: list[float] = []
    ys: list[float] = []
    for y in range(35, 124):
        xs = []
        for x in range(img.width):
            p = cast(tuple[int, ...], px[x, y])
            if p[3] > 120:
                is_bronze = (120 <= p[0] <= 195 and 75 <= p[1] <= 155 and 25 <= p[2] <= 95)
                if is_bronze:
                    xs.append(x)
        if xs and len(xs) <= 12:
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
        c = sum(1 for x in range(img.width) if cast(tuple[int, ...], px[x, y])[3] >= 8)
        counts.append(c)
    return counts

def generate_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    party_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/fox_idle.png").convert("RGBA")
    staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
    battle_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/fox_battle.png").convert("RGBA")
    
    clean_body_path = "/tmp/fox_test/char_no_shadow_no_wep.png"
    body_clean = Image.open(clean_body_path).convert("RGBA")

    anchors = [
        (0, 0), (127, 0), (0, 127), (127, 127),
        (0, 30), (127, 30), (0, 64), (127, 64), (0, 95), (127, 95),
        (30, 0), (95, 0), (30, 127), (95, 127),
    ]

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

    base_shadow = build_contact_shadow(cx=60, cy=119, rx=36, ry=5, blur=0.6)
    poses_data = {}

    # -------------------------------------------------------------
    # 1. IDLE (Standard upright neutral)
    # -------------------------------------------------------------
    idle_img = Image.alpha_composite(base_shadow, body_clean)
    idle_img = Image.alpha_composite(idle_img, staff_src)
    poses_data["idle"] = idle_img

    # -------------------------------------------------------------
    # 2. TELEGRAPH (Deep forward stance / crouched charge / horizontal staff guard)
    # True bodily shift: hunkered 6px lower, leaned forward +8px, knees bent outward, ears pinned back
    # -------------------------------------------------------------
    shifts_telegraph = {
        "ear_l": (6, 8), "ear_r": (8, 8), "forehead": (7, 6),
        "eye_l": (7, 5), "eye_r": (8, 5), "snout": (9, 5),
        "neck": (7, 6), "core": (7, 6), "shoulder_l": (5, 6), "shoulder_r": (8, 5),
        "key_mount": (5, 5), "key_top": (4, 5), "key_bot": (4, 5),
        "pelvis": (2, 7), "hip_l": (0, 7), "hip_r": (4, 7),
        "tail_base": (-1, 5), "tail_mid": (-6, 2), "tail_tip": (-10, -3),
        "knee_l": (-4, 5), "foot_l": (-2, 2),
        "knee_r": (5, 4), "foot_r": (3, 2),
        "hand": (-12, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
    
    warped_tele = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Rigid staff angled forward in horizontal-diagonal thrust guard (-32 deg)
    staff_tele = staff_src.rotate(-32, resample=Image.Resampling.BICUBIC, center=(92, 88), translate=(-12, 2))
    
    tele_shadow = build_contact_shadow(cx=64, cy=121, rx=38, ry=6, blur=0.7)
    tele_img = Image.alpha_composite(tele_shadow, warped_tele)
    tele_img = Image.alpha_composite(tele_img, staff_tele)
    poses_data["telegraph"] = tele_img

    # -------------------------------------------------------------
    # 3. ATTACK (Thrust strike / dynamic battle charge)
    # Perfectly scaled & centered fox_battle.png to eliminate right-edge boundary clipping!
    # -------------------------------------------------------------
    # Resize slightly (scale 0.93) to fit magic burst inside bounds with 6px margin
    bw, bh = battle_src.size
    scaled_w = int(round(bw * 0.93))
    scaled_h = int(round(bh * 0.93))
    battle_scaled = battle_src.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
    
    battle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Place with 4px left shift and 4px down shift so feet touch y=120
    battle_canvas.paste(battle_scaled, (0, 7), battle_scaled)
    
    # Clean bottom artifacts of battle_canvas
    b_px = battle_canvas.load()
    assert b_px is not None
    for y in range(120, 128):
        for x in range(128):
            p = cast(tuple[int, ...], b_px[x, y])
            if p[3] > 0:
                is_solid_paw = (44 <= x <= 62 or 80 <= x <= 100) and y <= 122 and p[0] < 80 and p[1] < 80
                if not is_solid_paw:
                    b_px[x, y] = (0, 0, 0, 0)
                    
    attack_shadow = build_contact_shadow(cx=62, cy=120, rx=44, ry=6, blur=0.8)
    attack_img = Image.alpha_composite(attack_shadow, battle_canvas)
    poses_data["attack"] = attack_img

    # -------------------------------------------------------------
    # 4. RECOVER (Low recoil crouch / deep body compression / grounded staff)
    # Bodily shift: Entire head and torso compress down 12px! Knees fold deep.
    # Height visibly compact like macaque recover.
    # -------------------------------------------------------------
    shifts_recover = {
        "ear_l": (-2, 13), "ear_r": (2, 13), "forehead": (0, 13),
        "eye_l": (-1, 13), "eye_r": (1, 13), "snout": (0, 14),
        "neck": (0, 13), "core": (0, 12), "shoulder_l": (-2, 12), "shoulder_r": (2, 12),
        "key_mount": (-2, 10), "key_top": (-2, 10), "key_bot": (-2, 10),
        "pelvis": (0, 12), "hip_l": (-4, 11), "hip_r": (4, 11),
        "tail_base": (0, 10), "tail_mid": (-4, 8), "tail_tip": (-8, 6),
        "knee_l": (-6, 8), "foot_l": (-3, 2),
        "knee_r": (6, 8), "foot_r": (3, 2),
        "hand": (-2, 12),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_recover = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Staff planted upright on ground, translated down +6px
    staff_recover = staff_src.rotate(0, resample=Image.Resampling.BICUBIC, center=(92, 88), translate=(-2, 6))
    
    recover_shadow = build_contact_shadow(cx=60, cy=121, rx=40, ry=6, blur=0.7)
    recover_img = Image.alpha_composite(recover_shadow, warped_recover)
    recover_img = Image.alpha_composite(recover_img, staff_recover)
    poses_data["recover"] = recover_img

    # -------------------------------------------------------------
    # 5. SKILL (Ascendant astral burst / staff held high / head thrown back skyward)
    # Bodily shift: Lifted upright (+4px), head tilted back looking up (snout lifted -8px), ears tall
    # Staff rotated +46 deg, held high above head toward sky
    # -------------------------------------------------------------
    shifts_skill = {
        "ear_l": (-2, -7), "ear_r": (3, -7), "forehead": (1, -6),
        "eye_l": (0, -7), "eye_r": (2, -7), "snout": (2, -9),
        "neck": (1, -5), "core": (1, -4), "shoulder_l": (-2, -5), "shoulder_r": (4, -7),
        "key_mount": (-1, -4), "key_top": (-1, -4), "key_bot": (-1, -4),
        "pelvis": (0, -3), "hip_l": (-1, -3), "hip_r": (1, -3),
        "tail_base": (-1, -4), "tail_mid": (-6, -10), "tail_tip": (-10, -16),
        "knee_l": (0, -2), "foot_l": (0, -1),
        "knee_r": (0, -2), "foot_r": (0, -1),
        "hand": (6, -26),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_skill = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Staff held high pointing to sky (+46 deg, tip at ~ 104, 16)
    staff_skill = staff_src.rotate(46, resample=Image.Resampling.BICUBIC, center=(92, 88), translate=(4, -22))
    
    # Hand-painted soft astral aura (feathered organic glow, NO harsh vector rings)
    skill_aura = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(skill_aura)
    # Staff crystal bright radiant core at (104, 18)
    a_draw.ellipse([92, 6, 116, 30], fill=(80, 235, 255, 110))
    a_draw.ellipse([98, 12, 110, 24], fill=(220, 255, 255, 200))
    # Chest core cyan luminescence
    a_draw.ellipse([48, 60, 74, 86], fill=(50, 220, 240, 80))
    skill_aura = skill_aura.filter(ImageFilter.GaussianBlur(1.2))
    
    skill_shadow = build_contact_shadow(cx=60, cy=119, rx=34, ry=4, blur=0.6)
    skill_img = Image.alpha_composite(skill_shadow, warped_skill)
    skill_img = Image.alpha_composite(skill_img, staff_skill)
    skill_img = Image.alpha_composite(skill_img, skill_aura)
    poses_data["skill"] = skill_img

    # -------------------------------------------------------------
    # 6. HIT (Violent recoil / stagger backward / off-axis tilt / staff displaced)
    # Bodily shift: Heavy diagonal lean backward (-16 px), head thrown back (-18 px), front foot lifted
    # -------------------------------------------------------------
    shifts_hit = {
        "ear_l": (-18, -2), "ear_r": (-14, -2), "forehead": (-16, -4),
        "eye_l": (-15, -5), "eye_r": (-13, -5), "snout": (-14, -6),
        "neck": (-12, -3), "core": (-10, -1), "shoulder_l": (-16, -1), "shoulder_r": (-8, -4),
        "key_mount": (-12, -1), "key_top": (-14, -2), "key_bot": (-14, 0),
        "pelvis": (-6, 2), "hip_l": (-9, 2), "hip_r": (-4, 2),
        "tail_base": (-6, 2), "tail_mid": (-4, 5), "tail_tip": (0, 8),
        "knee_l": (-5, 2), "foot_l": (-6, 1),
        "knee_r": (4, -6), "foot_r": (7, -9),  # Front foot lifted off ground in stagger
        "hand": (-10, -14),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_hit = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Staff thrown backward-upward (-42 deg, pushed off-axis)
    staff_hit = staff_src.rotate(-42, resample=Image.Resampling.BICUBIC, center=(92, 88), translate=(-10, -14))
    
    hit_shadow = build_contact_shadow(cx=54, cy=119, rx=35, ry=5, blur=0.6)
    hit_img = Image.alpha_composite(hit_shadow, warped_hit)
    hit_img = Image.alpha_composite(hit_img, staff_hit)
    poses_data["hit"] = hit_img

    # -------------------------------------------------------------
    # Save & Measure
    # -------------------------------------------------------------
    print("\n=== Generating and Verifying Fox Action Poses (Kinematic v2) ===")
    p_idle = poses_data["idle"]
    
    for p_name in ["idle", "telegraph", "attack", "recover", "skill", "hit"]:
        img = poses_data[p_name]
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
    generate_all()
