from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")
w, h = idle.size

# Let's inspect where pixels with r>195, g>195, b>195 are:
for y in range(h):
    line = []
    for x in range(w):
        r, g, b, a = idle.getpixel((x, y))
        if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
            line.append(x)
    if line:
        print(f"y={y:3d}: x in [{min(line):3d}, {max(line):3d}], count={len(line)}, xs={line}")
