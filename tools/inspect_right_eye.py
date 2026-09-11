from PIL import Image

im = Image.open('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png').convert('RGBA')
px = im.load()

print("Macaque right eye area (x: 65..78, y: 40..52):")
for y in range(40, 53):
    line = []
    for x in range(65, 78):
        r, g, b, a = px[x, y]
        if a < 128:
            line.append("    ")
        else:
            line.append(f"{r:3d}")
    print(f"y={y:2d} R: " + " ".join(line))

print("\nGreen channel:")
for y in range(40, 53):
    line = []
    for x in range(65, 78):
        r, g, b, a = px[x, y]
        if a < 128:
            line.append("    ")
        else:
            line.append(f"{g:3d}")
    print(f"y={y:2d} G: " + " ".join(line))
