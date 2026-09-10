#!/usr/bin/env python3
from PIL import Image

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
            # interior = all 4 neighbours opaque (not silhouette edge)
            if not(op(x-1, y) and op(x+1, y) and op(x, y-1) and op(x, y+1)):
                continue
            tot += 1
            mx = max(r, g, b)
            if 30 < mx < 110:
                n += 1
    pct = n / max(tot, 1) * 100
    print(f'{p.split("/")[-2]}/{p.split("/")[-1]:24s} interior={tot:5d} darkspeckle={n:5d} {pct:5.2f}%')
    return pct

if __name__ == '__main__':
    for p in ['game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png',
              'game/assets/sprites/player/paperdoll/macaque/chassis/paint_bamboo_bronze.png',
              'game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png']:
        interior_speckle(p)
