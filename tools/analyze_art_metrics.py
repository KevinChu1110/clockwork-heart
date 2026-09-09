#!/usr/bin/env python3
from typing import cast
from PIL import Image
from collections import Counter

def analyze(path: str):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    opaque = []
    for y in range(h):
        for x in range(w):
            pixel = cast(tuple[int, int, int, int], img.getpixel((x, y)))
            if pixel[3] > 0:
                opaque.append((pixel[0], pixel[1], pixel[2]))
    unique = set(opaque)
    cnt = len(opaque)
    u_cnt = len(unique)
    ratio = u_cnt / (cnt / 100.0) if cnt > 0 else 0
    print(f"{path}:")
    print(f"  opaque={cnt}, unique={u_cnt}, colors/100px={ratio:.2f}")
    c = Counter(opaque)
    print("  top 5 colors:", c.most_common(5))
    return cnt, u_cnt, ratio

if __name__ == "__main__":
    targets = [
        "game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard.png",
        "game/assets/sprites/player/paperdoll/rabbit/costume/costume_steam_artisan.png",
        "game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png",
        "game/assets/sprites/player/paperdoll/lion/chassis/paint_ivory_stock.png",
        "game/assets/sprites/player/paperdoll/lion/costume/costume_steam_artisan.png",
        "game/assets/sprites/player/paperdoll/lion/chassis/paint_midnight_navy.png",
    ]
    for t in targets:
        analyze(t)
