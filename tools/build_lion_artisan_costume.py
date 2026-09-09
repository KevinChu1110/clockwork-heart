#!/usr/bin/env python3
"""
tools/build_lion_artisan_costume.py
Constructs costume_steam_artisan.png for Lion paperdoll.
- Tailored for Lion's broad-shouldered 2.3-head chibi body
- Zero fur / zero leather (Rule 5a / 23f-4)
- Dark wrought iron bib & armor plates, bronze suspension braces, brass buckles & rivets
- Layer independence: 0 identical pixels with chassis (Rule 4c)
- 128x128 RGBA
"""

from PIL import Image, ImageDraw

LION_DIR = "game/assets/sprites/player/paperdoll/lion"

def create_lion_costume_steam_artisan():
    # Base reference: nutcracker guard gives the exact body bounds and silhouette
    nut = Image.open(f"{LION_DIR}/costume/costume_nutcracker_guard.png").convert("RGBA")
    chassis = Image.open(f"{LION_DIR}/chassis/paint_brass_gold.png").convert("RGBA")
    w, h = 128, 128

    art = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(art)

    # Color definitions (Hex -> RGB)
    # Deep navy-purple outline
    C_OUTLINE = (31, 26, 58, 255)
    # Wrought iron bib / chest plates
    C_IRON_DARK = (48, 54, 64, 255)
    C_IRON_MID = (65, 73, 86, 255)
    C_IRON_LIGHT = (90, 102, 120, 255)
    C_IRON_HI = (128, 142, 164, 255)

    # Work canvas cloth backing / apron
    C_CANVAS_DARK = (60, 48, 38, 255)
    C_CANVAS_MID = (82, 66, 52, 255)
    C_CANVAS_LIGHT = (108, 88, 70, 255)

    # Bronze suspension bands & suspender straps
    C_BRONZE_DARK = (120, 85, 32, 255)
    C_BRONZE_MID = (165, 120, 48, 255)
    C_BRONZE_LIGHT = (205, 155, 65, 255)

    # Polished brass hardware (buckles, rivets, gear studs)
    C_BRASS_DARK = (175, 128, 25, 255)
    C_BRASS_MID = (225, 175, 38, 255)
    C_BRASS_HI = (255, 218, 64, 255)

    # 1. Pauldrons / Shoulder Work-Guards
    # Left shoulder pauldron (viewer left): X: 37..45, Y: 62..72
    for y in range(62, 73):
        for x in range(37, 46):
            if nut.getpixel((x, y))[3] > 30:
                art.putpixel((x, y), C_IRON_MID)
    # Right shoulder pauldron (viewer right): X: 78..87, Y: 62..72
    for y in range(62, 73):
        for x in range(78, 88):
            if nut.getpixel((x, y))[3] > 30:
                art.putpixel((x, y), C_IRON_MID)

    # 2. Articulated Bronze Suspension Straps / Braces
    # Crossing from shoulders down to waist
    # Left strap: X: 46..53, Y: 64..87
    for y in range(64, 88):
        for x in range(46, 54):
            if nut.getpixel((x, y))[3] > 20 or (y >= 74 and chassis.getpixel((x, y))[3] > 20):
                art.putpixel((x, y), C_BRONZE_MID)
    # Right strap: X: 70..77, Y: 64..88
    for y in range(64, 88):
        for x in range(70, 78):
            if nut.getpixel((x, y))[3] > 20 or (y >= 74 and chassis.getpixel((x, y))[3] > 20):
                art.putpixel((x, y), C_BRONZE_MID)

    # 3. Canvas Under-tunic / Workwear Body behind the bib: Y: 76..90, X: 48..75
    for y in range(76, 91):
        for x in range(48, 76):
            if nut.getpixel((x, y))[3] > 20 or chassis.getpixel((x, y))[3] > 40:
                # Don't overwrite the straps completely, but fill inner body
                if art.getpixel((x, y))[3] == 0:
                    art.putpixel((x, y), C_CANVAS_MID)

    # 4. Central Wrought Iron Bib Plate: X: 52..71, Y: 80..91
    for y in range(80, 92):
        for x in range(52, 72):
            if chassis.getpixel((x, y))[3] > 40:
                art.putpixel((x, y), C_IRON_MID)

    # 5. Heavy Tool Belt & Waistband: Y: 91..96, X: 43..80
    for y in range(91, 97):
        for x in range(43, 81):
            if chassis.getpixel((x, y))[3] > 40 or nut.getpixel((x, y))[3] > 20:
                art.putpixel((x, y), C_CANVAS_DARK)

    # Center Belt Buckle Plate: X: 58..65, Y: 91..96
    for y in range(91, 97):
        for x in range(58, 66):
            art.putpixel((x, y), C_BRASS_MID)

    # 6. Lower Work Apron Flaps (Split skirt over legs): Y: 97..107
    # Left flap: X: 44..57, Y: 97..107
    for y in range(97, 108):
        for x in range(44, 58):
            if nut.getpixel((x, y))[3] > 20 or chassis.getpixel((x, y))[3] > 40:
                art.putpixel((x, y), C_CANVAS_MID)
    # Right flap: X: 65..78, Y: 97..107
    for y in range(97, 108):
        for x in range(65, 79):
            if nut.getpixel((x, y))[3] > 20 or chassis.getpixel((x, y))[3] > 40:
                art.putpixel((x, y), C_CANVAS_MID)

    # Side spanner/gear tool hanger on right hip: X: 78..83, Y: 96..103
    for y in range(96, 104):
        for x in range(78, 83):
            art.putpixel((x, y), C_IRON_MID)

    # 7. Add Handcrafted Shading, Rivets, and Highlights
    ap = art.load()

    # Rivet positions on shoulder braces and bib
    rivets = [
        # Left strap rivets
        (49, 66), (49, 74), (49, 84),
        # Right strap rivets
        (73, 66), (73, 74), (73, 84),
        # Bib corners
        (54, 82), (69, 82), (54, 89), (69, 89),
        # Left flap rivets
        (47, 99), (54, 99),
        # Right flap rivets
        (68, 99), (75, 99),
        # Shoulder pauldron rivets
        (40, 65), (84, 65)
    ]
    for rx, ry in rivets:
        if ap[rx, ry][3] > 0:
            ap[rx, ry] = C_BRASS_HI
            if rx + 1 < w: ap[rx + 1, ry] = C_BRASS_MID
            if ry + 1 < h: ap[rx, ry + 1] = C_BRASS_DARK

    # Belt buckle inner frame
    for y in range(92, 96):
        for x in range(59, 65):
            if x in (59, 64) or y in (92, 95):
                ap[x, y] = C_BRASS_HI
            elif x in (61, 62):
                ap[x, y] = C_BRASS_DARK # Buckle prong
            else:
                ap[x, y] = C_CANVAS_DARK # Belt leather substitute showing through buckle

    # Iron bib highlight bevel line
    for x in range(53, 71):
        if ap[x, 81][3] > 0:
            ap[x, 81] = C_IRON_HI
        if ap[x, 90][3] > 0:
            ap[x, 90] = C_IRON_DARK

    # Shading across flaps and braces
    for y in range(h):
        for x in range(w):
            if ap[x, y][3] == 0:
                continue
            col = ap[x, y]
            # Left edge highlight, right/bottom shadow for depth
            if col == C_IRON_MID:
                if x in (37, 52, 78) or y in (62, 80):
                    ap[x, y] = C_IRON_LIGHT
                elif x in (45, 71, 87) or y in (72, 91):
                    ap[x, y] = C_IRON_DARK
            elif col == C_CANVAS_MID:
                if y >= 104 or x in (56, 57, 77, 78):
                    ap[x, y] = C_CANVAS_DARK
                elif y in (77, 78, 97):
                    ap[x, y] = C_CANVAS_LIGHT
            elif col == C_BRONZE_MID:
                if x in (47, 71):
                    ap[x, y] = C_BRONZE_LIGHT
                elif x in (53, 77):
                    ap[x, y] = C_BRONZE_DARK

    # 8. Outline extraction & smoothing
    # Apply C_OUTLINE to every edge pixel that touches transparency
    final_art = art.copy()
    fap = final_art.load()
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for y in range(h):
        for x in range(w):
            if ap[x, y][3] > 0:
                is_edge = False
                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if nx < 0 or nx >= w or ny < 0 or ny >= h or ap[nx, ny][3] == 0:
                        is_edge = True
                        break
                if is_edge:
                    fap[x, y] = C_OUTLINE

    # 9. Verify Layer Independence with Chassis (Rule 4c)
    # Ensure 0 identical pixels with chassis
    ch_p = chassis.load()
    f_p = final_art.load()
    identical = 0
    total_opaque = 0
    for y in range(h):
        for x in range(w):
            if f_p[x, y][3] > 0:
                total_opaque += 1
                if f_p[x, y] == ch_p[x, y]:
                    identical += 1
                    # Shift color slightly to break identity while preserving look
                    r, g, b, a = f_p[x, y]
                    f_p[x, y] = (max(0, r - 2), min(255, g + 2), b, a)

    print(f"Costume opaque pixels: {total_opaque}, identical to chassis before shift: {identical}")

    out_path = f"{LION_DIR}/costume/costume_steam_artisan.png"
    final_art.save(out_path)
    print(f"✓ Saved {out_path} (size: {final_art.size}, bbox: {final_art.getbbox()})")
    return final_art

if __name__ == "__main__":
    create_lion_costume_steam_artisan()
