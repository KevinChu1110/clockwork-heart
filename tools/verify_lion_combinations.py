#!/usr/bin/env python3
import os
from PIL import Image, ImageChops, ImageDraw

LION_DIR = "game/assets/sprites/player/paperdoll/lion"

def count_holes(im, threshold=1):
    w, h = im.size
    visited = [[False]*w for _ in range(h)]
    q = []
    
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
        cx, cy = q.pop(0)
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

def build_lion_composite(chassis_file, costume_file=None):
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # 1. winding_key (z=5)
    comp.alpha_composite(Image.open(f"{LION_DIR}/winding_key/key_classic_brass.png").convert("RGBA"))
    # 2. back_curio (z=8)
    comp.alpha_composite(Image.open(f"{LION_DIR}/back_curio/curio_lion_fan_tail.png").convert("RGBA"))
    # 3. chassis (z=10)
    comp.alpha_composite(Image.open(f"{LION_DIR}/chassis/{chassis_file}").convert("RGBA"))
    # 4. head_unit (z=20)
    comp.alpha_composite(Image.open(f"{LION_DIR}/head_unit/ear_lion_gilded_mane.png").convert("RGBA"))
    # 5. costume (z=25)
    if costume_file and costume_file != "none":
        comp.alpha_composite(Image.open(f"{LION_DIR}/costume/{costume_file}").convert("RGBA"))
    # 6. optic_core (z=30)
    comp.alpha_composite(Image.open(f"{LION_DIR}/optic_core/core_amber_sun.png").convert("RGBA"))
    # 7. weapon (z=40)
    comp.alpha_composite(Image.open(f"{LION_DIR}/weapon/wpn_knight_lance.png").convert("RGBA"))
    return comp

def verify_all_lion_combos():
    chassis_list = ["paint_brass_gold.png", "paint_ivory_stock.png", "paint_midnight_navy.png"]
    costume_list = ["costume_nutcracker_guard.png", "costume_steam_artisan.png", "none"]

    print("=== VERIFYING ALL LION PAPERDOLL COMBINATIONS ===")
    bg_magenta = Image.new("RGBA", (128, 128), (255, 0, 255, 255))

    for ch in chassis_list:
        for cos in costume_list:
            comp = build_lion_composite(ch, cos)
            holes = count_holes(comp)
            mag = Image.alpha_composite(bg_magenta, comp)
            print(f"Chassis: {ch:24} | Costume: {cos:28} -> Holes: {len(holes):2d} px | bbox: {comp.getbbox()}")
            assert len(holes) == 0, f"Holes found in {ch} + {cos}: {len(holes)} px!"

    print("✓ All 9 chassis x costume combinations verified with 0 holes!")

if __name__ == "__main__":
    verify_all_lion_combos()
