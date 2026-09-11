#!/usr/bin/env python3
from PIL import Image

im = Image.open("/tmp/repaired_face.png").convert("RGBA")
w, h = im.size
print("repaired_face size:", w, h)

# Print all pixels where r < 120 and g < 120 and b < 120 and a > 200:
dark_px = []
for y in range(h):
    for x in range(w):
        r, g, b, a = im.getpixel((x, y))
        if a > 200 and (r + g + b) // 3 < 120:
            dark_px.append((x, y, r, g, b))

print(f"Total dark pixels in face crop: {len(dark_px)}")
for x, y, r, g, b in dark_px[:50]:
    print(f"({x}, {y}): rgb({r}, {g}, {b})")
