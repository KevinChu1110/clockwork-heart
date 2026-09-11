import os
from PIL import Image

rabbit_idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png")
print("Rabbit idle size:", rabbit_idle.size, rabbit_idle.mode)
w, h = rabbit_idle.size

# Let's find all pixels with r > 195 and g > 195 and b > 195 and abs(r - b) < 40 and a > 128
silver_pixels = []
for y in range(h):
    for x in range(w):
        r, g, b, a = rabbit_idle.getpixel((x, y))
        if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
            silver_pixels.append((x, y, r, g, b, a))

print("Total silver pixels in rabbit idle:", len(silver_pixels))

# Let's inspect the bounding box and distribution of these pixels
# Where is the dawn blade in rabbit idle?
# In idle, rabbit holds the sword on the right (or left).
# Let's cluster or check x coordinates.
xs = [p[0] for p in silver_pixels]
ys = [p[1] for p in silver_pixels]
print(f"X range: {min(xs)} - {max(xs)}, Y range: {min(ys)} - {max(ys)}")

# Check groups:
sword_pixels = [p for p in silver_pixels if p[0] >= 80] # sword is typically on the right
print("Silver pixels with x >= 80:", len(sword_pixels))
for thresh in [70, 75, 80, 82, 85]:
    sp = [p for p in silver_pixels if p[0] >= thresh]
    print(f"thresh {thresh}: count={len(sp)}")
