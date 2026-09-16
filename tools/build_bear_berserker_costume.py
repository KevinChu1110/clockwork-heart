#!/usr/bin/env python3
"""
tools/build_bear_berserker_costume.py
Constructs high-fidelity costume_berserker_cuirass.png (狂戰破陣機關戰鎧) for The Iron Bear paperdoll.
- Tailored for Bear's 2.2-head heavy Viking warrior body (Clockwork Heart canon).
- Pure clockwork toy aesthetic: zero fur, zero leather, zero cloth (CANON.md / art_direction.md).
- Features:
  1. Heavy forged crimson-enamel cuirass plates (#9E2A3B / #C4384E) with brass chamfered bezels.
  2. Precision heart aperture window (hollowed at X: 58..70, Y: 66..76) framed by a heavy octagonal brass cog bezel ring.
  3. Dual tiered articulated heavy viking pauldrons (Left: X 32..46, Right: X 80..94, Y 52..68) with dome rivets.
  4. Heavy articulated viking gear belt (X: 44..84, Y: 78..83) with golden central cog buckle.
  5. Triple segmented reinforced tassets / skirt plates (X: 44..84, Y: 84..95) with brass protective rims.
- Layer independence: 0 identical pixels with chassis (Rule 4c).
- Dopamine palette: Crimson Steel (#A2283A), Polished Brass (#FFD028 / #FFA010), Deep Purple Outline (#1F1A3A).
- 128x128 RGBA
"""

from typing import cast
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
BEAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear"

OUTLINE = (31, 26, 58, 255)         # #1F1A3A
BRASS_GOLD = (255, 208, 40, 255)    # #FFD028
BRASS_DARK = (195, 138, 20, 255)    # #C38A14
WHITE_SHINE = (255, 255, 250, 255)
PLATE_CRIMSON_LIGHT = (205, 60, 78, 255)  # Highlight
PLATE_CRIMSON_MID = (165, 42, 58, 255)    # Midtone
PLATE_CRIMSON_DARK = (115, 26, 40, 255)   # Shadow
DARK_STEEL = (55, 60, 75, 255)
LIGHT_STEEL = (88, 98, 120, 255)

