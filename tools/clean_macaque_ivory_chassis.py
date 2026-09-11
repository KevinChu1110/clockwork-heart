#!/usr/bin/env python3
"""
tools/clean_macaque_ivory_chassis.py
Repaints and cleans macaque chassis (paint_ivory_stock.png):
- Removes eye crack under left eye
- Removes chin dirt specks and ear flakes
- Cleans belly plate to smooth spherical enamel surface (like rabbit)
- Cleans chest/waist/crotch seams from chipping and dithering grunge
- Preserves all structural seams, mechanical rivets, and clean outlines
"""

import os
from PIL import Image

def clean_ivory_chassis():
    path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png"
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    
    # 1. Eye crack removal: (x: 65..70, y: 32..44)
    # The surrounding skin is smooth cream/ivory.
    # At y=32..34: x=65..68
    # At y=35..37: x=68..69
    # At y=38..44: x=70
    crack_coords = {
        (65, 32): (238, 234, 225, 255),
        (66, 32): (238, 234, 225, 255),
        (67, 33): (233, 228, 218, 255),
        (68, 34): (230, 225, 214, 255),
        (68, 35): (248, 245, 239, 255),
        (69, 35): (236, 232, 222, 255),
        (69, 36): (240, 236, 227, 255),
        (69, 37): (240, 236, 227, 255),
        (70, 38): (231, 227, 216, 255),
        (70, 39): (233, 228, 218, 255),
        (70, 40): (234, 229, 219, 255),
        (70, 41): (235, 230, 220, 255),
        (70, 42): (234, 229, 219, 255),
        (70, 43): (232, 227, 216, 255),
        (70, 44): (228, 223, 211, 255),
    }
    for (x, y), color in crack_coords.items():
        im.putpixel((x, y), color)

    # 2. Chin dirt specks:
    chin_specks = {
        (47, 47): (242, 239, 231, 255),
        (46, 48): (241, 238, 230, 255),
        (49, 48): (248, 245, 239, 255),
        (49, 51): (248, 245, 239, 255),
        (53, 51): (248, 245, 239, 255),
        (54, 51): (248, 245, 239, 255),
    }
    for (x, y), color in chin_specks.items():
        im.putpixel((x, y), color)

    # 3. Flakes / isolated debris under ear / cheek
    ear_flakes = {
        (76, 56): (0, 0, 0, 0), # floating isolated pixel
        (78, 57): (240, 236, 226, 255),
        (75, 57): (240, 236, 226, 255),
        (74, 58): (238, 234, 224, 255),
        (76, 61): (238, 234, 224, 255),
        (76, 62): (238, 234, 224, 255),
        (76, 63): (238, 234, 224, 255),
    }
    for (x, y), color in ear_flakes.items():
        if (x, y) == (76, 56):
            # check if isolated
            nbrs_a = [im.getpixel((x+dx, y+dy))[3] for dy in [-1,0,1] for dx in [-1,0,1] if (dx!=0 or dy!=0)]
            if sum(nbrs_a) == 0:
                im.putpixel((x, y), (0, 0, 0, 0))
        else:
            im.putpixel((x, y), color)

    # 4. Belly / torso:
    # Remove isolated dark specks in the belly (y: 65..95, x: 40..75)
    # The belly should be a smooth spherical plate.
    # Keep the structural bottom contour, outline #1F1A3A, but remove speckles and scratches inside!
    for y in range(65, 95):
        for x in range(40, 75):
            r, g, b, a = im.getpixel((x, y))
            if a < 200:
                continue
            val = (r + g + b) // 3
            # If dark (val < 130) inside belly:
            # Check 8-neighbors
            nbr_vals = []
            nbr_colors = []
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        nr, ng, nb, na = im.getpixel((nx, ny))
                        if na > 200:
                            nbr_vals.append((nr + ng + nb) // 3)
                            nbr_colors.append((nr, ng, nb, na))
            
            # If this is an isolated dark pixel or small scratch inside a light zone:
            # Check if majority of neighbors are light (> 180)
            light_count = sum(1 for v in nbr_vals if v > 180)
            if val < 130 and light_count >= 5:
                # Replace with average of light neighbors
                light_cols = [c for c, v in zip(nbr_colors, nbr_vals) if v > 180]
                avg_r = sum(c[0] for c in light_cols) // len(light_cols)
                avg_g = sum(c[1] for c in light_cols) // len(light_cols)
                avg_b = sum(c[2] for c in light_cols) // len(light_cols)
                im.putpixel((x, y), (avg_r, avg_g, avg_b, 255))

    # Also do a second pass for 2-pixel scratches (like (52..55, 82), (44..45, 92..93))
    for y in range(65, 95):
        for x in range(40, 75):
            r, g, b, a = im.getpixel((x, y))
            if a < 200:
                continue
            val = (r + g + b) // 3
            if val < 140:
                # 5x5 neighborhood
                light_5x5 = []
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            nr, ng, nb, na = im.getpixel((nx, ny))
                            if na > 200 and ((nr + ng + nb) // 3) > 185:
                                light_5x5.append((nr, ng, nb))
                if len(light_5x5) >= 14: # mostly surrounded by white/cream enamel
                    avg_r = sum(c[0] for c in light_5x5) // len(light_5x5)
                    avg_g = sum(c[1] for c in light_5x5) // len(light_5x5)
                    avg_b = sum(c[2] for c in light_5x5) // len(light_5x5)
                    im.putpixel((x, y), (avg_r, avg_g, avg_b, 255))

    # Also clean forehead hairline cracks / specks (y: 20..35, x: 45..65)
    for y in range(20, 35):
        for x in range(45, 65):
            r, g, b, a = im.getpixel((x, y))
            if a < 200:
                continue
            val = (r + g + b) // 3
            if val < 130:
                light_5x5 = []
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            nr, ng, nb, na = im.getpixel((nx, ny))
                            if na > 200 and ((nr + ng + nb) // 3) > 185:
                                light_5x5.append((nr, ng, nb))
                if len(light_5x5) >= 15:
                    avg_r = sum(c[0] for c in light_5x5) // len(light_5x5)
                    avg_g = sum(c[1] for c in light_5x5) // len(light_5x5)
                    avg_b = sum(c[2] for c in light_5x5) // len(light_5x5)
                    im.putpixel((x, y), (avg_r, avg_g, avg_b, 255))

    # Save to /tmp first to inspect
    im.save("/tmp/cleaned_paint_ivory_stock.png")
    print("Saved /tmp/cleaned_paint_ivory_stock.png")

if __name__ == "__main__":
    clean_ivory_chassis()
