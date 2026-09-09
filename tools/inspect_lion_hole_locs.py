#!/usr/bin/env python3
from PIL import Image
from collections import deque

def find_holes(im, threshold=1):
    w, h = im.size
    visited = [[False]*w for _ in range(h)]
    q = deque()
    for x in range(w):
        for y in [0, h - 1]:
            p = im.getpixel((x, y))
            if p[3] < threshold and not visited[y][x]:
                visited[y][x] = True
                q.append((x, y))
    for y in range(h):
        for x in [0, w - 1]:
            p = im.getpixel((x, y))
            if p[3] < threshold and not visited[y][x]:
                visited[y][x] = True
                q.append((x, y))
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        cx, cy = q.popleft()
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h:
                if not visited[ny][nx] and im.getpixel((nx, ny))[3] < threshold:
                    visited[ny][nx] = True
                    q.append((nx, ny))
    holes = []
    for y in range(h):
        for x in range(w):
            if im.getpixel((x, y))[3] < threshold and not visited[y][x]:
                holes.append((x, y))
    return holes

im = Image.open("game/assets/sprites/player/paperdoll/lion/proof_paperdoll_lion_composite.png").convert("RGBA")
holes = find_holes(im)
print(f"Holes in existing proof_paperdoll_lion_composite: {len(holes)}")
# Group holes by proximity
groups = []
for x, y in holes:
    print(f"  Hole at ({x}, {y})")
