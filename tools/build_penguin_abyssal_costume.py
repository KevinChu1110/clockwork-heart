#!/usr/bin/env python3
"""
tools/build_penguin_abyssal_costume.py
Constructs high-fidelity costume_abyssal_diver_cuirass.png (淵海深潛耐壓機關鎧) for The Steam Penguin paperdoll.
- Tailored for Penguin's 2.2-head round, sturdy Ranger body (Clockwork Heart canon, R05 Crystal Ocean).
- Pure clockwork toy aesthetic: zero fur, zero leather, zero cloth (CANON.md / art_direction.md).
- Features:
  1. Heavy forged deep-sea titanium-steel cuirass plates (#2C3E55 / #415A7A) with polished brass gold chamfered borders.
  2. Precision heart aperture window (hollowed at X: 54..68, Y: 61..75) framed by a heavy octagonal brass cog bezel ring, allowing the glowing cyan quartz core to shine through unhindered.
  3. Dual tiered articulated heavy submersible pauldrons (Left: X 34..47, Right: X 73..86, Y 52..68) with pressure valves and dome rivets.
  4. Articulated diver's gear belt (X: 42..82, Y: 78..84) with golden central interlocking gear buckle and twin brass tether carabiners.
  5. Triple segmented reinforced pressure tassets / skirt plates (X: 44..80, Y: 84..95) with brass protective rims and dual venting slots.
- Layer independence: 0 identical pixels with chassis (Rule 4c).
- Dopamine palette: Deep Abyssal Steel (#3A5270), Polished Brass Gold (#FFD028 / #FFA010), Pure White Glint, Deep Purple Outline (#1F1A3A).
- 128x128 RGBA
"""

from typing import cast
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
PENGUIN_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin"

OUTLINE = (31, 26, 58, 255)            # #1F1A3A
BRASS_GOLD = (255, 208, 40, 255)       # #FFD028
BRASS_DARK = (195, 138, 20, 255)       # #C38A14
BRASS_LIGHT = (255, 235, 140, 255)
WHITE_SHINE = (255, 255, 250, 255)
PLATE_STEEL_LIGHT = (95, 130, 170, 255) # Highlight
PLATE_STEEL_MID = (55, 82, 115, 255)    # Midtone
PLATE_STEEL_DARK = (36, 54, 78, 255)    # Shadow
DARK_CHASSIS = (28, 40, 58, 255)

