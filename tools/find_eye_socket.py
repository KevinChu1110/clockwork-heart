#!/usr/bin/env python3
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"
im_head = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_512.png").convert("RGBA")

# 尋找面部眼眶洞孔
holes = []
for y in range(100, 180):
    for x in range(190, 270):
        r, g, b, a = im_head.getpixel((x, y))
        if a < 100:
            holes.append((x, y, a, r, g, b))

print(f"Total hole/socket pixels in face: {len(holes)}")
if holes:
    xs = [h[0] for h in holes]
    ys = [h[1] for h in holes]
    print(f"Eye socket X range: {min(xs)}..{max(xs)}, Y range: {min(ys)}..{max(ys)}")
    print(f"Center: ({(min(xs)+max(xs))/2.0:.1f}, {(min(ys)+max(ys))/2.0:.1f})")
