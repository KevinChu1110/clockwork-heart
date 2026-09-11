from PIL import Image

im = Image.open('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png').convert('RGBA')
px = im.load()
w, h = im.size

def op(x, y):
    return 0 <= x < w and 0 <= y < h and px[x, y][3] >= 128

# Let's inspect y=30..49 (forehead)
forehead_speckles = []
for y in range(30, 50):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a >= 128 and op(x-1,y) and op(x+1,y) and op(x,y-1) and op(x,y+1):
            mx = max(r, g, b)
            if 30 < mx < 110:
                forehead_speckles.append((x, y, (r, g, b)))

print("Forehead speckles count:", len(forehead_speckles))
# sample some forehead speckles and their neighbors
for x, y, c in forehead_speckles[:10]:
    # inspect neighbors
    nbrs = [px[x+dx, y+dy][:3] for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]]
    print(f"  ({x}, {y}) = {c}, neighbors={nbrs}")
