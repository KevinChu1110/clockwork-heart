import sys
sys.path.insert(0, '/opt/side/bravesoul-game')
from PIL import Image
import numpy as np
from tools.measure_speckle import interior_speckle

def repair_ivory_chassis(src_p, out_p):
    im = Image.open(src_p).convert('RGBA')
    w, h = im.size
    px = im.load()
    
    def op(x, y):
        return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128
        
    # Step 1: Identify all dark speckles
    dark_mask = np.zeros((h, w), dtype=bool)
    interior_mask = np.zeros((h, w), dtype=bool)
    
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128: continue
            if op(x-1,y) and op(x+1,y) and op(x,y-1) and op(x,y+1):
                interior_mask[y, x] = True
                mx = max(r, g, b)
                if 30 < mx < 110:
                    dark_mask[y, x] = True

    # Step 2: Define preserved structural elements
    def is_preserved(x, y):
        # 1. Boots & legs (below waist)
        if y >= 105:
            return True
            
        # 2. Left eye (x: 46..54, y: 41..51)
        if 46 <= x <= 55 and 41 <= y <= 51:
            return True
            
        # 3. Right eye (x: 66..76, y: 41..51)
        if 66 <= x <= 76 and 41 <= y <= 51:
            return True
            
        # 4. Nostrils (x: 52..56, y: 55..57)
        if 52 <= x <= 56 and 55 <= y <= 57:
            return True
            
        # 5. Clean smile line (x: 50..63, y: 60)
        if 50 <= x <= 63 and y == 60:
            return True
            
        # 6. Neck center pivot hinge (x: 46..53, y: 66..71)
        if 46 <= x <= 53 and 66 <= y <= 71:
            return True
            
        # 7. Clean armor seam line on crown (1px horizontal / subtle vertical arch)
        # Center seam: x=58, y=28..37
        if x == 58 and 28 <= y <= 37:
            return True
            
        # 8. Chest / torso core socket or clean center seam
        if 57 <= x <= 59 and 78 <= y <= 85:
            return True
            
        return False

    dirt_pixels = []
    for y in range(h):
        for x in range(w):
            if dark_mask[y, x] and not is_preserved(x, y):
                dirt_pixels.append((x, y))

    print(f"Total dirt pixels to restore: {len(dirt_pixels)}")

    # Step 3: For each dirt pixel, interpolate clean surface color from surrounding clean opaque pixels
    repaired_px = {}
    for x, y in dirt_pixels:
        weights = 0.0
        r_sum = 0.0
        g_sum = 0.0
        b_sum = 0.0
        
        # Search radius
        for rad in range(2, 8):
            for dy in range(-rad, rad + 1):
                for dx in range(-rad, rad + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        na = px[nx, ny][3]
                        if na >= 128 and not dark_mask[ny, nx]:
                            nr, ng, nb = px[nx, ny][:3]
                            if max(nr, ng, nb) >= 115:
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
            dith = ((x * 7 + y * 13) % 5) - 2
            cr = max(0, min(255, cr + dith))
            cg = max(0, min(255, cg + dith))
            cb = max(0, min(255, cb + dith))
            repaired_px[(x, y)] = (cr, cg, cb, 255)
        else:
            repaired_px[(x, y)] = (228, 222, 210, 255)

    # Apply repairs
    for (x, y), color in repaired_px.items():
        im.putpixel((x, y), color)

    # Also clean any remaining stray cracks in face right cheek (x:65..75, y:52..64)
    for y in range(52, 64):
        for x in range(63, 76):
            r, g, b, a = im.getpixel((x, y))
            if a >= 128:
                mx = max(r, g, b)
                if 30 < mx < 115 and not (52 <= x <= 56 and 55 <= y <= 57):
                    if y == 60 and x <= 63:
                        continue
                    im.putpixel((x, y), (225 + (x%3), 218 + (y%3), 205 + (x%2), 255))

    im.save(out_p)
    print(f"Saved repaired image to {out_p}")
    return im

if __name__ == "__main__":
    out_p = '/tmp/test_repaired_ivory.png'
    repair_ivory_chassis('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png', out_p)
    interior_speckle(out_p)
