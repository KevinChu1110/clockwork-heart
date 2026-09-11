from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/attack.png").convert("RGBA")
px = im.load()
assert px is not None

visited = set()
components = []
for y in range(118):
    for x in range(128):
        if px[x, y][3] > 40 and (x, y) not in visited:
            comp = []
            queue = [(x, y)]
            visited.add((x, y))
            while queue:
                cx, cy = queue.pop(0)
                comp.append((cx, cy))
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0: continue
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < 128 and 0 <= ny < 118:
                            if px[nx, ny][3] > 40 and (nx, ny) not in visited:
                                visited.add((nx, ny))
                                queue.append((nx, ny))
            components.append(comp)

print(f"attack.png connected components (alpha>40, y<118): {len(components)}")
for i, comp in enumerate(components, 1):
    xs = [x for x, y in comp]
    ys = [y for x, y in comp]
    print(f"  Comp {i}: {len(comp)} px, bbox=({min(xs)}, {min(ys)}, {max(xs)}, {max(ys)})")
