from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ch_ivory = Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA")
w, h = ch_ivory.size
data = ch_ivory.load()

# Head is between y=42 and y=70
bright_head_edges = []
for y in range(42, 70):
    for x in range(w):
        r, g, b, a = data[x, y]
        if a > 0:
            touches_transparent = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= w or ny < 0 or ny >= h or data[nx, ny][3] == 0:
                    touches_transparent = True
                    break
            if touches_transparent:
                if (r + g + b) / 3 > 150:
                    bright_head_edges.append((x, y, r, g, b, a))

print(f"Bright head edge pixels in chassis ivory (y 42..70): {len(bright_head_edges)}")
for p in bright_head_edges[:10]:
    print(f"  x={p[0]:2d}, y={p[1]:2d}: RGB({p[2]}, {p[3]}, {p[4]}), a={p[5]}")
