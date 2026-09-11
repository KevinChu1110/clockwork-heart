#!/usr/bin/env python3
"""
tools/repair_macaque_surfaces.py
High-precision restoration of macaque chassis surfaces to pristine toy enamel:
1. Repairs face hairline cracks and eye crack
2. Removes chin specks and ear flakes
3. Cleans belly plate to pristine spherical enamel
4. Cleans arm/leg plates from dithering noise
5. Preserves all structural outlines, seams, rivets, and ground shadow
"""

import os
from PIL import Image

def repair_ivory_chassis(src_path: str, out_path: str):
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size

    # --- 1. REPAIR EYE CRACK & FOREHEAD CRACK ---
    # The crack runs from x=60,y=30 down to x=70,y=44.
    # At each y in 30..44, we replace crack pixels with smooth horizontal interpolation
    # between clean pixels to the left and right.
    for y in range(29, 46):
        for x in range(58, 73):
            r, g, b, a = im.getpixel((x, y))
            val = (r + g + b) // 3
            # If this is a crack pixel (dark in the midst of ivory):
            if val < 130 and a > 200:
                # Find clean left neighbor (x_left < x) with val > 180
                left_col = None
                for lx in range(x - 1, max(35, x - 6), -1):
                    lr, lg, lb, la = im.getpixel((lx, y))
                    if la > 200 and (lr + lg + lb) // 3 > 180:
                        left_col = (lr, lg, lb)
                        break
                # Find clean right neighbor (x_right > x) with val > 180
                right_col = None
                for rx in range(x + 1, min(w, x + 6)):
                    rr, rg, rb, ra = im.getpixel((rx, y))
                    if ra > 200 and (rr + rg + rb) // 3 > 180:
                        right_col = (rr, rg, rb)
                        break
                
                if left_col and right_col:
                    # interpolate
                    t = 0.5
                    nr = int(left_col[0] * (1 - t) + right_col[0] * t)
                    ng = int(left_col[1] * (1 - t) + right_col[1] * t)
                    nb = int(left_col[2] * (1 - t) + right_col[2] * t)
                    im.putpixel((x, y), (nr, ng, nb, 255))
                elif left_col:
                    im.putpixel((x, y), (*left_col, 255))
                elif right_col:
                    im.putpixel((x, y), (*right_col, 255))

    # Also clean forehead hairline cracks between x: 45..58, y: 24..34
    for y in range(24, 34):
        for x in range(45, 58):
            r, g, b, a = im.getpixel((x, y))
            val = (r + g + b) // 3
            if val < 130 and a > 200:
                # check 5x5 light neighbors
                light_nbrs = []
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            nr, ng, nb, na = im.getpixel((nx, ny))
                            if na > 200 and (nr + ng + nb) // 3 > 180:
                                light_nbrs.append((nr, ng, nb))
                if len(light_nbrs) >= 12:
                    avg_r = sum(c[0] for c in light_nbrs) // len(light_nbrs)
                    avg_g = sum(c[1] for c in light_nbrs) // len(light_nbrs)
                    avg_b = sum(c[2] for c in light_nbrs) // len(light_nbrs)
                    im.putpixel((x, y), (avg_r, avg_g, avg_b, 255))

    # --- 2. CHIN DIRT SPECKS & EAR FLAKES ---
    chin_specks = [
        (47, 47), (46, 48), (49, 48), (49, 51), (53, 51), (54, 51), (43, 53)
    ]
    for cx, cy in chin_specks:
        # replace with average of surrounding chin pixels
        nbrs = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = cx + dx, cy + dy
                nr, ng, nb, na = im.getpixel((nx, ny))
                if na > 200 and (nr + ng + nb) // 3 > 180:
                    nbrs.append((nr, ng, nb))
        if nbrs:
            ar = sum(c[0] for c in nbrs) // len(nbrs)
            ag = sum(c[1] for c in nbrs) // len(nbrs)
            ab = sum(c[2] for c in nbrs) // len(nbrs)
            im.putpixel((cx, cy), (ar, ag, ab, 255))

    # Remove floating / isolated pixels under right ear
    ear_flakes = [(76, 56), (78, 57), (75, 57), (74, 58), (76, 61), (76, 62), (76, 63)]
    for ex, ey in ear_flakes:
        # if isolated or sticking out into transparent:
        # check if it's surrounded by mostly transparent
        trans_count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue
                if im.getpixel((ex + dx, ey + dy))[3] == 0:
                    trans_count += 1
        if trans_count >= 5:
            im.putpixel((ex, ey), (0, 0, 0, 0))
        else:
            # fill with smooth ear/skin color
            im.putpixel((ex, ey), (238, 234, 224, 255))

    # --- 3. BELLY & TORSO RESTORATION ---
    # The belly plate is a clean, spherical, baked-enamel plate.
    # We remove all noise, dithering, and scratches (y: 65..95, x: 40..75).
    # Two passes of noise removal for isolated dark pixels:
    for _pass in range(2):
        for y in range(65, 95):
            for x in range(40, 75):
                r, g, b, a = im.getpixel((x, y))
                if a < 200:
                    continue
                val = (r + g + b) // 3
                # Don't touch rivet pixels at the bottom edge (y >= 93, x around 45..68, which are deliberate dots)
                # But remove random belly scratches (val < 130) inside light areas
                if val < 130 and y < 91:
                    light_nbrs = []
                    for dy in range(-2, 3):
                        for dx in range(-2, 3):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < w and 0 <= ny < h:
                                nr, ng, nb, na = im.getpixel((nx, ny))
                                if na > 200 and (nr + ng + nb) // 3 > 175:
                                    light_nbrs.append((nr, ng, nb))
                    if len(light_nbrs) >= 11:
                        avg_r = sum(c[0] for c in light_nbrs) // len(light_nbrs)
                        avg_g = sum(c[1] for c in light_nbrs) // len(light_nbrs)
                        avg_b = sum(c[2] for c in light_nbrs) // len(light_nbrs)
                        im.putpixel((x, y), (avg_r, avg_g, avg_b, 255))

    # Also clean scratches across middle belly (y=81..85, x=50..58) and (y=92..93, x=44..45)
    belly_scratch_coords = [
        (52, 82), (53, 82), (54, 82), (55, 82),
        (53, 84), (54, 84),
        (44, 92), (45, 93)
    ]
    for sx, sy in belly_scratch_coords:
        light_nbrs = []
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                nx, ny = sx + dx, sy + dy
                if 0 <= nx < w and 0 <= ny < h:
                    nr, ng, nb, na = im.getpixel((nx, ny))
                    if na > 200 and (nr + ng + nb) // 3 > 170:
                        light_nbrs.append((nr, ng, nb))
        if light_nbrs:
            avg_r = sum(c[0] for c in light_nbrs) // len(light_nbrs)
            avg_g = sum(c[1] for c in light_nbrs) // len(light_nbrs)
            avg_b = sum(c[2] for c in light_nbrs) // len(light_nbrs)
            im.putpixel((sx, sy), (avg_r, avg_g, avg_b, 255))

    # --- 4. CLEAN ARMS FROM DITHER NOISE ---
    # Left arm: x: 28..42, y: 55..90
    # Right arm: x: 78..95, y: 55..90
    for arm_x_range in [range(28, 42), range(78, 95)]:
        for y in range(55, 90):
            for x in arm_x_range:
                r, g, b, a = im.getpixel((x, y))
                if a < 200:
                    continue
                val = (r + g + b) // 3
                # If dark pixel in white arm plate:
                if val < 120:
                    light_nbrs = []
                    for dy in range(-2, 3):
                        for dx in range(-2, 3):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < w and 0 <= ny < h:
                                nr, ng, nb, na = im.getpixel((nx, ny))
                                if na > 200 and (nr + ng + nb) // 3 > 175:
                                    light_nbrs.append((nr, ng, nb))
                    # If surrounded mostly by white enamel:
                    if len(light_nbrs) >= 12:
                        avg_r = sum(c[0] for c in light_nbrs) // len(light_nbrs)
                        avg_g = sum(c[1] for c in light_nbrs) // len(light_nbrs)
                        avg_b = sum(c[2] for c in light_nbrs) // len(light_nbrs)
                        im.putpixel((x, y), (avg_r, avg_g, avg_b, 255))

    # Smooth the belly light bands so it has clean, banded cel-shading like rabbit:
    # A subtle 3x3 median on belly white pixels (val > 200) to remove single-pixel dithering noise:
    belly_smooth = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(67, 90):
        for x in range(43, 72):
            r, g, b, a = im.getpixel((x, y))
            if a > 200 and (r + g + b) // 3 > 180:
                # 3x3 median
                rs, gs, bs = [], [], []
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nr, ng, nb, na = im.getpixel((x + dx, y + dy))
                        if na > 200 and (nr + ng + nb) // 3 > 160:
                            rs.append(nr)
                            gs.append(ng)
                            bs.append(nb)
                if len(rs) >= 6:
                    rs.sort()
                    gs.sort()
                    bs.sort()
                    mid = len(rs) // 2
                    belly_smooth.putpixel((x, y), (rs[mid], gs[mid], bs[mid], 255))

    for y in range(67, 90):
        for x in range(43, 72):
            sp = belly_smooth.getpixel((x, y))
            if sp[3] > 0:
                im.putpixel((x, y), sp)

    im.save(out_path)
    print(f"✓ Saved repaired chassis to {out_path}")

if __name__ == "__main__":
    src = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png"
    out = "/tmp/repaired_ivory_stock.png"
    repair_ivory_chassis(src, out)
