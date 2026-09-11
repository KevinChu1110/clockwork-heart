from PIL import Image

rab = Image.open('game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png').convert('RGBA')
px = rab.load()
w, h = rab.size

def op(x, y):
    return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128

rab_speckles = []
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a >= 128 and op(x-1,y) and op(x+1,y) and op(x,y-1) and op(x,y+1):
            mx = max(r, g, b)
            if 30 < mx < 110:
                rab_speckles.append((x, y, (r, g, b)))

print("Rabbit speckles count:", len(rab_speckles))
for x, y, c in rab_speckles[:15]:
    nbrs = [px[x+dx, y+dy][:3] for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]]
    print(f"  ({x}, {y}) = {c}, nbrs={nbrs}")
