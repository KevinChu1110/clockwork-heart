from PIL import Image

def analyze_distribution(p):
    im = Image.open(p).convert('RGBA')
    w, h = im.size
    px = im.load()
    def op(x, y):
        return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128
        
    y_bins = {}
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128: continue
            if not(op(x-1,y) and op(x+1,y) and op(x,y-1) and op(x,y+1)): continue
            mx = max(r, g, b)
            if 30 < mx < 110:
                bin_idx = y // 10 * 10
                y_bins[bin_idx] = y_bins.get(bin_idx, 0) + 1
                
    print(f"--- Distribution for {p} ---")
    for bin_idx in sorted(y_bins.keys()):
        print(f"y={bin_idx:2d}..{bin_idx+9:2d}: {y_bins[bin_idx]:4d} dark speckles")

analyze_distribution('game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png')
analyze_distribution('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png')
