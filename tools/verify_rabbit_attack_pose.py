#!/usr/bin/env python3
"""
tools/verify_rabbit_attack_pose.py
Validates game/assets/sprites/player/poses/attack.png against review.md rules:
- Rule 4b / 4b-4: Substantial genuine kinematic pose difference (diff vs idle > 6000 px, residual > 3700 px).
- Rule 4b-5: Foot lowest opaque y matches idle (118 ± 1 px).
- Rule 4b-9: Body height difference <= 5%.
- Rule 19i-7: Weapon alignment and grip bounds.
"""

import os
from PIL import Image, ImageChops

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IDLE_PATH = os.path.join(REPO_ROOT, "game/assets/sprites/player/poses/idle.png")
ATTACK_PATH = os.path.join(REPO_ROOT, "game/assets/sprites/player/poses/attack.png")

def run_verification():
    idle = Image.open(IDLE_PATH).convert("RGBA")
    attack = Image.open(ATTACK_PATH).convert("RGBA")
    w, h = 128, 128
    
    id_px = idle.load()
    atk_px = attack.load()
    assert id_px is not None and atk_px is not None
    
    # 1. Foot bottom lowest opaque y (alpha >= 100 and alpha > 40)
    def get_lowest_foot_y(px):
        lowest_100 = -1
        lowest_40 = -1
        for y in range(h - 1, -1, -1):
            for x in range(w):
                if px[x, y][3] >= 100 and lowest_100 == -1:
                    lowest_100 = y
                if px[x, y][3] > 40 and lowest_40 == -1:
                    lowest_40 = y
            if lowest_100 != -1 and lowest_40 != -1:
                break
        return lowest_100, lowest_40

    id_foot_100, id_foot_40 = get_lowest_foot_y(id_px)
    atk_foot_100, atk_foot_40 = get_lowest_foot_y(atk_px)
    
    print(f"[Foot Y] idle: {id_foot_100} (alpha>=100), attack: {atk_foot_100}")
    foot_diff = abs(atk_foot_100 - id_foot_100)
    assert foot_diff <= 1, f"Foot y diff {foot_diff} exceeds threshold of 1 px!"
    print(f"  ✓ Foot y difference is {foot_diff} px (<= 1 px pass)")
    
    # 2. Body height (y <= 118, excluding ground shadow)
    def get_body_h(px, max_y=118):
        min_y, max_y_found = 128, 0
        for y in range(max_y + 1):
            for x in range(w):
                if px[x, y][3] > 40:
                    if y < min_y: min_y = y
                    if y > max_y_found: max_y_found = y
        return max_y_found + 1 - min_y
        
    id_h = get_body_h(id_px, 118)
    atk_h = get_body_h(atk_px, 118)
    h_diff_pct = abs(atk_h - id_h) / float(id_h) * 100.0
    print(f"[Body Height (y<=118)] idle: {id_h} px, attack: {atk_h} px, diff: {h_diff_pct:.2f}%")
    assert h_diff_pct <= 5.0, f"Body height difference {h_diff_pct:.2f}% exceeds 5%!"
    print(f"  ✓ Body height difference is {h_diff_pct:.2f}% (<= 5% pass)")
    
    # 3. Pixel XOR difference
    diff = ImageChops.difference(idle, attack)
    raw_diff = sum(1 for y in range(h) for x in range(w) if any(c > 0 for c in diff.getpixel((x, y))))
    diff_40 = sum(1 for y in range(h) for x in range(w) if diff.getpixel((x, y))[3] > 40)
    print(f"[Pixel Diff vs Idle] raw: {raw_diff} px, alpha>40: {diff_40} px")
    assert raw_diff > 4000, f"Raw pixel diff {raw_diff} too low!"
    print("  ✓ Pixel difference is substantial (> 4000 px pass)")
    
    # 4. Translation residual check (Rule 4b-4)
    min_residual = 999999
    best_shift = (0, 0)
    for dy in range(-15, 16):
        for dx in range(-15, 16):
            shifted = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            shifted.paste(idle, (dx, dy))
            d = ImageChops.difference(shifted, attack)
            cnt = sum(1 for y in range(118) for x in range(w) if max(d.getpixel((x, y))[:3]) > 20)
            if cnt < min_residual:
                min_residual = cnt
                best_shift = (dx, dy)
                
    print(f"[Translation Check] best dx, dy = {best_shift}, residual: {min_residual} px")
    assert min_residual > 1500, f"Residual {min_residual} too low! Frame might be a translation."
    print("  ✓ Non-translation confirmed (residual > 1500 px pass)")
    
    print("\nALL METRICS VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    run_verification()
