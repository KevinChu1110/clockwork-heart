#!/usr/bin/env python3
from PIL import Image

def find_regions():
    gold = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png").convert("RGBA")
    w, h = gold.size
    print(f"Size: {w}x{h}, bbox: {gold.getbbox()}")
    # Let's inspect where opaque pixels are
    # And check winding key, weapon, etc. to see where the chassis overlaps or has gaps
    key = Image.open("game/assets/sprites/player/paperdoll/lion/winding_key/key_classic_brass.png").convert("RGBA")
    wpn = Image.open("game/assets/sprites/player/paperdoll/lion/weapon/wpn_knight_lance.png").convert("RGBA")
    print(f"Key bbox: {key.getbbox()}")
    print(f"Weapon bbox: {wpn.getbbox()}")

find_regions()
