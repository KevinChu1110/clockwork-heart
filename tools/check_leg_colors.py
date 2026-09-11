from PIL import Image

im = Image.open('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png').convert('RGBA')
px = im.load()
w, h = im.size

colors = {}
for y in range(105, h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a >= 128:
            colors[(r, g, b)] = colors.get((r, g, b), 0) + 1

print("Top colors in macaque legs (y>=105):")
for c, cnt in sorted(colors.items(), key=lambda x: x[1], reverse=True)[:15]:
    mx = max(c)
    is_darkspeckle = (30 < mx < 110)
    print(f"  color={c}: count={cnt:3d}, max={mx}, darkspeckle={is_darkspeckle}")
