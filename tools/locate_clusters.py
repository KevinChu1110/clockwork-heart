from PIL import Image
import numpy as np

def locate_components(p):
    im = Image.open(p).convert('RGBA')
    w, h = im.size
    px = im.load()
    def op(x, y):
        return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128
        
    grid = np.zeros((h, w), dtype=int)
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128: continue
            if not(op(x-1,y) and op(x+1,y) and op(x,y-1) and op(x,y+1)): continue
            mx = max(r, g, b)
            if 30 < mx < 110:
                grid[y, x] = 1
                
    visited = np.zeros((h, w), dtype=bool)
    comps = []
    
    for y in range(h):
        for x in range(w):
            if grid[y, x] == 1 and not visited[y, x]:
                q = [(x, y)]
                visited[y, x] = True
                comp = []
                while q:
                    cx, cy = q.pop()
                    comp.append((cx, cy))
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < w and 0 <= ny < h and grid[ny, nx] == 1 and not visited[ny, nx]:
                                visited[ny, nx] = True
                                q.append((nx, ny))
                comps.append(comp)
                
    comps.sort(key=lambda c: len(c), reverse=True)
    for i, c in enumerate(comps):
        min_x = min(p[0] for p in c)
        max_x = max(p[0] for p in c)
        min_y = min(p[1] for p in c)
        max_y = max(p[1] for p in c)
        print(f"Rab Comp {i:2d}: size={len(c):3d}, bbox=({min_x:2d},{min_y:2d}) to ({max_x:2d},{max_y:2d})")

locate_components('game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png')
