from PIL import Image

im = Image.open('/tmp/test_repaired_ivory.png').convert('RGBA')
px = im.load()
w, h = im.size

print("Checking remaining dark pixels in repaired head (y: 15..70, x: 25..95):")
dark_list = []
for y in range(15, 70):
    for x in range(25, 95):
        r, g, b, a = px[x, y]
        if a >= 64:
            mx = max(r, g, b)
            if mx < 130:
                dark_list.append((x, y, (r, g, b, a)))

print(f"Total pixels with max(r,g,b) < 130: {len(dark_list)}")
for x, y, c in dark_list[:30]:
    print(f"  ({x:2d}, {y:2d}) = {c}")
