#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
idle_ref_path = f"{REPO_ROOT}/game/assets/sprites/player/party/kite_idle.png"
ref_im = Image.open(idle_ref_path).convert("RGBA")

shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = ref_im.load()
assert s_px is not None and c_px is not None

for y in range(118, 128):
    for x in range(4, 124):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p
        else:
            s_px[x, y] = (0, 0, 0, 0)

for x in range(128):
    s_px[x, 126] = (0, 0, 0, 0)
    s_px[x, 127] = (0, 0, 0, 0)
for y in range(128):
    s_px[0, y] = (0, 0, 0, 0)
    s_px[1, y] = (0, 0, 0, 0)
    s_px[2, y] = (0, 0, 0, 0)
    s_px[3, y] = (0, 0, 0, 0)
    s_px[124, y] = (0, 0, 0, 0)
    s_px[125, y] = (0, 0, 0, 0)
    s_px[126, y] = (0, 0, 0, 0)
    s_px[127, y] = (0, 0, 0, 0)

EXPECTED_SHADOW = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], s_px[x, y])[3] > 20) for y in range(118, 128)]
print("EXPECTED_SHADOW =", EXPECTED_SHADOW)
bbox = shadow_master.getbbox()
print("Shadow bbox =", bbox)
