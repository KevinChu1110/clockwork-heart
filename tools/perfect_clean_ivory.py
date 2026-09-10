from PIL import Image
import numpy as np

def interior_speckle(p):
    im = Image.open(p).convert('RGBA')
    w, h = im.size
    px = im.load()
    def op(x, y):
        return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128
    n = 0
    tot = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128:
                continue
            if not(op(x-1, y) and op(x+1, y) and op(x, y-1) and op(x, y+1)):
                continue
            tot += 1
            mx = max(r, g, b)
            if 30 < mx < 110:
                n += 1
    pct = n / max(tot, 1) * 100
    print(f'{p.split("/")[-1]:24s} interior={tot:5d} darkspeckle={n:5d} {pct:5.2f}%')
    return pct

def perfect_clean_ivory(src_path, out_path):
    im = Image.open(src_path).convert('RGBA')
    w, h = im.size
    px = im.load()
    
    def op(x, y):
        return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128

    # 1. Precise definition of TRUE structural elements that MUST be kept:
    def is_true_structure(x, y):
        # Boots and feet (y >= 105)
        if y >= 105:
            return True
            
        # Left eye sensor (x: 46..55, y: 42..51)
        if 46 <= x <= 55 and 42 <= y <= 51:
            return True
            
        # Nostrils (x: 53..55, y: 55..56)
        if 53 <= x <= 55 and 55 <= y <= 56:
            return True
            
        # Smile line (x: 50..58, y: 60)
        if 50 <= x <= 58 and y == 60:
            return True
            
        # Neck center pivot hinge (x: 47..53, y: 67..70)
        if 47 <= x <= 53 and 67 <= y <= 70:
            return True
            
        # Clean mechanical outline itself (strictly at the outermost boundary next to alpha < 128)
        if px[x, y][3] >= 128:
            is_edge = not (op(x-1, y) and op(x+1, y) and op(x, y-1) and op(x, y+1))
            if is_edge and max(px[x, y][:3]) <= 65:
                return True
                
        return False

    # 2. Identify all pixels to clean (y < 105)
    clean_target = set()
    for y in range(105):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128:
                continue
            if is_true_structure(x, y):
                continue
                
            mx = max(r, g, b)
            if mx < 160:
                clean_target.add((x, y))

    print(f"Total crack/grunge pixels identified for cleaning: {len(clean_target)}")

    # 3. IDW interpolation to restore porcelain/enamel ivory surface
    repaired_px = {}
    for (x, y) in clean_target:
        weights = 0.0
        r_sum = 0.0
        g_sum = 0.0
        b_sum = 0.0
        
        for rad in range(2, 12):
            for dy in range(-rad, rad + 1):
                for dx in range(-rad, rad + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in clean_target:
                        na = px[nx, ny][3]
                        if na >= 128:
                            nr, ng, nb = px[nx, ny][:3]
                            if max(nr, ng, nb) >= 150:
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
            dith = ((x * 7 + y * 13) % 3) - 1
            cr = max(0, min(255, cr + dith))
            cg = max(0, min(255, cg + dith))
            cb = max(0, min(255, cb + dith))
            repaired_px[(x, y)] = (cr, cg, cb, 255)
        else:
            repaired_px[(x, y)] = (235, 230, 220, 255)

    for (x, y), c in repaired_px.items():
        im.putpixel((x, y), c)

    # Clean isolated stray arm points
    isolated_arms = [
        (35, 77), (34, 79), (76, 83), (28, 88), (30, 91), (34, 92),
        (41, 93), (87, 93), (76, 94), (86, 98), (38, 99), (79, 99),
        (80, 99), (39, 100), (31, 101), (38, 102), (85, 102), (84, 103)
    ]
    for ax, ay in isolated_arms:
        nbrs = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = ax + dx, ay + dy
            if 0 <= nx < w and 0 <= ny < h and im.getpixel((nx, ny))[3] >= 128:
                if max(im.getpixel((nx, ny))[:3]) >= 150:
                    nbrs.append(im.getpixel((nx, ny))[:3])
        if nbrs:
            avg_c = tuple(int(sum(c[i] for c in nbrs)/len(nbrs)) for i in range(3))
            im.putpixel((ax, ay), (*avg_c, 255))

    # Clean background stray pixels
    for y in range(h):
        for x in range(w):
            if 0 < im.getpixel((x, y))[3] < 64:
                nbr_op = sum(1 for dx in [-1,0,1] for dy in [-1,0,1] if (dx!=0 or dy!=0) and 0<=x+dx<w and 0<=y+dy<h and im.getpixel((x+dx, y+dy))[3] >= 64)
                if nbr_op == 0:
                    im.putpixel((x, y), (0, 0, 0, 0))

    im.save(out_path)
    print(f"✓ Saved cleaned chassis to {out_path}")
    return im

if __name__ == "__main__":
    p = "game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png"
    perfect_clean_ivory(p, p)
    interior_speckle(p)
