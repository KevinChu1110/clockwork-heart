#!/usr/bin/env python3
import os
from PIL import Image, ImageChops
from collections import deque

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar"

def count_holes(im, conn=4, threshold=1):
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
    if conn == 8:
        dirs += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
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

def build_comp(ch_fn, cos_fn):
    im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Z-index: winding_key(5) -> back_curio(8) -> chassis(10) -> head_unit(20) -> costume(25) -> optic_core(30) -> weapon(40)
    im.alpha_composite(Image.open(f"{BASE}/winding_key/key_classic_brass.png").convert("RGBA"))
    im.alpha_composite(Image.open(f"{BASE}/back_curio/curio_spring_tail.png").convert("RGBA"))
    im.alpha_composite(Image.open(f"{BASE}/chassis/{ch_fn}").convert("RGBA"))
    im.alpha_composite(Image.open(f"{BASE}/head_unit/ear_boar_rivet_cowl.png").convert("RGBA"))
    if cos_fn != "none":
        im.alpha_composite(Image.open(f"{BASE}/costume/{cos_fn}").convert("RGBA"))
    im.alpha_composite(Image.open(f"{BASE}/optic_core/core_cyan_emerald.png").convert("RGBA"))
    im.alpha_composite(Image.open(f"{BASE}/weapon/wpn_anvil_greathammer.png").convert("RGBA"))
    return im

chassis_list = ["paint_brass_gold.png", "paint_ivory_stock.png", "paint_molten_crimson.png"]
costume_list = ["none", "costume_viking_harness.png", "costume_viking_ironclad.png"]

print("=== 9-Matrix Hole Verification for Boar ===")
for ch in chassis_list:
    for cos in costume_list:
        comp = build_comp(ch, cos)
        h4 = count_holes(comp, conn=4)
        h8 = count_holes(comp, conn=8)
        non_trans = sum(1 for p in comp.getdata() if isinstance(p, tuple) and len(p) >= 4 and p[3] > 30)
        print(f"chassis: {ch:25} | costume: {cos:27} -> non-trans: {non_trans:4d} px | 4-conn: {len(h4):2d} px | 8-conn: {len(h8):2d} px")
