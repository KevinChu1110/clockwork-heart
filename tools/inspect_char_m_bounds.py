#!/usr/bin/env python3
from PIL import Image

char_m = Image.open("/opt/side/bravesoul-game/branding/char_macaque.png").convert("RGBA")
print("size:", char_m.size)
# find non-white pixels
w, h = char_m.size
min_x, min_y, max_x, max_y = w, h, 0, 0
for y in range(h):
    for x in range(w):
        r, g, b, a = char_m.getpixel((x, y))
        # if not white
        if not (r > 250 and g > 250 and b > 250):
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

print(f"Character bounds in char_macaque (non-white): ({min_x}, {min_y}, {max_x}, {max_y})")
print(f"Width: {max_x - min_x}, Height: {max_y - min_y}")
