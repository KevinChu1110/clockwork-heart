from PIL import Image

im = Image.open('/tmp/test_clean_ivory_v2.png').convert('RGBA')
px = im.load()

print("Finding pixels in right cheek (x: 70..90, y: 35..65):")
for y in range(35, 65):
    line = []
    for x in range(65, 90):
        r, g, b, a = px[x, y]
        if a < 128:
            line.append(" ")
        else:
            mx = max(r, g, b)
            if mx < 130:
                line.append(f"({x},{y}:{r},{g},{b})")
    if line:
        print(f"y={y}: " + " ".join(line))
