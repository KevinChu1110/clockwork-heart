#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import cast
from PIL import Image

body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")
large_hit = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
large_hit.paste(body_clean, (64, 64))
rotated_hit = large_hit.rotate(14, resample=Image.Resampling.BICUBIC, center=(64 + 52, 64 + 118))
hit_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
hit_body.paste(rotated_hit, (-64, -64), rotated_hit)

px = hit_body.load()
assert px is not None

print("hit_body colored pixels in right shoulder region:")
for y in range(54, 76):
    row = []
    for x in range(64, 86):
        p = cast(tuple[int,int,int,int], px[x, y])
        if p[3] > 40:
            # classify color: navy, gold, bronze, crimson, cream, outline
            row.append(f"{x}:{p[:3]}")
    if row:
        print(f"y={y}: " + " | ".join(row))