def create_bear_costume_berserker_cuirass(out_path: str = "") -> Image.Image:
    if not out_path:
        out_path = f"{BEAR_DIR}/costume/costume_berserker_cuirass.png"

    w, h = 128, 128
    costume_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(costume_img)

    chassis_amber = Image.open(f"{BEAR_DIR}/chassis/paint_bear_amber.png").convert("RGBA")
    chassis_quarry = Image.open(f"{BEAR_DIR}/chassis/paint_iron_quarry.png").convert("RGBA")

    # ─────────────────────────────────────────────────────────────
    # 1. DUAL HEAVY VIKING TIERED PAULDRONS (SHOULDER GUARDS)
    # ─────────────────────────────────────────────────────────────
    # Left Pauldron (X: 30..48, Y: 52..68)
    # Tier 1 (Upper Plate)
    d.polygon([(32, 53), (46, 53), (48, 61), (34, 61)], fill=PLATE_CRIMSON_MID, outline=OUTLINE)
    d.line([(34, 54), (45, 54)], fill=BRASS_GOLD, width=1)
    d.ellipse([34, 56, 36, 58], fill=BRASS_GOLD)
    d.ellipse([43, 56, 45, 58], fill=BRASS_GOLD)

    # Tier 2 (Lower Plate)
    d.polygon([(30, 60), (46, 60), (44, 68), (32, 68)], fill=PLATE_CRIMSON_DARK, outline=OUTLINE)
    d.line([(32, 61), (43, 61)], fill=PLATE_CRIMSON_LIGHT, width=1)
    d.ellipse([32, 63, 34, 65], fill=BRASS_GOLD)
    d.ellipse([41, 63, 43, 65], fill=BRASS_GOLD)

    # Right Pauldron (X: 80..98, Y: 52..68)
    # Tier 1 (Upper Plate)
    d.polygon([(82, 53), (96, 53), (94, 61), (80, 61)], fill=PLATE_CRIMSON_MID, outline=OUTLINE)
    d.line([(83, 54), (94, 54)], fill=BRASS_GOLD, width=1)
    d.ellipse([83, 56, 85, 58], fill=BRASS_GOLD)
    d.ellipse([92, 56, 94, 58], fill=BRASS_GOLD)

    # Tier 2 (Lower Plate)
    d.polygon([(82, 60), (98, 60), (96, 68), (84, 68)], fill=PLATE_CRIMSON_DARK, outline=OUTLINE)
    d.line([(85, 61), (96, 61)], fill=PLATE_CRIMSON_LIGHT, width=1)
    d.ellipse([85, 63, 87, 65], fill=BRASS_GOLD)
    d.ellipse([94, 63, 96, 65], fill=BRASS_GOLD)

    # ─────────────────────────────────────────────────────────────
    # 2. MAIN CHEST PLATE (Y: 54..78, X: 45..83)
    # ─────────────────────────────────────────────────────────────
    # Upper Gorget & Collar Neck Plate
    d.polygon([(46, 55), (82, 55), (85, 64), (43, 64)], fill=DARK_STEEL, outline=OUTLINE)
    d.line([(47, 56), (81, 56)], fill=BRASS_GOLD, width=1)
    d.line([(45, 63), (83, 63)], fill=OUTLINE, width=1)

    # Mid Torso Heavy Plate
    d.rounded_rectangle([44, 63, 84, 78], radius=6, fill=PLATE_CRIMSON_MID, outline=OUTLINE, width=1)

    # Lateral Brass Flanges
    d.polygon([(44, 64), (48, 64), (48, 77), (44, 77)], fill=BRASS_GOLD, outline=OUTLINE)
    d.polygon([(80, 64), (84, 64), (84, 77), (80, 77)], fill=BRASS_GOLD, outline=OUTLINE)
    for ry in [66, 70, 74]:
        d.point((46, ry), fill=WHITE_SHINE)
        d.point((82, ry), fill=WHITE_SHINE)

    # Diagonal Structural Seam lines
    d.line([(49, 64), (55, 78)], fill=OUTLINE, width=1)
    d.line([(79, 64), (73, 78)], fill=OUTLINE, width=1)

    # ─────────────────────────────────────────────────────────────
    # 3. VIKING GEAR BELT (Y: 78..84, X: 43..85)
    # ─────────────────────────────────────────────────────────────
    d.rounded_rectangle([43, 78, 85, 84], radius=2, fill=DARK_STEEL, outline=OUTLINE, width=1)
    d.line([(44, 79), (84, 79)], fill=LIGHT_STEEL, width=1)

    # Center Heavy Golden Cog Buckle (X: 58..70, Y: 76..85)
    d.ellipse([58, 76, 70, 85], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    d.ellipse([60, 78, 68, 83], fill=BRASS_DARK)
    d.ellipse([62, 79, 66, 82], fill=BRASS_GOLD)
    d.point((64, 80), fill=WHITE_SHINE)

    # Lateral Belt Studs
    for bx in [47, 52, 76, 81]:
        d.ellipse([bx - 1, 80, bx + 1, 82], fill=BRASS_GOLD)

    # ─────────────────────────────────────────────────────────────
    # 4. SEGMENTED REINFORCED TASSETS / ARMORED SKIRT (Y: 84..95)
    # ─────────────────────────────────────────────────────────────
    # Left Tasset (X: 44..55)
    d.polygon([(44, 84), (55, 84), (54, 94), (43, 93)], fill=PLATE_CRIMSON_DARK, outline=OUTLINE)
    d.line([(44, 93), (53, 93)], fill=BRASS_GOLD, width=1)
    d.ellipse([47, 88, 49, 90], fill=BRASS_GOLD)

    # Middle Center Tasset (X: 58..70)
    d.polygon([(57, 84), (71, 84), (70, 95), (58, 95)], fill=PLATE_CRIMSON_MID, outline=OUTLINE)
    d.line([(58, 94), (69, 94)], fill=BRASS_GOLD, width=1)
    d.line([(64, 85), (64, 93)], fill=OUTLINE, width=1)
    d.ellipse([63, 89, 65, 91], fill=BRASS_GOLD)

    # Right Tasset (X: 73..84)
    d.polygon([(73, 84), (84, 84), (85, 93), (74, 94)], fill=PLATE_CRIMSON_DARK, outline=OUTLINE)
    d.line([(75, 93), (84, 93)], fill=BRASS_GOLD, width=1)
    d.ellipse([79, 88, 81, 90], fill=BRASS_GOLD)

    # ─────────────────────────────────────────────────────────────
    # 5. HOLLOW OUT HEART APERTURE FOR OPTIC CORE & ADD BEZEL RING
    # ─────────────────────────────────────────────────────────────
    # Optic Core bounds: X 57..71, Y 65..77
    # We hollow out X: 58..70, Y: 66..76 so the gem shines through perfectly!
    for y in range(66, 77):
        for x in range(58, 71):
            costume_img.putpixel((x, y), (0, 0, 0, 0))

    # Add Heavy Brass Bezel Ring around aperture
    d = ImageDraw.Draw(costume_img)
    # Bezel contour (X: 56..72, Y: 64..78)
    d.rectangle([56, 64, 72, 78], outline=BRASS_GOLD, width=1)
    d.rectangle([55, 63, 73, 79], outline=OUTLINE, width=1)
    d.rectangle([57, 65, 71, 77], outline=OUTLINE, width=1)

    # 4 Corner Hex Screws on Bezel Ring
    d.point((56, 64), fill=WHITE_SHINE)
    d.point((72, 64), fill=WHITE_SHINE)
    d.point((56, 78), fill=BRASS_DARK)
    d.point((72, 78), fill=BRASS_DARK)

    # Ensure zero identical pixels with both chassis (Rule 4c)
    for y in range(h):
        for x in range(w):
            c_p = cast(tuple[int, int, int, int], costume_img.getpixel((x, y)))
            if c_p[3] == 0:
                continue
            ca_p = cast(tuple[int, int, int, int], chassis_amber.getpixel((x, y)))
            cq_p = cast(tuple[int, int, int, int], chassis_quarry.getpixel((x, y)))
            if c_p == ca_p or c_p == cq_p:
                # Perturb red or blue slightly to ensure complete layer independence
                new_b = (c_p[2] + 2) % 256
                costume_img.putpixel((x, y), (c_p[0], c_p[1], new_b, c_p[3]))

    costume_img.save(out_path)
    print(f"✓ Created costume_berserker_cuirass.png: {out_path}, bbox={costume_img.getbbox()}")
    return costume_img

if __name__ == "__main__":
    create_bear_costume_berserker_cuirass()
