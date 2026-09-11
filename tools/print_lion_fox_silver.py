from PIL import Image

for race, path in [
    ("lion", "/opt/side/bravesoul-game/game/assets/sprites/player/poses/lion/idle.png"),
    ("fox", "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/idle.png"),
]:
    im = Image.open(path).convert("RGBA")
    print(f"=== {race} all silver pixels ===")
    silvers = []
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = im.getpixel((x, y))
            if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
                silvers.append((x, y, r, g, b))
    # Group by y
    by_y = {}
    for x, y, r, g, b in silvers:
        by_y.setdefault(y, []).append((x, r, g, b))
    for y in sorted(by_y.keys()):
        xs = [item[0] for item in by_y[y]]
        print(f"y={y:3d}: count={len(xs):2d}, x in [{min(xs):3d}, {max(xs):3d}], xs={xs}")
