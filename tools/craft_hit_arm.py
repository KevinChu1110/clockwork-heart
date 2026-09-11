#!/usr/bin/env python3
import sys
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter

def create_hit_arm():
    # We want a beautiful, seamless sleeve and mechanical arm
    # connecting the right shoulder (x=70..76, y=62..70) to the hand grip at (84, 58).
    # Target hand grip center is at (84, 58).
    #
    # Anatomy:
    # 1. Upper sleeve (deep navy blue) flowing from shoulder (70..76, 62..70) to sleeve opening (78..85, 58..66)
    # 2. Golden rim on the cuff opening (78..85, 59..65)
    # 3. Crimson lining visible inside the wide bell sleeve opening
    # 4. Mechanical arm & wrist extending from inside the cuff (81, 60) to (84, 58)
    # 5. Crisp dark cel-shading outline around sleeve
    
    arm_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(arm_img)
    
    # Base sleeve shape (Deep navy fabric with dark outline)
    # Outline
    sleeve_outline = [
        (71, 63), (76, 56), (82, 53), (85, 57),
        (87, 63), (83, 69), (77, 72), (73, 71)
    ]
    draw.polygon(sleeve_outline, fill=(30, 25, 35, 255))
    
    # Navy fabric fill
    sleeve_inner = [
        (72, 64), (76, 57), (81, 55), (83, 58),
        (85, 63), (82, 67), (77, 70), (74, 69)
    ]
    draw.polygon(sleeve_inner, fill=(55, 75, 95, 255))
    
    # Upper sleeve highlight (lighter navy)
    draw.polygon([(73, 64), (77, 58), (81, 56), (80, 60), (74, 66)], fill=(75, 100, 125, 255))
    
    # Inside the wide sleeve opening: Crimson lining
    draw.polygon([(80, 59), (84, 58), (85, 63), (81, 65)], fill=(125, 25, 30, 255))
    draw.polygon([(81, 60), (83, 59), (84, 62), (82, 63)], fill=(85, 15, 20, 255))
    
    # Gold decorative cuff trim on the sleeve rim
    draw.polygon([(82, 55), (86, 57), (87, 60), (84, 59)], fill=(215, 175, 65, 255))
    draw.polygon([(84, 63), (87, 60), (85, 66), (82, 67)], fill=(185, 145, 50, 255))
    
    # Mechanical automaton arm/wrist protruding from the crimson cuff lining to grip the staff
    # Wrist socket & brass articulators
    draw.polygon([(82, 57), (85, 56), (86, 59), (83, 60)], fill=(145, 115, 75, 255))
    draw.polygon([(83, 58), (86, 57), (85, 60), (83, 59)], fill=(175, 145, 95, 255))
    # Brass rivet on wrist joint
    draw.point((84, 58), fill=(235, 205, 120, 255))
    
    # Dark border contour accents
    draw.line([(71, 63), (76, 56), (82, 53)], fill=(30, 22, 28, 255), width=1)
    draw.line([(87, 63), (83, 69), (77, 72)], fill=(30, 22, 28, 255), width=1)
    
    return arm_img

if __name__ == "__main__":
    arm = create_hit_arm()
    arm.save("/tmp/fox_test/crafted_hit_arm.png")
    print("Saved /tmp/fox_test/crafted_hit_arm.png")
