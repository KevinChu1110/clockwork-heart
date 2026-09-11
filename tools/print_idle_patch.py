from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")

print("idle.png pixels around (69, 90):")
for y in range(86, 96):
    row = []
    for x in range(65, 75):
        r, g, b, a = idle.getpixel((x, y))
        row.append(f"({r},{g},{b})")
    print(f"y={y:2d}: " + " ".join(row))
