#!/usr/bin/env python3
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
W, H = 128, 128

OUTLINE = (31, 26, 58, 255)
JADE_PRIMARY = (45, 106, 79, 255)
JADE_DARK = (28, 68, 50, 255)
JADE_LIGHT = (72, 160, 120, 255)
JADE_SHINE = (110, 210, 160, 255)
BRASS_GOLD = (255, 208, 40, 255)
BRASS_DARK = (180, 130, 20, 255)
BRASS_DEEP = (110, 75, 15, 255)
WHITE_SHINE = (255, 255, 255, 255)

def test_feet_crafting():
    # 1. Base scaled character
    raw_img = Image.open("/tmp/xuanji_tortoise_concept.png").convert("RGBA")
    arr = np.array(raw_img)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    # Pure white background
    is_white = (r > 240) & (g > 240) & (b > 240)
    arr[is_white, 3] = 0
    clean_raw = Image.fromarray(arr)
    
    bbox = clean_raw.getbbox()
    cropped = clean_raw.crop(bbox)
    
    target_h = 80
    scale = target_h / cropped.height
    target_w = int(cropped.width * scale)
    scaled = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    master = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = 64 - target_w // 2
    py = 110 - target_h
    master.paste(scaled, (px, py), scaled)
    
    # Let's inspect chassis
    chassis = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(chassis)
    
    # Ground soft contact shadow at (64, 117)
    cd.ellipse([64 - 34, 117 - 5, 64 + 34, 117 + 5], fill=(31, 26, 58, 130))
    chassis = chassis.filter(ImageFilter.GaussianBlur(1.6))
    cd = ImageDraw.Draw(chassis)
    
    # Copy character body pixels, but strictly cut off floor shadow at y >= 106
    for y in range(H):
        for x in range(W):
            raw_p = master.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 30: continue
            
            # Floor shadow cut-off: anything at y >= 106 that is light brownish floor
            if y >= 106:
                continue
                
            # Exclude floating weapon on right (x >= 86, y <= 72)
            if x >= 86 and y <= 72: continue
            # Exclude floating key on left (x <= 42, y <= 33)
            if x <= 42 and y <= 33: continue
            # Exclude upper head shell (y <= 48, 38 <= x <= 78)
            if y <= 48 and 38 <= x <= 78: continue
            
            chassis.putpixel((x, y), (r, g, b, a))
            
    # Now craft the four sturdy hydraulic leg pillars and stamped metal claws
    # Front-left leg footpad around x=44, y=104..114
    # Front-right leg footpad around x=76, y=104..114
    # Hind-left leg footpad around x=30, y=98..106
    # Hind-right leg footpad around x=88, y=98..106
    
    # 1. Hind-left foot
    cd.rounded_rectangle([26, 99, 36, 107], radius=3, fill=JADE_DARK, outline=OUTLINE, width=1)
    cd.polygon([(24, 107), (27, 103), (30, 107)], fill=JADE_PRIMARY, outline=OUTLINE)
    cd.polygon([(30, 107), (33, 103), (36, 107)], fill=JADE_PRIMARY, outline=OUTLINE)
    
    # 2. Hind-right foot
    cd.rounded_rectangle([84, 99, 94, 107], radius=3, fill=JADE_DARK, outline=OUTLINE, width=1)
    cd.polygon([(84, 107), (87, 103), (90, 107)], fill=JADE_PRIMARY, outline=OUTLINE)
    cd.polygon([(90, 107), (93, 103), (96, 107)], fill=JADE_PRIMARY, outline=OUTLINE)

    # 3. Main Fore-Left Pillar Foot (x=38..52, y=103..115)
    cd.rounded_rectangle([38, 103, 52, 112], radius=4, fill=JADE_PRIMARY, outline=OUTLINE, width=1)
    cd.line([(40, 105), (50, 105)], fill=JADE_SHINE, width=1)
    # Brass shock ring
    cd.rounded_rectangle([39, 107, 51, 109], radius=1, fill=BRASS_GOLD, outline=BRASS_DEEP, width=1)
    # Stamped claws (3 claws)
    cd.polygon([(37, 115), (41, 110), (43, 115)], fill=JADE_DARK, outline=OUTLINE)
    cd.polygon([(42, 116), (45, 110), (48, 116)], fill=JADE_PRIMARY, outline=OUTLINE)
    cd.polygon([(47, 115), (50, 110), (53, 115)], fill=JADE_DARK, outline=OUTLINE)
    cd.point((45, 113), fill=WHITE_SHINE)

    # 4. Main Fore-Right Pillar Foot (x=68..82, y=103..115)
    cd.rounded_rectangle([68, 103, 82, 112], radius=4, fill=JADE_PRIMARY, outline=OUTLINE, width=1)
    cd.line([(70, 105), (80, 105)], fill=JADE_SHINE, width=1)
    # Brass shock ring
    cd.rounded_rectangle([69, 107, 81, 109], radius=1, fill=BRASS_GOLD, outline=BRASS_DEEP, width=1)
    # Stamped claws (3 claws)
    cd.polygon([(67, 115), (71, 110), (73, 115)], fill=JADE_DARK, outline=OUTLINE)
    cd.polygon([(72, 116), (75, 110), (78, 116)], fill=JADE_PRIMARY, outline=OUTLINE)
    cd.polygon([(77, 115), (80, 110), (83, 115)], fill=JADE_DARK, outline=OUTLINE)
    cd.point((75, 113), fill=WHITE_SHINE)

    # Test on magenta
    mag = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    mag.alpha_composite(chassis)
    mag.save("/tmp/test_chassis_crafted_magenta.png")
    print("Saved /tmp/test_chassis_crafted_magenta.png, bbox:", chassis.getbbox())

if __name__ == "__main__":
    test_feet_crafting()
