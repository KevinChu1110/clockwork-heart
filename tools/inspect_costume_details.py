#!/usr/bin/env python3
from typing import cast
from PIL import Image

def inspect_costume(path: str, name: str):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    print(f"=== {name}: {path} ===")
    print(f"Size: {w}x{h}, bbox: {img.getbbox()}")
    
    opaque_pixels = []
    for y in range(h):
        for x in range(w):
            p = cast(tuple[int, int, int, int], img.getpixel((x, y)))
            if p[3] > 0:
                opaque_pixels.append((x, y, p))
    print(f"Opaque pixels: {len(opaque_pixels)}")
    unique_colors = set(p[2][:3] for p in opaque_pixels)
    print(f"Unique colors: {len(unique_colors)}, colors/100px: {len(unique_colors)/(len(opaque_pixels)/100.0):.2f}")
    
    # Check bounding box of opaque pixels
    xs = [p[0] for p in opaque_pixels]
    ys = [p[1] for p in opaque_pixels]
    print(f"X range: {min(xs)}..{max(xs)}, Y range: {min(ys)}..{max(ys)}")

inspect_costume("game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard.png", "Lion Nutcracker Guard")
inspect_costume("game/assets/sprites/player/paperdoll/rabbit/costume/costume_steam_artisan.png", "Rabbit Steam Artisan")
inspect_costume("game/assets/sprites/player/paperdoll/rabbit/costume/costume_nutcracker_guard.png", "Rabbit Nutcracker Guard")
