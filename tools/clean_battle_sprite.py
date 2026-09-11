import sys
sys.path.insert(0, '/opt/side/bravesoul-game')
from PIL import Image
import numpy as np
from tools.measure_speckle import interior_speckle

def clean_macaque_battle_sprite():
    p = "game/assets/sprites/player/macaque_battle.png"
    im = Image.open(p).convert('RGBA')
    w, h = im.size
    px = im.load()
    
    def op(x, y):
        return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128
        
    dirty = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128: continue
            
            # preserve boots (y >= 105)
            if y >= 105: continue
            # preserve eye area (x: 45..56, y: 40..50)
            if 45 <= x <= 56 and 40 <= y <= 50: continue
            # preserve nostrils
            if 52 <= x <= 56 and 54 <= y <= 57: continue
            
            mx = max(r, g, b)
            is_interior = op(x-1,y) and op(x+1,y) and op(x,y-1) and op(x,y+1)
            
            if is_interior and 30 < mx < 115:
                dirty.append((x, y))
            elif not is_interior and 55 <= mx <= 125 and r > b:
                dirty.append((x, y))
                
    print(f"Macaque battle dirty pixels: {len(dirty)}")
    dirty_set = set(dirty)
    
    for (x, y) in dirty:
        weights = 0.0
        r_sum = 0.0
        g_sum = 0.0
        b_sum = 0.0
        
        for rad in range(2, 10):
            for dy in range(-rad, rad + 1):
                for dx in range(-rad, rad + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in dirty_set:
                        if px[nx, ny][3] >= 128:
                            nr, ng, nb = px[nx, ny][:3]
                            if max(nr, ng, nb) >= 130:
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
            im.putpixel((x, y), (max(0,min(255,cr+dith)), max(0,min(255,cg+dith)), max(0,min(255,cb+dith)), 255))
        else:
            im.putpixel((x, y), (230, 225, 215, 255))
            
    im.save(p)
    print("✓ Saved cleaned macaque_battle.png")
    interior_speckle(p)

if __name__ == "__main__":
    clean_macaque_battle_sprite()
