import sys
sys.path.insert(0, '/opt/side/bravesoul-game')
from PIL import Image
import numpy as np
from tools.measure_speckle import interior_speckle

def clean_full_ivory_chassis(src_path, out_path):
    im = Image.open(src_path).convert('RGBA')
    w, h = im.size
    px = im.load()
    
    def op(x, y):
        return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128
        
    # Criteria for structural pixels that MUST be preserved:
    def is_structural_feature(x, y):
        # 1. Boots and lower legs (below y=105)
        if y >= 105:
            return True
            
        # 2. Left eye sensor & frame
        if 46 <= x <= 55 and 41 <= y <= 51:
            return True
            
        # 3. Right eye sensor & frame
        if 66 <= x <= 76 and 41 <= y <= 51:
            return True
            
        # 4. Nostrils
        if 52 <= x <= 56 and 54 <= y <= 57:
            return True
            
        # 5. Clean smile line (horizontal 1px at y=60)
        if 50 <= x <= 63 and y == 60:
            return True
            
        # 6. Neck center pivot hinge (x=47..53, y=66..70)
        if 47 <= x <= 53 and 66 <= y <= 70:
            return True
            
        # 7. Subtle 1px center panel line on crown (x=58, y=28..36)
        if x == 58 and 28 <= y <= 36:
            return True
            
        return False

    # First pass: find all pixels that are dirty (either dark speckle inside, or grunge near edge)
    dirty_coords = set()
    
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128:
                continue
            if is_structural_feature(x, y):
                continue
                
            mx = max(r, g, b)
            
            # Check 1: interior speckles (30 < mx < 110)
            is_interior = op(x-1,y) and op(x+1,y) and op(x,y-1) and op(x,y+1)
            if is_interior and 30 < mx < 115:
                dirty_coords.add((x, y))
                
            # Check 2: near-edge brownish grunge (not the clean #1F1A3A outline)
            # Normal outline has mx < 60 and is directly next to alpha < 128.
            # Grunge is brownish (r > b + 10 or mx between 60 and 125) on white chassis parts (y < 105)
            if not is_interior and y < 105:
                # If it's a brownish grunge pixel
                if 55 <= mx <= 125 and (r > b):
                    # Check if there is an outline pixel further out
                    # If so, this is inner grunge!
                    dirty_coords.add((x, y))

    print(f"Total dirty coordinates identified: {len(dirty_coords)}")

    # For each dirty coordinate, calculate smooth ivory enamel color using IDW from clean ivory pixels
    repaired_colors = {}
    for (x, y) in dirty_coords:
        weights = 0.0
        r_sum = 0.0
        g_sum = 0.0
        b_sum = 0.0
        
        # Search radius
        for rad in range(2, 10):
            for dy in range(-rad, rad + 1):
                for dx in range(-rad, rad + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in dirty_coords:
                        na = px[nx, ny][3]
                        if na >= 128:
                            nr, ng, nb = px[nx, ny][:3]
                            if max(nr, ng, nb) >= 120:
                                dist = (dx*dx + dy*dy) ** 0.5
                                if dist == 0: continue
                                w_val = 1.0 / (dist * dist)
                                weights += w_val
                                r_sum += nr * w_val
                                g_sum += ng * w_val
                                b_sum += nb * w_val
            if weights > 0:
                break
                
        if weights > 0:
            cr = int(round(r_sum / weights))
            cg = int(round(g_sum / weights))
            cb = int(round(b_sum / weights))
            # Subtle coordinate dithering (+-1) for hand-painted feel, avoiding flat solid color
            dith = ((x * 11 + y * 17) % 3) - 1
            cr = max(0, min(255, cr + dith))
            cg = max(0, min(255, cg + dith))
            cb = max(0, min(255, cb + dith))
            repaired_colors[(x, y)] = (cr, cg, cb, 255)
        else:
            repaired_colors[(x, y)] = (230, 224, 212, 255)

    # Apply repairs
    for (x, y), c in repaired_colors.items():
        im.putpixel((x, y), c)

    # Specific refinement for right cheek / chin crack (x=62..78, y=52..65)
    # Ensure this area is completely free of crack fragments and smoothly blended
    for y in range(52, 65):
        for x in range(62, 78):
            r, g, b, a = im.getpixel((x, y))
            if a >= 128 and not is_structural_feature(x, y):
                mx = max(r, g, b)
                if mx < 150: # any leftover dark crack
                    # replace with clean cheek tone
                    # interpolate between nose (x=55) and right ear (x=80)
                    t = (x - 62) / 16.0
                    base_r = int(240 - t * 20)
                    base_g = int(234 - t * 20)
                    base_b = int(222 - t * 20)
                    im.putpixel((x, y), (base_r, base_g, base_b, 255))

    # Refinement for forehead (x=28..45, y=32..44)
    for y in range(32, 45):
        for x in range(28, 45):
            r, g, b, a = im.getpixel((x, y))
            if a >= 128 and not is_structural_feature(x, y):
                mx = max(r, g, b)
                if mx < 150:
                    im.putpixel((x, y), (228 + (x%3), 222 + (y%3), 210 + (x%2), 255))

    # Refinement for neck upper-right grunge (x=54..72, y=65..72)
    for y in range(65, 72):
        for x in range(54, 72):
            r, g, b, a = im.getpixel((x, y))
            if a >= 128 and not is_structural_feature(x, y):
                mx = max(r, g, b)
                if mx < 150:
                    im.putpixel((x, y), (215 + (x%3), 208 + (y%3), 195 + (x%2), 255))

    # Refinement for belly edges (y=85..100)
    for y in range(85, 101):
        # left belly edge
        for x in range(35, 41):
            r, g, b, a = im.getpixel((x, y))
            if a >= 128 and not is_structural_feature(x, y):
                if max(r, g, b) < 140:
                    im.putpixel((x, y), (218, 212, 200, 255))
        # right belly center/lower
        for x in range(60, 75):
            r, g, b, a = im.getpixel((x, y))
            if a >= 128 and not is_structural_feature(x, y):
                if max(r, g, b) < 135:
                    im.putpixel((x, y), (225 + (x%2), 218 + (y%2), 206 + (x%2), 255))

    im.save(out_path)
    print(f"✓ Saved repaired chassis to {out_path}")
    return im

if __name__ == "__main__":
    out = "/tmp/test_clean_ivory_v2.png"
    clean_full_ivory_chassis("game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png", out)
    interior_speckle(out)
