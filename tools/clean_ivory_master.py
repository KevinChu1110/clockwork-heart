#!/usr/bin/env python3
"""
tools/clean_ivory_master.py
Comprehensive restoration of macaque ivory chassis (paint_ivory_stock.png):
Removes all cracks, specks, dithering noise, and ragged chipping,
while preserving all structural panel lines, mechanical rivets, and ground shadow.
"""

from PIL import Image

def clean_chassis():
    src = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png"
    im = Image.open(src).convert("RGBA")
    w, h = im.size

    # --- 1. REPAIR CRACKS IN FACE ---
    # Crack 1: Eye crack (64..72, 31..45)
    for y in range(30, 46):
        for x in range(64, 73):
            r, g, b, a = im.getpixel((x, y))
            val = (r + g + b) // 3
            if val < 140 and a > 200:
                # Find left light neighbor (val > 180)
                l_col = None
                for lx in range(x - 1, max(30, x - 8), -1):
                    lr, lg, lb, la = im.getpixel((lx, y))
                    if la > 200 and (lr + lg + lb) // 3 > 180:
                        l_col = (lr, lg, lb)
                        break
                # Find right light neighbor (val > 180)
                r_col = None
                for rx in range(x + 1, min(w, x + 8)):
                    rr, rg, rb, ra = im.getpixel((rx, y))
                    if ra > 200 and (rr + rg + rb) // 3 > 180:
                        r_col = (rr, rg, rb)
                        break
                if l_col and r_col:
                    nr = (l_col[0] + r_col[0]) // 2
                    ng = (l_col[1] + r_col[1]) // 2
                    nb = (l_col[2] + r_col[2]) // 2
                    im.putpixel((x, y), (nr, ng, nb, 255))
                elif l_col:
                    im.putpixel((x, y), (*l_col, 255))
                elif r_col:
                    im.putpixel((x, y), (*r_col, 255))

    # Crack 2: Cheek / ear crack (73..83, 31..45)
    for y in range(31, 46):
        for x in range(73, 83):
            r, g, b, a = im.getpixel((x, y))
            val = (r + g + b) // 3
            if val < 140 and a > 200:
                # Check if this is an interior crack pixel (surrounded by ivory):
                l_col = None
                for lx in range(x - 1, max(60, x - 8), -1):
                    lr, lg, lb, la = im.getpixel((lx, y))
                    if la > 200 and (lr + lg + lb) // 3 > 180:
                        l_col = (lr, lg, lb)
                        break
                r_col = None
                for rx in range(x + 1, min(w, x + 8)):
                    rr, rg, rb, ra = im.getpixel((rx, y))
                    if ra > 200 and (rr + rg + rb) // 3 > 180:
                        r_col = (rr, rg, rb)
                        break
                if l_col and r_col:
                    nr = (l_col[0] + r_col[0]) // 2
                    ng = (l_col[1] + r_col[1]) // 2
                    nb = (l_col[2] + r_col[2]) // 2
                    im.putpixel((x, y), (nr, ng, nb, 255))
                elif l_col:
                    im.putpixel((x, y), (*l_col, 255))

    # Crack 3: Forehead hairline cracks (45..65, 23..34)
    for y in range(23, 35):
        for x in range(45, 65):
            r, g, b, a = im.getpixel((x, y))
            val = (r + g + b) // 3
            if val < 150 and a > 200:
                light_nbrs = []
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            nr, ng, nb, na = im.getpixel((nx, ny))
                            if na > 200 and (nr + ng + nb) // 3 > 180:
                                light_nbrs.append((nr, ng, nb))
                if len(light_nbrs) >= 10:
                    ar = sum(c[0] for c in light_nbrs) // len(light_nbrs)
                    ag = sum(c[1] for c in light_nbrs) // len(light_nbrs)
                    ab = sum(c[2] for c in light_nbrs) // len(light_nbrs)
                    im.putpixel((x, y), (ar, ag, ab, 255))

    # --- 2. CHIN & EAR SPECKS ---
    chin_specks = [
        (46, 47), (47, 47), (46, 48), (49, 48), (49, 51), (53, 51), (54, 51),
        (43, 53), (49, 50), (50, 50), (52, 51)
    ]
    for cx, cy in chin_specks:
        light_nbrs = []
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                nx, ny = cx + dx, cy + dy
                nr, ng, nb, na = im.getpixel((nx, ny))
                if na > 200 and (nr + ng + nb) // 3 > 180:
                    light_nbrs.append((nr, ng, nb))
        if light_nbrs:
            ar = sum(c[0] for c in light_nbrs) // len(light_nbrs)
            ag = sum(c[1] for c in light_nbrs) // len(light_nbrs)
            ab = sum(c[2] for c in light_nbrs) // len(light_nbrs)
            im.putpixel((cx, cy), (ar, ag, ab, 255))

    # Clear ear floating pixels
    ear_flakes = [(76, 56), (78, 57), (75, 57), (74, 58), (76, 61), (76, 62), (76, 63)]
    for ex, ey in ear_flakes:
        # if surrounded by transparent
        trans = sum(1 for dy in [-1,0,1] for dx in [-1,0,1] if im.getpixel((ex+dx, ey+dy))[3] < 50)
        if trans >= 5:
            im.putpixel((ex, ey), (0, 0, 0, 0))
        else:
            im.putpixel((ex, ey), (238, 234, 224, 255))

    # --- 3. BELLY & TORSO RESTORATION ---
    # Clean belly plate (y: 65..92, x: 42..74)
    for y in range(65, 93):
        for x in range(42, 74):
            r, g, b, a = im.getpixel((x, y))
            if a < 200:
                continue
            val = (r + g + b) // 3
            # If dark pixel inside the white belly plate:
            if val < 150:
                light_nbrs = []
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            nr, ng, nb, na = im.getpixel((nx, ny))
                            if na > 200 and (nr + ng + nb) // 3 > 175:
                                light_nbrs.append((nr, ng, nb))
                if len(light_nbrs) >= 15:
                    ar = sum(c[0] for c in light_nbrs) // len(light_nbrs)
                    ag = sum(c[1] for c in light_nbrs) // len(light_nbrs)
                    ab = sum(c[2] for c in light_nbrs) // len(light_nbrs)
                    im.putpixel((x, y), (ar, ag, ab, 255))

    # Belly scratches
    for (sx, sy) in [(52, 82), (53, 82), (54, 82), (55, 82), (53, 84), (54, 84), (44, 92), (45, 93)]:
        light_nbrs = []
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                nx, ny = sx + dx, sy + dy
                nr, ng, nb, na = im.getpixel((nx, ny))
                if na > 200 and (nr + ng + nb) // 3 > 175:
                    light_nbrs.append((nr, ng, nb))
        if light_nbrs:
            ar = sum(c[0] for c in light_nbrs) // len(light_nbrs)
            ag = sum(c[1] for c in light_nbrs) // len(light_nbrs)
            ab = sum(c[2] for c in light_nbrs) // len(light_nbrs)
            im.putpixel((sx, sy), (ar, ag, ab, 255))

    # Smooth the belly surface with 3x3 median on white enamel:
    smooth_belly = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(67, 92):
        for x in range(43, 73):
            r, g, b, a = im.getpixel((x, y))
            if a > 200 and (r + g + b) // 3 > 180:
                rs, gs, bs = [], [], []
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nr, ng, nb, na = im.getpixel((x + dx, y + dy))
                        if na > 200 and (nr + ng + nb) // 3 > 165:
                            rs.append(nr)
                            gs.append(ng)
                            bs.append(nb)
                if len(rs) >= 6:
                    rs.sort(); gs.sort(); bs.sort()
                    mid = len(rs) // 2
                    smooth_belly.putpixel((x, y), (rs[mid], gs[mid], bs[mid], 255))

    for y in range(67, 92):
        for x in range(43, 73):
            p = smooth_belly.getpixel((x, y))
            if p[3] > 0:
                im.putpixel((x, y), p)

    # --- 4. ARMS & LIMBS RESTORATION ---
    for arm_x in [range(27, 42), range(77, 96)]:
        for y in range(55, 95):
            for x in arm_x:
                r, g, b, a = im.getpixel((x, y))
                if a < 200:
                    continue
                val = (r + g + b) // 3
                if val < 130:
                    light_nbrs = []
                    for dy in range(-2, 3):
                        for dx in range(-2, 3):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < w and 0 <= ny < h:
                                nr, ng, nb, na = im.getpixel((nx, ny))
                                if na > 200 and (nr + ng + nb) // 3 > 175:
                                    light_nbrs.append((nr, ng, nb))
                    if len(light_nbrs) >= 12:
                        ar = sum(c[0] for c in light_nbrs) // len(light_nbrs)
                        ag = sum(c[1] for c in light_nbrs) // len(light_nbrs)
                        ab = sum(c[2] for c in light_nbrs) // len(light_nbrs)
                        im.putpixel((x, y), (ar, ag, ab, 255))

    out_path = "/tmp/clean_master_ivory.png"
    im.save(out_path)
    print("Saved", out_path)

if __name__ == "__main__":
    clean_chassis()