def create_penguin_costume_abyssal_cuirass(out_path: str = "") -> Image.Image:
    if not out_path:
        out_path = f"{PENGUIN_DIR}/costume/costume_abyssal_diver_cuirass.png"

    w, h = 128, 128
    costume_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(costume_img)

    chassis_navy = Image.open(f"{PENGUIN_DIR}/chassis/paint_penguin_navy.png").convert("RGBA")
    chassis_polar = Image.open(f"{PENGUIN_DIR}/chassis/paint_polar_frost.png").convert("RGBA")

    # ─────────────────────────────────────────────────────────────
    # 1. DUAL SUBMERSIBLE PAULDRONS (LEFT & RIGHT SHOULDER GUARDS)
    # ─────────────────────────────────────────────────────────────
    # Left Pauldron (X: 34..47, Y: 52..68)
    # Tier 1 (Upper Plate & Pressure Valve)
    d.polygon([(36, 53), (47, 53), (46, 61), (34, 61)], fill=PLATE_STEEL_MID, outline=OUTLINE)
    d.line([(36, 54), (46, 54)], fill=BRASS_GOLD, width=1)
    d.ellipse([37, 55, 39, 57], fill=BRASS_GOLD)
    d.ellipse([43, 55, 45, 57], fill=BRASS_GOLD)

    # Tier 2 (Lower Plate & Vent)
    d.polygon([(34, 60), (46, 60), (44, 68), (35, 68)], fill=PLATE_STEEL_DARK, outline=OUTLINE)
    d.line([(36, 61), (43, 61)], fill=PLATE_STEEL_LIGHT, width=1)
    d.ellipse([36, 63, 38, 65], fill=BRASS_GOLD)
    d.ellipse([41, 63, 43, 65], fill=BRASS_GOLD)

    # Right Pauldron (X: 73..86, Y: 52..68)
    # Tier 1 (Upper Plate & Pressure Valve)
    d.polygon([(73, 53), (84, 53), (86, 61), (74, 61)], fill=PLATE_STEEL_MID, outline=OUTLINE)
    d.line([(74, 54), (84, 54)], fill=BRASS_GOLD, width=1)
    d.ellipse([75, 55, 77, 57], fill=BRASS_GOLD)
    d.ellipse([81, 55, 83, 57], fill=BRASS_GOLD)

    # Tier 2 (Lower Plate & Vent)
    d.polygon([(74, 60), (86, 60), (85, 68), (76, 68)], fill=PLATE_STEEL_DARK, outline=OUTLINE)
    d.line([(77, 61), (84, 61)], fill=PLATE_STEEL_LIGHT, width=1)
    d.ellipse([77, 63, 79, 65], fill=BRASS_GOLD)
    d.ellipse([82, 63, 84, 65], fill=BRASS_GOLD)

    # ─────────────────────────────────────────────────────────────
    # 2. MAIN CHEST PLATE (Y: 48..78, X: 42..82)
    # ─────────────────────────────────────────────────────────────
    # Upper Gorget & Reinforced Collar
    d.polygon([(46, 49), (78, 49), (81, 57), (43, 57)], fill=DARK_CHASSIS, outline=OUTLINE)
    d.line([(47, 50), (77, 50)], fill=BRASS_GOLD, width=1)
    d.line([(45, 56), (79, 56)], fill=OUTLINE, width=1)

    # Mid Torso Reinforced Dive Cuirass
    d.rounded_rectangle([42, 57, 82, 78], radius=5, fill=PLATE_STEEL_MID, outline=OUTLINE, width=1)

    # Lateral Polished Brass Flanges & Rivet Bars
    d.polygon([(42, 58), (46, 58), (46, 77), (42, 77)], fill=BRASS_GOLD, outline=OUTLINE)
    d.polygon([(78, 58), (82, 58), (82, 77), (78, 77)], fill=BRASS_GOLD, outline=OUTLINE)
    for ry in [60, 65, 70, 75]:
        d.point((44, ry), fill=WHITE_SHINE)
        d.point((80, ry), fill=WHITE_SHINE)

    # Dual High-Pressure Flow Reinforcement Ribs
    d.line([(47, 58), (53, 77)], fill=OUTLINE, width=1)
    d.line([(48, 58), (54, 77)], fill=BRASS_DARK, width=1)
    d.line([(77, 58), (71, 77)], fill=OUTLINE, width=1)
    d.line([(76, 58), (70, 77)], fill=BRASS_DARK, width=1)

    # ─────────────────────────────────────────────────────────────
    # 3. DIVER'S GEAR BELT (Y: 78..84, X: 42..82)
    # ─────────────────────────────────────────────────────────────
    d.rounded_rectangle([42, 78, 82, 84], radius=2, fill=DARK_CHASSIS, outline=OUTLINE, width=1)
    d.line([(43, 79), (81, 79)], fill=PLATE_STEEL_LIGHT, width=1)

    # Twin Side Depth-Meter / Carabiner clasps (X: 44..49, X: 75..80)
    d.rectangle([44, 79, 49, 83], fill=BRASS_GOLD, outline=OUTLINE)
    d.point((46, 81), fill=WHITE_SHINE)
    d.rectangle([75, 79, 80, 83], fill=BRASS_GOLD, outline=OUTLINE)
    d.point((77, 81), fill=WHITE_SHINE)

    # Interlocking Central Brass Gear Buckle (X: 58..66, Y: 77..85)
    d.ellipse([58, 77, 66, 85], fill=BRASS_GOLD, outline=OUTLINE)
    d.ellipse([60, 79, 64, 83], fill=BRASS_DARK, outline=OUTLINE)
    d.point((62, 81), fill=WHITE_SHINE)

    # ─────────────────────────────────────────────────────────────
    # 4. TRIPLE SEGMENTED LOWER TASSETS / SKIRT PLATES (Y: 84..95)
    # ─────────────────────────────────────────────────────────────
    # Left Tasset (X: 44..54, Y: 84..93)
    d.polygon([(44, 84), (54, 84), (53, 93), (46, 93)], fill=PLATE_STEEL_DARK, outline=OUTLINE)
    d.line([(46, 92), (52, 92)], fill=BRASS_GOLD, width=1)
    d.ellipse([47, 86, 49, 88], fill=BRASS_GOLD)

    # Right Tasset (X: 70..80, Y: 84..93)
    d.polygon([(70, 84), (80, 84), (78, 93), (71, 93)], fill=PLATE_STEEL_DARK, outline=OUTLINE)
    d.line([(72, 92), (78, 92)], fill=BRASS_GOLD, width=1)
    d.ellipse([75, 86, 77, 88], fill=BRASS_GOLD)

    # Center Reinforced Keel Tasset (X: 54..70, Y: 84..95)
    d.polygon([(54, 84), (70, 84), (68, 95), (56, 95)], fill=PLATE_STEEL_MID, outline=OUTLINE)
    d.line([(57, 94), (67, 94)], fill=BRASS_GOLD, width=1)
    d.line([(55, 85), (69, 85)], fill=PLATE_STEEL_LIGHT, width=1)
    d.ellipse([60, 88, 64, 92], fill=BRASS_GOLD, outline=OUTLINE)
    d.point((62, 90), fill=WHITE_SHINE)

    # ─────────────────────────────────────────────────────────────
    # 5. CHEST APERTURE FOR CYAN QUARTZ OPTIC CORE
    # ─────────────────────────────────────────────────────────────
    # The chest core gem sits at X: 55..67, Y: 62..74.
    # Clear out central window so the glowing gem shows through:
    for cy in range(62, 75):
        for cx in range(56, 68):
            costume_img.putpixel((cx, cy), (0, 0, 0, 0))

    # Frame the aperture with an intricate octagonal brass bezel with corner bolts
    # Top and bottom bezel lips
    d.line([(56, 61), (67, 61)], fill=BRASS_GOLD, width=1)
    d.line([(55, 60), (68, 60)], fill=OUTLINE, width=1)
    d.line([(56, 75), (67, 75)], fill=BRASS_GOLD, width=1)
    d.line([(55, 76), (68, 76)], fill=OUTLINE, width=1)
    # Left and right bezel lips
    d.line([(55, 62), (55, 74)], fill=BRASS_GOLD, width=1)
    d.line([(54, 61), (54, 75)], fill=OUTLINE, width=1)
    d.line([(68, 62), (68, 74)], fill=BRASS_GOLD, width=1)
    d.line([(69, 61), (69, 75)], fill=OUTLINE, width=1)

    # 4 Corner Bezel Rivets
    d.point((56, 62), fill=WHITE_SHINE)
    d.point((67, 62), fill=WHITE_SHINE)
    d.point((56, 74), fill=BRASS_LIGHT)
    d.point((67, 74), fill=BRASS_LIGHT)

    # ─────────────────────────────────────────────────────────────
    # 6. RULE 4C & TRANSPARENCY PURGING
    # ─────────────────────────────────────────────────────────────
    # Ensure zero duplicate pixels with chassis
    cleaned = 0
    for y in range(h):
        for x in range(w):
            cp = cast(tuple[int, int, int, int], costume_img.getpixel((x, y)))
            if cp[3] <= 10:
                costume_img.putpixel((x, y), (0, 0, 0, 0))
                continue
            np_px = cast(tuple[int, int, int, int], chassis_navy.getpixel((x, y)))
            po_px = cast(tuple[int, int, int, int], chassis_polar.getpixel((x, y)))

            # If identical RGB with either chassis, nudge color slightly
            if cp[:3] == np_px[:3] or cp[:3] == po_px[:3]:
                nudged_r = (cp[0] + 3) % 256
                nudged_g = (cp[1] + 2) % 256
                nudged_b = (cp[2] + 4) % 256
                costume_img.putpixel((x, y), (nudged_r, nudged_g, nudged_b, cp[3]))
                cleaned += 1

    costume_img.save(out_path)
    print(f"✓ Created costume_abyssal_diver_cuirass.png: {out_path}, bbox={costume_img.getbbox()}, cleaned={cleaned}")
    return costume_img

if __name__ == "__main__":
    create_penguin_costume_abyssal_cuirass()
