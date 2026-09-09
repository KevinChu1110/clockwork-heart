#!/usr/bin/env python3
import os
import sys
from typing import cast
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from test_artisan_generator import generate_lion_artisan_costume

art = generate_lion_artisan_costume()
gold = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png").convert("RGBA")
ivory = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_ivory_stock.png").convert("RGBA")

def check_overlap(layer: Image.Image, ch: Image.Image, ch_name: str):
    w, h = layer.size
    opaque = 0
    identical = 0
    for y in range(h):
        for x in range(w):
            lp = cast(tuple[int, int, int, int], layer.getpixel((x, y)))
            cp = cast(tuple[int, int, int, int], ch.getpixel((x, y)))
            if lp[3] > 0:
                opaque += 1
                if lp[:3] == cp[:3]:
                    identical += 1
    ratio = identical / (opaque / 100.0)
    print(f"Overlap with {ch_name}: {identical}/{opaque} identical ({ratio:.2f}%)")

check_overlap(art, gold, "paint_brass_gold")
check_overlap(art, ivory, "paint_ivory_stock")
