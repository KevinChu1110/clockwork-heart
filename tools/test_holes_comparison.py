#!/usr/bin/env python3
import os
import sys
from typing import cast
from collections import deque
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from test_navy_hsv import new_img, gold

def count_holes(im: Image.Image, conn: int = 4, threshold: int = 1):
    w, h = im.size
    visited = [[False]*w for _ in range(h)]
    q = deque()
    
    for x in range(w):
        for y in [0, h - 1]:
            p = cast(tuple[int, int, int, int], im.getpixel((x, y)))
            if p[3] < threshold and not visited[y][x]:
                visited[y][x] = True
                q.append((x, y))
    for y in range(h):
        for x in [0, w - 1]:
            p = cast(tuple[int, int, int, int], im.getpixel((x, y)))
            if p[3] < threshold and not visited[y][x]:
                visited[y][x] = True
                q.append((x, y))
                
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if conn == 8:
        dirs += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
    while q:
        cx, cy = q.popleft()
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h:
                if not visited[ny][nx]:
                    np_pix = cast(tuple[int, int, int, int], im.getpixel((nx, ny)))
                    if np_pix[3] < threshold:
                        visited[ny][nx] = True
                        q.append((nx, ny))
                    
    holes = []
    for y in range(h):
        for x in range(w):
            np_pix = cast(tuple[int, int, int, int], im.getpixel((x, y)))
            if np_pix[3] < threshold and not visited[y][x]:
                holes.append((x, y))
    return holes

gold_h4 = count_holes(gold, conn=4)
gold_h8 = count_holes(gold, conn=8)
navy_h4 = count_holes(new_img, conn=4)
navy_h8 = count_holes(new_img, conn=8)

print(f"Gold: 4conn={len(gold_h4)}, 8conn={len(gold_h8)}")
print(f"Navy: 4conn={len(navy_h4)}, 8conn={len(navy_h8)}")
