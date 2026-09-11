from PIL import Image
import numpy as np

def visualize_speckles(p, out_p):
    im = Image.open(p).convert('RGBA')
    w, h = im.size
    px = im.load()
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out_px = out.load()
    
    def op(x, y):
        return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128
        
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128:
                continue
            if not(op(x-1, y) and op(x+1, y) and op(x, y-1) and op(x, y+1)):
                out_px[x, y] = (100, 100, 100, 120) # outline
                continue
            mx = max(r, g, b)
            if 30 < mx < 110:
                out_px[x, y] = (255, 0, 0, 255) # dark speckle
            else:
                out_px[x, y] = (r, g, b, 180) # normal body
                
    out.save(out_p)
    print("Saved visualization to", out_p)

visualize_speckles('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png', '/tmp/ivory_speckles.png')
visualize_speckles('game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png', '/tmp/rabbit_speckles.png')
