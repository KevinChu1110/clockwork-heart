#!/usr/bin/env python3
"""
tools/build_fox_core_assets.py
Generates the 11 core character assets for Fox (fox mage) in Clockwork Heart:
1. web/media/hero/fox_idle.png (128x128, sourced from party/fox_idle.png)
2. game/assets/sprites/player/fox_battle.png (128x128 dynamic combat crouch, staff forward, tail flared)
3. game/assets/sprites/player/fox_walk_{0..3}.png (64x64, 4-frame gait cycle)
4. game/assets/sprites/player/fox_walk_{0..3}_x3.png (128x128, 4-frame gait cycle)
5. game/assets/sprites/portraits/fox.png (128x128 HUD combat portrait from fox_mage.png)
"""

import math
import os
from typing import cast
from PIL import Image, ImageChops

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

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

def main():
    print("=== Building Fox Core Asset Suite ===")
    print(f"Repository root: {REPO_ROOT}")
    
    party_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/fox_idle.png").convert("RGBA")
    portrait_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/portraits/fox_mage.png").convert("RGBA")
    
    # 1. web/media/hero/fox_idle.png (128x128) - 沿用既有 party 幀
    os.makedirs(f"{REPO_ROOT}/web/media/hero", exist_ok=True)
    web_idle_path = f"{REPO_ROOT}/web/media/hero/fox_idle.png"
    party_src.save(web_idle_path)
    print(f"[1/5] web/media/hero/fox_idle.png saved ({party_src.size}) [沿用既有 party 幀]")
    
    # 2. game/assets/sprites/portraits/fox.png (128x128 HUD combat portrait)
    # 由 fox_mage.png 縮到 106x106 置中留邊，構圖標準與兔族一致
    os.makedirs(f"{REPO_ROOT}/game/assets/sprites/portraits", exist_ok=True)
    portrait_hud = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    p_scaled = portrait_src.resize((106, 106), Image.Resampling.LANCZOS)
    ox = (128 - 106) // 2
    oy = (128 - 106) // 2 + 2
    portrait_hud.paste(p_scaled, (ox, oy), p_scaled)
    portrait_path = f"{REPO_ROOT}/game/assets/sprites/portraits/fox.png"
    portrait_hud.save(portrait_path)
    print(f"[2/5] game/assets/sprites/portraits/fox.png saved ({portrait_hud.size}) bbox={portrait_hud.getbbox()}")
    
    # 3. game/assets/sprites/player/fox_battle.png (128x128 戰鬥特寫姿態)
    # 實際戰鬥架勢：軀幹前傾、重心下沉、法杖抬起指向前方、尾巴後揚、青綠魔法施法爆發
    battle_src_path = "/tmp/fox_test/fox_battle_scaled104.png"
    battle_path = f"{REPO_ROOT}/game/assets/sprites/player/fox_battle.png"
    if not os.path.exists(battle_src_path):
        ai_raw_path = "/tmp/fox_test/fox_battle_ai.png"
        if not os.path.exists(ai_raw_path):
            raise RuntimeError("Missing /tmp/fox_test/fox_battle_ai.png")
        im = Image.open(ai_raw_path)
        w, h = im.size
        px = im.load()
        assert px is not None
        out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        out_px = out.load()
        assert out_px is not None
        for y in range(h):
            for x in range(w):
                if x > 1100:
                    continue
                pix = cast(tuple[int, ...], px[x, y])
                r, g, b = pix[0], pix[1], pix[2]
                brightness = (r + g + b) / 3.0
                max_diff = max(abs(r - g), abs(g - b), abs(r - b))
                if brightness > 238 and max_diff < 15:
                    continue
                if brightness > 210 and max_diff < 20 and y > h * 0.7:
                    alpha = int((255 - brightness) * 2.2)
                    if alpha > 10:
                        out_px[x, y] = (40, 30, 45, min(255, alpha))
                else:
                    out_px[x, y] = (r, g, b, 255)
        bbox = out.getbbox()
        assert bbox is not None
        cropped = out.crop(bbox)
        target_h = 104
        aspect = cropped.width / cropped.height
        target_w = int(round(target_h * aspect))
        if target_w > 120:
            target_w = 120
            target_h = int(round(target_w / aspect))
        scaled = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
        final_battle = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        box_x = (128 - target_w) // 2
        box_y = 128 - target_h - 4
        final_battle.paste(scaled, (box_x, box_y), scaled)
        final_battle.save(battle_src_path)
    
    battle_img = Image.open(battle_src_path).convert("RGBA")
    battle_img.save(battle_path)
    print(f"[3/5] game/assets/sprites/player/fox_battle.png saved ({battle_img.size}) bbox={battle_img.getbbox()}")
    
    # 4 & 5. Walk cycle animations:
    # fox_walk_{0..3}_x3.png (128x128) and fox_walk_{0..3}.png (64x64)
    # Standard 4-frame gait cycle with contrapposto stride articulation
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
        "tail_base": (33, 90), "tail_mid": (26, 102), "tail_tip": (22, 118),
        "hip_l": (48, 95), "knee_l": (50, 106), "foot_l": (52, 121), "toe_l": (48, 123),
        "hip_r": (68, 95), "knee_r": (72, 106), "foot_r": (74, 121), "toe_r": (78, 123),
        "hand": (92, 88), "staff_top": (96, 42), "staff_bot": (96, 122),
        "shadow_l": (38, 123), "shadow_c": (60, 123), "shadow_r": (82, 123),
    }
    
    shifts_list = [
        # Frame 0: Contact 1 (Left rear push-off, Right front contact)
        {
            "foot_l": (-2, 0), "toe_l": (-2, 0), "knee_l": (-1, 0),
            "foot_r": (2, 0), "toe_r": (3, 0), "knee_r": (1, 0),
            "hand": (0, 0), "staff_top": (0, 0), "staff_bot": (0, 0),
            "shadow_l": (-1, 0), "shadow_r": (1, 0),
        },
        # Frame 1: Passing 1 (Rise 3px, Left foot lifts 6px off ground, knee bent, staff swings forward)
        {
            "ear_l": (0, -3), "ear_r": (0, -3), "forehead": (0, -3),
            "eye_l": (0, -3), "eye_r": (0, -3), "snout": (0, -3),
            "neck": (0, -3), "core": (0, -3), "shoulder_l": (0, -3), "shoulder_r": (0, -3),
            "key_mount": (0, -3), "key_top": (0, -3), "key_bot": (0, -3),
            "pelvis": (0, -3), "hip_l": (0, -3), "hip_r": (0, -3),
            "tail_base": (0, -3), "tail_mid": (1, -3), "tail_tip": (1, -4),
            "knee_l": (2, -4), "foot_l": (2, -6), "toe_l": (3, -6),
            "shadow_l": (0, 1),
            "knee_r": (0, -1), "foot_r": (0, 0), "toe_r": (0, 0),
            "hand": (3, -3), "staff_top": (5, -4), "staff_bot": (1, -1),
        },
        # Frame 2: Contact 2 (Down 2px compression, Left foot plants forward, Right foot pushes back)
        {
            "ear_l": (0, 2), "ear_r": (0, 2), "forehead": (0, 2),
            "eye_l": (0, 2), "eye_r": (0, 2), "snout": (0, 2),
            "neck": (0, 2), "core": (0, 2), "shoulder_l": (0, 2), "shoulder_r": (0, 2),
            "key_mount": (0, 2), "key_top": (0, 2), "key_bot": (0, 2),
            "pelvis": (0, 2), "hip_l": (0, 2), "hip_r": (0, 2),
            "tail_base": (0, 2), "tail_mid": (-1, 2), "tail_tip": (-1, 2),
            "knee_l": (2, 2), "foot_l": (3, 1), "toe_l": (4, 1),
            "shadow_l": (1, 1),
            "knee_r": (-2, 1), "foot_r": (-3, 1), "toe_r": (-3, 1),
            "shadow_r": (-1, 1),
            "hand": (4, 2), "staff_top": (6, 1), "staff_bot": (2, 3),
        },
        # Frame 3: Passing 2 (Rise 2px, Right foot lifts 6px off ground, knee bent, staff swings back)
        {
            "ear_l": (0, -2), "ear_r": (0, -2), "forehead": (0, -2),
            "eye_l": (0, -2), "eye_r": (0, -2), "snout": (0, -2),
            "neck": (0, -2), "core": (0, -2), "shoulder_l": (0, -2), "shoulder_r": (0, -2),
            "key_mount": (0, -2), "key_top": (0, -2), "key_bot": (0, -2),
            "pelvis": (0, -2), "hip_l": (0, -2), "hip_r": (0, -2),
            "tail_base": (0, -2), "tail_mid": (0, -2), "tail_tip": (0, -2),
            "knee_l": (0, -1), "foot_l": (0, 0), "toe_l": (0, 0),
            "knee_r": (-1, -4), "foot_r": (-1, -6), "toe_r": (0, -6),
            "shadow_r": (0, 1),
            "hand": (-2, -2), "staff_top": (-4, -3), "staff_bot": (0, -1),
        },
    ]
    
    walk_frames: list[Image.Image] = []
    for idx, shifts in enumerate(shifts_list):
        src_pts = list(anchors)
        dst_pts = list(anchors)
        for k, (bx, by) in base_landmarks.items():
            dx, dy = shifts.get(k, (0, 0))
            src_pts.append((bx, by))
            dst_pts.append((bx + dx, by + dy))
            
        f_128 = warp_image_idw(party_src, src_pts, dst_pts, power=2.0, epsilon=4.0)
        walk_frames.append(f_128)
        
        path_x3 = f"{REPO_ROOT}/game/assets/sprites/player/fox_walk_{idx}_x3.png"
        f_128.save(path_x3)
        print(f"[4/5] Saved {path_x3} ({f_128.size}) bbox={f_128.getbbox()}")
        
        f_64 = f_128.resize((64, 64), Image.Resampling.LANCZOS)
        path_64 = f"{REPO_ROOT}/game/assets/sprites/player/fox_walk_{idx}.png"
        f_64.save(path_64)
        print(f"[5/5] Saved {path_64} ({f_64.size}) bbox={f_64.getbbox()}")

    # Objective validation
    print("\n=== Objective Quality Validation ===")
    # 1. fox_battle vs fox_idle difference
    diff_battle = ImageChops.difference(battle_img, party_src)
    diff_b_bbox = diff_battle.getbbox()
    diff_b_px = sum(1 for y in range(128) for x in range(128) if cast(tuple[int, ...], diff_battle.getpixel((x, y)))[3] > 0 or any(cast(tuple[int, ...], diff_battle.getpixel((x, y)))[:3]))
    print(f"fox_battle vs fox_idle: diff bbox={diff_b_bbox}, changed pixels={diff_b_px} / 16384 ({diff_b_px/16384*100:.1f}%)")
    assert diff_b_bbox is not None, "fox_battle must not be identical to fox_idle!"
    assert diff_b_px > 5000, f"fox_battle must have significant pixel changes, got {diff_b_px}"
    
    # 2. walk diffs against frame 0
    f0 = walk_frames[0]
    for i in [1, 2, 3]:
        fi = walk_frames[i]
        diff_w = ImageChops.difference(f0, fi)
        diff_w_bbox = diff_w.getbbox()
        diff_w_px = sum(1 for y in range(128) for x in range(128) if cast(tuple[int, ...], diff_w.getpixel((x, y)))[3] > 0 or any(cast(tuple[int, ...], diff_w.getpixel((x, y)))[:3]))
        print(f"walk_0 vs walk_{i}: diff bbox={diff_w_bbox}, changed pixels={diff_w_px} / 16384 ({diff_w_px/16384*100:.1f}%)")
        assert diff_w_bbox is not None, f"walk_{i} must not be identical to walk_0!"
        assert diff_w_px > 5000, f"walk_{i} must have significant pixel changes, got {diff_w_px}"

    print("\n=== All 11 fox core assets built and verified successfully! ===")

if __name__ == "__main__":
    main()
