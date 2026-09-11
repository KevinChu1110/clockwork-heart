from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ear = Image.open(f"{r_dir}/head_unit/ear_rabbit_straight.png").convert("RGBA")
w, h = ear.size
data = ear.load()

# Contour color from art_direction.md: deep warm brown #2C1C16 -> (44, 28, 22)
OUTLINE = (44, 28, 22)

# Any outer edge pixel that has (r+g+b)/3 > 140 and touches alpha 0
# We want the outer boundary to be a solid/clean dark outline.
# Let's inspect where bright edge pixels are:
bright_edge_coords = set()
for y in range(h):
    for x in range(w):
        r, g, b, a = data[x, y]
        if a > 0:
            touches_alpha0 = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= w or ny < 0 or ny >= h or data[nx, ny][3] == 0:
                    touches_alpha0 = True
                    break
            if touches_alpha0 and (r + g + b) / 3 > 130:
                bright_edge_coords.add((x, y))

print(f"Found {len(bright_edge_coords)} bright outer edge pixels on ears.")
