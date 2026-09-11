#!/usr/bin/env python3
from typing import cast
from PIL import Image

costs = [
    ("macaque", "costume_dawn_monk_tunic.png"),
    ("fox", "costume_astral_cape.png"),
    ("fox", "costume_astral_observer.png"),
    ("lion", "costume_nutcracker_guard.png"),
    ("lion", "costume_steam_artisan.png"),
    ("rabbit", "costume_nutcracker_guard.png"),
    ("rabbit", "costume_royal_parade.png"),
    ("boar", "costume_viking_harness.png"),
    ("boar", "costume_viking_ironclad.png"),
]

for race, fn in costs:
    p = f"/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/{race}/costume/{fn}"
    im = Image.open(p)
    bbox = im.getbbox()
    opaque = sum(1 for y in range(128) for x in range(128) if cast(tuple[int,int,int,int], im.getpixel((x, y)))[3] > 0)
    print(f"{race:7s} {fn:30s} bbox: {bbox} opaque: {opaque}")
