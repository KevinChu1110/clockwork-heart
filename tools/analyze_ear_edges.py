from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ear = Image.open(f"{r_dir}/head_unit/ear_rabbit_straight.png").convert("RGBA")
w, h = ear.size
data = ear.load()

# Find all edge pixels: pixels with a > 0 that touch a pixel with a == 0
edge_pixels = []
for y in range(h):
    for x in range(w):
        r, g, b, a = data[x, y]
        if a > 0:
            # check 4 neighbors
            touches_transparent = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= w or ny < 0 or ny >= h or data[nx, ny][3] == 0:
                    touches_transparent = True
                    break
            if touches_transparent:
                edge_pixels.append((x, y, r, g, b, a))

print(f"Total edge pixels on ear: {len(edge_pixels)}")
# How many edge pixels have high brightness (r+g+b)/3 > 150?
bright_edges = [p for p in edge_pixels if (p[2]+p[3]+p[4])/3 > 150]
print(f"Bright edge pixels on ear: {len(bright_edges)} / {len(edge_pixels)} ({len(bright_edges)/len(edge_pixels)*100:.1f}%)")

for p in bright_edges[:20]:
    print(f"  x={p[0]:2d}, y={p[1]:2d}: RGB({p[2]}, {p[3]}, {p[4]}), a={p[5]}")
