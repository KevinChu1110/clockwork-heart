#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PATHS = [
    f"{REPO_ROOT}/game/assets/sprites/player/party/kite_idle.png",
    f"{REPO_ROOT}/game/assets/sprites/player/kite_idle.png",
    f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/kite/proof_paperdoll_kite_composite.png"
]

for p in PATHS:
    if os.path.exists(p):
        im = Image.open(p).convert("RGBA")
        px = im.load()
        assert px is not None
        bbox = im.getbbox()
        w, h = im.size
        if w == 128 and h == 128:
            shadow_counts = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], px[x, y])[3] > 20) for y in range(118, 128)]
            print(f"{p:70s}: size={im.size} bbox={bbox} shadow(118..127)={shadow_counts}")
        else:
            print(f"{p:70s}: size={im.size} bbox={bbox}")
    else:
        print(f"{p:70s}: NOT FOUND")
