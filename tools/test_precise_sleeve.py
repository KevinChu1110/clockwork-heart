#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw

def create_precise_sleeve():
    arm_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(arm_img)
    
    # 1. Dark outline of sleeve extending upward-right from shoulder to wrist:
    # Shoulder: (70, 62) down to (75, 73)
    # Cuff opening: (82, 48) to (89, 55)
    sleeve_outline = [
        (69, 61), (74, 53), (82, 47), (87, 49),
        (90, 55), (84, 62), (77, 72), (73, 72)
    ]
    draw.polygon(sleeve_outline, fill=(30, 22, 28, 255))
    
    # 2. Main navy fabric of the sleeve:
    sleeve_navy = [
        (70, 62), (75, 54), (82, 48), (86, 50),
        (88, 55), (83, 61), (76, 70), (74, 70)
    ]
    draw.polygon(sleeve_navy, fill=(55, 75, 95, 255))
    
    # Highlight along the top fold of the sleeve
    draw.polygon([(71, 62), (76, 54), (82, 49), (81, 53), (75, 59)], fill=(80, 105, 130, 255))
    # Shadow along the bottom/underarm fold
    draw.polygon([(75, 68), (81, 61), (86, 56), (88, 55), (83, 61), (76, 70)], fill=(38, 48, 65, 255))
    
    # 3. Crimson inner lining visible at cuff rim
    draw.polygon([(82, 49), (86, 50), (87, 54), (83, 53)], fill=(125, 25, 30, 255))
    
    # 4. Gold decorative cuff trim:
    draw.line([(82, 48), (87, 50), (89, 55)], fill=(215, 175, 65, 255), width=2)
    draw.point((82, 48), fill=(245, 215, 110, 255))
    draw.point((87, 50), fill=(245, 215, 110, 255))
    
    # 5. Mechanical forearm connector bridging cuff lining to hand:
    # Connecting (83, 52) to hand at (86, 51)
    draw.polygon([(83, 51), (86, 50), (87, 53), (84, 53)], fill=(150, 115, 75, 255))
    draw.point((85, 52), fill=(235, 205, 120, 255))
    
    return arm_img

if __name__ == "__main__":
    from test_crafted_hit import staff_src, body_clean, build_contact_shadow, place_rigid_staff, clean_staff, staff_hit_src, staff_hit, large_hit, rotated_hit, hit_body
    arm = create_precise_sleeve()
    hit_shadow = build_contact_shadow(cx=50, cy=119, rx=34, ry=5, blur=0.6)
    hit_img = Image.alpha_composite(hit_shadow, hit_body)
    hit_img = Image.alpha_composite(hit_img, arm)
    hit_img = Image.alpha_composite(hit_img, staff_hit)
    hit_img.save("/tmp/fox_test/precise_hit.png")
    print("Saved /tmp/fox_test/precise_hit.png")
