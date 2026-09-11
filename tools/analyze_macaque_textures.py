#!/usr/bin/env python3
import os
from PIL import Image

def analyze(path):
    if not os.path.exists(path):
        print("Not found:", path)
        return
    im = Image.open(path).convert("RGBA")
    print(f"=== {path} ===")
    print("Size:", im.size)
    # count non-transparent pixels
    w, h = im.size
    pixels = [im.getpixel((x, y)) for y in range(h) for x in range(w) if im.getpixel((x, y))[3] > 0]
    print(f"Opaque/semi pixels: {len(pixels)}")

analyze("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png")
analyze("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_bamboo_bronze.png")
analyze("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/costume/costume_zen_striker.png")
analyze("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/costume/costume_dawn_monk_tunic.png")
analyze("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_battle.png")
analyze("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_idle.png")
