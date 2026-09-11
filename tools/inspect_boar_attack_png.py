#!/usr/bin/env python3
from PIL import Image

im = Image.open('/opt/side/bravesoul-game/game/assets/sprites/player/poses/boar/attack.png').convert('RGBA')
w, h = im.size
print(f"boar attack size: {w}x{h}")
# check white/light gray pixels
white_pixels = []
for y in range(h):
    for x in range(w):
        px = im.getpixel((x, y))
        if isinstance(px, tuple) and len(px) >= 4:
            r, g, b, a = px[0], px[1], px[2], px[3]
            if a > 200 and r > 200 and g > 200 and b > 200:
                white_pixels.append((x, y, r, g, b, a))

print(f"Total bright white pixels (a>200, rgb>200): {len(white_pixels)}")
if white_pixels:
    min_x = min(p[0] for p in white_pixels)
    max_x = max(p[0] for p in white_pixels)
    min_y = min(p[1] for p in white_pixels)
    max_y = max(p[1] for p in white_pixels)
    print(f"Bounding box of white pixels: ({min_x}, {min_y}) - ({max_x}, {max_y})")
