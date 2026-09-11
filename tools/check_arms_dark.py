from PIL import Image

im = Image.open('/tmp/perfect_ivory.png').convert('RGBA')
px = im.load()

print("Arm dark pixels (y: 75..105, x < 42 or x > 75):")
for y in range(75, 105):
    line = []
    for x in range(128):
        if x < 42 or x > 75:
            r, g, b, a = px[x, y]
            if a >= 128:
                mx = max(r, g, b)
                if mx < 130:
                    line.append(f"({x},{y}:{r},{g},{b})")
    if line:
        print(f"y={y}: " + " ".join(line[:10]))
