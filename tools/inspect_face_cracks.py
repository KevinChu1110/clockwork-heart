#!/usr/bin/env python3
from PIL import Image

ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")
w, h = ivory.size

# Let's inspect face region (e.g. x between 40 and 85, y between 25 and 55)
# What colors are in the face?
print("=== Face pixels (y: 25..55, x: 40..85) ===")
face_pixels = []
for y in range(25, 55):
    for x in range(40, 85):
        r, g, b, a = ivory.getpixel((x, y))
        if a > 0:
            face_pixels.append((x, y, r, g, b, a))

# Sort by brightness / darkness
dark_in_face = [p for p in face_pixels if p[2] < 120 and p[3] > 200]
print(f"Total opaque in face: {len(face_pixels)}, Dark in face: {len(dark_in_face)}")
for p in dark_in_face[:30]:
    print(f"  ({p[0]}, {p[1]}): rgb({p[2]}, {p[3]}, {p[4]})")
