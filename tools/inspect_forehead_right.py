from PIL import Image

im = Image.open('/tmp/test_clean_ivory_v2.png').convert('RGBA')
px = im.load()

print("Forehead upper-right (x: 50..75, y: 22..38):")
for y in range(22, 38):
    line = []
    for x in range(50, 75):
        r, g, b, a = px[x, y]
        if a < 128:
            line.append("    ")
        else:
            mx = max(r, g, b)
            if mx < 210:
                line.append(f"*{mx:3d}")
            else:
                line.append(f" {mx:3d}")
    print(f"y={y:2d}: " + " ".join(line))
