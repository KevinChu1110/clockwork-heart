from PIL import Image

im = Image.open('/opt/side/bravesoul-game/proofs/hud_dopamine/proof_explore_hud_hotbar.png')
rgb = im.convert('RGB')
w, h = im.size

# Find all pixels that are cream #FFFDF8 (allowing small tolerance)
cream_pixels = []
for y in range(h):
    for x in range(w):
        r, g, b = rgb.getpixel((x, y))
        # cream #FFFDF8 is approx (255, 253, 248)
        if r >= 250 and g >= 245 and b >= 240:
            cream_pixels.append((x, y))

print(f"Total cream pixels: {len(cream_pixels)}")

# Cluster them into components or bounding boxes
from collections import defaultdict

# Simple grid binning to find clusters
grid = defaultdict(list)
for x, y in cream_pixels:
    grid[(x // 40, y // 20)].append((x, y))

boxes = []
for (gx, gy), pts in grid.items():
    min_x = min(p[0] for p in pts)
    max_x = max(p[0] for p in pts)
    min_y = min(p[1] for p in pts)
    max_y = max(p[1] for p in pts)
    boxes.append((min_x, min_y, max_x, max_y, len(pts)))

# Merge overlapping/adjacent boxes
merged = True
while merged:
    merged = False
    new_boxes = []
    while boxes:
        b1 = boxes.pop(0)
        combined = False
        for i, b2 in enumerate(boxes):
            # Check if close
            if not (b1[2] + 25 < b2[0] or b2[2] + 25 < b1[0] or b1[3] + 15 < b2[1] or b2[3] + 15 < b1[1]):
                # merge
                merged_b = (
                    min(b1[0], b2[0]),
                    min(b1[1], b2[1]),
                    max(b1[2], b2[2]),
                    max(b1[3], b2[3]),
                    b1[4] + b2[4]
                )
                boxes[i] = merged_b
                merged = True
                combined = True
                break
        if not combined:
            new_boxes.append(b1)
    boxes = new_boxes

boxes = sorted(boxes, key=lambda b: (b[1], b[0]))
print("Found label/card regions (x1, y1, x2, y2, pixel_count):")
for b in boxes:
    print(f"Box: {b}, width={b[2]-b[0]+1}, height={b[3]-b[1]+1}")
