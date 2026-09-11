#!/usr/bin/env python3
from PIL import Image

im = Image.open("/tmp/test_clean_bamboo_bronze.png").convert("RGBA")
w, h = im.size

visited = [[False]*w for _ in range(h)]
components = []

for y in range(h):
    for x in range(w):
        if im.getpixel((x, y))[3] > 0 and not visited[y][x]:
            comp = []
            queue = [(x, y)]
            visited[y][x] = True
            while queue:
                cx, cy = queue.pop(0)
                comp.append((cx, cy))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1,-1), (-1,1), (1,-1), (1,1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        if im.getpixel((nx, ny))[3] > 0 and not visited[ny][nx]:
                            visited[ny][nx] = True
                            queue.append((nx, ny))
            components.append(comp)

print(f"Total connected components: {len(components)}")
for i, c in enumerate(components):
    if len(c) < 50:
        print(f"Small component {i} (size {len(c)}):")
        for x, y in c:
            print(f"  ({x}, {y}): rgba={im.getpixel((x, y))}")
