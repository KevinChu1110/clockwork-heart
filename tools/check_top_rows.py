from PIL import Image

for name in ["idle", "telegraph", "attack", "recover", "skill", "hit"]:
    im = Image.open(f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/{name}.png")
    px = im.load()
    top_pixels = []
    for y in range(30):
        row = [x for x in range(128) if px[x, y][3] > 10]
        if row:
            top_pixels.append((y, min(row), max(row), len(row)))
            if len(top_pixels) >= 3:
                break
    print(f"{name:10s} top 3 rows with alpha>10: {top_pixels}")
