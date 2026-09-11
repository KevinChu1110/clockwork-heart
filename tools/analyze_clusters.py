from PIL import Image
import numpy as np

def analyze_components(p):
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
                
    # Connected component analysis of the dark speckle grid (8-connected)
    visited = np.zeros((h, w), dtype=bool)
    comps = []
    
    for y in range(h):
        for x in range(w):
            if grid[y, x] == 1 and not visited[y, x]:
                # flood fill
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
                
    print(f"Total components in {p}: {len(comps)}")
    size_dist = {}
    for c in comps:
        s = len(c)
        size_dist[s] = size_dist.get(s, 0) + 1
        
    for s in sorted(size_dist.keys()):
        print(f"  size {s:3d}: {size_dist[s]:3d} clusters (total {s * size_dist[s]} px)")
        
    return comps

print("--- Rabbit Components ---")
rab_comps = analyze_components('game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png')

print("\n--- Macaque Ivory Components ---")
mac_comps = analyze_components('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png')
