from PIL import Image

im = Image.open('/tmp/test_clean_ivory_v2.png').convert('RGBA')
px = im.load()

print("Macaque chin area (x: 45..65, y: 60..68):")
for y in range(60, 69):
    line = []
    for x in range(45, 65):
        r, g, b, a = px[x, y]
        if a < 128:
            line.append("    ")
        else:
            mx = max(r, g, b)
            if mx < 130:
                line.append(f"*{mx:2d}*")
            else:
                line.append(f" {mx:2d} ")
    print(f"y={y:2d}: " + " ".join(line))
