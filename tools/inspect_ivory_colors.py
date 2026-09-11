#!/usr/bin/env python3
from PIL import Image

ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")
w, h = ivory.size

# Let's crop various regions and save them or check coordinates
# Where are the pixels?
bbox = ivory.getbbox()
print("Chassis bbox:", bbox)

# Let's check unique colors and their frequency
from collections import Counter
counts = Counter()
for y in range(h):
    for x in range(w):
        p = ivory.getpixel((x, y))
        if p[3] > 0:
            counts[p] += 1

print(f"Total unique opaque/semi colors: {len(counts)}")
print("Top 10 most common colors:")
for c, cnt in counts.most_common(10):
    print(f"  {c}: {cnt}")

print("Darkest colors (v < 0.2):")
darkest = [(c, cnt) for c, cnt in counts.items() if (c[0]+c[1]+c[2]) < 100]
print(f"Count of dark colors: {len(darkest)}")
for c, cnt in darkest[:15]:
    print(f"  {c}: {cnt}")
