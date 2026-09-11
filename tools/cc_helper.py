#!/usr/bin/env python3
from collections import deque
from typing import cast
from PIL import Image

def get_connected_components(img: Image.Image, alpha_thresh: int = 40, y_max: int = 118) -> list[list[tuple[int, int]]]:
    w, h = img.size
    px = img.load()
    assert px is not None
    visited = [[False]*h for _ in range(w)]
    components: list[list[tuple[int, int]]] = []
    
    for y in range(min(h, y_max)):
        for x in range(w):
            if visited[x][y]:
                continue
            p = cast(tuple[int, int, int, int], px[x, y])
            if p[3] > alpha_thresh:
                # BFS 8-connected
                comp: list[tuple[int, int]] = []
                q = deque([(x, y)])
                visited[x][y] = True
                while q:
                    cx, cy = q.popleft()
                    comp.append((cx, cy))
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < w and 0 <= ny < y_max:
                                if not visited[nx][ny]:
                                    np_val = cast(tuple[int, int, int, int], px[nx, ny])
                                    if np_val[3] > alpha_thresh:
                                        visited[nx][ny] = True
                                        q.append((nx, ny))
                components.append(comp)
    return components
