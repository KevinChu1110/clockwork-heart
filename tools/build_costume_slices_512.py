#!/usr/bin/env python3
"""
tools/build_costume_slices_512.py
Generates 512x512 transparent costume slices for Clockwork Heart paperdoll system:
1. costume_viking_harness_512.png (維京束帶 / 粗獷鍛爐護胸鐵束帶)
2. costume_astral_cape_512.png (星紋斗篷 / 星紋見習占星斗篷)
3. costume_dawn_monk_tunic_512.png (武道短褙 / 晨曦行者武道短褂)

Specifications:
- 512x512 RGBA, transparent background.
- Chibi 2.2-head toy torso fit: X ~195..324, Y ~270..412.
- Strictly below chin (Y=268) so it NEVER covers face or cheek.
- Deep warm brown #2C1C16 outline, cell-shaded dopamine palette.
- Generates corresponding 128x128 versions for battle/walk compatibility.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

def create_viking_harness_512() -> Image.Image:
    # 512x512 canvas
    img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    OUTLINE = (44, 28, 22, 255)       # #2C1C16 深暖褐描邊
    LEATHER_BASE = (120, 68, 33, 255) # 暖棕皮革
    LEATHER_SHADOW = (84, 46, 20, 255)
    LEATHER_HILIGHT = (156, 91, 45, 255)
    
    IRON_BASE = (68, 80, 100, 255)    # 鍛鐵板件
    IRON_SHADOW = (44, 54, 70, 255)
    IRON_HILIGHT = (105, 122, 150, 255)
    
    BRASS_BASE = (255, 208, 40, 255)  # 黃銅鉚釘與扣件 #FFD028
    BRASS_HILIGHT = (255, 235, 120, 255)
    BRASS_SHADOW = (180, 136, 20, 255)

    # 1. Back straps / shoulder harness
    # Left shoulder strap (from Y=272 down across chest)
    # Right shoulder strap
    # Shoulder guard plates at top
    # Left shoulder plate: (200, 272) to (236, 298)
    draw.polygon([(198, 274), (236, 270), (238, 296), (200, 300)], fill=IRON_SHADOW, outline=OUTLINE, width=4)
    draw.polygon([(202, 276), (234, 272), (234, 292), (204, 296)], fill=IRON_BASE)
    draw.line([(204, 278), (232, 274)], fill=IRON_HILIGHT, width=3)
    # Rivet on left shoulder
    draw.ellipse([214, 278, 224, 288], fill=BRASS_BASE, outline=OUTLINE, width=2)
    draw.ellipse([216, 280, 220, 284], fill=BRASS_HILIGHT)

    # Right shoulder plate: (282, 270) to (320, 298)
    draw.polygon([(282, 270), (320, 274), (318, 300), (280, 296)], fill=IRON_SHADOW, outline=OUTLINE, width=4)
    draw.polygon([(284, 272), (316, 276), (314, 296), (284, 292)], fill=IRON_BASE)
    draw.line([(286, 274), (314, 278)], fill=IRON_HILIGHT, width=3)
    # Rivet on right shoulder
    draw.ellipse([294, 278, 304, 288], fill=BRASS_BASE, outline=OUTLINE, width=2)
    draw.ellipse([296, 280, 300, 284], fill=BRASS_HILIGHT)

    # 2. Diagonal crossing leather straps (X harness)
    # Strap 1: Left shoulder to right waist (215, 295) -> (295, 375)
    # Outline
    strap1_pts = [(210, 294), (232, 290), (308, 370), (286, 378)]
    draw.polygon(strap1_pts, fill=LEATHER_SHADOW, outline=OUTLINE, width=4)
    draw.polygon([(213, 295), (229, 292), (305, 371), (289, 377)], fill=LEATHER_BASE)
    draw.line([(218, 298), (298, 373)], fill=LEATHER_HILIGHT, width=3)

    # Strap 2: Right shoulder to left waist (305, 294) -> (225, 378)
    strap2_pts = [(308, 294), (286, 290), (210, 370), (232, 378)]
    draw.polygon(strap2_pts, fill=LEATHER_SHADOW, outline=OUTLINE, width=4)
    draw.polygon([(305, 295), (289, 292), (213, 371), (229, 377)], fill=LEATHER_BASE)
    draw.line([(300, 298), (220, 373)], fill=LEATHER_HILIGHT, width=3)

    # 3. Flank reinforcement harness bands (waist flanks)
    draw.polygon([(198, 335), (225, 332), (228, 362), (198, 366)], fill=LEATHER_BASE, outline=OUTLINE, width=3)
    draw.polygon([(292, 332), (322, 335), (322, 366), (290, 362)], fill=LEATHER_SHADOW, outline=OUTLINE, width=3)

    # 4. Central forged iron medallion & brass heart ring
    # Center is at (259, 326)
    cx, cy = 259, 326
    r_med = 28
    draw.ellipse([cx - r_med, cy - r_med, cx + r_med, cy + r_med], fill=IRON_SHADOW, outline=OUTLINE, width=4)
    draw.ellipse([cx - r_med + 3, cy - r_med + 3, cx + r_med - 3, cy + r_med - 3], fill=IRON_BASE)
    draw.arc([cx - r_med + 5, cy - r_med + 5, cx + r_med - 5, cy + r_med - 5], start=180, end=360, fill=IRON_HILIGHT, width=3)

    # Brass ring framing the optic core center
    r_brass = 18
    draw.ellipse([cx - r_brass, cy - r_brass, cx + r_brass, cy + r_brass], fill=BRASS_SHADOW, outline=OUTLINE, width=3)
    draw.ellipse([cx - r_brass + 2, cy - r_brass + 2, cx + r_brass - 2, cy + r_brass - 2], fill=BRASS_BASE)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=OUTLINE)
    # Golden rivets around medallion
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        rx = int(cx + (r_med - 7) * math.cos(rad))
        ry = int(cy + (r_med - 7) * math.sin(rad))
        draw.ellipse([rx - 4, ry - 4, rx + 4, ry + 4], fill=BRASS_BASE, outline=OUTLINE, width=2)
        draw.ellipse([rx - 2, ry - 2, rx + 1, ry + 1], fill=BRASS_HILIGHT)

    # 5. Heavy wide leather & iron plate belt (Y=370..398)
    belt_pts = [(196, 372), (322, 372), (320, 396), (196, 396)]
    draw.polygon(belt_pts, fill=LEATHER_SHADOW, outline=OUTLINE, width=4)
    draw.polygon([(198, 374), (320, 374), (318, 394), (198, 394)], fill=LEATHER_BASE)
    draw.line([(198, 376), (320, 376)], fill=LEATHER_HILIGHT, width=2)

    # Studded iron segment plates on belt
    for sx in [208, 230, 288, 308]:
        draw.rectangle([sx - 8, 374, sx + 8, 394], fill=IRON_BASE, outline=OUTLINE, width=2)
        draw.ellipse([sx - 3, 381, sx + 3, 387], fill=BRASS_BASE, outline=OUTLINE, width=1)

    # Central massive rectangular iron buckle at (259, 385)
    bx1, by1, bx2, by2 = 244, 368, 274, 400
    draw.rectangle([bx1, by1, bx2, by2], fill=IRON_SHADOW, outline=OUTLINE, width=4)
    draw.rectangle([bx1 + 3, by1 + 3, bx2 - 3, by2 - 3], fill=IRON_BASE)
    draw.rectangle([bx1 + 7, by1 + 7, bx2 - 7, by2 - 7], fill=LEATHER_SHADOW, outline=OUTLINE, width=2)
    # Brass buckle pin / prong
    draw.rectangle([bx1 + 12, by1 + 4, bx1 + 17, by2 - 4], fill=BRASS_BASE, outline=OUTLINE, width=2)
    draw.line([(bx1 + 4, by1 + 4), (bx2 - 4, by1 + 4)], fill=IRON_HILIGHT, width=2)

    # 6. Hanging leather tassets / studded straps below belt (Y=396..412)
    tassets = [(218, 236), (250, 268), (282, 300)]
    for tx1, tx2 in tassets:
        t_pts = [(tx1, 396), (tx2, 396), (tx2 - 3, 412), (tx1 + 3, 412)]
        draw.polygon(t_pts, fill=LEATHER_SHADOW, outline=OUTLINE, width=3)
        draw.polygon([(tx1 + 2, 397), (tx2 - 2, 397), (tx2 - 4, 410), (tx1 + 4, 410)], fill=LEATHER_BASE)
        # Brass tip rivet
        mx = (tx1 + tx2) // 2
        draw.ellipse([mx - 3, 403, mx + 3, 409], fill=BRASS_BASE, outline=OUTLINE, width=1)

    return img


def create_astral_cape_512() -> Image.Image:
    img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    OUTLINE = (31, 26, 58, 255)         # #1F1A3A 深藍紫厚描邊
    CAPE_BASE = (44, 66, 120, 255)      # 鮮亮星空夜藍 #2C4278
    CAPE_HILIGHT = (68, 100, 172, 255)  # 暮星天藍 #4464AC
    CAPE_SHADOW = (26, 38, 76, 255)     # 深藍暗影 #1A264C
    LINING_BASE = (78, 55, 115, 255)    # 暮色紫羅蘭內襯
    
    GOLD_BASE = (255, 208, 40, 255)     # 占星星紋金 #FFD028
    GOLD_HILIGHT = (255, 238, 140, 255)
    GOLD_SHADOW = (185, 140, 20, 255)

    # 1. Back cape folds (draping down from shoulders behind flanks)
    # Left cape wing: (188, 280) down to (196, 414)
    left_cape_pts = [
        (210, 274), (192, 285), (186, 320), (188, 365), 
        (192, 412), (215, 415), (224, 385), (220, 320)
    ]
    draw.polygon(left_cape_pts, fill=CAPE_SHADOW, outline=OUTLINE, width=4)
    draw.polygon([(p[0] + 3, p[1] + 2) for p in left_cape_pts[:-1]], fill=CAPE_BASE)
    draw.line([(192, 300), (196, 408)], fill=CAPE_HILIGHT, width=4)

    # Right cape wing: (324, 280) down to (326, 414)
    right_cape_pts = [
        (308, 274), (326, 285), (332, 320), (330, 365), 
        (326, 412), (302, 415), (294, 385), (298, 320)
    ]
    draw.polygon(right_cape_pts, fill=CAPE_SHADOW, outline=OUTLINE, width=4)
    draw.polygon([(p[0] - 3, p[1] + 2) for p in right_cape_pts[:-1]], fill=CAPE_BASE)
    draw.line([(326, 300), (322, 408)], fill=CAPE_HILIGHT, width=4)

    # 2. Front mantle collar & lapels (resting across chest, Y=272..360)
    # Mantle spans from left shoulder (202, 274) through center clasp (259, 288) to right shoulder (316, 274)
    mantle_pts = [
        (204, 274), (259, 286), (314, 274), # Top collar line below chin
        (322, 300), (315, 345), (296, 365), # Right flank
        (275, 340), (259, 325), (243, 340), # Center cutout over heart core!
        (222, 365), (203, 345), (196, 300)  # Left flank
    ]
    draw.polygon(mantle_pts, fill=CAPE_SHADOW, outline=OUTLINE, width=4)
    draw.polygon([
        (207, 277), (259, 289), (311, 277),
        (318, 301), (311, 342), (294, 361),
        (274, 338), (259, 327), (244, 338),
        (224, 361), (207, 342), (200, 301)
    ], fill=CAPE_BASE)

    # Mantle fold highlights
    draw.line([(212, 284), (220, 348)], fill=CAPE_HILIGHT, width=3)
    draw.line([(306, 284), (298, 348)], fill=CAPE_HILIGHT, width=3)

    # Gold embroidered border along collar & hem
    draw.line([(206, 277), (259, 288), (312, 277)], fill=GOLD_BASE, width=3)
    draw.line([(206, 344), (222, 363), (243, 340), (259, 328), (275, 340), (296, 363), (312, 344)], fill=GOLD_BASE, width=3)

    # 3. Celestial Star Brooch / Brass Clasp at (259, 288)
    cx, cy = 259, 288
    # 8-pointed star brooch
    r_star = 14
    star_poly = []
    for i in range(16):
        a = i * (math.pi / 8)
        d = r_star if (i % 2 == 0) else (r_star * 0.45)
        star_poly.append((cx + int(d * math.cos(a)), cy + int(d * math.sin(a))))
    draw.polygon(star_poly, fill=GOLD_SHADOW, outline=OUTLINE, width=3)
    draw.polygon([(p[0], p[1]) for p in star_poly], fill=GOLD_BASE)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD_HILIGHT, outline=OUTLINE, width=1)

    # 4. Golden Constellation / Star Patterns on Cloak
    # Left shoulder star
    def draw_star(sx, sy, rad):
        pts = []
        for i in range(8):
            a = i * (math.pi / 4)
            d = rad if (i % 2 == 0) else (rad * 0.4)
            pts.append((sx + int(d * math.cos(a)), sy + int(d * math.sin(a))))
        draw.polygon(pts, fill=GOLD_BASE, outline=OUTLINE, width=1)
        draw.point((sx, sy), fill=GOLD_HILIGHT)

    draw_star(222, 312, 8)
    draw_star(296, 312, 8)
    draw_star(206, 385, 6)
    draw_star(312, 385, 6)
    draw_star(259, 375, 7)

    # Constellation connecting lines
    draw.line([(222, 312), (236, 332)], fill=GOLD_BASE, width=2)
    draw.line([(296, 312), (282, 332)], fill=GOLD_BASE, width=2)
    draw.ellipse([234, 330, 238, 334], fill=GOLD_HILIGHT)
    draw.ellipse([280, 330, 284, 334], fill=GOLD_HILIGHT)

    # 5. Bottom Hem Gold Fringe & Trim (Y=408..415)
    draw.line([(192, 412), (215, 415)], fill=GOLD_BASE, width=3)
    draw.line([(302, 415), (326, 412)], fill=GOLD_BASE, width=3)

    return img


def create_dawn_monk_tunic_512() -> Image.Image:
    img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    OUTLINE = (44, 28, 22, 255)          # #2C1C16 深暖褐描邊
    CINNABAR_BASE = (216, 66, 38, 255)   # 晨曦硃砂紅 #D84226
    CINNABAR_HILIGHT = (245, 96, 66, 255)
    CINNABAR_SHADOW = (158, 38, 24, 255)
    
    WHITE_BORDER = (255, 253, 248, 255)  # 象牙米白滾邊 #FFFDF8
    WHITE_SHADOW = (218, 212, 200, 255)
    
    SASH_BASE = (36, 40, 56, 255)        # 墨青武道腰封 #242838
    SASH_HILIGHT = (54, 62, 86, 255)
    
    GOLD_BASE = (255, 208, 40, 255)      # 晨曦黃金繩結/盤扣 #FFD028
    GOLD_HILIGHT = (255, 238, 120, 255)
    GOLD_SHADOW = (180, 136, 20, 255)

    # 1. Main tunic vest body (Y=272..410, X=198..322)
    # Sleeveless armhole curves on both sides
    tunic_pts = [
        (204, 274), (259, 284), (314, 274), # Neckline
        (322, 298), (320, 342), (322, 380), (318, 408), # Right side
        (200, 408), (196, 380), (198, 342), (196, 298)  # Left side
    ]
    draw.polygon(tunic_pts, fill=CINNABAR_SHADOW, outline=OUTLINE, width=4)
    draw.polygon([
        (206, 276), (259, 286), (312, 276),
        (319, 299), (317, 342), (319, 379), (315, 406),
        (203, 406), (199, 379), (201, 342), (199, 299)
    ], fill=CINNABAR_BASE)

    # Tunic cell shading (left side in light, right side in shadow)
    draw.polygon([
        (206, 276), (259, 286), (259, 406), (203, 406),
        (199, 379), (201, 342), (199, 299)
    ], fill=CINNABAR_HILIGHT)

    # 2. Wrapped diagonal collar (右衽/斜襟)
    # Runs from left shoulder (208, 276) down across chest to right waist (288, 365)
    draw.line([(208, 276), (288, 365)], fill=OUTLINE, width=8)
    draw.line([(208, 276), (288, 365)], fill=WHITE_BORDER, width=5)
    # Collar border on opposite side
    draw.line([(310, 276), (259, 286)], fill=OUTLINE, width=7)
    draw.line([(310, 276), (259, 286)], fill=WHITE_BORDER, width=4)

    # White piping along armholes
    draw.line([(198, 300), (200, 335)], fill=WHITE_BORDER, width=3)
    draw.line([(319, 300), (317, 335)], fill=WHITE_BORDER, width=3)

    # 3. Traditional frogged brass clasps (盤扣) across chest
    # Clasp 1: (240, 298) -> (258, 303)
    # Clasp 2: (254, 320) -> (272, 325)
    # Clasp 3: (268, 342) -> (286, 347)
    clasps = [(240, 300), (254, 322), (268, 344)]
    for fx, fy in clasps:
        # Loop and knot
        draw.line([(fx - 8, fy), (fx + 12, fy)], fill=OUTLINE, width=4)
        draw.line([(fx - 7, fy), (fx + 11, fy)], fill=GOLD_BASE, width=2)
        # Central golden knot button
        draw.ellipse([fx - 3, fy - 4, fx + 5, fy + 4], fill=GOLD_BASE, outline=OUTLINE, width=2)
        draw.ellipse([fx - 1, fy - 2, fx + 2, fy + 1], fill=GOLD_HILIGHT)

    # 4. Broad dark martial sash / obi (Y=365..392)
    sash_pts = [(197, 366), (321, 366), (319, 392), (199, 392)]
    draw.polygon(sash_pts, fill=SASH_BASE, outline=OUTLINE, width=4)
    draw.line([(199, 368), (319, 368)], fill=SASH_HILIGHT, width=2)
    draw.line([(199, 390), (319, 390)], fill=OUTLINE, width=2)

    # 5. Tied martial knot and twin hanging tassels / cords at (242, 380)
    # Central knot
    draw.ellipse([234, 372, 252, 390], fill=GOLD_SHADOW, outline=OUTLINE, width=3)
    draw.ellipse([236, 374, 250, 388], fill=GOLD_BASE)
    draw.ellipse([240, 378, 246, 384], fill=GOLD_HILIGHT)

    # Left hanging tassel down to Y=412
    draw.polygon([(236, 388), (242, 388), (240, 412), (234, 412)], fill=GOLD_BASE, outline=OUTLINE, width=2)
    draw.ellipse([233, 408, 241, 414], fill=GOLD_HILIGHT, outline=OUTLINE, width=1)

    # Right hanging tassel down to Y=408
    draw.polygon([(244, 388), (250, 388), (249, 408), (243, 408)], fill=GOLD_BASE, outline=OUTLINE, width=2)
    draw.ellipse([242, 404, 250, 410], fill=GOLD_HILIGHT, outline=OUTLINE, width=1)

    # 6. Lower tunic hem split / vents (Y=392..408)
    draw.line([(259, 392), (259, 408)], fill=OUTLINE, width=3)
    draw.line([(201, 406), (317, 406)], fill=WHITE_BORDER, width=2)

    return img


def main():
    root = "/opt/side/bravesoul-game"
    common_dir = f"{root}/game/assets/sprites/player/paperdoll/common/costume"
    os.makedirs(common_dir, exist_ok=True)

    # 1. Generate Viking Harness
    im_viking = create_viking_harness_512()
    p_viking_512 = f"{common_dir}/costume_viking_harness_512.png"
    im_viking.save(p_viking_512)
    print("Saved:", p_viking_512)

    # 2. Generate Astral Cape
    im_astral = create_astral_cape_512()
    p_astral_512 = f"{common_dir}/costume_astral_cape_512.png"
    im_astral.save(p_astral_512)
    print("Saved:", p_astral_512)

    # 3. Generate Dawn Monk Tunic
    im_monk = create_dawn_monk_tunic_512()
    p_monk_512 = f"{common_dir}/costume_dawn_monk_tunic_512.png"
    im_monk.save(p_monk_512)
    print("Saved:", p_monk_512)

    # Copy / also save to race dirs
    boar_dir = f"{root}/game/assets/sprites/player/paperdoll/boar/costume"
    fox_dir = f"{root}/game/assets/sprites/player/paperdoll/fox/costume"
    macaque_dir = f"{root}/game/assets/sprites/player/paperdoll/macaque/costume"
    rabbit_dir = f"{root}/game/assets/sprites/player/paperdoll/rabbit/costume"
    os.makedirs(boar_dir, exist_ok=True)
    os.makedirs(fox_dir, exist_ok=True)
    os.makedirs(macaque_dir, exist_ok=True)
    os.makedirs(rabbit_dir, exist_ok=True)

    im_viking.save(f"{boar_dir}/costume_viking_harness_512.png")
    im_viking.save(f"{rabbit_dir}/costume_viking_harness_512.png")
    im_astral.save(f"{fox_dir}/costume_astral_cape_512.png")
    im_astral.save(f"{rabbit_dir}/costume_astral_cape_512.png")
    im_monk.save(f"{macaque_dir}/costume_dawn_monk_tunic_512.png")
    im_monk.save(f"{rabbit_dir}/costume_dawn_monk_tunic_512.png")

    # Also copy nutcracker 512 to common
    p_nut_src = f"{rabbit_dir}/costume_nutcracker_guard_512.png"
    if os.path.exists(p_nut_src):
        im_nut = Image.open(p_nut_src)
        im_nut.save(f"{common_dir}/costume_nutcracker_guard_512.png")

    # 128x128 versions for battle/walk compatibility
    for im, name, r_dir in [
        (im_viking, "costume_viking_harness.png", boar_dir),
        (im_astral, "costume_astral_cape.png", fox_dir),
        (im_monk, "costume_dawn_monk_tunic.png", macaque_dir)
    ]:
        im_128 = im.resize((128, 128), Image.Resampling.LANCZOS)
        im_128.save(f"{common_dir}/{name}")
        im_128.save(f"{r_dir}/{name}")
        im_128.save(f"{rabbit_dir}/{name}")

    print("ALL COSTUME SLICES GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
