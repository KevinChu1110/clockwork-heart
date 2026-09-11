from PIL import Image

rab = Image.open('game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png').convert('RGBA')
px = rab.load()
w, h = rab.size

print("Rabbit colors near edge (y: 35..65):")
edge_colors = {}
for y in range(35, 65):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a >= 128:
            # check if adjacent to transparent
            has_trans = False
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= w or ny < 0 or ny >= h or px[nx, ny][3] < 128:
                    has_trans = True
                    break
            if has_trans:
                edge_colors[(r, g, b)] = edge_colors.get((r, g, b), 0) + 1

for c, cnt in sorted(edge_colors.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {c}: {cnt}")
