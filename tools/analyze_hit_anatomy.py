#!/usr/bin/env python3
import os
from collections import deque
from typing import cast
from PIL import Image

def get_connected_components(img: Image.Image, alpha_thresh=40, y_max=118):
    w, h = img.size
    px = img.load()
    assert px is not None
    visited = [[False]*h for _ in range(w)]
    components = []
    
    for y in range(min(h, y_max)):
        for x in range(w):
            if visited[x][y]:
                continue
            p = cast(tuple[int, int, int, int], px[x, y])
            if p[3] > alpha_thresh:
                # BFS 8-connected
                comp = []
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

def inspect():
    img = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/hit.png")
    comps = get_connected_components(img, alpha_thresh=40, y_max=118)
    print(f"Number of components (y < 118, alpha > 40): {len(comps)}")
    for i, c in enumerate(comps):
        xs = [pt[0] for pt in c]
        ys = [pt[1] for pt in c]
        print(f"  Comp {i+1}: count={len(c)}, bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")

    # Check hit_body alone
    body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")
    large_hit = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    large_hit.paste(body_clean, (64, 64))
    rotated_hit = large_hit.rotate(14, resample=Image.Resampling.BICUBIC, center=(64 + 52, 64 + 118))
    hit_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_body.paste(rotated_hit, (-64, -64), rotated_hit)
    
    b_comps = get_connected_components(hit_body, alpha_thresh=40, y_max=118)
    print(f"\nhit_body alone components: {len(b_comps)}")
    for i, c in enumerate(b_comps):
        xs = [pt[0] for pt in c]
        ys = [pt[1] for pt in c]
        print(f"  hb Comp {i+1}: count={len(c)}, bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")

if __name__ == "__main__":
    inspect()
